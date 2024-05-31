#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

import concurrent.futures
import logging

from osc_lib.command import command
from osc_lib import exceptions
from osc_lib.i18n import _
from oslo_utils import uuidutils

from esiclient import utils


class List(command.Lister):
    """List networks attached to node"""

    log = logging.getLogger(__name__ + ".List")

    def get_parser(self, prog_name):
        parser = super(List, self).get_parser(prog_name)
        parser.add_argument(
            '--node',
            dest='node',
            metavar='<node>',
            help=_("Filter by this node (name or UUID).")
        )
        parser.add_argument(
            '--network',
            dest='network',
            metavar='<network>',
            help=_("Filter by this network (name or UUID).")
        )
        return parser

    def _get_ports(self, neutron_client, network=None):
        if network:
            filter_network = neutron_client.find_network(network)
            neutron_ports = list(neutron_client.ports(
                network_id=filter_network.id))
        else:
            neutron_ports = list(neutron_client.ports())
        return neutron_ports

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)

        ironic_client = self.app.client_manager.baremetal
        neutron_client = self.app.client_manager.network

        if parsed_args.node:
            ports = ironic_client.port.list(node=parsed_args.node, detail=True)
            if uuidutils.is_uuid_like(parsed_args.node):
                node_name = ironic_client.node.get(parsed_args.node).name
            else:
                node_name = parsed_args.node
        else:
            ports = None
            nodes = None

            with concurrent.futures.ThreadPoolExecutor() as executor:
                f1 = executor.submit(ironic_client.port.list, detail=True)
                f2 = executor.submit(ironic_client.node.list)
                ports = f1.result()
                nodes = f2.result()

        filter_network = None
        if parsed_args.network:
            filter_network = neutron_client.find_network(parsed_args.network)

        # base network information
        with concurrent.futures.ThreadPoolExecutor() as executor:
            f1 = executor.submit(neutron_client.ips)
            f2 = executor.submit(neutron_client.networks)
            f3 = executor.submit(
                self._get_ports, neutron_client, filter_network)
            floating_ips = list(f1.result())
            networks = list(f2.result())
            networks_dict = {n.id: n for n in networks}
            neutron_ports = f3.result()

        # update floating IP list to include port forwarding information
        for fip in floating_ips:
            # no need to do this for floating IPs associated with a port,
            # as port forwarding is irrelevant in such a case
            if not fip.port_id:
                pfws = list(neutron_client.port_forwardings(fip))
                if len(pfws):
                    fip.port_id = pfws[0].internal_port_id
                    pfw_ports = ["%s:%s" % (pfw.internal_port,
                                            pfw.external_port)
                                 for pfw in pfws]
                    fip.floating_ip_address = "%s (%s)" % (
                        fip.floating_ip_address, ','.join(pfw_ports))

        data = []
        for port in ports:
            if not parsed_args.node:
                node_name = next((node for node in nodes
                                  if node.uuid == port.node_uuid), None).name

            neutron_port_id = port.internal_info.get('tenant_vif_port_id')
            neutron_port = None

            if neutron_port_id:
                neutron_port = next((np for np in neutron_ports
                                     if np.id == neutron_port_id), None)

            if neutron_port is not None:
                network_id = neutron_port.network_id

                if not filter_network or filter_network.id == network_id:
                    network_names, _, fixed_ips \
                        = utils.get_full_network_info_from_port(
                            neutron_port, neutron_client, networks_dict)
                    floating_ip_addresses, floating_network_names \
                        = utils.get_floating_ip(neutron_port_id,
                                                floating_ips,
                                                networks_dict)
                    data.append([node_name, port.address,
                                 neutron_port.name,
                                 "\n".join(network_names),
                                 "\n".join(fixed_ips),
                                 "\n".join(floating_network_names)
                                 if floating_network_names else None,
                                 "\n".join(floating_ip_addresses)
                                 if floating_ip_addresses else None]
                                )
            elif not filter_network:
                data.append([node_name, port.address,
                             None, None, None, None, None])

        return ["Node", "MAC Address", "Port", "Network", "Fixed IP",
                "Floating Network", "Floating IP"], data


class Attach(command.ShowOne):
    """Attach network to node"""

    log = logging.getLogger(__name__ + ".Attach")

    def get_parser(self, prog_name):
        parser = super(Attach, self).get_parser(prog_name)
        parser.add_argument(
            "node",
            metavar="<node>",
            help=_("Name or UUID of the node"))
        parser.add_argument(
            "--network",
            metavar="<network>",
            help=_("Name or UUID of the network"))
        parser.add_argument(
            '--port',
            dest='port',
            metavar='<port>',
            help=_("Attach to this neutron port (name or UUID).")
        )
        parser.add_argument(
            '--trunk',
            dest='trunk',
            metavar='<trunk>',
            help=_("Attach to this trunk's (name or UUID) parent port.")
        )
        parser.add_argument(
            '--mac-address',
            dest='mac_address',
            metavar='<mac address>',
            help=_("Attach to this mac address.")
        )

        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)

        node_uuid = parsed_args.node
        if (parsed_args.network and parsed_args.port) \
           or (parsed_args.network and parsed_args.trunk) \
           or (parsed_args.port and parsed_args.trunk):
            raise exceptions.CommandError(
                "ERROR: Specify only one of network, port or trunk")
        if not parsed_args.network and not parsed_args.port \
           and not parsed_args.trunk:
            raise exceptions.CommandError(
                "ERROR: You must specify either network, port, or trunk")

        ironic_client = self.app.client_manager.baremetal
        neutron_client = self.app.client_manager.network

        if parsed_args.network:
            network = neutron_client.find_network(parsed_args.network)
            port = None
            if network is None:
                raise exceptions.CommandError(
                    "ERROR: Unknown network")
        elif parsed_args.port:
            port = neutron_client.find_port(parsed_args.port)
            if port is None:
                raise exceptions.CommandError(
                    "ERROR: This is not a port name or UUID")
        elif parsed_args.trunk:
            trunk = neutron_client.find_trunk(parsed_args.trunk)
            port = None
            if trunk is None:
                raise exceptions.CommandError(
                    "ERROR: no trunk named {0}".format(parsed_args.name))

        node = ironic_client.node.get(node_uuid)

        if parsed_args.mac_address:
            bp = ironic_client.port.get_by_address(parsed_args.mac_address)
            vif_info = {'port_uuid': bp.uuid}
            mac_string = " on {0}".format(parsed_args.mac_address)
        else:
            vif_info = {}
            mac_string = ""

            baremetal_ports = ironic_client.port.list(
                node=node_uuid, detail=True)
            has_free_port = False
            for bp in baremetal_ports:
                if 'tenant_vif_port_id' not in bp.internal_info:
                    has_free_port = True
                    break

            if not has_free_port:
                raise exceptions.CommandError(
                    "ERROR: Node {0} has no free ports".format(node.name))

        if port:
            print("Attaching port {1} to node {0}{2}".format(
                node.name, port.name, mac_string))
            ironic_client.node.vif_attach(node_uuid, port.id, **vif_info)
        elif parsed_args.network:
            print("Attaching network {1} to node {0}{2}".format(
                node.name, network.name, mac_string))
            port_name = utils.get_port_name(network.name, prefix=node.name)
            port = utils.get_or_create_port(port_name, network,
                                            neutron_client)
            ironic_client.node.vif_attach(node_uuid, port.id, **vif_info)
            port = neutron_client.get_port(port.id)
        elif parsed_args.trunk:
            print("Attaching trunk {1} to node {0}{2}".format(
                node.name, trunk.name, mac_string))
            port = neutron_client.get_port(trunk.port_id)
            ironic_client.node.vif_attach(node_uuid, port.id, **vif_info)

        network_names, port_names, fixed_ips \
            = utils.get_full_network_info_from_port(
                port, neutron_client)

        return ["Node", "MAC Address", "Port", "Network", "Fixed IP"], \
            [node.name, port.mac_address,
             "\n".join(port_names),
             "\n".join(network_names),
             "\n".join(fixed_ips)]


class Detach(command.Command):
    """Detach network from node"""

    log = logging.getLogger(__name__ + ".Detach")

    def get_parser(self, prog_name):
        parser = super(Detach, self).get_parser(prog_name)
        parser.add_argument(
            "node",
            metavar="<node>",
            help=_("Name or UUID of the node"))
        parser.add_argument(
            "--port",
            metavar="<port>",
            help=_("Name or UUID of the port"))

        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)

        node_uuid = parsed_args.node
        port_uuid = parsed_args.port

        ironic_client = self.app.client_manager.baremetal
        neutron_client = self.app.client_manager.network

        node = ironic_client.node.get(node_uuid)

        if port_uuid:
            port = neutron_client.find_port(port_uuid)
            if not port:
                raise exceptions.CommandError(
                    "ERROR: Port {1} not attached to node {0}".format(
                        node.name, port_uuid))
        else:
            bm_ports = ironic_client.port.list(node=node_uuid, detail=True)

            mapped_node_port_list = []
            for bm_port in bm_ports:
                if bm_port.internal_info.get("tenant_vif_port_id"):
                    mapped_node_port_list.append(bm_port)
            if(len(mapped_node_port_list) == 0):
                raise exceptions.CommandError(
                    "ERROR: Node {0} is not associated with any port".format(
                        node.name))
            elif(len(mapped_node_port_list) > 1):
                raise exceptions.CommandError(
                    "ERROR: Node {0} is associated with multiple ports.\
                    Port must be specified with --port".format(node.name))
            elif(len(mapped_node_port_list) == 1):
                port_uuid = mapped_node_port_list[0].internal_info[
                    "tenant_vif_port_id"]
                port = neutron_client.find_port(port_uuid)

        print("Detaching node {0} from port {1}".format(
            node.name, port.name))

        ironic_client.node.vif_detach(node_uuid, port.id)

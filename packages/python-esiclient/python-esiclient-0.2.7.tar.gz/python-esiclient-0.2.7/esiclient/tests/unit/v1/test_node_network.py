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
#

import mock

from osc_lib import exceptions

from esiclient.tests.unit import base
from esiclient.tests.unit import utils
from esiclient.v1 import node_network


class TestList(base.TestCommand):

    def setUp(self):
        super(TestList, self).setUp()
        self.cmd = node_network.List(self.app, None)

        self.port1 = utils.create_mock_object({
            "uuid": "port_uuid_1",
            "node_uuid": "11111111-2222-3333-4444-aaaaaaaaaaaa",
            "address": "aa:aa:aa:aa:aa:aa",
            "internal_info": {'tenant_vif_port_id': 'neutron_port_uuid_1'}
        })
        self.port2 = utils.create_mock_object({
            "uuid": "port_uuid_2",
            "node_uuid": "11111111-2222-3333-4444-bbbbbbbbbbbb",
            "address": "bb:bb:bb:bb:bb:bb",
            "internal_info": {}
        })
        self.port3 = utils.create_mock_object({
            "uuid": "port_uuid_3",
            "node_uuid": "11111111-2222-3333-4444-bbbbbbbbbbbb",
            "address": "cc:cc:cc:cc:cc:cc",
            "internal_info": {'tenant_vif_port_id': 'neutron_port_uuid_2'}
        })
        self.port4 = utils.create_mock_object({
            "uuid": "port_uuid_4",
            "node_uuid": "11111111-2222-3333-4444-bbbbbbbbbbbb",
            "address": "dd:dd:dd:dd:dd:dd",
            "internal_info": {'tenant_vif_port_id': 'neutron_port_uuid_4'}
        })
        self.node1 = utils.create_mock_object({
            "uuid": "11111111-2222-3333-4444-aaaaaaaaaaaa",
            "name": "node1"
        })
        self.node2 = utils.create_mock_object({
            "uuid": "11111111-2222-3333-4444-bbbbbbbbbbbb",
            "name": "node2"
        })
        self.network = utils.create_mock_object({
            "id": "network_uuid",
            "name": "test_network"
        })
        self.neutron_port1 = utils.create_mock_object({
            "id": "neutron_port_uuid_1",
            "network_id": "network_uuid",
            "name": "neutron_port_1",
            "fixed_ips": [{"ip_address": "1.1.1.1"}],
            "trunk_details": None
        })
        self.neutron_port2 = utils.create_mock_object({
            "id": "neutron_port_uuid_2",
            "network_id": "network_uuid",
            "name": "neutron_port_2",
            "fixed_ips": [{"ip_address": "2.2.2.2"}],
            "trunk_details": None
        })
        self.floating_network = utils.create_mock_object({
            "id": "floating_network_id",
            "name": "floating_network"
        })
        self.floating_ip = utils.create_mock_object({
            "id": "floating_ip_uuid_2",
            "floating_ip_address": "8.8.8.8",
            "floating_network_id": "floating_network_id",
            "port_id": "neutron_port_uuid_2"
        })
        self.floating_ip_pfw = utils.create_mock_object({
            "id": "floating_ip_uuid_1",
            "floating_ip_address": "9.9.9.9",
            "floating_network_id": "floating_network_id",
            "port_id": None
        })
        self.pfw1 = utils.create_mock_object({
            "internal_port": 22,
            "external_port": 22,
            "internal_port_id": "neutron_port_uuid_1"
        })
        self.pfw2 = utils.create_mock_object({
            "internal_port": 23,
            "external_port": 23,
            "internal_port_id": "neutron_port_uuid_1"
        })

        def mock_node_get(node_uuid):
            if node_uuid == "11111111-2222-3333-4444-aaaaaaaaaaaa":
                return self.node1
            elif node_uuid == "11111111-2222-3333-4444-bbbbbbbbbbbb":
                return self.node2
            return None
        self.app.client_manager.baremetal.node.get.side_effect = mock_node_get

        def mock_neutron_port_get(port_uuid):
            if port_uuid == "neutron_port_uuid_1":
                return self.neutron_port1
            elif port_uuid == "neutron_port_uuid_2":
                return self.neutron_port2
            return None
        self.app.client_manager.network.get_port.\
            side_effect = mock_neutron_port_get

        def mock_neutron_port_forwardings(fip):
            if fip.id == "floating_ip_uuid_1":
                return [self.pfw1, self.pfw2]
            return []
        self.app.client_manager.network.port_forwardings.\
            side_effect = mock_neutron_port_forwardings

        self.app.client_manager.network.find_network.\
            return_value = self.network
        self.app.client_manager.network.get_network.\
            return_value = self.network
        self.app.client_manager.network.ports.\
            return_value = [self.neutron_port1, self.neutron_port2]
        self.app.client_manager.network.networks.\
            return_value = [self.network, self.floating_network]
        self.app.client_manager.baremetal.node.list.\
            return_value = [self.node1, self.node2]
        self.app.client_manager.network.ips.\
            return_value = [self.floating_ip, self.floating_ip_pfw]

    def test_take_action(self):
        self.app.client_manager.baremetal.port.list.\
            return_value = [self.port1, self.port2, self.port3]

        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        results = self.cmd.take_action(parsed_args)
        expected = (
          ["Node", "MAC Address", "Port", "Network", "Fixed IP",
           "Floating Network", "Floating IP"],
          [['node1', 'aa:aa:aa:aa:aa:aa', 'neutron_port_1', 'test_network',
           '1.1.1.1', 'floating_network', '9.9.9.9 (22:22,23:23)'],
           ['node2', 'bb:bb:bb:bb:bb:bb', None, None, None, None, None],
           ['node2', 'cc:cc:cc:cc:cc:cc', 'neutron_port_2', 'test_network',
            '2.2.2.2', 'floating_network', '8.8.8.8']]
        )
        self.assertEqual(expected, results)
        self.app.client_manager.baremetal.port.list.\
            assert_called_once_with(detail=True)

    def test_take_action_neutron_port_does_not_exist(self):
        self.app.client_manager.baremetal.port.list.\
            return_value = [self.port4]

        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        results = self.cmd.take_action(parsed_args)
        expected = (
            ["Node", "MAC Address", "Port", "Network", "Fixed IP",
             "Floating Network", "Floating IP"],
            [["node2", "dd:dd:dd:dd:dd:dd", None, None, None, None, None]]
        )
        self.assertEqual(expected, results)
        self.app.client_manager.baremetal.port.list.\
            assert_called_once_with(detail=True)

    def test_take_action_node_filter(self):
        self.app.client_manager.baremetal.port.list.\
            return_value = [self.port2, self.port3]

        arglist = ['--node', '11111111-2222-3333-4444-bbbbbbbbbbbb']
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        results = self.cmd.take_action(parsed_args)
        expected = (
           ["Node", "MAC Address", "Port", "Network", "Fixed IP",
            "Floating Network", "Floating IP"],
           [['node2', 'bb:bb:bb:bb:bb:bb', None, None, None, None, None],
            ['node2', 'cc:cc:cc:cc:cc:cc', 'neutron_port_2', 'test_network',
             '2.2.2.2', 'floating_network', '8.8.8.8']]
        )
        self.assertEqual(expected, results)
        self.app.client_manager.baremetal.port.list.\
            assert_called_once_with(
                node="11111111-2222-3333-4444-bbbbbbbbbbbb", detail=True)

    def test_take_action_network_filter(self):

        self.app.client_manager.baremetal.port.list.\
            return_value = [self.port1, self.port2, self.port3]

        arglist = ['--network', 'network']
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        results = self.cmd.take_action(parsed_args)
        expected = (
            ["Node", "MAC Address", "Port", "Network", "Fixed IP",
             "Floating Network", "Floating IP"],
            [["node1", "aa:aa:aa:aa:aa:aa",
              "neutron_port_1", "test_network", "1.1.1.1",
              "floating_network", "9.9.9.9 (22:22,23:23)"],
             ["node2", "cc:cc:cc:cc:cc:cc",
              "neutron_port_2", "test_network", "2.2.2.2",
              "floating_network", "8.8.8.8"]]
        )
        self.assertEqual(expected, results)
        self.app.client_manager.baremetal.port.list.\
            assert_called_once_with(detail=True)

    def test_take_action_node_network_filter(self):
        self.app.client_manager.baremetal.port.list.\
            return_value = [self.port2, self.port3]

        arglist = ['--node', 'node2', '--network', 'network']
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        results = self.cmd.take_action(parsed_args)
        expected = (
            ["Node", "MAC Address", "Port", "Network", "Fixed IP",
             "Floating Network", "Floating IP"],
            [["node2", "cc:cc:cc:cc:cc:cc",
              "neutron_port_2", "test_network", "2.2.2.2",
              "floating_network", "8.8.8.8"]]
        )
        self.assertEqual(expected, results)
        self.app.client_manager.baremetal.port.list.\
            assert_called_once_with(node="node2", detail=True)


class TestAttach(base.TestCommand):

    def setUp(self):
        super(TestAttach, self).setUp()
        self.cmd = node_network.Attach(self.app, None)

        self.port1 = utils.create_mock_object({
            "uuid": "port_uuid_1",
            "node_uuid": "node_uuid_1",
            "address": "aa:aa:aa:aa:aa:aa",
            "internal_info": {'tenant_vif_port_id': 'neutron_port_uuid_1'}
        })
        self.port2 = utils.create_mock_object({
            "uuid": "port_uuid_2",
            "node_uuid": "node_uuid_1",
            "address": "bb:bb:bb:bb:bb:bb",
            "internal_info": {}
        })
        self.node = utils.create_mock_object({
            "uuid": "node_uuid_1",
            "name": "node1",
            "provision_state": "active"
        })
        self.node_available = utils.create_mock_object({
            "uuid": "node_uuid_1",
            "name": "node1",
            "provision_state": "available"
        })
        self.node_manageable = utils.create_mock_object({
            "uuid": "node_uuid_1",
            "name": "node1",
            "provision_state": "manageable",
            "instance_info": {},
            "driver_info": {'deploy_ramdisk': 'fake-image'},
        })
        self.node_manageable_instance_info = utils.create_mock_object({
            "uuid": "node_uuid_1",
            "name": "node1",
            "provision_state": "manageable",
            "instance_info": {'image_source': 'fake-image',
                              'capabilities': {}},
            "driver_info": {'deploy_ramdisk': 'fake-image'},
        })
        self.network = utils.create_mock_object({
            "id": "network_uuid",
            "name": "test_network"
        })
        self.neutron_port = utils.create_mock_object({
            "id": "neutron_port_uuid_2",
            "network_id": "network_uuid",
            "name": "node1-port",
            "mac_address": "bb:bb:bb:bb:bb:bb",
            "fixed_ips": [{"ip_address": "2.2.2.2"}],
            "trunk_details": None
        })
        self.trunk = utils.create_mock_object({
            "port_id": self.neutron_port.id,
            "name": "test_trunk"
        })

        self.app.client_manager.network.find_network.\
            return_value = self.network
        self.app.client_manager.network.get_network.\
            return_value = self.network
        self.app.client_manager.network.create_port.\
            return_value = self.neutron_port
        self.app.client_manager.network.find_port.\
            return_value = self.neutron_port
        self.app.client_manager.network.get_port.\
            return_value = self.neutron_port
        self.app.client_manager.network.ports.\
            return_value = []
        self.app.client_manager.network.find_trunk.\
            return_value = self.trunk

    @mock.patch('esiclient.utils.get_full_network_info_from_port',
                return_value=(["test_network"], ["node1-port"],
                              ["2.2.2.2"]),
                autospec=True)
    def test_take_action_network(self, mock_gfnifp):
        self.app.client_manager.baremetal.node.get.\
            return_value = self.node
        self.app.client_manager.baremetal.port.list.\
            return_value = [self.port1, self.port2]

        arglist = ['node1', '--network', 'test_network']
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        results = self.cmd.take_action(parsed_args)
        expected = (
            ["Node", "MAC Address", "Port", "Network", "Fixed IP"],
            ["node1", "bb:bb:bb:bb:bb:bb", "node1-port", "test_network",
             "2.2.2.2"]
        )
        self.assertEqual(expected, results)
        self.app.client_manager.network.create_port.\
            assert_called_once_with(name='esi-node1-test_network',
                                    network_id=self.network.id,
                                    device_owner='baremetal:none')
        self.app.client_manager.baremetal.node.vif_attach.\
            assert_called_once_with('node1', self.neutron_port.id)
        mock_gfnifp.assert_called_once

    @mock.patch('esiclient.utils.get_full_network_info_from_port',
                return_value=(["test_network"], ["node1-port"],
                              ["2.2.2.2"]),
                autospec=True)
    def test_take_action_port(self, mock_gfnifp):
        self.app.client_manager.baremetal.node.get.\
            return_value = self.node
        self.app.client_manager.baremetal.port.list.\
            return_value = [self.port1, self.port2]

        arglist = ['node1', '--port', 'node1-port']
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        results = self.cmd.take_action(parsed_args)
        expected = (
            ["Node", "MAC Address", "Port", "Network", "Fixed IP"],
            ["node1", "bb:bb:bb:bb:bb:bb", "node1-port", "test_network",
             "2.2.2.2"]
        )
        self.assertEqual(expected, results)
        self.app.client_manager.network.find_port.\
            assert_called_once_with("node1-port")
        self.app.client_manager.baremetal.node.vif_attach.\
            assert_called_once_with('node1', self.neutron_port.id)
        mock_gfnifp.assert_called_once

    @mock.patch('esiclient.utils.get_full_network_info_from_port',
                return_value=(["test_network"], ["node1-port"],
                              ["2.2.2.2"]),
                autospec=True)
    def test_take_action_port_and_mac_address(self, mock_gfnifp):
        self.app.client_manager.baremetal.node.get.\
            return_value = self.node
        self.app.client_manager.baremetal.port.get_by_address.\
            return_value = self.port2

        arglist = ['node1', '--port', 'node1-port',
                   '--mac-address', 'bb:bb:bb:bb:bb:bb']
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        results = self.cmd.take_action(parsed_args)
        expected = (
            ["Node", "MAC Address", "Port", "Network", "Fixed IP"],
            ["node1", "bb:bb:bb:bb:bb:bb", "node1-port", "test_network",
             "2.2.2.2"]
        )
        self.assertEqual(expected, results)
        self.app.client_manager.network.find_port.\
            assert_called_once_with("node1-port")
        self.app.client_manager.baremetal.port.get_by_address.\
            assert_called_once_with('bb:bb:bb:bb:bb:bb')
        self.app.client_manager.baremetal.node.vif_attach.\
            assert_called_once_with('node1', self.neutron_port.id,
                                    port_uuid='port_uuid_2')
        mock_gfnifp.assert_called_once

    @mock.patch('esiclient.utils.get_full_network_info_from_port',
                return_value=(["test_network"], ["node1-port"],
                              ["2.2.2.2"]),
                autospec=True)
    def test_take_action_trunk(self, mock_gfnifp):
        self.app.client_manager.baremetal.node.get.\
            return_value = self.node
        self.app.client_manager.baremetal.port.list.\
            return_value = [self.port1, self.port2]

        arglist = ['node1', '--trunk', 'test_trunk']
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        results = self.cmd.take_action(parsed_args)
        expected = (
            ["Node", "MAC Address", "Port", "Network", "Fixed IP"],
            ["node1", "bb:bb:bb:bb:bb:bb", "node1-port",
             "test_network", "2.2.2.2"]
        )
        self.assertEqual(expected, results)
        self.app.client_manager.network.find_trunk.\
            assert_called_once_with("test_trunk")
        self.app.client_manager.baremetal.node.vif_attach.\
            assert_called_once_with('node1', self.neutron_port.id)
        mock_gfnifp.assert_called_once

    def test_take_action_port_network_and_trunk_exception(self):
        arglist1 = ['node1', '--network', 'test_network', '--port', 'node1']
        arglist2 = ['node1', '--network', 'test_network', '--trunk', 'trunk']
        arglist3 = ['node1', '--port', 'node1', '--trunk', 'trunk']
        arglist4 = ['node1', '--network', 'test_network', '--port', 'node1',
                    '--trunk', 'trunk']
        verifylist = []

        parsed_args1 = self.check_parser(self.cmd, arglist1, verifylist)
        parsed_args2 = self.check_parser(self.cmd, arglist2, verifylist)
        parsed_args3 = self.check_parser(self.cmd, arglist3, verifylist)
        parsed_args4 = self.check_parser(self.cmd, arglist4, verifylist)

        self.assertRaisesRegex(
            exceptions.CommandError,
            'ERROR: Specify only one of network, port or trunk',
            self.cmd.take_action, parsed_args1)
        self.assertRaisesRegex(
            exceptions.CommandError,
            'ERROR: Specify only one of network, port or trunk',
            self.cmd.take_action, parsed_args2)
        self.assertRaisesRegex(
            exceptions.CommandError,
            'ERROR: Specify only one of network, port or trunk',
            self.cmd.take_action, parsed_args3)
        self.assertRaisesRegex(
            exceptions.CommandError,
            'ERROR: Specify only one of network, port or trunk',
            self.cmd.take_action, parsed_args4)

    def test_take_action_no_port_or_network_or_trunk_exception(self):
        arglist = ['node1']
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.assertRaisesRegex(
            exceptions.CommandError,
            'ERROR: You must specify either network, port, or trunk',
            self.cmd.take_action, parsed_args)

    def test_take_action_invalid_network_exception(self):
        self.app.client_manager.baremetal.node.get.\
            return_value = self.node
        self.app.client_manager.baremetal.port.list.\
            return_value = [self.port1]
        self.app.client_manager.network.find_network.\
            return_value = None

        arglist = ['node1', '--network', 'test_network_invalid']
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.assertRaisesRegex(
            exceptions.CommandError,
            'ERROR: Unknown network',
            self.cmd.take_action, parsed_args)

    def test_take_action_port_free_exception(self):
        self.app.client_manager.baremetal.node.get.\
            return_value = self.node
        self.app.client_manager.baremetal.port.list.\
            return_value = [self.port1]

        arglist = ['node1', '--network', 'test_network']
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.assertRaisesRegex(
            exceptions.CommandError,
            'ERROR: Node node1 has no free ports',
            self.cmd.take_action, parsed_args)


class TestDetach(base.TestCommand):

    def setUp(self):
        super(TestDetach, self).setUp()
        self.cmd = node_network.Detach(self.app, None)

        self.node = utils.create_mock_object({
            "uuid": "node_uuid_1",
            "name": "node1",
            "provision_state": "active"
        })
        self.neutron_port1 = utils.create_mock_object({
            "id": "neutron_port_uuid_1",
            "network_id": "network_uuid",
            "name": "node1",
            "mac_address": "bb:bb:bb:bb:bb:bb",
            "fixed_ips": [{"ip_address": "2.2.2.2"}],
            "trunk_details": None
        })
        self.neutron_port2 = utils.create_mock_object({
            "id": "neutron_port_uuid_2",
            "network_id": "network_uuid",
            "name": "node1",
            "mac_address": "cc:cc:cc:cc:cc:cc",
            "fixed_ips": [{"ip_address": "3.3.3.3"}],
            "trunk_details": None
        })
        self.port1 = utils.create_mock_object({
            "uuid": "port_uuid_1",
            "node_uuid": "node_uuid_1",
            "address": "aa:aa:aa:aa:aa:aa",
            "internal_info": {'tenant_vif_port_id': 'neutron_port_uuid_1'}
        })
        self.port2 = utils.create_mock_object({
            "uuid": "port_uuid_2",
            "node_uuid": "node_uuid_1",
            "address": "bb:bb:bb:bb:bb:bb",
            "internal_info": {}
        })
        self.port3 = utils.create_mock_object({
            "uuid": "port_uuid_3",
            "node_uuid": "node_uuid_1",
            "address": "cc:cc:cc:cc:cc:cc",
            "internal_info": {'tenant_vif_port_id': 'neutron_port_uuid_2'}
        })

        self.app.client_manager.baremetal.node.get.\
            return_value = self.node

    def test_take_action(self):
        self.app.client_manager.network.find_port.\
            return_value = self.neutron_port1
        self.app.client_manager.baremetal.port.list.\
            return_value = [self.port1]

        arglist = ['node1']
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)
        self.app.client_manager.baremetal.node.vif_detach.\
            assert_called_once_with('node1', self.neutron_port1.id)

    def test_take_multiple_port_action(self):
        self.app.client_manager.network.find_port.\
            return_value = self.neutron_port1
        self.app.client_manager.baremetal.port.list.\
            return_value = [self.port1, self.port2]

        arglist = ['node1', '--port', 'port_uuid_1']
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)
        self.app.client_manager.baremetal.node.vif_detach.\
            assert_called_once_with('node1', self.neutron_port1.id)

    def test_take_action_port_exception(self):
        self.app.client_manager.network.find_port.\
            return_value = None
        self.app.client_manager.baremetal.port.list.\
            return_value = [self.port1, self.port2]

        arglist = ['node1', '--port', 'bad-port']
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.assertRaisesRegex(
            exceptions.CommandError,
            'ERROR: Port bad-port not attached to node node1',
            self.cmd.take_action, parsed_args
        )

    def test_take_action_mutiple_port_exception(self):
        self.app.client_manager.network.find_port.\
            return_value = None
        self.app.client_manager.baremetal.port.list.\
            return_value = [self.port1, self.port2, self.port3]

        arglist = ['node1']
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.assertRaisesRegex(
            exceptions.CommandError,
            'ERROR: Node node1 is associated with multiple ports.\
                    Port must be specified with --port',
            self.cmd.take_action, parsed_args
        )

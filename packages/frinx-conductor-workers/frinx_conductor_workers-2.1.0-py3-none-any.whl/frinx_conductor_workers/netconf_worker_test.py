import json
import unittest
from unittest.mock import patch

import frinx_conductor_workers.netconf_worker
from frinx_conductor_workers.frinx_rest import uniconfig_url_base

netconf_node_connecting = {
    "node": [
        {
            "node-id": "xr6",
            "netconf-node-topology:host": "192.168.1.213",
            "netconf-node-topology:connected-message": "Connecting",
            "netconf-node-topology:connection-status": "connecting",
            "netconf-node-topology:port": 830,
        }
    ]
}

netconf_node_connected = {
    "node": [
        {
            "node-id": "xr6",
            "netconf-node-topology:unavailable-capabilities": {"unavailable-capability": []},
            "netconf-node-topology:available-capabilities": {"available-capability": []},
            "netconf-node-topology:host": "192.168.1.213",
            "netconf-node-topology:connected-message": "Success",
            "netconf-node-topology:connection-status": "connected",
            "netconf-node-topology:port": 830,
            "topology-node-extension:node-type-fingerprint": "1319530689",
        }
    ]
}

netconf_node_non_exist = {
    "errors": {
        "error": [
            {
                "error-message": "Request could not be completed because the relevant data model content does not exist",
                "error-tag": "data-missing",
                "error-type": "protocol",
            }
        ]
    }
}

bad_request_response = {
    "errors": {
        "error": [
            {
                "error-type": "protocol",
                "error-tag": "data-missing",
                "error-message": "Request could not be completed because the relevant data model content does not exist",
            }
        ]
    }
}

alarms_response = {
    "alarms": {
        "alarm": [
            {
                "id": "302/1",
                "state": {
                    "severity": "openconfig-alarm-types:CRITICAL",
                    "id": "302",
                    "text": "Physical Port Link Down",
                    "time-created": 1597308680,
                    "resource": "GigabitEthernet0/0/1",
                },
            },
            {
                "id": "387/1",
                "state": {
                    "severity": "openconfig-alarm-types:CRITICAL",
                    "id": "387",
                    "text": "Transceiver Missing - Link Down",
                    "time-created": 1597308667,
                    "resource": "subslot 0/0 transceiver container 2",
                },
            },
        ]
    }
}

netconf_node_already_installed = {
    "errors": {
        "error": [
            {
                "error-tag": "data-exists",
                "error-info": {"node-id": "xr6", "topology-id": "protocol"},
                "error-message": "Node has already been installed using other protocols",
                "error-type": "application",
            }
        ]
    }
}


class MockResponse:
    def __init__(self, content, status_code):
        self.content = content
        self.status_code = status_code

    def json(self):
        return self.content


class TestMount(unittest.TestCase):
    def test_mount_new_device(self):
        with patch("frinx_conductor_workers.netconf_worker.requests.post") as mock:
            mock.return_value = MockResponse(bytes(json.dumps({}), encoding="utf-8"), 204)
            request = frinx_conductor_workers.netconf_worker.execute_mount_netconf(
                {
                    "inputData": {
                        "device_id": "xr6",
                        "host": "192.168.1.1",
                        "port": "830",
                        "keepalive-delay": "1000",
                        "tcp-only": "false",
                        "username": "name",
                        "password": "password",
                    }
                }
            )
            self.assertEqual(request["status"], "COMPLETED")
            self.assertEqual(
                request["output"]["url"],
                uniconfig_url_base + "/operations/connection-manager:install-node",
            )
            self.assertEqual(request["output"]["response_code"], 204)
            self.assertEqual(request["output"]["response_body"], {})

    def test_mount_existing_device(self):
        with patch("frinx_conductor_workers.netconf_worker.requests.post") as mock:
            mock.return_value = MockResponse(
                bytes(json.dumps(netconf_node_already_installed), encoding="utf-8"), 409
            )
            request = frinx_conductor_workers.netconf_worker.execute_mount_netconf(
                {
                    "inputData": {
                        "device_id": "xr6",
                        "host": "192.168.1.1",
                        "port": "830",
                        "keepalive-delay": "1000",
                        "tcp-only": "false",
                        "username": "name",
                        "password": "password",
                    }
                }
            )
            self.assertEqual(request["status"], "COMPLETED")
            self.assertEqual(
                request["output"]["url"],
                uniconfig_url_base + "/operations/connection-manager:install-node",
            )
            self.assertEqual(request["output"]["response_code"], 409)
            self.assertEqual(request["output"]["response_body"], netconf_node_already_installed)


class TestUnmount(unittest.TestCase):
    def test_unmount_existing_device(self):
        with patch("frinx_conductor_workers.netconf_worker.requests.post") as mock:
            mock.return_value = MockResponse(bytes(json.dumps({}), encoding="utf-8"), 204)
            request = frinx_conductor_workers.netconf_worker.execute_unmount_netconf(
                {"inputData": {"device_id": "xr6"}}
            )
            self.assertEqual(request["status"], "COMPLETED")
            self.assertEqual(
                request["output"]["url"],
                uniconfig_url_base + "/operations/connection-manager:uninstall-node",
            )
            self.assertEqual(request["output"]["response_code"], 204)
            self.assertEqual(request["output"]["response_body"], {})


class TestReadStructuredData(unittest.TestCase):
    def test_read_structured_data_with_device(self):
        with patch("frinx_conductor_workers.netconf_worker.requests.get") as mock:
            mock.return_value = MockResponse(
                bytes(json.dumps(alarms_response), encoding="utf-8"), 200
            )
            request = frinx_conductor_workers.netconf_worker.read_structured_data(
                {"inputData": {"device_id": "xr5", "uri": "/openconfig-system/system/alarms"}}
            )
            self.assertEqual(request["status"], "COMPLETED")
            self.assertEqual(
                request["output"]["url"],
                uniconfig_url_base
                + "/data/network-topology:network-topology/topology=topology-netconf/node=xr5"
                "/yang-ext:mount/openconfig-system/system/alarms",
            )
            self.assertEqual(request["output"]["response_code"], 200)
            self.assertEqual(len(request["output"]["response_body"]["alarms"]["alarm"]), 2)
            self.assertEqual(
                request["output"]["response_body"]["alarms"]["alarm"][0]["id"], "302/1"
            )
            self.assertEqual(
                request["output"]["response_body"]["alarms"]["alarm"][0]["state"]["text"],
                "Physical Port Link Down",
            )
            self.assertEqual(
                request["output"]["response_body"]["alarms"]["alarm"][1]["id"], "387/1"
            )
            self.assertEqual(
                request["output"]["response_body"]["alarms"]["alarm"][1]["state"]["text"],
                "Transceiver Missing - Link Down",
            )

    def test_read_structured_data_no_device(self):
        with patch("frinx_conductor_workers.netconf_worker.requests.get") as mock:
            mock.return_value = MockResponse(
                bytes(json.dumps(bad_request_response), encoding="utf-8"), 404
            )
            request = frinx_conductor_workers.netconf_worker.read_structured_data(
                {"inputData": {"device_id": "", "uri": "/openconfig-system/system/alarms"}}
            )
            self.assertEqual(request["status"], "FAILED")
            self.assertEqual(request["output"]["response_code"], 404)
            self.assertEqual(
                request["output"]["response_body"]["errors"]["error"][0]["error-type"], "protocol"
            )
            self.assertEqual(
                request["output"]["response_body"]["errors"]["error"][0]["error-message"],
                "Request could not be completed because the relevant data model content does not exist",
            )


class TestCheckCliConnected(unittest.TestCase):
    def test_execute_check_connected_netconf_connecting(self):
        with patch("frinx_conductor_workers.netconf_worker.requests.get") as mock:
            mock.return_value = MockResponse(
                bytes(json.dumps(netconf_node_connecting), encoding="utf-8"), 200
            )
            request = frinx_conductor_workers.netconf_worker.execute_check_connected_netconf(
                {"inputData": {"device_id": "xr6"}}
            )
            self.assertEqual(request["status"], "FAILED")
            self.assertEqual(
                request["output"]["url"],
                uniconfig_url_base
                + "/data/network-topology:network-topology/topology=topology-netconf"
                "/node=xr6?content=nonconfig",
            )
            self.assertEqual(
                request["output"]["response_body"]["node"][0][
                    "netconf-node-topology:connection-status"
                ],
                "connecting",
            )

    def test_execute_check_connected_netconf_connected(self):
        with patch("frinx_conductor_workers.netconf_worker.requests.get") as mock:
            mock.return_value = MockResponse(
                bytes(json.dumps(netconf_node_connected), encoding="utf-8"), 200
            )
            request = frinx_conductor_workers.netconf_worker.execute_check_connected_netconf(
                {"inputData": {"device_id": "xr6"}}
            )
            self.assertEqual(request["status"], "COMPLETED")
            self.assertEqual(
                request["output"]["url"],
                uniconfig_url_base
                + "/data/network-topology:network-topology/topology=topology-netconf"
                "/node=xr6?content=nonconfig",
            )
            self.assertEqual(
                request["output"]["response_body"]["node"][0][
                    "netconf-node-topology:connection-status"
                ],
                "connected",
            )


if __name__ == "__main__":
    unittest.main()

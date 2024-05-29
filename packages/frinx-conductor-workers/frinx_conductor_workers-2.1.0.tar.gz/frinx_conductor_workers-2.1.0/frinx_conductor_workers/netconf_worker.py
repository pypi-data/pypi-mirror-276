from __future__ import print_function

import copy
import json
import logging
from string import Template

import requests
from frinx_conductor_workers.frinx_rest import additional_uniconfig_request_params
from frinx_conductor_workers.frinx_rest import extract_uniconfig_cookies
from frinx_conductor_workers.frinx_rest import get_uniconfig_cluster_from_task
from frinx_conductor_workers.frinx_rest import parse_response

local_logs = logging.getLogger(__name__)

uniconfig_url_netconf_mount = (
    "$base_url/data/network-topology:network-topology/topology=topology-netconf/node=$id"
)
uniconfig_url_netconf_mount_sync = "$base_url/operations/connection-manager:install-node"
uniconfig_url_netconf_unmount_sync = "$base_url/operations/connection-manager:uninstall-node"
uniconfig_url_netconf_mount_oper = "$base_url/data/network-topology:network-topology/topology=topology-netconf/node=$id?content=nonconfig"

sync_mount_template = {
    "input": {
        "node-id": "",
        "netconf": {
            "netconf-node-topology:host": "",
            "netconf-node-topology:port": 2022,
            "netconf-node-topology:keepalive-delay": 5,
            "netconf-node-topology:max-connection-attempts": 1,
            "netconf-node-topology:connection-timeout-millis": 60000,
            "netconf-node-topology:default-request-timeout-millis": 60000,
            "netconf-node-topology:tcp-only": False,
            "netconf-node-topology:username": "",
            "netconf-node-topology:password": "",
            "netconf-node-topology:sleep-factor": 1.0,
            "uniconfig-config:uniconfig-native-enabled": True,
            "netconf-node-topology:edit-config-test-option": "set",
            "uniconfig-config:blacklist": {"extension": ["tailf:display-when false"]},
        },
    }
}


def execute_mount_netconf(task):
    """
    Build a template for netconf mounting body after parsing input device
    parameters and send a PUT request to Uniconfig. These requests can be
    viewed and tested also in postman collections for each device.

    Args:
        task: A dict with a complete device data
    Returns:
        response: dict, e.g. {'status': 'COMPLETED', 'output': {'url': id_url,
                                                  'request_body': mount_body,
                                                  'response_code': 200,
                                                  'response_body': response_json},
                }}
    """
    # First, check the validity of the provided IP address.

    device_id = task["inputData"]["device_id"]

    mount_body = copy.deepcopy(sync_mount_template)
    mount_body["input"]["node-id"] = task["inputData"]["device_id"]
    mount_body["input"]["netconf"]["netconf-node-topology:host"] = task["inputData"]["host"]
    mount_body["input"]["netconf"]["netconf-node-topology:port"] = task["inputData"]["port"]
    mount_body["input"]["netconf"]["netconf-node-topology:keepalive-delay"] = task["inputData"][
        "keepalive-delay"
    ]
    mount_body["input"]["netconf"]["netconf-node-topology:tcp-only"] = task["inputData"]["tcp-only"]
    mount_body["input"]["netconf"]["netconf-node-topology:username"] = task["inputData"]["username"]
    mount_body["input"]["netconf"]["netconf-node-topology:password"] = task["inputData"]["password"]

    if (
        "reconcile" in task["inputData"]
        and task["inputData"]["reconcile"] is not None
        and task["inputData"]["reconcile"] != ""
    ):
        mount_body["input"]["netconf"]["node-extension:reconcile"] = task["inputData"]["reconcile"]

    if (
        "schema-cache-directory" in task["inputData"]
        and task["inputData"]["schema-cache-directory"] is not None
        and task["inputData"]["schema-cache-directory"] != ""
    ):
        mount_body["input"]["netconf"]["netconf-node-topology:schema-cache-directory"] = task[
            "inputData"
        ]["schema-cache-directory"]

    if (
        "sleep-factor" in task["inputData"]
        and task["inputData"]["sleep-factor"] is not None
        and task["inputData"]["sleep-factor"] != ""
    ):
        mount_body["input"]["netconf"]["netconf-node-topology:sleep-factor"] = task["inputData"][
            "sleep-factor"
        ]

    if (
        "between-attempts-timeout-millis" in task["inputData"]
        and task["inputData"]["between-attempts-timeout-millis"] is not None
        and task["inputData"]["between-attempts-timeout-millis"] != ""
    ):
        mount_body["input"]["netconf"]["netconf-node-topology:between-attempts-timeout-millis"] = (
            task["inputData"]["between-attempts-timeout-millis"]
        )

    if (
        "connection-timeout-millis" in task["inputData"]
        and task["inputData"]["connection-timeout-millis"] is not None
        and task["inputData"]["connection-timeout-millis"] != ""
    ):
        mount_body["input"]["netconf"]["netconf-node-topology:connection-timeout-millis"] = task[
            "inputData"
        ]["connection-timeout-millis"]

    if (
        "uniconfig-native" in task["inputData"]
        and task["inputData"]["uniconfig-native"] is not None
        and task["inputData"]["uniconfig-native"] != ""
    ):
        mount_body["input"]["netconf"]["uniconfig-config:uniconfig-native-enabled"] = task[
            "inputData"
        ]["uniconfig-native"]

    if "blacklist" in task["inputData"] and task["inputData"]["blacklist"] is not None:
        mount_body["input"]["netconf"]["uniconfig-config:blacklist"] = {"uniconfig-config:path": []}
        model_array = [model.strip() for model in task["inputData"]["blacklist"].split(",")]
        for model in model_array:
            mount_body["input"]["netconf"]["uniconfig-config:blacklist"][
                "uniconfig-config:path"
            ].append(model)

    if (
        "dry-run-journal-size" in task["inputData"]
        and task["inputData"]["dry-run-journal-size"] is not None
    ):
        mount_body["input"]["netconf"]["netconf-node-topology:dry-run-journal-size"] = task[
            "inputData"
        ]["dry-run-journal-size"]

    if (
        "enabled-notifications" in task["inputData"]
        and task["inputData"]["enabled-notifications"] is not None
    ):
        mount_body["input"]["netconf"]["netconf-node-topology:enabled-notifications"] = task[
            "inputData"
        ]["enabled-notifications"]

    if "capability" in task["inputData"]:
        mount_body["input"]["netconf"]["netconf-node-topology:yang-module-capabilities"] = {
            "capability": []
        }
        mount_body["input"]["netconf"]["netconf-node-topology:yang-module-capabilities"][
            "capability"
        ].append(task["inputData"]["capability"])

    id_url = Template(uniconfig_url_netconf_mount_sync).substitute(
        {"base_url": get_uniconfig_cluster_from_task(task)}
    )

    r = requests.post(
        id_url, data=json.dumps(mount_body), timeout=600, **additional_uniconfig_request_params
    )
    response_code, response_json = parse_response(r)

    if response_code in [requests.codes.no_content, requests.codes.conflict]:
        return {
            "status": "COMPLETED",
            "output": {
                "url": id_url,
                "request_body": mount_body,
                "response_code": response_code,
                "response_body": response_json,
            },
            "logs": ["Mountpoint with ID %s registered" % device_id],
        }

    else:
        return {
            "status": "FAILED",
            "output": {
                "url": id_url,
                "request_body": mount_body,
                "response_code": response_code,
                "response_body": response_json,
            },
            "logs": ["Unable to register device with ID %s" % device_id],
        }


def execute_unmount_netconf(task):
    device_id = task["inputData"]["device_id"]

    id_url = Template(uniconfig_url_netconf_unmount_sync).substitute(
        {"base_url": get_uniconfig_cluster_from_task(task)}
    )
    unmount_body = {"input": {"node-id": device_id, "connection-type": "netconf"}}

    r = requests.post(id_url, data=json.dumps(unmount_body), **additional_uniconfig_request_params)
    response_code, response_json = parse_response(r)

    return {
        "status": "COMPLETED",
        "output": {"url": id_url, "response_code": response_code, "response_body": response_json},
        "logs": ["Mountpoint with ID %s removed" % device_id],
    }


def execute_check_connected_netconf(task):
    device_id = task["inputData"]["device_id"]
    uniconfig_cookies = extract_uniconfig_cookies(task)

    id_url = Template(uniconfig_url_netconf_mount_oper).substitute(
        {"id": device_id, "base_url": get_uniconfig_cluster_from_task(task)}
    )

    r = requests.get(id_url, cookies=uniconfig_cookies, **additional_uniconfig_request_params)
    response_code, response_json = parse_response(r)

    if (
        response_code == requests.codes.ok
        and response_json["node"][0]["netconf-node-topology:connection-status"] == "connected"
    ):
        return {
            "status": "COMPLETED",
            "output": {
                "url": id_url,
                "response_code": response_code,
                "response_body": response_json,
            },
            "logs": ["Mountpoint with ID %s is connected" % device_id],
        }
    else:
        return {
            "status": "FAILED",
            "output": {
                "url": id_url,
                "response_code": response_code,
                "response_body": response_json,
            },
            "logs": ["Mountpoint with ID %s not yet connected" % device_id],
        }


def read_structured_data(task):
    device_id = task["inputData"]["device_id"]
    uri = task["inputData"]["uri"]

    uniconfig_cookies = extract_uniconfig_cookies(task)

    id_url = (
        Template(uniconfig_url_netconf_mount).substitute(
            {"id": device_id, "base_url": get_uniconfig_cluster_from_task(task)}
        )
        + "/yang-ext:mount"
        + (uri if uri else "")
    )

    r = requests.get(id_url, cookies=uniconfig_cookies, **additional_uniconfig_request_params)
    response_code, response_json = parse_response(r)

    if response_code == requests.codes.ok:
        return {
            "status": "COMPLETED",
            "output": {
                "url": id_url,
                "response_code": response_code,
                "response_body": response_json,
            },
            "logs": ["Node with ID %s read successfully" % device_id],
        }
    else:
        return {
            "status": "FAILED",
            "output": {
                "url": id_url,
                "response_code": response_code,
                "response_body": response_json,
            },
            "logs": ["Unable to read device with ID %s" % device_id],
        }


def start(cc):
    local_logs.info("Starting Netconf workers")

    cc.register(
        "Netconf_mount_netconf",
        {
            "description": '{"description": "mount a Netconf device", "labels": ["BASICS","NETCONF"]}',
            "timeoutSeconds": 600,
            "responseTimeoutSeconds": 600,
            "inputKeys": [
                "device_id",
                "host",
                "port",
                "keepalive-delay",
                "tcp-only",
                "username",
                "password",
                "uniconfig-native",
                "blacklist",
                "dry-run-journal-size",
                "reconcile",
                "sleep-factor",
                "between-attempts-timeout-millis",
                "connection-timeout-millis",
            ],
            "outputKeys": ["url", "request_body", "response_code", "response_body"],
        },
        execute_mount_netconf,
    )

    cc.register(
        "Netconf_unmount_netconf",
        {
            "description": '{"description": "unmount a CLI device", "labels": ["BASICS","NETCONF"]}',
            "inputKeys": ["device_id"],
            "outputKeys": ["url", "response_code", "response_body"],
        },
        execute_unmount_netconf,
    )

    cc.register(
        "Netconf_read_structured_device_data",
        {
            "description": '{"description": "Read device configuration or operational data in structured format e.g. netconf", "labels": ["BASICS","NETCONF"]}',
            "inputKeys": ["device_id", "uri", "uniconfig_context"],
            "outputKeys": ["url", "response_code", "response_body"],
        },
        read_structured_data,
    )

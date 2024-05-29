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

uniconfig_url_cli_mount_sync = "$base_url/operations/connection-manager:install-node"
uniconfig_url_cli_unmount_sync = "$base_url/operations/connection-manager:uninstall-node"
uniconfig_url_cli_mount_rpc = (
    "$base_url/operations/network-topology:network-topology/topology=cli/node=$id"
)
uniconfig_url_cli_read_journal = "$base_url/operations/network-topology:network-topology/topology=cli/node=$id/yang-ext:mount/journal:read-journal?content=nonconfig"

sync_mount_template = {
    "input": {
        "node-id": "",
        "cli": {
            "cli-topology:host": "",
            "cli-topology:port": "",
            "cli-topology:transport-type": "ssh",
            "cli-topology:device-type": "",
            "cli-topology:device-version": "",
            "cli-topology:username": "",
            "cli-topology:password": "",
            "cli-topology:journal-size": 500,
            "cli-topology:dry-run-journal-size": 180,
        },
    }
}


def execute_mount_cli(task):
    """
    Build a template for CLI mounting body (mount_body) from input device
    parameters and issue a PUT request to Uniconfig to mount it. These requests
    can also be viewed and tested in postman collections for each device.

    Args:
        task: A dict with a complete device data (mandatory) and optional
    Returns:
        response: dict, e.g. {"status": "COMPLETED", "output": {"url": id_url,
                                                  "request_body": mount_body,
                                                  "response_code": 200,
                                                  "response_body": response_json},
                }}
    """
    device_id = task["inputData"]["device_id"]
    mount_body = copy.deepcopy(sync_mount_template)

    mount_body["input"]["node-id"] = task["inputData"]["device_id"]
    mount_body["input"]["cli"]["cli-topology:host"] = task["inputData"]["host"]
    mount_body["input"]["cli"]["cli-topology:port"] = task["inputData"]["port"]
    mount_body["input"]["cli"]["cli-topology:transport-type"] = task["inputData"]["protocol"]
    mount_body["input"]["cli"]["cli-topology:device-type"] = task["inputData"]["type"]
    mount_body["input"]["cli"]["cli-topology:device-version"] = task["inputData"]["version"]
    mount_body["input"]["cli"]["cli-topology:username"] = task["inputData"]["username"]
    mount_body["input"]["cli"]["cli-topology:password"] = task["inputData"]["password"]
    mount_body["input"]["cli"]["cli-topology:parsing-engine"] = task["inputData"].get(
        "parsing-engine", "tree-parser"
    )
    mount_body["input"]["cli"]["uniconfig-config:install-uniconfig-node-enabled"] = task[
        "inputData"
    ].get("install-uniconfig-node-enabled", True)

    id_url = Template(uniconfig_url_cli_mount_sync).substitute(
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


def execute_and_read_rpc_cli(task):
    device_id = task["inputData"]["device_id"]
    template = task["inputData"]["template"]
    params = task["inputData"]["params"] if task["inputData"]["params"] else {}
    params = params if isinstance(params, dict) else eval(params)
    uniconfig_cookies = extract_uniconfig_cookies(task)
    output_timer = task["inputData"].get("output_timer")

    commands = Template(template).substitute(params)
    execute_and_read_template = {"input": {"ios-cli:command": ""}}
    exec_body = copy.deepcopy(execute_and_read_template)

    exec_body["input"]["ios-cli:command"] = commands
    if output_timer:
        exec_body["input"]["wait-for-output-timer"] = output_timer

    id_url = (
        Template(uniconfig_url_cli_mount_rpc).substitute(
            {"id": device_id, "base_url": get_uniconfig_cluster_from_task(task)}
        )
        + "/yang-ext:mount/cli-unit-generic:execute-and-read"
    )

    r = requests.post(
        id_url,
        data=json.dumps(exec_body),
        cookies=uniconfig_cookies,
        **additional_uniconfig_request_params,
    )

    response_code, response_json = parse_response(r)

    if response_code == requests.codes.ok:
        return {
            "status": "COMPLETED",
            "output": {
                "url": id_url,
                "request_body": exec_body,
                "response_code": response_code,
                "response_body": response_json,
            },
            "logs": ["Mountpoint with ID %s configured" % device_id],
        }
    else:
        return {
            "status": "FAILED",
            "output": {
                "url": id_url,
                "request_body": exec_body,
                "response_code": response_code,
                "response_body": response_json,
            },
            "logs": ["Unable to configure device with ID %s" % device_id],
        }


def execute_unmount_cli(task):
    device_id = task["inputData"]["device_id"]

    id_url = Template(uniconfig_url_cli_unmount_sync).substitute(
        {"base_url": get_uniconfig_cluster_from_task(task)}
    )

    unmount_body = {"input": {"node-id": device_id, "connection-type": "cli"}}
    r = requests.post(id_url, data=json.dumps(unmount_body), **additional_uniconfig_request_params)
    response_code, response_json = parse_response(r)

    return {
        "status": "COMPLETED",
        "output": {"url": id_url, "response_code": response_code, "response_body": response_json},
        "logs": ["Mountpoint with ID %s removed" % device_id],
    }


def execute_get_cli_journal(task):
    device_id = task["inputData"]["device_id"]
    uniconfig_cookies = extract_uniconfig_cookies(task)

    id_url = Template(uniconfig_url_cli_read_journal).substitute(
        {"id": device_id, "base_url": get_uniconfig_cluster_from_task(task)}
    )

    r = requests.post(id_url, cookies=uniconfig_cookies, **additional_uniconfig_request_params)
    response_code, response_json = parse_response(r)

    if response_code == requests.codes.ok:
        return {
            "status": "COMPLETED",
            "output": {
                "url": id_url,
                "response_code": response_code,
                "response_body": response_json,
            },
            "logs": [],
        }
    else:
        return {
            "status": "FAILED",
            "output": {
                "url": id_url,
                "response_code": response_code,
                "response_body": response_json,
            },
            "logs": ["Mountpoint with ID %s, cannot read journal" % device_id],
        }


execute_template = {"input": {"command": "", "wait-for-output-timer": "5"}}


def execute_cli(task):
    device_id = task["inputData"]["device_id"]
    template = task["inputData"]["template"]
    params = task["inputData"]["params"] if task["inputData"]["params"] else {}
    params = params if isinstance(params, dict) else eval(params)

    uniconfig_cookies = extract_uniconfig_cookies(task)

    commands = Template(template).substitute(params)
    exec_body = copy.deepcopy(execute_template)

    exec_body["input"]["command"] = commands

    id_url = (
        Template(uniconfig_url_cli_mount_rpc).substitute(
            {"id": device_id, "base_url": get_uniconfig_cluster_from_task(task)}
        )
        + "/yang-ext:mount/cli-unit-generic:execute"
    )

    r = requests.post(
        id_url,
        data=json.dumps(exec_body),
        cookies=uniconfig_cookies,
        **additional_uniconfig_request_params,
    )
    response_code, response_json = parse_response(r)

    if response_code == requests.codes.ok:
        return {
            "status": "COMPLETED",
            "output": {
                "url": id_url,
                "request_body": exec_body,
                "response_code": response_code,
                "response_body": response_json,
            },
            "logs": ["Mountpoint with ID %s configured" % device_id],
        }
    else:
        return {
            "status": "FAILED",
            "output": {
                "url": id_url,
                "request_body": exec_body,
                "response_code": response_code,
                "response_body": response_json,
            },
            "logs": ["Unable to configure device with ID %s" % device_id],
        }


def execute_and_expect_cli(task):
    device_id = task["inputData"]["device_id"]
    template = task["inputData"]["template"]
    params = task["inputData"]["params"] if task["inputData"]["params"] else {}
    params = params if isinstance(params, dict) else eval(params)

    uniconfig_cookies = extract_uniconfig_cookies(task)

    commands = Template(template).substitute(params)
    exec_body = copy.deepcopy(execute_template)

    exec_body["input"]["command"] = commands

    id_url = (
        Template(uniconfig_url_cli_mount_rpc).substitute(
            {"id": device_id, "base_url": get_uniconfig_cluster_from_task(task)}
        )
        + "/yang-ext:mount/cli-unit-generic:execute-and-expect"
    )

    r = requests.post(
        id_url,
        data=json.dumps(exec_body),
        cookies=uniconfig_cookies,
        **additional_uniconfig_request_params,
    )
    response_code, response_json = parse_response(r)

    if response_code == requests.codes.ok:
        return {
            "status": "COMPLETED",
            "output": {
                "url": id_url,
                "request_body": exec_body,
                "response_code": response_code,
                "response_body": response_json,
            },
            "logs": ["Mountpoint with ID %s configured" % device_id],
        }
    else:
        return {
            "status": "FAILED",
            "output": {
                "url": id_url,
                "request_body": exec_body,
                "response_code": response_code,
                "response_body": response_json,
            },
            "logs": ["Unable to configure device with ID %s" % device_id],
        }


def start(cc):
    local_logs.info("Starting CLI workers")

    cc.register(
        "CLI_mount_cli",
        {
            "description": '{"description": "mount a CLI device", "labels": ["BASICS","CLI"]}',
            "timeoutSeconds": 600,
            "responseTimeoutSeconds": 600,
            "inputKeys": [
                "device_id",
                "type",
                "version",
                "host",
                "protocol",
                "port",
                "username",
                "password",
            ],
            "outputKeys": ["url", "request_body", "response_code", "response_body"],
        },
        execute_mount_cli,
    )

    cc.register(
        "CLI_unmount_cli",
        {
            "description": '{"description": "unmount a CLI device", "labels": ["BASICS","CLI"]}',
            "timeoutSeconds": 600,
            "responseTimeoutSeconds": 600,
            "inputKeys": ["device_id"],
            "outputKeys": ["url", "response_code", "response_body"],
        },
        execute_unmount_cli,
    )

    cc.register(
        "CLI_execute_and_read_rpc_cli",
        {
            "description": '{"description": "execute commands for a CLI device", "labels": ["BASICS","CLI"]}',
            "inputKeys": ["device_id", "template", "params", "uniconfig_context", "output_timer"],
            "outputKeys": ["url", "request_body", "response_code", "response_body"],
        },
        execute_and_read_rpc_cli,
    )

    cc.register(
        "CLI_get_cli_journal",
        {
            "description": '{"description": "Read cli journal for a device", "labels": ["BASICS","CLI"]}',
            "responseTimeoutSeconds": 10,
            "inputKeys": ["device_id", "uniconfig_context"],
            "outputKeys": ["url", "response_code", "response_body"],
        },
        execute_get_cli_journal,
    )

    cc.register(
        "CLI_execute_cli",
        {
            "description": '{"description": "execute commands for a CLI device", "labels": ["BASICS","CLI"]}',
            "timeoutSeconds": 60,
            "responseTimeoutSeconds": 60,
            "inputKeys": ["device_id", "template", "params", "uniconfig_context"],
            "outputKeys": ["url", "request_body", "response_code", "response_body"],
        },
        execute_cli,
    )

    cc.register(
        "CLI_execute_and_expect_cli",
        {
            "description": '{"description": "execute commands for a CLI device", "labels": ["BASICS","CLI"]}',
            "responseTimeoutSeconds": 30,
            "inputKeys": ["device_id", "template", "params", "uniconfig_context"],
            "outputKeys": ["url", "request_body", "response_code", "response_body"],
        },
        execute_and_expect_cli,
    )

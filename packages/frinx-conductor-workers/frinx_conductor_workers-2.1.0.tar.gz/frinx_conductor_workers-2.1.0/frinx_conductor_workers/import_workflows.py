import json
import logging
import os
from pathlib import Path

import requests
from frinx_conductor_workers.frinx_rest import conductor_headers
from frinx_conductor_workers.frinx_rest import conductor_url_base

local_logs = logging.getLogger(__name__)

workflow_import_url = conductor_url_base + "/metadata/workflow"

DIR_PATH = Path(os.path.dirname(os.path.realpath(__file__))).parent
FRINX_CONDUCTOR_WORKFLOWS: Path = Path(f"{DIR_PATH}/frinx_conductor_workflows")


def import_base_workflows():
    import_workflows(FRINX_CONDUCTOR_WORKFLOWS)


def import_workflows(path):
    if os.path.isdir(path):
        local_logs.info("Importing workflows from folder %s", path)
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.endswith(".json"):
                    try:
                        local_logs.info("Importing workflow %s", entry.name)
                        with open(entry, "r") as payload_file:
                            # api expects array in payload
                            payload = []
                            payload_json = json.load(payload_file)
                            payload.append(payload_json)
                            r = requests.put(
                                workflow_import_url,
                                data=json.dumps(payload),
                                headers=conductor_headers,
                            )
                            local_logs.info("Response status code - %s", r.status_code)
                            if r.status_code != requests.codes.ok:
                                local_logs.warning(
                                    "Import of workflow %s failed. "
                                    "Ignoring the workflow. Response content: %s",
                                    entry.name,
                                    r.content,
                                )
                    except Exception as err:
                        local_logs.error("Error while registering workflow %s", entry.name, err)
                        raise err
                elif entry.is_dir():
                    import_workflows(entry.path)
                else:
                    local_logs.warning("Ignoring, unknown type %s", entry)
    else:
        local_logs.error("Path to workflows %s is not a directory.", path)

# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022-2025 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Helper functions for artifact management"""

import json

import phantom.rules as phantom


__version__ = "1.1.1"

STANDARD_CEF_MAPPING = {
    "action": ["act"],
    "process_name": ["deviceProcessName", "dproc", "sproc"],
    "device_id": ["deviceExternalId"],
    "device_username": ["suser", "duser"],
    "device_external_ip": ["src"],
    "process_sha256": ["fileHashSha256"],
    "name": ["msg"],
    "alertId": ["id"],
}

CEF_TYPES_MAPPING = {
    "_raw": ["cbc alert"],
    "alertId": ["cbc alert id"],
    "id": ["cbc alert id"],
    "device_id": ["cbc device id"],
    "deviceExternalId": ["cbc device id"],
    "fileHashSha256": ["cbc process hash"],
    "process_sha256": ["cbc process hash"],
    "sha256": ["cbc process hash"],
    "process_guid": ["cbc process guid"],
    "process_pid": ["pid"],
    "process_name": ["process name"],
    "process_path": ["process name"],
}


def prepare_artifact(alert, config, container_id=None):
    """Prepare artifact from CBC alert"""
    artifact = dict()

    # Standard artifact fields
    if container_id:
        artifact["container_id"] = container_id
    artifact["label"] = config["ingest"]["container_label"]
    severity = alert.get("severity", 1)
    if severity < 4:
        artifact["severity"] = "low"
    elif severity < 7:
        artifact["severity"] = "medium"
    else:
        artifact["severity"] = "high"

    if "process_name" in alert.keys():
        process_name = ",{}".format(alert["process_name"])
    else:
        process_name = ""
    artifact["name"] = "CBC {} - {}{}".format(alert.get("type", ""), alert.get("device_name"), process_name)
    if "reason" in alert.keys():
        reason = alert["reason"]
    else:
        reason = ""
    artifact["description"] = f"{reason} Artifact added by CBC"
    if "type" in alert.keys():
        artifact["type"] = alert["type"]
    if "backend_timestamp" in alert.keys():
        artifact["start_time"] = alert["backend_timestamp"]
    if "backend_update_timestamp" in alert.keys():
        artifact["end_time"] = alert["backend_update_timestamp"]

    if "id" in alert.keys():
        artifact["source_data_identifier"] = alert["id"]
    elif "event_id" in alert.keys():
        artifact["source_data_identifier"] = alert["event_id"]
    else:
        artifact["source_data_identifier"] = "None"

    # Standard CEF fields - https://docs.microsoft.com/en-us/azure/sentinel/cef-name-mapping
    artifact["cef"] = dict()
    for key in STANDARD_CEF_MAPPING.keys():
        if key in alert.keys():
            for dest in STANDARD_CEF_MAPPING[key]:
                artifact["cef"][dest] = alert[key]

    # Custom fields - if really needed
    if "id" in alert.keys():
        artifact["cef"]["alertId"] = alert["id"]

    # _raw contents also available to conform to what Splunk App ingests from SIEM
    artifact["cef"]["_raw"] = json.dumps(alert)

    # Also put the alert fields inside the artifact
    for key in alert.keys():
        artifact["cef"][key] = alert[key]

    # CEF Data type mappings for "contains"
    artifact["cef_types"] = dict()
    for key in CEF_TYPES_MAPPING.keys():
        artifact["cef_types"][key] = CEF_TYPES_MAPPING[key]

    return artifact


def delete_artifact(artifact_id):
    """Delete an artifact"""
    return phantom.delete_artifact(artifact_id=artifact_id)

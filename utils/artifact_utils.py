# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
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
from cbcapp_consts import STANDARD_CEF_MAPPING, CEF_TYPES_MAPPING


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
    artifact["name"] = "CBC {} - {}{}".format(alert.get("type", ""),
                                              alert.get("device_name"),
                                              process_name)
    if "reason" in alert.keys():
        reason = alert["reason"]
    else:
        reason = ""
    artifact["description"] = "{} Artifact added by CBC".format(reason)
    if "type" in alert.keys():
        artifact["type"] = alert["type"]
    if "create_time" in alert.keys():
        artifact["start_time"] = alert["create_time"]
    if "last_update_time" in alert.keys():
        artifact["end_time"] = alert["last_update_time"]

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

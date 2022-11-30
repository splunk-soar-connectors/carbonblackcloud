# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Normalize artifact action"""
import json
import traceback

from actions import BaseAction
from utils.artifact_utils import prepare_artifact, delete_artifact
import phantom.app as phantom


class NormalizeArtifactAction(BaseAction):
    """Class to handle Normalize action."""

    def call(self):
        """Execute Normalize action."""
        result = self._normalize()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _normalize(self):
        result = {"success": True, "details": ""}
        container_id = self.connector.get_container_id()
        config = self.connector.get_config()

        status, container, _ = self.connector.get_container_info(container_id)
        if status != phantom.APP_SUCCESS:
            result["success"] = False
            result["details"] = "Could not find container id:{}".format(container_id)
            return result

        # Check for input parameters
        if "artifact_id" not in self.param.keys() or "raw" not in self.param.keys():
            result["success"] = False
            result["details"] = "artifact_id or raw parameters not supplied"
            return result

        # Check if the container is of ingested data from Splunk SIEM

        if container["artifact_count"] != 1 \
           or container["description"] != "Container added by Splunk" \
           or "Splunk Log Entry" not in container["name"] \
           or container["status"] != "new":
            result["success"] = True

            result["details"] = "Container does not contain Splunk SIEM ingested data"
            return result

        artifact_id = self.param["artifact_id"]
        _raw = self.param["raw"]

        # Recreate the artifact based on the _raw attribute
        try:
            raw = json.loads(_raw)
        except:
            result["success"] = False
            exc = traceback.format_exc()
            result["details"] = "Invalid JSON data in raw parameter: {}".format(exc)
            return result

        artifact = prepare_artifact(raw, config, container_id=container_id)
        if not delete_artifact(artifact_id):
            result["success"] = False
            result["details"] = "Could not delete original artifact, data duplication possible " + str(artifact_id)

        success, _, result_artifact = self.connector.save_artifact(artifact)
        if success == phantom.APP_SUCCESS:
            result["success"] = True
            return result
        else:
            result["success"] = False
            result["details"] = "Could not save new artifact"
            return result

        result["success"] = True
        result["details"] = "Container: {}: artifact normalized".format(container_id)
        return result

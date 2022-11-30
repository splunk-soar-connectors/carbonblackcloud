# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Get Process Metadata Class Action"""
import traceback

from cbc_sdk.platform import Process

from actions import BaseAction
import phantom.app as phantom


class GetProcessMetadataAction(BaseAction):
    """Class to handle process metadata action."""
    def call(self):
        """Execute process metadata action."""
        result = self._get_process_meta_data()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _get_process_meta_data(self):
        process_guid = self.param.get("process_guid", "")
        self.connector.debug_print(f"Get Process Metadata action with parameters {self.param}")
        result = {"success": False, "details": ""}

        # generic checks
        checks = super().call()
        if checks is not None:
            return checks

        if process_guid:
            try:
                process = self.cbc.select(Process, process_guid)
                if len(process._info) <= 1:
                    result["details"] = f"Could not find {process_guid}."
                    return result
                process_details = process.get_details()
                process_info = {
                    "process_name": process_details.get("process_name"),
                    "process_sha256": process_details.get("process_sha256"),
                    "process_pid": ",".join(map(str, process_details.get("process_pid", []))),
                    "process_cmdline": process_details.get("process_cmdline"),
                    "parent_pid": process_details.get("parent_pid", ""),
                    "alert_id": ",".join(process_details.get("alert_id", [])),
                    "alert_category": ",".join(process_details.get("alert_category", [])),
                    "backend_timestamp": process_details.get("backend_timestamp"),
                    "device_id": process_details.get("device_id"),
                    "device_name": process_details.get("device_name"),
                    "device_os": process_details.get("device_os"),
                    "device_policy": process_details.get("device_policy")
                }
                self.action_result.add_data({
                    "raw_details": process_details,
                    "details": process_info
                })
                result["success"], result["details"] = True, "Successfully retrieved metadata for "\
                                                             f"{process_guid}."
            except Exception as e:
                result["details"] = f"Could not get process metadata for {process_guid} - {e}."
                self.connector.error_print(traceback.format_exc())
        else:
            result["details"] = "Missing process guid."
            self.connector.error_print(result["details"])
        return result

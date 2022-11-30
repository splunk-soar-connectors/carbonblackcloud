# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Delete File Action Class"""
import traceback
from cbc_sdk.platform import Device
from cbc_sdk.live_response_api import LiveResponseError
from actions import BaseAction
import phantom.app as phantom


class DeleteFileAction(BaseAction):
    """Class to handle delete file live response action."""

    def call(self):
        """Execute delete file action."""
        result = self._delete_file()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _delete_file(self):
        """Delete File Live Response action."""
        device_id = self.param.get("device_id", "")
        if "file_name" not in self.param.keys():
            return {"success": False, "details": "No file_name provided."}

        filename = self.param["file_name"]
        self.connector.debug_print(
            f"Delete File Live Response action with parameters {self.param}"
        )
        result = {
            "success": False,
            "details": f"Could not delete file for {device_id}.",
        }

        # generic checks
        checks = super().call()
        if checks is not None:
            return checks

        if device_id:
            try:
                device = self.cbc.select(Device, device_id)
                try:
                    lr_session = device.lr_session()
                except Exception as e:
                    self.connector.error_print(traceback.format_exc())
                    result["success"] = False
                    result["details"] = "Could not establish LR session - {}".format(e)
                    return result
                try:
                    lr_session.delete_file(filename)
                except LiveResponseError as ex:
                    result["success"] = False
                    if (
                        "ERROR_PATH_NOT_FOUND" in ex.message
                        or "ERROR_FILE_NOT_FOUND" in ex.message
                    ):
                        result["details"] = "No such file {}.".format(filename)
                    else:
                        self.connector.error_print(traceback.format_exc())
                        result["details"] = "Could not delete file contents - {}".format(ex)
                    return result
                except Exception as e:
                    self.connector.error_print(traceback.format_exc())
                    result["success"] = False
                    result["details"] = "Could not delete file contents - {}.".format(e)
                    return result
                result_data = {"device_id": device_id, "file_name": filename}
                self.action_result.add_data(result_data)
                result["success"], result["details"] = True, "File successfully deleted."
            except Exception as e:
                self.connector.error_print(traceback.format_exc())
                result["details"] = "Could not delete file - {}".format(e)
        else:
            result["details"] = "Missing device id."
        return result

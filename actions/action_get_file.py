# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Get File Action Class"""
import traceback
from cbc_sdk.platform import Device

from actions import BaseAction
from phantom.vault import Vault
import phantom.app as phantom


class GetFileAction(BaseAction):
    """Class to handle get file live response action."""
    def call(self):
        """Execute get file action."""
        result = self._get_file()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _get_file(self):
        """Get File Live Response action."""
        device_id = self.param.get("device_id", "")
        if "file_name" not in self.param.keys():
            return {"success": False, "details": "No file_name provided"}

        filename = self.param["file_name"]
        self.connector.debug_print(f"Get File Live Response action with parameters {self.param}")
        result = {"success": False, "details": f"Could not get file for {device_id}."}

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
                    file_contents = lr_session.get_file(filename)
                except Exception as e:
                    self.connector.error_print(traceback.format_exc())
                    result["success"] = False
                    result["details"] = "Could not get file contents - {}".format(e)
                    return result
                status = Vault.create_attachment(file_contents,
                                                 self.connector.get_container_id(),
                                                 file_name=filename)
                if not status.get("succeeded", False):
                    result["success"] = False
                    result["details"] = "Could not create vault"
                    return result

                result_data = {"device_id": device_id,
                               "vault_id": status.get("vault_id", None),
                               "file_name": filename}
                self.action_result.add_data(result_data)
                result["success"], result["details"] = True, "File successfully retrieved"
            except Exception as e:
                self.connector.error_print(traceback.format_exc())
                result["details"] = "Could not get file - {}".format(e)
        else:
            result["details"] = "Missing device id."
        return result

# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""List Processes Class Action"""
import traceback

from cbc_sdk.platform import Device

from actions import BaseAction
import phantom.app as phantom


class ListProcessesAction(BaseAction):
    """Class to handle list processes live response action."""
    def call(self):
        """Execute list processes action."""
        result = self._list_processes()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _list_processes(self):
        """List Processes Live Response action."""
        device_id = self.param.get("device_id", "")
        self.connector.debug_print(f"List Processes Live Response action with parameters {self.param}")
        result = {"success": False, "details": f"Could not get processes for {device_id}."}

        # generic checks
        checks = super().call()
        if checks is not None:
            return checks

        if device_id:
            try:
                device = self.cbc.select(Device, device_id)
                lr_session = device.lr_session()
                processes = lr_session.list_processes()

                for process in processes:
                    self.action_result.add_data(process)
                result["success"], result["details"] = True, "List Processes successfully retrieved."
            except Exception as e:
                self.connector.error_print(traceback.format_exc())
                result["details"] = f"Could not get processes for {device_id} - {e}."
        else:
            result["details"] = "Missing device id."
        return result

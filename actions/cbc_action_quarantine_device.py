# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022-2025 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Quarantine Device Class Action"""

import traceback

import phantom.app as phantom
from cbc_sdk.platform import Device

from actions import BaseAction


class QuarantineAction(BaseAction):
    """Class to handle quarantine device action."""

    def call(self):
        """Execute quarantine device action."""
        result = self._quarantine_device()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _quarantine_device(self):
        """Quarantine device action."""
        device_id = self.param.get("device_id", "")
        self.connector.debug_print(f"Quarantine device action with parameters {self.param}")
        result = {"success": False, "details": f"Could not quarantine the device {device_id}."}

        # generic checks
        checks = super().call()
        if checks is not None:
            return checks

        if device_id:
            try:
                device = self.cbc.select(Device, device_id)
                if device.quarantined:
                    result["success"], result["details"] = True, "The device is already quarantined."
                    self.connector.debug_print(result["details"])
                else:
                    device.quarantine(True)
                    result["success"], result["details"] = True, "Device quarantined successfully."
            except Exception as e:
                self.connector.error_print(traceback.format_exc())
                result["details"] = f"Could not quarantine {device_id} - {e}."
        else:
            result["details"] = "Missing device id."
        return result

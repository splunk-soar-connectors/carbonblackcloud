# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2023-2025 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Get Asset Info Action Class"""

import traceback

import phantom.app as phantom
from cbc_sdk.platform import Device

from actions import BaseAction


class GetAssetInfoAction(BaseAction):
    """Class to handle get asset info action."""

    def call(self):
        """Execute get asset info action."""
        result = self._get_asset_info()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _get_asset_info(self):
        """Get Asset Info action."""
        result = {"success": False, "details": ""}
        device_id = self.param.get("device_id", None)
        if not device_id:
            return {"success": False, "details": "No device_id provided"}

        # generic checks
        checks = super().call()
        if checks is not None:
            return checks

        try:
            device = self.cbc.select(Device, device_id)
            self.action_result.add_data(device._info)
            result["success"], result["details"] = True, "Get asset info successfully retrieved."
        except Exception as e:
            result["details"] = f"Could not retrieve asset info for device {device_id} - {e}."
            self.connector.error_print(traceback.format_exc())

        return result

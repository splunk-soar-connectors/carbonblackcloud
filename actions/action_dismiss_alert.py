# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Dismiss Alert Class Action"""
from actions import BaseAction
from cbc_sdk.platform import BaseAlert
import phantom.app as phantom
import traceback


class DismissAlertAction(BaseAction):
    """Class to handle dismiss alert action."""
    def call(self):
        """Execute dismiss alert action."""
        result = self._dismiss_alert()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _dismiss_alert(self):
        """Dismiss alert action"""
        alert_id = self.param.get("alert_id", "")
        self.connector.debug_print(f"Dismiss alert action with parameters {self.param}")
        result = {"success": False, "details": f"Could not dismiss alert {alert_id}."}

        # generic checks
        checks = super().call()
        if checks is not None:
            return checks

        try:
            if alert_id:
                alert = self.cbc.select(BaseAlert, alert_id)
                alert.dismiss("Fixed", "Dismissed via Splunk app.")
                result["success"], result["details"] = True, f"Alert dismissed {alert_id}."
            else:
                result["details"] = "Missing alert id."
                self.connector.error_print(result["details"])
        except Exception as e:
            self.connector.error_print(traceback.format_exc())
            result["details"] = f"Could not dismiss alert {alert_id} - {e}."
        return result

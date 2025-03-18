# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2023-2025 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Dismiss All Future Alerts Class Action"""

import traceback

import phantom.app as phantom
from cbc_sdk.platform import Alert

from actions import BaseAction


class DismissFutureAlertsAction(BaseAction):
    """Class to handle dismiss all future alerts action."""

    def call(self):
        """Execute dismiss all future alerts action."""
        result = self._dismiss_future_alerts()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _dismiss_future_alerts(self):
        """Dismiss all future alerts action"""
        alert_id = self.param.get("alert_id", "")
        remediation_status = self.param.get("remediation_status", None)
        comment = self.param.get("comment", None)
        self.connector.debug_print(f"Dismiss all future alerts action with parameters {self.param}")
        result = {"success": False, "details": "Could not dismiss all future alerts."}

        # generic checks
        checks = super().call()
        if checks is not None:
            return checks

        try:
            if alert_id:
                alert = self.cbc.select(Alert, alert_id)
                alert.dismiss_threat(remediation=remediation_status, comment=comment)
                result["success"], result["details"] = (
                    True,
                    f"All future alerts that are associated with the threat_id {alert.threat_id} will be dismissed.",
                )
            else:
                result["details"] = "Missing alert id."
                self.connector.error_print(result["details"])
        except Exception as e:
            result["details"] = f"Could not dismiss all future alerts - {e}"
            self.connector.error_print(traceback.format_exc())

        return result

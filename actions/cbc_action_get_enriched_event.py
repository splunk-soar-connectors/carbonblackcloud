# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Get Enriched Events By Alert Class Action"""
import traceback

import phantom.app as phantom
from cbc_sdk.errors import FunctionalityDecommissioned, ObjectNotFoundError
from cbc_sdk.platform import CBAnalyticsAlert

from actions import BaseAction


class GetEnrichedEventAction(BaseAction):
    """Class to handle get enriched events by alert action."""
    def call(self):
        """Execute get enriched events by alert action."""
        result = self._get_events()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _get_events(self):
        """Get Enriched Event action - available only for CBAnalyticsAlert"""
        alert_id = self.param.get("alert_id", "")
        self.connector.debug_print(f"Get Enriched Events action with parameters {self.param}")
        result = {"success": False, "details": ""}

        # generic checks
        checks = super().call()
        if checks is not None:
            return checks

        try:
            if alert_id:
                alert = self.cbc.select(CBAnalyticsAlert, alert_id)
                _ = alert.get_events()
            else:
                result["details"] = "Missing alert id."
                self.connector.error_print(result["details"])
        except ObjectNotFoundError:
            result["details"] = f"No such alert {alert_id}."
        except FunctionalityDecommissioned as e:
            result["details"] = f"{e}"
        except Exception as e:
            self.connector.error_print(traceback.format_exc())
            result["details"] = f"Could not get enriched events by alert {alert_id}: {e}."
        return result

# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022-2025 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Get Observations By Alert Class Action"""

import traceback

import phantom.app as phantom
from cbc_sdk.errors import ObjectNotFoundError
from cbc_sdk.platform import Alert

from actions import BaseAction


class GetObservationsAction(BaseAction):
    """Class to handle get observations by alert action."""

    def call(self):
        """Execute get observations by alert action."""
        result = self._get_observations()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _get_observations(self):
        """Get Observations action - available only for CBAnalyticsAlert"""
        alert_id = self.param.get("alert_id", "")
        self.connector.debug_print(f"Get Observations action with parameters {self.param}")
        result = {"success": False, "details": ""}

        # generic checks
        checks = super().call()
        if checks is not None:
            return checks

        try:
            if alert_id:
                alert = self.cbc.select(Alert, alert_id)
                observations = alert.get_observations()
                if observations is None:
                    result["details"] = f"No observations returned for alert {alert_id}."
                    self.connector.error_print(result["details"])
                else:
                    for obs in observations:
                        obs_info = {
                            "observation_id": obs._info.get("observation_id"),
                            "observation_type": obs._info.get("observation_type"),
                            "alert_id": ",".join(obs._info.get("alert_id", [])),
                            "alert_category": ",".join(obs._info.get("alert_category", [])),
                            "backend_timestamp": obs._info.get("backend_timestamp"),
                            "device_id": obs._info.get("device_id"),
                            "device_name": obs._info.get("device_name"),
                            "device_os": obs._info.get("device_os"),
                            "device_policy": obs._info.get("device_policy"),
                            "process_name": obs._info.get("process_name"),
                            "process_hash": obs._info.get("process_hash", [""])[-1],
                            "parent_pid": obs._info.get("parent_pid", ""),
                            "process_pid": ",".join(map(str, obs._info.get("process_pid", []))),
                        }
                        self.action_result.add_data({"raw_details": obs._info, "details": obs_info})
                    result["success"] = True
                    result["details"] = f"Successfully retrieved {len(observations)} observations for {alert_id}."
            else:
                result["details"] = "Missing alert id."
                self.connector.error_print(result["details"])
        except ObjectNotFoundError:
            result["details"] = f"No such alert {alert_id}."
        except Exception as e:
            self.connector.error_print(traceback.format_exc())
            result["details"] = f"Could not get observations by alert {alert_id}: {e}."
        return result

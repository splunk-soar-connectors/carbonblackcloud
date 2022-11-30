# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Set Device Policy Class Action"""
from actions import BaseAction
from cbc_sdk.platform import Policy, Device
import phantom.app as phantom
import traceback


class SetDevicePolicyAction(BaseAction):
    """Class to handle set device policy action."""

    def call(self):
        """Execute set device policy action."""
        result = self._set_device_policy()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _set_device_policy(self):
        """Set Device Policy action"""
        device_id = self.param.get("device_id", "")
        self.connector.debug_print(
            f"Set Device Policy action with parameters {self.param}"
        )
        result = {"success": True, "details": "Successfully set device policy"}

        # generic checks
        checks = super().call()
        if checks is not None:
            return checks

        if device_id:
            policy = None
            policy_id = self.param.get("policy_id", None)
            policy_name = self.param.get("policy_name", None)
            if not policy_id and not policy_name:
                return {
                    "success": False,
                    "details": "You must provide policy_id or policy_name",
                }
            if policy_id:
                try:
                    policy = self.cbc.select(Policy, policy_id)
                    if policy_name and policy.name != policy_name:
                        result["details"] = "Policy ID and policy name mismatch, Set Device Policy " \
                                            "action with policy ID {}".format(policy_id)
                        self.connector.debug_print(result["details"])

                # Exception due to Policy select error
                except Exception as e:
                    self.connector.error_print(traceback.format_exc())
                    result["details"] = "Could not get device policy: {}".format(e)
                    result["success"] = False
                    return result
            else:
                try:
                    policy = self.cbc.select(Policy).add_names([policy_name])[0]
                # Exception due to Policy select error
                except IndexError:
                    self.connector.error_print(traceback.format_exc())
                    result["details"] = "Could not get device policy - no such policy {}".format(policy_name)
                    result["success"] = False
                    return result
                except Exception as e:
                    self.connector.error_print(traceback.format_exc())
                    result["details"] = "Could not get device policy - {}".format(e)
                    result["success"] = False
                    return result
            try:
                device = self.cbc.select(Device, device_id)
            # Exception due to Device select error
            except Exception as e:
                self.connector.error_print(traceback.format_exc())
                result["details"] = "Could not select device - {}".format(e)
                result["success"] = False
                return result
            try:
                device.update_policy(policy.id)
                self.action_result.add_data(
                    {
                        "policy_id": policy.id,
                        "device_id": device_id,
                        "policy_name": policy.name,
                    }
                )
            # Exception due to update policy error
            except Exception as e:
                self.connector.error_print(traceback.format_exc())
                result["details"] = "Could not set device policy - {}".format(e)
                result["success"] = False
        # No device ID provided
        else:
            result["details"] = "Missing device id."
            result["success"] = False
        return result

# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""List Policies Class Action"""
from actions import BaseAction
from cbc_sdk.platform import Policy
import phantom.app as phantom
import traceback


class ListPoliciesAction(BaseAction):
    """Class to handle list policies action."""
    def call(self):
        """Execute list policies action."""
        result = self._list_policies()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _list_policies(self):
        """List Policies action"""
        self.connector.debug_print(f"List policies action with parameters {self.param}")
        result = {"success": True, "details": "Successfully fetched policies list"}

        # generic checks
        checks = super().call()
        if checks is not None:
            return checks

        try:
            policies = self.cbc.select(Policy)
            for policy in policies:
                self.action_result.add_data(policy._info)
        except Exception as e:
            self.connector.error_print(traceback.format_exc())
            result["details"] = "Could not list policies - {}".format(e)
            result["success"] = False
        return result

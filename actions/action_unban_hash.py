# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Unban Hash Class Action"""
import traceback

from actions import BaseAction
import phantom.app as phantom
from cbc_sdk.platform import ReputationOverride


class UnbanHashAction(BaseAction):
    """Class to handle Unban hash action."""
    def call(self):
        """Execute unban hash action."""
        result = self._unban_hash()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _unban_hash(self):
        process_hash = self.param.get("process_hash", "")
        self.connector.debug_print(f"Unban Hash action with parameters {self.param}")
        result = {"success": False, "details": f"Could not unban {process_hash}."}

        # generic checks
        checks = super().call()
        if checks is not None:
            return checks

        try:
            if process_hash:
                overrides = self.cbc.select(ReputationOverride).where(process_hash) \
                    .set_override_list("BLACK_LIST") \
                    .set_override_type("SHA256")
                if len(overrides) == 0:
                    self.connector.error_print(f"There was no record for {process_hash}.")
                    result["success"], result["details"] = True, f"The process {process_hash} was not banned."
                elif len(overrides) > 1:
                    self.connector.error_print(f"There are multiple records for {process_hash}.")
                    result["details"] = f"There are multiple records for {process_hash}."
                else:
                    overrides[0].delete()
                    self.connector.debug_print(f"Successfully deleted the record for {process_hash}.")
                    result["success"], result["details"] = True, f"Hash {process_hash} was unbanned."
            else:
                result["details"] = "Missing process hash."
                self.connector.error_print(result["details"])
        except Exception as e:
            self.connector.error_print(traceback.format_exc())
            result["details"] = f"Could not unban {process_hash} - {e}."
        return result

# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Ban Hash Class Action"""
import traceback

from cbc_sdk.platform import ReputationOverride
from cbc_sdk.enterprise_edr import Binary

from actions import BaseAction
import phantom.app as phantom


class BanHashAction(BaseAction):
    """Class to handle ban hash action."""
    def call(self):
        """Execute ban hash action."""
        result = self._ban_hash()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _ban_hash(self):
        process_hash = self.param.get("process_hash", "")
        self.connector.debug_print(f"Ban Hash action with parameters {self.param}")
        result = {"success": False, "details": f"Could not ban {process_hash}."}

        # generic checks
        checks = super().call()
        if checks is not None:
            return checks

        if process_hash:
            try:
                binary = self.cbc.select(Binary, process_hash)
                filename = binary._info["original_filename"]
            except Exception:
                filename = "Actor name not defined"
                self.connector.error_print("No Binary record, using action name not defined")
            try:
                ReputationOverride.create(
                    self.cbc,
                    {
                        "sha256_hash": process_hash,
                        "override_type": "SHA256",
                        "override_list": "BLACK_LIST",
                        "filename": filename,
                        "description": "Banned via Splunk Soar Action",
                    },
                )
                result["success"], result["details"] = True, f"Hash {process_hash} was banned."
            except Exception as e:
                self.connector.error_print(traceback.format_exc())
                result["details"] = f"Could not ban {process_hash} - {e}."
        else:
            result["details"] = "Missing process hash."
            self.connector.error_print(result["details"])
        return result

# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Get Binary File Metadata Action Class"""
import traceback
from cbc_sdk.enterprise_edr.ubs import Binary
from cbc_sdk.errors import ObjectNotFoundError

from actions import BaseAction
import phantom.app as phantom
import copy


class GetBinaryMetadataAction(BaseAction):
    """Class to handle get binary file metadata from UBS action."""
    def call(self):
        """Execute get binary file metadata action."""
        result = self._get_binary_metadata()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _get_binary_metadata(self):
        """Get Binary File Metadata from UBS action."""
        result = {"success": False, "details": ""}
        file_hash = self.param.get("file_hash", None)
        if not file_hash:
            return {"success": False, "details": "No file_hash provided"}

        # generic checks
        checks = super().call()
        if checks is not None:
            return checks

        try:
            binary = self.cbc.select(Binary, file_hash)
            metadata = copy.deepcopy(binary._info)
            metadata["architecture"] = ",".join(metadata.get("architecture", []))
            self.action_result.add_data(metadata)
            result["success"], result["details"] = True, "Get UBS metadata successfully retrieved."
        except ObjectNotFoundError:
            self.connector.error_print(traceback.format_exc())
            result["details"] = "Could not find hash in UBS: {}.".format(file_hash)
        except Exception as e:
            result["details"] = f"Could not retrieve binary metadata for {file_hash} - {e}."
            self.connector.error_print(traceback.format_exc())

        return result

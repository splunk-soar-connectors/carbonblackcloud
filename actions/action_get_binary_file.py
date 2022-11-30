# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Get Binary File Action Class"""
import traceback
import urllib
from cbc_sdk.enterprise_edr.ubs import Binary

from actions import BaseAction
from phantom.vault import Vault
import phantom.app as phantom


class GetBinaryFileAction(BaseAction):
    """Class to handle get binary file from UBS action."""
    def call(self):
        """Execute get binary file action."""
        result = self._get_file()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _get_file(self):
        """Get Binary File UBS action."""
        result = {"success": False, "details": ""}
        if "file_hash" not in self.param.keys():
            return {"success": False, "details": "No file_hash provided"}

        file_hash = self.param["file_hash"]
        # generic checks
        checks = super().call()
        if checks is not None:
            return checks

        if self._is_sha256(file_hash):
            try:
                binary = Binary(self.cbc, file_hash)
                download_url = binary.download_url(expiration_seconds=60)
            except Exception as e:
                self.connector.error_print(traceback.format_exc())
                result["success"] = False
                result["details"] = "Could not find file in UBS: {}".format(e)
                return result
            try:
                file_contents = urllib.request.urlopen(download_url).read()
            except Exception as e:
                self.connector.error_print(traceback.format_exc())
                result["success"] = False
                result["details"] = "Could not fetch file: {}".format(e)
                return result

            status = Vault.create_attachment(file_contents,
                                             self.connector.get_container_id(),
                                             file_name=binary.original_filename)
            if not status.get("succeeded", False):
                result["success"] = False
                result["details"] = "Could not create vault"
                return result

            result_data = {"file_hash": file_hash,
                           "vault_id": status.get("vault_id", None),
                           "file_name": binary.original_filename}

            self.action_result.add_data(result_data)
            result["success"], result["details"] = True, "File successfully retrieved"
        else:
            result["details"] = "Malformed sha256 hash"

        return result

    def _is_sha256(self, str_hash):
        """Check whether string is sha256 hash"""
        if len(str_hash) != 64:
            return False
        try:
            _ = int(str_hash, 16)
        except ValueError:
            return False

        return True

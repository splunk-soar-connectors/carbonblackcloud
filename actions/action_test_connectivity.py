# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Test Connectivity Action Class"""
from actions import BaseAction
import phantom.app as phantom
import datetime
from cbc_sdk.platform import BaseAlert
from cbc_sdk.errors import UnauthorizedError, TimeoutError, ConnectionError, CredentialError, ObjectNotFoundError


class CheckConnectivityAction(BaseAction):
    """Class to handle test connectivity action."""
    def call(self):
        """Execute test connectivity action."""
        result = self._test_cbc_connectivity()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR

        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _test_cbc_connectivity(self):
        """Tests connectivity to CBC instance"""
        result = {"success": True, "details": "Connection successful."}
        if not self.cbc:
            result["success"] = False
            result["details"] = "Please configure all connection parameters."
            return result

        try:
            timestamp = datetime.datetime.utcnow()
            start_time = "{}Z".format(timestamp.isoformat())
            end_time = start_time
            alerts = self.cbc.select(BaseAlert).set_time_range("last_update_time", start=start_time, end=end_time)
            _ = len(alerts)
        except (UnauthorizedError, CredentialError):
            result["success"] = False
            result["details"] = "Bad Custom Connector ID or key."
            return result
        except (TimeoutError, ConnectionError):
            result["success"] = False
            result["details"] = "Could not connect to CBC. Check the Server URL."
            return result
        except ObjectNotFoundError:
            result["success"] = False
            result["details"] = "Invalid ORG key."
            return result
        except Exception as e:
            result["success"] = False
            result["details"] = f"Unknown error - {e}"
            return result

        return result

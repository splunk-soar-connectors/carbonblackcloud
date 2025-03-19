# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2023-2025 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Get Cleared Event Logs Class Action"""

import phantom.app as phantom

from actions import BaseAction
from utils.cbc_live_query import LiveQuery


SQL_QUERY = """SELECT datetime,
                   json_extract(DATA, '$.UserData.LogFileCleared.SubjectDomainName') AS DOMAIN,
                   json_extract(DATA, '$.UserData.LogFileCleared.SubjectUserName') AS USER,
                   json_extract(DATA, '$.UserData.LogFileCleared.SubjectUserSid') AS sid
               FROM windows_eventlog
               WHERE channel = 'Security'
                 AND eventid = '1102';"""


class GetClearedEventlogsAction(BaseAction):
    """Class to handle get cleared eventlogs action (utilizing Live Query)"""

    def call(self):
        """Execute get clered eventlogs action."""
        result = self._get_cleared_eventlogs()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _get_cleared_eventlogs(self):
        """Get cleared eventlogs action"""
        # generic checks
        checks = super().call()
        if checks is not None:
            return checks

        device_id = self.param.get("device_id", "")
        self.connector.debug_print(f"Get cleared eventlogs action with parameters {self.param}")
        result = {"success": False, "details": f"Could not get cleared eventlogs for {device_id}."}
        if device_id == "":
            result = {"success": False, "details": "Could not get cleared eventlogs, missing device_id."}
            return result

        live_query = LiveQuery(self.cbc)
        results = live_query.run(SQL_QUERY, device_id, run_name="Splunk SOAR CBC App - Cleared Event Logs")
        result = {"success": live_query.success, "details": live_query.message}
        if not live_query.success:
            return result

        for res in results:
            if res["status"] == "matched":
                data = {
                    "datetime": res["fields"]["datetime"],
                    "domain": res["fields"]["DOMAIN"],
                    "user": res["fields"]["USER"],
                    "sid": res["fields"]["sid"],
                }
                self.action_result.add_data(data)

        return result

# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2023 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Get Scheduled Task Created Class Action"""
import phantom.app as phantom
from utils.cbc_live_query import LiveQuery

from actions import BaseAction

SQL_QUERY = """SELECT * FROM windows_eventlog WHERE channel = 'Security' AND eventid = '4698';"""


class GetScheduledTaskAction(BaseAction):
    """Class to handle get scheduled task created action (utilizing Live Query)"""
    def call(self):
        """Execute get scheduled task created action."""
        result = self._get_scheduled_task()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _get_scheduled_task(self):
        """Get scheduled task created action"""
        # generic checks
        checks = super().call()
        if checks is not None:
            return checks

        device_id = self.param.get("device_id", "")
        self.connector.debug_print(f"Get scheduled task created action with parameters {self.param}")
        result = {"success": False, "details": f"Could not get scheduled task created for {device_id}."}
        if device_id == "":
            result = {"success": False, "details": "Could not get scheduled task created, missing device_id."}
            return result

        live_query = LiveQuery(self.cbc)
        results = live_query.run(SQL_QUERY, device_id, run_name="Splunk SOAR CBC App - Scheduled Task Created")
        result = {"success": live_query.success, "details": live_query.message}
        if not live_query.success:
            return result

        for res in results:
            if res["status"] == "matched":
                data = {"event_channel": res["fields"]["channel"],
                        "datetime": res["fields"]["datetime"],
                        "task": res["fields"]["task"],
                        "severity": res["fields"]["level"],
                        "provider_name": res["fields"]["provider_name"],
                        "provider_guid": res["fields"]["provider_guid"],
                        "host": res["fields"]["computer_name"],
                        "event_id": res["fields"]["eventid"],
                        "keywords": res["fields"]["keywords"],
                        "data": res["fields"]["data"],
                        "process_pid": res["fields"]["pid"],
                        "thread_id": res["fields"]["tid"],
                        "time_range": res["fields"]["time_range"],
                        "timestamp": res["fields"]["timestamp"],
                        "xpath": res["fields"]["xpath"]}
                self.action_result.add_data(data)

        return result

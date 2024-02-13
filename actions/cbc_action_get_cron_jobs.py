# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2023 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Get Cron Jobs Class Action"""
import phantom.app as phantom
from utils.cbc_live_query import LiveQuery

from actions import BaseAction

SQL_QUERY = """SELECT event,
                      minute,
                      hour,
                      day_of_month,
                      month,
                      day_of_week,
                      command,
                      path
                FROM crontab;"""


class GetCronJobsAction(BaseAction):
    """Class to handle get cron jobs action (utilizing Live Query)"""
    def call(self):
        """Execute get cron jobs action."""
        result = self._get_cron_jobs()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _get_cron_jobs(self):
        """Get cron jobs action"""
        # generic checks
        checks = super().call()
        if checks is not None:
            return checks

        device_id = self.param.get("device_id", "")
        self.connector.debug_print(f"Get cron jobs action with parameters {self.param}")

        if device_id == "":
            result = {"success": False, "details": "Could not get cron jobs, missing device_id."}
            return result

        live_query = LiveQuery(self.cbc)
        results = live_query.run(SQL_QUERY, device_id, run_name="Splunk SOAR CBC App - Cron Jobs")
        result = {"success": live_query.success, "details": live_query.message}
        if not live_query.success:
            return result

        for res in results:
            if res["status"] == "matched":
                data = {
                    "name": res["fields"]["event"],
                    "minute": res["fields"]["minute"],
                    "hour": res["fields"]["hour"],
                    "day_of_month": res["fields"]["day_of_month"],
                    "month": res["fields"]["month"],
                    "day_of_week": res["fields"]["day_of_week"],
                    "command": res["fields"]["command"],
                    "path": res["fields"]["path"]
                }
                self.action_result.add_data(data)
        return result

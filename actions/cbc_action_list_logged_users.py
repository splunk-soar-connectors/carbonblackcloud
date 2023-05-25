# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2023 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""List Logged In Users Class Action"""
import phantom.app as phantom
from cbc_sdk.platform import Device

from actions import BaseAction
from utils.cbc_live_query import LiveQuery

WINDOWS_SQL_QUERY = """SELECT TYPE, USER, tty, HOST, datetime(TIME, 'unixepoch', 'localtime') AS TIME,
                       pid, sid, registry_hive FROM logged_in_users;"""
LINUX_MAC_SQL_QUERY = """SELECT TYPE, USER, tty, HOST, datetime(TIME, 'unixepoch', 'localtime') AS TIME,
                         pid, p.name, p.cmdline, sid, registry_hive
                         FROM logged_in_users JOIN processes AS p USING(pid);"""


class ListLoggedUsersAction(BaseAction):
    """Class to handle list logged in users action (utilizing Live Query)"""
    def call(self):
        """Execute list logged in users action."""
        result = self._list_logged_users()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _list_logged_users(self):
        """List logged in users action"""
        # generic checks
        checks = super().call()
        if checks is not None:
            return checks

        device_id = self.param.get("device_id", "")
        self.connector.debug_print(f"List logged in users action with parameters {self.param}")
        result = {"success": False, "details": f"Could not list logged in users for {device_id}."}
        if device_id == "":
            result = {"success": False, "details": "Could not list logged in users, missing device_id."}
            return result

        live_query = LiveQuery(self.cbc)
        device = self.cbc.select(Device, device_id)
        os = device._info.get("os")
        if os == "WINDOWS":
            results = live_query.run(WINDOWS_SQL_QUERY, device_id,
                                     run_name="Splunk SOAR CBC App - List Logged in Users (Windows)")
        elif (os == "MAC") or (os == "LINUX"):
            results = live_query.run(LINUX_MAC_SQL_QUERY, device_id,
                                     run_name="Splunk SOAR CBC App - List Logged in Users (MacOS/Linux)")
        else:
            result = {"success": False, "details": f"Could not list logged in users, {os} is not supported."}
            return result

        result = {"success": live_query.success, "details": live_query.message}
        if not live_query.success:
            return result

        for res in results:
            if res["status"] == "matched":
                data = {"login_type": res["fields"]["type"],
                        "user": res["fields"]["user"],
                        "device_name": res["fields"]["tty"],
                        "host": res["fields"]["host"],
                        "time": res["fields"]["TIME"],
                        "process_pid": res["fields"]["pid"],
                        "sid": res["fields"]["sid"],
                        "registry_hive": res["fields"]["registry_hive"]}
                if (os == "MAC") or (os == "LINUX"):
                    data.update({"process_name": res["fields"]["name"], "cmdline": res["fields"]["cmdline"]})
                else:
                    data.update({"process_name": "", "cmdline": ""})
                self.action_result.add_data(data)

        return result

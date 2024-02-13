# Copyright 2023 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""List Windows Persistence Locations Class Action"""
import phantom.app as phantom
from utils.cbc_live_query import LiveQuery

from actions import BaseAction

SQL_QUERY = """SELECT * FROM autoexec;"""


class ListWindowsPersistenceLocationsAction(BaseAction):
    """Class to handle list windows persistence locations action (utilizing Live Query)"""
    def call(self):
        """Execute list windows persistence locations action."""
        result = self._list_windows_persistence_locations()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _list_windows_persistence_locations(self):
        """List windows persistence locations action"""
        # generic checks
        checks = super().call()
        if checks is not None:
            return checks

        device_id = self.param.get("device_id", "")
        self.connector.debug_print(f"List windows persistence locations action with parameters {self.param}")
        result = {"success": False, "details": f"Could not glist windows persistence locations for {device_id}."}
        if device_id == "":
            result = {"success": False, "details": "Could not list windows persistence locations, missing device_id."}
            return result

        live_query = LiveQuery(self.cbc)
        results = live_query.run(SQL_QUERY, device_id, run_name="Splunk SOAR CBC App - Windows Persistence Locations")
        result = {"success": live_query.success, "details": live_query.message}
        if not live_query.success:
            return result

        for res in results:
            if res["status"] == "matched":
                data = {"path": res["fields"]["path"],
                        "name": res["fields"]["name"],
                        "source": res["fields"]["source"]}
                self.action_result.add_data(data)

        return result

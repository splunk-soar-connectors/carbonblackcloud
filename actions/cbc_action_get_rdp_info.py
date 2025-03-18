# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2023-2025 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Get RDP Connection Info Class Action"""

import phantom.app as phantom

from actions import BaseAction
from utils.cbc_live_query import LiveQuery


SQL_QUERY = """SELECT processes.pid,
                   processes.name,
                   processes.cmdline,
                   process_open_sockets.local_address,
                   process_open_sockets.remote_address,
                   process_open_sockets.local_port,
                   process_open_sockets.remote_port
               FROM processes
               INNER JOIN process_open_sockets ON processes.pid=process_open_sockets.pid
               WHERE remote_port!=0
                 AND local_port=3389;"""


class GetRDPInfoAction(BaseAction):
    """Class to handle get RDP connection information action (utilizing Live Query)"""

    def call(self):
        """Execute get RDP info action."""
        result = self._get_rdp_info()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _get_rdp_info(self):
        """Get RDP info action"""
        # generic checks
        checks = super().call()
        if checks is not None:
            return checks

        device_id = self.param.get("device_id", "")
        self.connector.debug_print(f"Get RDP info action with parameters {self.param}")
        result = {"success": False, "details": f"Could not get RDP info for {device_id}."}
        if device_id == "":
            result = {"success": False, "details": "Could not get RDP info, missing device_id."}
            return result

        live_query = LiveQuery(self.cbc)
        results = live_query.run(SQL_QUERY, device_id, run_name="Splunk SOAR CBC App - RDP Connection Information")
        result = {"success": live_query.success, "details": live_query.message}
        if not live_query.success:
            return result

        for res in results:
            if res["status"] == "matched":
                data = {
                    "process_pid": res["fields"]["pid"],
                    "process_name": res["fields"]["name"],
                    "process_cmdline": res["fields"]["cmdline"],
                    "local_address": res["fields"]["local_address"],
                    "remote_address": res["fields"]["remote_address"],
                    "local_port": res["fields"]["local_port"],
                    "remote_port": res["fields"]["remote_port"],
                }
                self.action_result.add_data(data)

        return result

# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Create operation over a Carbon Black Cloud's Watchlist"""
import traceback

import phantom.app as phantom
from cbc_sdk.enterprise_edr import Watchlist

from actions import BaseAction


class CreateWatchlistAction(BaseAction):
    """
    Create Watchlist action

    Splunk Phantom Parameters: (* - required)
        - (*)watchlist_name: (str) - The Watchlist's name
        - watchlist_description: (str) - The Watchlist's description
        - watchlist_tags_enabled: (boolean) - If the tags should be enabled
        - watchlist_alerts_enabled: (boolean) - If the alerts should be enabled
        - watchlist_report_ids: (str) - The IDs of the reports in the Watchlist (CSV)
    """

    def call(self):
        """Execute create watchlist action"""
        result = self._create_watchlist()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _create_watchlist(self):
        """Create Watchlist implementation"""
        try:
            builder = Watchlist.create(self.cbc, self.param.get("watchlist_name"))
            builder.set_description(self.param.get("watchlist_description", None))
            builder.set_tags_enabled(self.param.get("watchlist_tags_enabled", False))
            builder.set_alerts_enabled(self.param.get("watchlist_alerts_enabled", True))
            if self.param.get("watchlist_report_ids", None):
                builder.add_report_ids(self.param.get("watchlist_report_ids").split(","))
            watchlist = builder.build()
            watchlist = watchlist.save()
            self.action_result.add_data(watchlist._info)
            result = {"success": True, "details": f"Created Watchlist {watchlist.id}"}
        except Exception as e:
            self.connector.error_print(traceback.format_exc())
            result = {"success": False, "details": f"Watchlist was not created - {e}"}
        return result

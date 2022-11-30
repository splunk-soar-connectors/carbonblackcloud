# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Update operation over a Carbon Black Cloud's Watchlist"""
import traceback

import phantom.app as phantom
from cbc_sdk.enterprise_edr import Watchlist
from cbc_sdk.errors import ObjectNotFoundError

from actions import BaseAction
from copy import deepcopy


class UpdateWatchlistAction(BaseAction):
    """
    Update Watchlist action

    Splunk Phantom Parameters: (* - required)
        - (*)watchlist_id: (str) - The ID of the Watchlist
        - watchlist_name: (str) - The Watchlist's name
        - watchlist_description: (str) - The Watchlist's description
        - watchlist_tags_enabled: (boolean) - If the tags should be enabled
        - watchlist_alerts_enabled: (boolean) - If the alerts should be enabled
        - add_report_ids: (str) - The IDs of the reports to be added in the Watchlist (CSV)
        - remove_report_ids: (str) - The IDs of reports to be removed from the Watchlist (CSV)
    """

    def call(self):
        """Execute update Watchlist action"""
        result = self._update_watchlist()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _update_watchlist(self):
        """Update Watchlist implementation"""
        watchlist_id = self.param.get("watchlist_id")
        update_dict = {
            "name": self.param.get("watchlist_name", None),
            "description": self.param.get("watchlist_description", None),
            "tags_enabled": self.param.get("watchlist_tags_enabled", None),
            "alerts_enabled": self.param.get("watchlist_alerts_enabled", None),
            "category": self.param.get("watchlist_category", None),
        }
        try:
            watchlist = self.cbc.select(Watchlist, watchlist_id)
            if self.param.get("add_report_ids", None):
                watchlist.add_report_ids(self.param.get("add_report_ids").split(","))
            if self.param.get("remove_report_ids", None):
                # There is no remove_report_ids, so doing that the ugly way,
                # if such functionality is provided, replace it!
                reports = deepcopy(watchlist.report_ids)
                for report_id in self.param.get("remove_report_ids").split(","):
                    if report_id in watchlist.report_ids:
                        reports.remove(report_id)
                update_dict["report_ids"] = reports
            watchlist.update(**update_dict)
            self.action_result.add_data(watchlist._info)
            result = {"success": True, "details": f"Successfully updated {watchlist_id}"}
        except ObjectNotFoundError:
            result = {"success": False, "details": "Watchlist not found"}
        except Exception as e:
            self.connector.error_print(traceback.format_exc())
            result = {"success": False, "details": f"Watchlist couldn't be updated - {e}"}
        return result

# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Retrieve operation over a Carbon Black Cloud's Watchlist"""
import traceback

import phantom.app as phantom
from cbc_sdk.enterprise_edr import Watchlist
from cbc_sdk.errors import ObjectNotFoundError

from actions import BaseAction


class RetrieveWatchlistAction(BaseAction):
    """
    Retrieve Watchlist action

    Splunk Phantom Parameters: (* - required)
        - (*)watchlist_id: (str) - The ID of the Watchlist
    """

    def call(self):
        """Execute retrieve Watchlist action"""
        result = self._retrieve_watchlist()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _retrieve_watchlist(self):
        """Retrieve watchlist implementation"""
        watchlist_id = self.param.get("watchlist_id")
        try:
            watchlist = self.cbc.select(Watchlist, watchlist_id)
            self.action_result.add_data(watchlist._info)
            result = {"success": True, "details": f"Retrieved {watchlist.id}"}
        except ObjectNotFoundError:
            result = {"success": False, "details": "Watchlist not found"}
        except Exception as e:
            self.connector.error_print(traceback.format_exc())
            result = {"success": False, "details": f"Watchlist couldn't be retrieved - {e}"}
        return result

# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Remove an IOC from a Watchlist"""
import traceback

import phantom.app as phantom
from cbc_sdk.enterprise_edr import Watchlist

from actions import BaseAction


class RemoveIOCWatchlistAction(BaseAction):
    """Remove an IOC from a Watchlist Action"""

    def call(self):
        """Remove Remove an IOC from Watchlist"""
        result = self._remove_ioc()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _get_report(self):
        """Returning the Report based on the `self.param`"""
        report = None
        if self.param.get("watchlist_id", None):
            # `Report` doesn't support the `watchlist_id` param so we have to
            # fetch everything manually
            watchlist = self.cbc.select(Watchlist, self.param["watchlist_id"])
            for report_ in watchlist.reports:
                if report_.id == self.param["report_id"]:
                    report = report_
                    break
            if not report:
                raise ValueError("Report cannot be found")
        else:
            raise ValueError("You must provide `watchlist_id`")
        return report

    def _remove_ioc(self):
        """Remove an IOC from a Watchlist"""
        ioc_id = self.param.get("ioc_id")
        ioc_value = self.param.get("ioc_value")
        try:
            report = self._get_report()
            if ioc_id:
                report.remove_iocs_by_id([ioc_id])
            elif ioc_value:
                ioc = None
                for item in report.iocs_v2:
                    if ioc_value in item['values']:
                        ioc = item
                        break
                if ioc:
                    report.remove_iocs_by_id([ioc["id"]])

            report.update()
            result = {"success": True, "details": f"Removed IOC {ioc_id or ioc_value}"}
        except Exception as e:
            self.connector.error_print(traceback.format_exc())
            result = {"success": False, "details": f"IOC was not Removed - {e}"}
        return result

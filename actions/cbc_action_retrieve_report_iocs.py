# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Retrieve IOCs from a Report"""
import traceback

import phantom.app as phantom
from cbc_sdk.enterprise_edr import Report
from cbc_sdk.errors import ObjectNotFoundError

from actions import BaseAction


class RetrieveIOCAction(BaseAction):
    """Retrieve IOCs from a Report Action"""

    def call(self):
        """Retrieve IOCs from a Report"""
        result = self._retrieve_iocs()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _get_report(self):
        """Retrieve iocs from a report"""
        report = None
        if self.param.get("feed_id", None) and self.param.get("watchlist_id", None):
            raise ValueError("You should provide either feed_id or watchlist_id.")
        elif not (self.param.get("feed_id", None) or self.param.get("watchlist_id", None)):
            raise ValueError("You should provide either feed_id or watchlist_id.")
        elif self.param.get("feed_id", None):
            # There is no filtering by ID, so grab all reports in a feed and filter manually
            reports = self.cbc.select(Report).where(feed_id=self.param["feed_id"])
            for report_ in reports:
                if report_.id == self.param["report_id"]:
                    report = report_
                    break
            if not report:
                raise ValueError("Report cannot be found.")
        else:
            try:
                report = self.cbc.select(Report, self.param["report_id"])
            except ObjectNotFoundError:
                raise ValueError("Report cannot be found.")
        return report

    def _retrieve_iocs(self):
        """Retrieve IOCs from a Feed/Watchlist"""
        # generic checks
        checks = super().call()
        if checks is not None:
            return checks
        try:
            report = self._get_report()
            for ioc in report.iocs_v2:
                self.action_result.add_data(ioc)
            result = {"success": True, "details": f"Successfully retrieved iocs for report {report.id}"}
        except Exception as e:
            self.connector.error_print(traceback.format_exc())
            result = {"success": False, "details": f"Could not retrieve iocs for report - {e}"}
        return result

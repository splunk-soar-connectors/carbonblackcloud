# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Add an IOC to Feed/Watchlist"""
import traceback
import uuid

import phantom.app as phantom
from cbc_sdk.enterprise_edr import IOC_V2, Report
from cbc_sdk.errors import ObjectNotFoundError

from actions import BaseAction


class AddIOCAction(BaseAction):
    """Add an IOC to Feed/Watchlist"""

    def call(self):
        """Execute Add an IOC to Feed/Watchlist"""
        result = self._add_ioc()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _get_report(self) -> Report:
        """Returning the Report based on the `self.param`"""
        report = None
        if self.param.get("feed_id", None) and self.param.get("watchlist_id", None):
            raise ValueError("You should provide either watchlist_id or feed_id.")
        elif self.param.get("feed_id", None):
            # There is no filtering by ID, so grab all reports in a feed and filter manually
            reports = self.cbc.select(Report).where(feed_id=self.param["feed_id"])
            for report_ in reports:
                if report_.id == self.param["report_id"]:
                    report = report_
                    break
            if not report:
                raise ValueError("Report cannot be found")
        elif self.param.get("watchlist_id", None):
            try:
                report = self.cbc.select(Report, self.param["report_id"])
            except ObjectNotFoundError:
                raise ValueError("Report cannot be found.")
        else:
            raise ValueError("You must provide either `feed_id` or `watchlist_id`")
        return report

    def _add_ioc(self):
        """Add an IOC to Feed/Watchlist"""
        ioc_id = self.param.get("ioc_id", str(uuid.uuid4()))
        cbc_field = self.param.get("cbc_field")
        ioc_value = self.param.get("ioc_value")
        try:
            report = self._get_report()
            if len(report.iocs_) >= 1000:
                result = {"success": False, "details": "The report is full, create a new report!"}
                return result
            ioc = IOC_V2.create_equality(self.cbc, ioc_id, cbc_field, ioc_value)
            report.append_iocs([ioc])
            report.update()
            self.action_result.add_data({"ioc": ioc._info})
            result = {"success": True, "details": f"Added IOC {ioc.id}"}
        except Exception as e:
            self.connector.error_print(traceback.format_exc())
            result = {"success": False, "details": f"IOC was not added - {e}"}
        return result

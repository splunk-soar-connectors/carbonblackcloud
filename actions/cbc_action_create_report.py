# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Create operation over a Carbon Black Cloud's Report"""
import traceback
import uuid

import phantom.app as phantom
from cbc_sdk.enterprise_edr import Report

from actions import BaseAction


class CreateReportAction(BaseAction):
    """Create report action

    Splunk Phantom Parameters: (* - required)
        - feed_id: (str) - The ID of the Feed
        - report_save_as_watchlist: (bool) - If the Report is going to be saved as a Watchlist Report
            (it doesnt require the `feed_id` if it's set to True)
        - (*)report_name: (str) - The name of the report
        - (*)report_severity: (str) - The string is converted to Integer
            and the severity of the Report must be between 1 and 10
        - (*)report_summary: (str) - Summary of the Report
        - report_tags: (str) - Comma separated values of tags

    """

    def call(self):
        """Execute create report action"""
        result = self._create_report()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _create_report(self):
        """Create report implementation"""
        feed_id = self.param.get("feed_id", None)
        report_save_as_watchlist = self.param.get("report_save_as_watchlist", False)
        report_name = self.param.get("report_name")
        report_severity = self.param.get("report_severity")
        report_summary = self.param.get("report_summary")
        report_tags = self.param.get("report_tags", None)
        try:
            if not int(report_severity) in range(1, 10):
                raise ValueError("Report severity must be an integer and inbetween 1 and 10.")
            report_builder = Report.create(self.cbc, report_name, report_summary, report_severity)
            report_builder._report_body["id"] = str(uuid.uuid4())
            if report_tags:
                for tag in report_tags.split(","):
                    report_builder.add_tag(tag)
            if report_save_as_watchlist and not feed_id:
                report = Report(self.cbc, initial_data=report_builder._report_body)
                report.save_watchlist()
            elif feed_id and not report_save_as_watchlist:
                report = Report(self.cbc, initial_data=report_builder._report_body, feed_id=feed_id)
            else:
                raise ValueError("You have to set `feed_id` or set `Save to Watchlist` to True.")
            report = report.update()
            self.action_result.add_data(report._info)
            result = {"success": True, "details": f"Created Report {report.id}"}
        except Exception as e:
            self.connector.error_print(traceback.format_exc())
            result = {"success": False, "details": f"Report was not created - {e}"}
        return result

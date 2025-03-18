# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022-2025 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Helper class for LiveQuery runs"""

import time
import traceback

from cbc_sdk.audit_remediation import Run


class LiveQuery:
    """The class responsible for LiveQuery runs"""

    def __init__(self, cbc):
        """Class constructor"""
        self.cbc = cbc
        self.success = False
        self.message = "No query submitted"

    def run(self, query, device_id, run_name=None):
        """Submits a LiveQuery run, returns results"""
        if not self.cbc:
            self.message = "No valid CBCloudAPI object passed"
            self.success = False
            return None
        try:
            output = []
            if run_name:
                run_query = self.cbc.select(Run).where(query).device_ids([int(device_id)]).name(run_name)
            else:
                run_query = self.cbc.select(Run).where(query).device_ids([int(device_id)])
            res_query = run_query.submit()
            finished = False
            while not finished:
                res_query.refresh()
                results = res_query.query_results()
                for element in results:
                    if element._info not in output:
                        output.append(element._info)
                if res_query.in_progress_count == 0 and res_query.not_started_count == 0:
                    finished = True
                else:
                    time.sleep(1)

            self.message = "LiveQuery completed successfully"
            self.success = True
            return output

        except:
            self.message = "LiveQuery run error: "
            self.message += traceback.format_exc()
            self.success = False
            return None

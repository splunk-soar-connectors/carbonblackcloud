# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Create operation over a Carbon Black Cloud's Feed"""
import traceback

import phantom.app as phantom
from cbc_sdk.enterprise_edr import Feed

from actions import BaseAction


class CreateFeedAction(BaseAction):
    """
    Create feed action

    Splunk Phantom Parameters: (* - required)
        - (*)feed_name: (str) - The name of the Feed
        - (*)feed_provider_url: (str) - The Provider URL of the Feed
        - (*)feed_summary: (str) - The Feed's summary
        - (*)feed_category: (str) - The Feed's category
    """

    def call(self):
        """Execute create feed action"""
        result = self._create_feed()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _create_feed(self):
        """Create feed implementation"""
        feed_name = self.param.get("feed_name")
        feed_provider_url = self.param.get("feed_provider_url")
        feed_summary = self.param.get("feed_summary")
        feed_category = self.param.get("feed_category")
        try:
            builder = Feed.create(
                self.cbc, feed_name, feed_provider_url, feed_summary, feed_category
            )
            feed = builder.build()
            feed = feed.save()
            self.action_result.add_data(feed._info)
            result = {"success": True, "details": f"Created Feed {feed.id}"}
        except Exception as e:
            self.connector.error_print(traceback.format_exc())
            result = {"success": False, "details": f"Feed was not created - {e}"}
        return result

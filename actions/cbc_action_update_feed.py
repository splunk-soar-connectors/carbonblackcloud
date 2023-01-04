# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Update operation over a Carbon Black Cloud's Feed"""
import traceback

import phantom.app as phantom
from cbc_sdk.enterprise_edr import Feed
from cbc_sdk.errors import ObjectNotFoundError

from actions import BaseAction


class UpdateFeedAction(BaseAction):
    """
    Update Feed action

    Splunk Phantom Parameters: (* - required)
        - (*)feed_id: (str) - The ID of the Feed
        - feed_name: (str) - The name of the Feed
        - feed_provider_url: (str) - The Provider URL of the Feed
        - feed_summary: (str) - The Feed's summary
        - feed_category: (str) - The Feed's category
    """

    def call(self):
        """Execute delete feed action"""
        result = self._update_feed()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _update_feed(self):
        """Update feed implementation"""
        feed_id = self.param.get("feed_id")
        update_dict = {
            "name": self.param.get("feed_name", None),
            "provider_url": self.param.get("feed_provider_url", None),
            "summary": self.param.get("feed_summary", None),
            "category": self.param.get("feed_category", None),
        }
        try:
            feed = self.cbc.select(Feed, feed_id)
            feed.update(**update_dict)
            self.action_result.add_data(feed._info)
            result = {"success": True, "details": f"Successfully updated {feed_id}"}
        except ObjectNotFoundError:
            result = {"success": False, "details": "Feed not found"}
        except Exception as e:
            self.connector.error_print(traceback.format_exc())
            result = {"success": False, "details": f"Feed couldn't be updated - {e}"}
        return result

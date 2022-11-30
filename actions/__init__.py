# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
from phantom.action_result import ActionResult
from cbc_sdk import CBCloudAPI
from cbcapp_consts import __version__


class BaseAction:
    def __init__(self, connector, param):
        self.connector = connector
        self.action_result = ActionResult(dict(param))
        self.connector.add_action_result(self.action_result)
        self.param = param
        self.cbc = self._get_cbc()

    def call(self):
        """All generic checks. If None is returned, then can continue with the action"""
        if not self.cbc:
            self.connector.error_print("No valid connection to Carbon Black Cloud")
            return {"success": False, "details": "Please configure all connection parameters."}
        return None

    def _get_cbc(self):
        """Returns a configured CBCloudAPI instance with custom key"""
        config = self.connector.get_config()
        try:
            custom = CBCloudAPI(
                url=config["cbc_url"].rstrip("/"),
                org_key=config["org_key"],
                token=f"{config['api_secret_key']}/{config['api_id']}",
                integration_name=f"SplunkSoar-{__version__}"
            )
        except Exception:
            custom = None
        return custom

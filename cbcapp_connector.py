#!/usr/bin/python
# -*- coding: utf-8 -*-
# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.

"""Phantom sample App Connector python file"""


from __future__ import print_function, unicode_literals

# Dynamically imported actions
from importlib import import_module
from glob import glob
from actions import BaseAction

# Phantom App imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector

# from phantom.action_result import ActionResult

# Usage of the consts file is recommended
# from carbonblackcloudsplunksoaraoo_consts import *
import requests
import json
import os


class RetVal(tuple):
    """Helper class RetVal"""
    def __new__(cls, val1, val2=None):
        """New magic method"""
        return tuple.__new__(RetVal, (val1, val2))


class CarbonBlackCloudSplunkSoarAppConnector(BaseConnector):
    """Main Class for CBC Splunk App"""

    def __init__(self):
        """Initializer of CarbonBlackCloudSplunkSoarAppConnector"""
        # Call the BaseConnectors init first
        super(CarbonBlackCloudSplunkSoarAppConnector, self).__init__()

        self._state = None

        # Variable to hold a base_url in case the app makes REST calls
        # Do note that the app json defines the asset config, so please
        # modify this as you deem fit.
        self._base_url = None

    def handle_action(self, params):
        """Handle action method"""
        ret_val = phantom.APP_ERROR

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()
        self.debug_print(f"action_id, {params}", self.get_action_identifier())

        # When running the action, CWD is not the same as the script directory, so glob requires a full path
        base = os.path.dirname(os.path.realpath(__file__)) + "/"
        path = base + "actions/action_*.py"
        for mod_path in glob(path):
            module = mod_path.replace(base, "").replace("/", ".").replace(".py", "")
            import_module(module, package="actions")
        actions = BaseAction.__subclasses__()
        action_name = "actions.action_" + action_id
        action_name = action_name.replace(" ", "_")
        for action_class in actions:
            if action_class.__module__ == action_name:
                action = action_class(self, params)
                ret_val = action.call()
                break

        return ret_val

    def initialize(self):
        """Load the state in initialize, use it to store data that needs to be accessed across actions"""
        self._state = self.load_state()

        # get the asset config
        config = self.get_config()
        """
        # Access values in asset config by the name

        # Required values can be accessed directly
        required_config_name = config['required_config_name']

        # Optional values should use the .get() function
        optional_config_name = config.get('optional_config_name')
        """

        self._base_url = config.get("base_url")

        return phantom.APP_SUCCESS

    def finalize(self):
        """Save the state, this data is saved across actions and app upgrades"""
        self.save_state(self._state)
        return phantom.APP_SUCCESS


def main():
    """Main Entry"""
    import pudb
    import argparse

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument("input_test_json", help="Input Test JSON file")
    argparser.add_argument("-u", "--username", help="username", required=False)
    argparser.add_argument("-p", "--password", help="password", required=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password

    if username is not None and password is None:

        # User specified a username but not a password, so ask
        import getpass

        password = getpass.getpass("Password: ")

    if username and password:
        try:
            login_url = (CarbonBlackCloudSplunkSoarAppConnector._get_phantom_base_url() + "/login")

            print("Accessing the Login page")
            r = requests.get(login_url, verify=False)
            csrftoken = r.cookies["csrftoken"]

            data = dict()
            data["username"] = username
            data["password"] = password
            data["csrfmiddlewaretoken"] = csrftoken

            headers = dict()
            headers["Cookie"] = "csrftoken=" + csrftoken
            headers["Referer"] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=False, data=data, headers=headers)
            session_id = r2.cookies["sessionid"]
        except Exception as e:
            print("Unable to get session id from the platform. Error: " + str(e))
            exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = CarbonBlackCloudSplunkSoarAppConnector()
        connector.print_progress_message = True

        if session_id is not None:
            in_json["user_session_token"] = session_id
            connector._set_csrf_info(csrftoken, headers["Referer"])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    exit(0)


if __name__ == "__main__":
    main()

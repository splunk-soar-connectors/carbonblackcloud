# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Execute Command Action Class"""
import traceback
from cbc_sdk.platform import Device
from cbc_sdk.errors import TimeoutError

from actions import BaseAction
import phantom.app as phantom


class ExecuteCommandAction(BaseAction):
    """Class to handle execute command live response action."""
    def call(self):
        """Execute execute command action."""
        result = self._execute_command()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _execute_command(self):
        """Execute Live Response action."""
        checks = super().call()
        if checks is not None:
            return checks
        device_id = self.param.get("device_id", "")
        work_dir = self.param.get("work_dir", None)
        timeout = self.param.get("timeout", 30)
        if "command_line" not in self.param.keys():
            return {"success": False, "details": "No command_line provided"}
        commandline = self.param["command_line"]

        self.connector.debug_print(f"execute command Live Response action with parameters {self.param}")
        result = {"success": False, "details": f"Could not execute command for {device_id}."}

        if device_id:
            try:
                device = self.cbc.select(Device, device_id)
                try:
                    lr_session = device.lr_session()
                except Exception as e:
                    self.connector.error_print(traceback.format_exc())
                    result["success"] = False
                    result["details"] = "Could not establish LR session - {}".format(e)
                    return result
                try:
                    stdout = lr_session.create_process(commandline,
                                                       wait_for_output=True,
                                                       wait_timeout=timeout,
                                                       wait_for_completion=True,
                                                       working_directory=work_dir)
                except TimeoutError:
                    self.connector.error_print(traceback.format_exc())
                    result["success"] = False
                    result["details"] = "Timeout executing command"
                    return result
                except Exception as e:
                    self.connector.error_print(traceback.format_exc())
                    result["success"] = False
                    result["details"] = "Could not execute command {}: {}".format(commandline, e)
                    return result

                result_data = {"device_id": device_id,
                               "command_line": commandline,
                               "stdout": stdout}
                self.action_result.add_data(result_data)
                result["success"], result["details"] = True, "Command successfully executed"
            except Exception as e:
                self.connector.error_print(traceback.format_exc())
                result["details"] = "Could not execute command {}: {}".format(commandline, e)
        else:
            result["details"] = "Missing device id."
        return result

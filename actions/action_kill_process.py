# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Kill Process Action Class"""
import traceback
from cbc_sdk.platform import Device
from cbc_sdk.platform import Process

from actions import BaseAction
import phantom.app as phantom


class KillProcessAction(BaseAction):
    """Class to handle kill process live response action."""

    def call(self):
        """Execute kill process action."""
        result = self._kill_process()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR
        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _kill_pid(self, lr_session, device_id, process_pid, process_name):
        """LR action - kill by PID"""
        try:
            killed = lr_session.kill_process(process_pid)
        except:
            killed = False
        data = {
            "device_id": device_id,
            "process_pid": process_pid,
            "process_name": process_name,
            "process_killed": killed,
        }
        self.action_result.add_data(data)

    def _kill_process(self):
        """Kill Process Live Response action."""
        checks = super().call()
        if checks is not None:
            return checks

        device_id = self.param.get("device_id", "")

        self.connector.debug_print(f"Kill Process Live Response action with parameters {self.param}")
        result = {"success": False, "details": f"Could not kill process for {device_id}."}

        if device_id:
            proc_pid = self.param.get("process_pid", None)
            proc_name = self.param.get("process_name", None)
            proc_hash = self.param.get("process_hash", None)
            proc_guid = self.param.get("process_guid", None)
            if not proc_pid and not proc_name and not proc_hash and not proc_guid:
                return {
                    "success": False,
                    "details": "You must provide process_pid or process_name or process_hash or process_guid",
                }

            # If process name is a full path, leave just the executable name
            if proc_name:
                proc_name = proc_name.replace("\\", "/")
                proc_name = proc_name.split("/")[-1]

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
                    pid_list = []
                    if proc_pid:
                        pid_list.append(proc_pid)
                    if proc_hash:
                        query = f"process_hash:{proc_hash} AND device_id:{device_id}"
                        proc_list = self.cbc.select(Process).where(query)
                        for proc in proc_list:
                            pid_list.extend(proc._info["process_pid"])
                    if proc_guid:
                        query = f"process_guid:{proc_guid} AND device_id:{device_id}"
                        proc_list = self.cbc.select(Process).where(query)
                        for proc in proc_list:
                            pid_list.extend(proc._info["process_pid"])

                    # Remove duplicate PIDs
                    pid_list = list(set(pid_list))
                    processes = lr_session.list_processes()
                    for process in processes:
                        # We have process name match, kill the process
                        if (
                            proc_name is not None
                            and proc_name in process["process_path"]
                            and process["process_pid"] not in pid_list
                        ):
                            self._kill_pid(
                                lr_session,
                                device_id,
                                process["process_pid"],
                                process["process_path"],
                            )
                        # We have match from pid_list, kill the PID and remove it from list
                        if process["process_pid"] in pid_list:
                            pid = process["process_pid"]
                            self._kill_pid(lr_session, device_id, pid, process["process_path"])
                            pid_list.remove(pid)
                    # If we have remaining PIDs in pid_list, declare them killed
                    for pid in pid_list:
                        data = {
                            "device_id": device_id,
                            "process_pid": pid,
                            "process_name": "N/A",
                            "process_killed": True,
                        }
                        self.action_result.add_data(data)
                # Exception due to List Processes on Device
                except Exception as e:
                    self.connector.error_print(traceback.format_exc())
                    result["success"] = False
                    result["details"] = "Could not kill process - {}".format(e)
                    return result
                result["success"], result["details"] = True, "Process(es) successfully killed"

            # Exception due to Device select error
            except Exception as e:
                self.connector.error_print(traceback.format_exc())
                result["details"] = "Could not kill process - {}".format(e)
        # No device ID provided
        else:
            result["details"] = "Missing device id."
        return result

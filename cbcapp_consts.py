# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Define your constants here"""
__version__ = "1.0"

STANDARD_CEF_MAPPING = {"action": ["act"],
                        "process_name": ["deviceProcessName", "dproc"],
                        "threat_cause_actor_process_pid": ["dpid"],
                        "device_id": ["deviceExternalId"],
                        "device_username": ["suser", "duser"],
                        "device_external_ip": ["src"],
                        "threat_cause_actor_sha256": ["fileHashSha256"],
                        "threat_cause_actor_name": ["sproc"],
                        "name": ["msg"],
                        "alertId": ["id"]
                        }

CEF_TYPES_MAPPING = {"_raw": ["cbc alert"],
                     "alertId": ["cbc alert id"],
                     "id": ["cbc alert id"],
                     "device_id": ["cbc device id"],
                     "deviceExternalId": ["cbc device id"],
                     "fileHashSha256": ["cbc process hash"],
                     "threat_cause_actor_sha256": ["cbc process hash"],
                     "sha256": ["cbc process hash"],
                     "threat_cause_process_guid": ["cbc process guid"],
                     "process_pid": ["pid"],
                     "process_name": ["process name"],
                     "process_path": ["process name"]
                     }

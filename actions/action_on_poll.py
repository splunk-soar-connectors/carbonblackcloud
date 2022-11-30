# VMware Carbon Black Cloud App for Splunk SOAR
# Copyright 2022 VMware, Inc.
#
# This product is licensed to you under the BSD-2 license (the "License").
# You may not use this product except in compliance with the BSD-2 License.
#
# This product may include a number of subcomponents with separate copyright notices and license terms.
# Your use of these subcomponents is subject to the terms and conditions
# of the subcomponent's license, as noted in the LICENSE file.
"""Data Ingestion Action Class"""
from actions import BaseAction
from utils.artifact_utils import prepare_artifact
import phantom.app as phantom
import datetime
from datetime import timezone
import traceback
from cbc_sdk.platform import BaseAlert


class OnPollAction(BaseAction):
    """Class to handle on poll action."""

    def call(self):
        """Execute on poll action."""
        result = self._poll_data()
        if result["success"]:
            status = phantom.APP_SUCCESS
        else:
            status = phantom.APP_ERROR

        self.connector.save_progress(result["details"])
        return self.action_result.set_status(status, result["details"])

    def _poll_data(self):
        """Ingest alerts and create artifact containers"""
        self.connector.debug_print("Polling data, params={}".format(self.param))
        start_time, end_time = self._phantom_daterange(self.param)
        self.connector.save_progress("Start fetching alerts")
        result = {"success": True, "details": ""}
        config = self.connector.get_config()

        if start_time is None or end_time is None:
            result["success"] = False
            result["details"] = "start time or end time not specified"
            return result
        else:
            container_limit = self.param.get("container_count", -1)
            artifact_limit = self.param.get("artifact_count", -1)
            alerts_limit = max(container_limit, artifact_limit)
            if alerts_limit > 0:
                self.connector.save_progress(
                    "Ingesting up to {} alerts from {} to {}".format(
                        alerts_limit, start_time, end_time
                    )
                )
            else:
                self.connector.save_progress(
                    "Ingesting alerts from {} to {}".format(str(start_time), str(end_time))
                )

            completed = False
            alerts_list = []
            cb_start_time = start_time.replace(tzinfo=timezone.utc).isoformat()
            cb_end_time = end_time.replace(tzinfo=timezone.utc).isoformat()
            while not completed:
                try:
                    alerts = (
                        self.cbc.select(BaseAlert)
                        .set_time_range("last_update_time", start=cb_start_time, end=cb_end_time)
                        .set_types(self._determine_alert_types())
                        .set_minimum_severity(config["min_severity"])
                    )
                    self.connector.debug_print("{} alerts found.".format(len(alerts)))
                except Exception as ex:
                    if "WATCHLIST alerts are not available" in str(ex):
                        result[
                            "details"
                        ] = "Failed: WATCHLIST alerts not available, please enable Enterprise EDR"
                    else:
                        result["details"] = "Failed: {}".format(ex)
                    self.connector.error_print("Failed: {}".format(traceback.format_exc()))
                    result["success"] = False
                    return result

                current_batch = list(alerts)
                diff = len(alerts_list) + len(current_batch) - alerts_limit

                if alerts_limit < 0 or diff <= 0:
                    alerts_list.extend(current_batch)
                else:
                    alerts_list.extend(current_batch[: (len(current_batch) - diff)])

                if len(alerts) < 10000:
                    completed = True
                else:
                    cb_start_time = alerts[-1]._info["last_update_time"]

            try:
                for alert in alerts_list:
                    try:
                        container = self._prepare_alert_container(alert._info)
                        status, message, container_id = self.connector.save_container(container)
                        container["id"] = container_id
                        self.connector.debug_print(
                            "Saved container {}/{}/{}".format(status, message, container_id)
                        )
                    except Exception:
                        self.connector.error_print(
                            "Error creating container: {}".format(traceback.format_exc())
                        )
                        self.connector.save_progress(
                            "Error creating container: {}".format(traceback.format_exc())
                        )
                    else:
                        if (
                            container
                            and status == phantom.APP_SUCCESS
                            and message != "Duplicate container found"
                        ):
                            artifact = prepare_artifact(
                                alert._info, config, container_id=container_id
                            )
                            self.connector.save_artifact(artifact)
                            self.connector.save_progress(
                                "Created container {} successfully".format(container_id)
                            )

                result["success"] = True
                result["details"] = "Polling complete. Found {} alerts.".format(len(alerts_list))

            except Exception:
                self.connector.error_print(
                    "Error fetching alerts: {}".format(traceback.format_exc())
                )
                result["success"] = False
                result["details"] = "Error fetching alerts from CBC: {}".format(
                    traceback.format_exc()
                )
            finally:
                return result

    def _determine_alert_types(self):
        """Get a list of alert types to poll from configuration"""
        config = self.connector.get_config()
        types = []
        if config["fetch_cb_analytics"]:
            types.append("CB_ANALYTICS")
        if config["fetch_device_control"]:
            types.append("DEVICE_CONTROL")
        if config["fetch_watchlist"]:
            types.append("WATCHLIST")
        if config["fetch_container_runtime"]:
            types.append("CONTAINER_RUNTIME")
        return types

    def _phantom_daterange(self, param):
        """
        Return datetime objects from start/end timestamps in param.

        Timestamps are in local time not UTC
        """
        try:
            start_time_param = float(param.get("start_time"))
            end_time_param = float(param.get("end_time"))
        except TypeError:
            self.connector.error_print("Start time or end time not specified")
            return None, None
        start = datetime.datetime.fromtimestamp(start_time_param / 1000.0)
        end = datetime.datetime.fromtimestamp(end_time_param / 1000.0)
        return start, end

    def _prepare_alert_container(self, alert):
        """Create an empty initial container for the alert artifact"""
        container = dict()
        config = self.connector.get_config()

        # Standard container fields go here:
        container["label"] = config["ingest"]["container_label"]
        container["name"] = alert["id"]
        container["custom_fields"] = dict()
        container["source_data_identifier"] = alert["id"]
        container["start_time"] = alert["create_time"]
        container["status"] = "new"
        container["ingest_app_id"] = self.connector.get_app_id()
        if "reason" in alert.keys():
            container["description"] = alert["reason"]
        elif "reason_code" in alert.keys():
            # Watchlist alerts have no reason field
            container["description"] = alert["reason_code"]
        else:
            container["description"] = ""

        # Custom container fields go here:
        container["custom_fields"]["alert_id"] = alert["id"]
        container["custom_fields"]["device_id"] = alert["device_id"]
        container["custom_fields"]["device_username"] = alert["device_username"]

        # Severity mapping (1-3:low, 4-6:medium, 7-10:high)
        if alert["severity"] < 4:
            container["severity"] = "low"
        elif alert["severity"] < 7:
            container["severity"] = "medium"
        else:
            container["severity"] = "high"
        return container

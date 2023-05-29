[comment]: # "Auto-generated SOAR connector documentation"
# Carbon Black Cloud

Publisher: VMware  
Connector Version: 1.0.1  
Product Vendor: VMware  
Product Name: Carbon Black Cloud  
Product Version Supported (regex): ".\*"  
Minimum Product Version: 5.5.0  

Carbon Black Cloud App for Splunk SOAR


## Requirements

This app requires Custom Type API Key for data inputs and SOAR Actions. Follow the steps [described
here](https://developer.carbonblack.com/reference/carbon-black-cloud/authentication/) to create API
Keys with the appropriate permissions to start pulling in Carbon Black Cloud data.

  

#### Set up Keys and Permissions in Carbon Black Cloud

Custom Type Credentials Note: For VMware Carbon Black Cloud customers who use VMware Cloud Services
Platform for Identity and Access Management, OAuth App Id and OAuth App Secret can be used.

1.  Open your Carbon Black Cloud console, go to Settings \> API Access, select "Access Levels" and
    click "Add Access Level".
2.  Fill in the "Name" and "Description" fields, grant the new Access Level with the following RBAC
    permissions and click Save.
    -   Alerts (org.alerts) - READ
    -   Alerts (org.alerts.dismiss) - EXECUTE
    -   Applications (org.reputations) - CREATE, DELETE
    -   Custom Detections (org.watchlists) - CREATE, READ, UPDATE, DELETE
    -   Custom Detections (org.feeds) - CREATE, READ, UPDATE, DELETE
    -   Device (device.quarantine) - EXECUTE
    -   Device (device) - READ
    -   Device (device.policy) - UPDATE
    -   Live Response File (org.liveresponse.file) - READ, DELETE
    -   Live Response Process (org.liveresponse.process) - EXECUTE, READ, DELETE
    -   Live Response Session (org.liveresponse.session) - CREATE, READ, DELETE
    -   Live Query (livequery.manage) - CREATE,READ,UPDATE,DELETE
    -   Policies (org.policies) - READ
    -   Search (org.search.events) - CREATE, READ
    -   Unified Binary Store (ubs.org.sha256) - READ
    -   Unified Binary Store (ubs.org.file) - READ
3.  Go to the "API Keys" tab and click "Add API Key".
4.  Enter a "Name", click on the "Access Level type" dropdown, select "Custom", click on the "Custom
    Access Level" dropdown and select the level you created in step 2, then click Save.
5.  Copy the API Secret Key and API ID from the pop-up modal.
6.  Copy Carbon Black Cloud console URL(including the "https://"), and ORG KEY.

## Configure the Carbon Black Cloud SOAR app Asset

1.  Open the Splunk SOAR console. Go to Apps \> Unconfigured Apps \> Carbon Black Cloud click
    Configure New Asset.
2.  Go to "Asset Info" Tab and enter "Asset name".
3.  Go to "Asset Settings" Tab and add Carbon Black Cloud instance URL, Carbon Black Cloud Org Key,
    API ID and API Secret Key to their respective fields. Click on the corresponding checkbox to
    enable fetching a specific type of alerts(CB_ANALYTICS alerts, DEVICE_CONTROL alerts, WATCHLIST
    alerts(requires Enterprise EDR), CONTAINER_RUNTIME alerts). Select minimum alerts severity.
4.  Go to "Ingest Settings" Tab and enable polling on the asset. Select a polling interval or
    schedule to configure polling on this asset. The suggested Polling interval is 3 minutes. Click
    Save.
5.  Go back to "Asset Settings" tab and click "Test Connectivity" to ensure successful connection.

## Port Information

The app uses HTTPS protocol for communicating with the Carbon Black Cloud instance. Below is the
default ports used by Splunk SOAR:

|         Service Name | Transport Protocol | Port |
|----------------------|--------------------|------|
|         http         | tcp                | 443  |


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a Carbon Black Cloud asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**cbc_url** |  required  | string | Carbon Black Cloud instance URL
**org_key** |  required  | string | Carbon Black Cloud Org Key
**api_id** |  required  | string | API ID
**api_secret_key** |  required  | password | API Secret Key
**fetch_cb_analytics** |  required  | boolean | Fetch CB_ANALYTICS alerts
**fetch_device_control** |  required  | boolean | Fetch DEVICE_CONTROL alerts
**fetch_watchlist** |  required  | boolean | Fetch WATCHLIST alerts (requires Enterprise EDR)
**fetch_container_runtime** |  required  | boolean | Fetch CONTAINER_RUNTIME alerts
**min_severity** |  required  | numeric | Minimum alerts severity

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity with the supplied configuration  
[on poll](#action-on-poll) - Callback action for the on_poll ingest functionality  
[normalize artifact](#action-normalize-artifact) - Normalize artifact ingested by Splunk App for Splunk Phantom  
[dismiss alert](#action-dismiss-alert) - Dismiss Carbon Black Cloud alert  
[dismiss future alerts](#action-dismiss-future-alerts) - Dismiss Carbon Black Cloud all future alerts  
[get enriched event](#action-get-enriched-event) - Get Enriched Event  
[get file](#action-get-file) - Get File  
[delete file](#action-delete-file) - Delete File  
[get binary file](#action-get-binary-file) - Get Binary File  
[kill process](#action-kill-process) - Kill process on Carbon Black Cloud endpoint  
[get binary metadata](#action-get-binary-metadata) - Get binary metadata from Carbon Black Cloud  
[get process metadata](#action-get-process-metadata) - Get Process Metadata  
[quarantine device](#action-quarantine-device) - Quarantine device in Carbon Black Cloud  
[unquarantine device](#action-unquarantine-device) - Unquarantine device in Carbon Black Cloud  
[ban hash](#action-ban-hash) - Ban process by hash in Carbon Black Cloud  
[unban hash](#action-unban-hash) - Unban process by hash in Carbon Black Cloud  
[list policies](#action-list-policies) - List device policies in Carbon Black Cloud  
[set device policy](#action-set-device-policy) - Set device policy of a Carbon Black Cloud endpoint  
[add ioc](#action-add-ioc) - Add IOC to feed/watchlist in Carbon Black Cloud  
[remove watchlist ioc](#action-remove-watchlist-ioc) - Remove IOC from watchlist in Carbon Black Cloud  
[remove feed ioc](#action-remove-feed-ioc) - Remove IOC from feed in Carbon Black Cloud  
[list processes](#action-list-processes) - List processes on a device in Carbon Black Cloud  
[execute command](#action-execute-command) - Execute command on a device in Carbon Black Cloud  
[create report](#action-create-report) - Create a report in Carbon Black Cloud  
[delete report](#action-delete-report) - Delete a report in Carbon Black Cloud feed or watchlist  
[create feed](#action-create-feed) - Create a feed in Carbon Black Cloud  
[create watchlist](#action-create-watchlist) - Create a watchlist in Carbon Black Cloud  
[delete feed](#action-delete-feed) - Delete a feed in Carbon Black Cloud  
[delete watchlist](#action-delete-watchlist) - Delete a watchlist in Carbon Black Cloud  
[retrieve watchlist](#action-retrieve-watchlist) - Retrieve a watchlist in Carbon Black Cloud  
[retrieve feed](#action-retrieve-feed) - Retrieve a feed in Carbon Black Cloud  
[retrieve iocs](#action-retrieve-iocs) - Retrieve IOCs for a given report in Carbon Black Cloud  
[update feed](#action-update-feed) - Update a feed in Carbon Black Cloud  
[update watchlist](#action-update-watchlist) - Update a watchlist in Carbon Black Cloud  
[get scheduled task](#action-get-scheduled-task) - Get Scheduled Task Created in Carbon Black Cloud  
[get asset info](#action-get-asset-info) - Get Asset Info  
[get cleared eventlogs](#action-get-cleared-eventlogs) - Get Cleared Event Logs  
[list persistence locations](#action-list-persistence-locations) - List Windows Persistence Locations  
[get rdp info](#action-get-rdp-info) - Get RDP Connection Information  
[list logged users](#action-list-logged-users) - List Logged In Users  

## action: 'test connectivity'
Validate the asset configuration for connectivity with the supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'on poll'
Callback action for the on_poll ingest functionality

Type: **ingest**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**container_id** |  optional  | Container IDs to limit the ingestion to | string | 
**start_time** |  optional  | Start of time range, in epoch time (milliseconds) | numeric | 
**end_time** |  optional  | End of time range, in epoch time (milliseconds) | numeric | 
**container_count** |  optional  | Maximum number of container records to query for. | numeric | 
**artifact_count** |  optional  | Maximum number of artifact records to query for. | numeric | 

#### Action Output
No Output  

## action: 'normalize artifact'
Normalize artifact ingested by Splunk App for Splunk Phantom

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**raw** |  optional  | Artifact _raw data | string |  `cbc alert` 
**artifact_id** |  optional  | Artifact ID to process | numeric |  `phantom artifact id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.parameter.artifact_id | string |  `phantom artifact id`  |  
action_result.summary | string |  |  
action_result.message | string |  |   Artifact updated successfully.   

## action: 'dismiss alert'
Dismiss Carbon Black Cloud alert

Type: **correct**  
Read only: **False**

Dismiss Alert in Carbon Black Cloud.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**alert_id** |  required  | Carbon Black Cloud Alert ID | string |  `cbc alert id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.alert_id | string |  |  
action_result.status | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.message | string |  |    

## action: 'dismiss future alerts'
Dismiss Carbon Black Cloud all future alerts

Type: **correct**  
Read only: **False**

Dismiss All Future Alerts in Carbon Black Cloud.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**alert_id** |  required  | Carbon Black Cloud Alert ID | string |  `cbc alert id` 
**remediation_status** |  optional  | Carbon Black Cloud remediation status to set for the alert | string | 
**comment** |  optional  | Carbon Black Cloud comment to set for the alert | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.message | string |  |    

## action: 'get enriched event'
Get Enriched Event

Type: **investigate**  
Read only: **False**

Get enriched event from Carbon Black Cloud.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**alert_id** |  required  | CBC Alert ID | string |  `cbc alert id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.details.event_id | string |  |  
action_result.data.\*.details.event_type | string |  |  
action_result.data.\*.details.event_description | string |  |  
action_result.data.\*.details.alert_id | string |  |  
action_result.data.\*.details.alert_category | string |  |  
action_result.data.\*.details.backend_timestamp | string |  |  
action_result.data.\*.details.device_id | string |  |  
action_result.data.\*.details.device_name | string |  |  
action_result.data.\*.details.device_os | string |  |  
action_result.data.\*.details.device_policy | string |  |  
action_result.data.\*.details.process_name | string |  |  
action_result.data.\*.details.process_hash | string |  |  
action_result.data.\*.details.parent_pid | string |  |  
action_result.data.\*.details.process_pid | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.status | string |  |  
action_result.message | string |  |    

## action: 'get file'
Get File

Type: **investigate**  
Read only: **True**

Get file From Carbon Black Cloud endpoint.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**device_id** |  required  | CBC Device ID | string |  `cbc device id` 
**file_name** |  required  | File Name | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.vault_id | string |  |  
action_result.data.\*.file_name | string |  |  
action_result.data.\*.device_id | string |  `cbc device id`  |  
action_result.status | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.message | string |  |    

## action: 'delete file'
Delete File

Type: **contain**  
Read only: **True**

Delete file from Carbon Black Cloud endpoint.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**device_id** |  required  | CBC Device ID | string |  `cbc device id` 
**file_name** |  required  | File Name | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.device_id | string |  |  
action_result.data.\*.file_name | string |  |  
action_result.status | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.message | string |  |    

## action: 'get binary file'
Get Binary File

Type: **investigate**  
Read only: **True**

Get binary file From Carbon Black Cloud endpoint.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**file_hash** |  required  | Binary file sha256 hash | string |  `cbc process hash` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.vault_id | string |  |  
action_result.data.\*.file_hash | string |  `cbc process hash`  |  
action_result.data.\*.file_name | string |  |  
action_result.status | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.message | string |  |    

## action: 'kill process'
Kill process on Carbon Black Cloud endpoint

Type: **contain**  
Read only: **False**

Kill process on a Carbon Black Cloud endpoint by PID, process name, process hash or GUID.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**device_id** |  required  | CBC Device ID | string |  `cbc device id` 
**process_pid** |  optional  | Process PID | numeric |  `pid` 
**process_name** |  optional  | Process Name | string |  `process name` 
**process_hash** |  optional  | Process Hash | string |  `cbc process hash` 
**process_guid** |  optional  | Process GUID | string |  `cbc process guid` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.process_pid | string |  `pid`  |  
action_result.data.\*.process_name | string |  `process name`  |  
action_result.data.\*.process_killed | boolean |  |  
action_result.status | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.message | string |  |    

## action: 'get binary metadata'
Get binary metadata from Carbon Black Cloud

Type: **investigate**  
Read only: **True**

Get binary metadata from Carbon Black Cloud.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**file_hash** |  required  | Binary file sha256 hash | string |  `cbc process hash` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.sha256 | string |  |  
action_result.data.\*.architecture | string |  |  
action_result.data.\*.available_file_size | string |  |  
action_result.data.\*.charset_id | string |  |  
action_result.data.\*.comments | string |  |  
action_result.data.\*.company_name | string |  |  
action_result.data.\*.copyright | string |  |  
action_result.data.\*.file_available | string |  |  
action_result.data.\*.file_description | string |  |  
action_result.data.\*.file_size | string |  |  
action_result.data.\*.file_version | string |  |  
action_result.data.\*.internal_name | string |  |  
action_result.data.\*.lang_id | string |  |  
action_result.data.\*.md5 | string |  |  
action_result.data.\*.original_filename | string |  |  
action_result.data.\*.os_type | string |  |  
action_result.data.\*.private_build | string |  |  
action_result.data.\*.product_description | string |  |  
action_result.data.\*.product_name | string |  |  
action_result.data.\*.product_version | string |  |  
action_result.data.\*.special_build | string |  |  
action_result.data.\*.trademark | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.status | string |  |  
action_result.message | string |  |    

## action: 'get process metadata'
Get Process Metadata

Type: **investigate**  
Read only: **True**

Get process metadata from Carbon Black Cloud.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**process_guid** |  required  | Process GUID | string |  `cbc process guid` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.details.process_name | string |  |  
action_result.data.\*.details.process_sha256 | string |  |  
action_result.data.\*.details.process_pid | string |  |  
action_result.data.\*.details.process_cmdline | string |  |  
action_result.data.\*.details.parent_pid | string |  |  
action_result.data.\*.details.alert_id | string |  |  
action_result.data.\*.details.alert_category | string |  |  
action_result.data.\*.details.backend_timestamp | string |  |  
action_result.data.\*.details.device_id | string |  |  
action_result.data.\*.details.device_name | string |  |  
action_result.data.\*.details.device_os | string |  |  
action_result.data.\*.details.device_policy | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.status | string |  |  
action_result.message | string |  |    

## action: 'quarantine device'
Quarantine device in Carbon Black Cloud

Type: **contain**  
Read only: **False**

Quarantine device in Carbon Black Cloud.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**device_id** |  required  | CBC Device ID | string |  `cbc device id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.device_id | string |  |  
action_result.status | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.message | string |  |    

## action: 'unquarantine device'
Unquarantine device in Carbon Black Cloud

Type: **contain**  
Read only: **False**

Unquarantine device in Carbon Black Cloud.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**device_id** |  required  | CBC Device ID | string |  `cbc device id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.device_id | string |  |  
action_result.status | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.message | string |  |    

## action: 'ban hash'
Ban process by hash in Carbon Black Cloud

Type: **contain**  
Read only: **False**

Ban process by hash in Carbon Black Cloud.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**process_hash** |  required  | CBC Process Hash | string |  `cbc process hash` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.process_hash | string |  |  
action_result.status | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.message | string |  |    

## action: 'unban hash'
Unban process by hash in Carbon Black Cloud

Type: **contain**  
Read only: **False**

Unban process by hash in Carbon Black Cloud.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**process_hash** |  required  | CBC Process Hash | string |  `cbc process hash` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.process_hash | string |  |  
action_result.status | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.message | string |  |    

## action: 'list policies'
List device policies in Carbon Black Cloud

Type: **investigate**  
Read only: **True**

List device policies in Carbon Black Cloud.

#### Action Parameters
No parameters are required for this action

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.id | numeric |  |  
action_result.data.\*.name | string |  |  
action_result.data.\*.description | string |  |  
action_result.data.\*.num_devices | string |  |  
action_result.data.\*.priority_level | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.status | string |  |  
action_result.message | string |  |    

## action: 'set device policy'
Set device policy of a Carbon Black Cloud endpoint

Type: **contain**  
Read only: **True**

Set device policy of a Carbon Black Cloud endpoint.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**device_id** |  required  | CBC Device ID | string |  `cbc device id` 
**policy_id** |  optional  | Policy ID | string | 
**policy_name** |  optional  | Policy Name | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.policy_id | string |  |  
action_result.data.\*.policy_name | string |  |  
action_result.data.\*.device_id | string |  |  
action_result.status | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.status | string |  |  
action_result.message | string |  |    

## action: 'add ioc'
Add IOC to feed/watchlist in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Add IOC to feed/watchlist in Carbon Black Cloud.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**feed_id** |  optional  | Feed ID | string | 
**watchlist_id** |  optional  | Watchlist ID | string | 
**report_id** |  required  | Report ID | string | 
**ioc_id** |  optional  | IOC ID | string | 
**cbc_field** |  required  | CBC IOC Field | string | 
**ioc_value** |  required  | CBC IOC Value | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |  
action_result.message | string |  |  
action_result.data.\*.ioc_id | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |    

## action: 'remove watchlist ioc'
Remove IOC from watchlist in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Remove IOC from watchlist in Carbon Black Cloud.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**watchlist_id** |  required  | Watchlist ID | string | 
**report_id** |  required  | Report ID | string | 
**ioc_id** |  optional  | IOC ID | string | 
**ioc_value** |  optional  | IOC Value | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.status | string |  |  
action_result.message | string |  |    

## action: 'remove feed ioc'
Remove IOC from feed in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Remove IOC from feed in Carbon Black Cloud.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**feed_id** |  required  | Feed ID | string | 
**report_id** |  required  | Report ID | string | 
**ioc_id** |  optional  | IOC ID | string | 
**ioc_value** |  optional  | IOC Value | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.status | string |  |  
action_result.message | string |  |    

## action: 'list processes'
List processes on a device in Carbon Black Cloud

Type: **investigate**  
Read only: **False**

List processes on a device in Carbon Black Cloud.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**device_id** |  required  | CBC Device ID | string |  `cbc device id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.process_pid | numeric |  `pid`  |  
action_result.data.\*.process_path | string |  `process name`  |  
action_result.data.\*.sid | string |  |  
action_result.data.\*.parent_pid | numeric |  `pid`  |  
action_result.data.\*.process_cmdline | string |  |  
action_result.data.\*.process_username | string |  |  
action_result.data.\*.process_create_time | numeric |  |  
action_result.data.\*.parent_create_time | numeric |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.status | string |  |  
action_result.message | string |  |    

## action: 'execute command'
Execute command on a device in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Execute command on a device in Carbon Black Cloud.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**device_id** |  required  | CBC Device ID | string |  `cbc device id` 
**command_line** |  required  | Command Line | string | 
**timeout** |  optional  | Execution timeout (seconds) | numeric | 
**work_dir** |  optional  | Working directory | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.device_id | string |  |  
action_result.data.\*.command_line | string |  |  
action_result.data.\*.stdout | string |  |  
action_result.status | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.message | string |  |    

## action: 'create report'
Create a report in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Create a report in Carbon Black Cloud.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**feed_id** |  optional  | Feed ID | string | 
**report_save_as_watchlist** |  optional  | Save as a Watchlist Report | boolean | 
**report_name** |  required  | Report Name | string | 
**report_severity** |  required  | Report Severity | numeric | 
**report_summary** |  required  | Report Summary | string | 
**report_tags** |  optional  | Comma Separated Report Tags | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |  
action_result.message | string |  |  
action_result.data.\*.id | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |    

## action: 'delete report'
Delete a report in Carbon Black Cloud feed or watchlist

Type: **correct**  
Read only: **True**

Delete a report in Carbon Black Cloud feed or watchlist.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**report_id** |  required  | Report ID | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |  
action_result.message | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |    

## action: 'create feed'
Create a feed in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Create a feed in Carbon Black Cloud.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**feed_name** |  required  | Feed Name | string | 
**feed_provider_url** |  required  | Feed Provider URL | string | 
**feed_summary** |  required  | Feed Summary | string | 
**feed_category** |  required  | Feed Category | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |  
action_result.message | string |  |  
action_result.data.\*.id | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |    

## action: 'create watchlist'
Create a watchlist in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Create a watchlist in Carbon Black Cloud.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**watchlist_name** |  required  | Watchlist Name | string | 
**watchlist_description** |  optional  | Description | string | 
**watchlist_tags_enabled** |  optional  | Enable Tags | boolean | 
**watchlist_alerts_enabled** |  optional  | Enable Alerts | boolean | 
**watchlist_report_ids** |  optional  | Report IDs (CSV) | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |  
action_result.message | string |  |  
action_result.data.\*.id | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |    

## action: 'delete feed'
Delete a feed in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Delete a feed in Carbon Black Cloud.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**feed_id** |  required  | Feed ID | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |  
action_result.message | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |    

## action: 'delete watchlist'
Delete a watchlist in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Delete a watchlist in Carbon Black Cloud.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**watchlist_id** |  required  | Watchlist ID | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |  
action_result.message | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |    

## action: 'retrieve watchlist'
Retrieve a watchlist in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Retrieve a watchlist in Carbon Black Cloud.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**watchlist_id** |  required  | Watchlist ID | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.id | string |  |  
action_result.data.\*.name | string |  |  
action_result.data.\*.description | string |  |  
action_result.data.\*.tags_enabled | string |  |  
action_result.data.\*.alerts_enabled | string |  |  
action_result.data.\*.create_timestamp | string |  |  
action_result.data.\*.last_update_timestamp | string |  |  
action_result.data.\*.report_ids | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.status | string |  |  
action_result.message | string |  |    

## action: 'retrieve feed'
Retrieve a feed in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Retrieve a feed in Carbon Black Cloud.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**feed_id** |  required  | Feed ID | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.id | string |  |  
action_result.data.\*.name | string |  |  
action_result.data.\*.access | string |  |  
action_result.data.\*.summary | string |  |  
action_result.data.\*.category | string |  |  
action_result.data.\*.provider_url | string |  |  
action_result.data.\*.reports_count | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.status | string |  |  
action_result.message | string |  |    

## action: 'retrieve iocs'
Retrieve IOCs for a given report in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Retrieve IOCs for a given report in Carbon Black Cloud.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**watchlist_id** |  optional  | Watchlist ID | string | 
**feed_id** |  optional  | Feed ID | string | 
**report_id** |  required  | Report ID | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.id | string |  |  
action_result.data.\*.match_type | string |  |  
action_result.data.\*.field | string |  |  
action_result.data.\*.values | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.status | string |  |  
action_result.message | string |  |    

## action: 'update feed'
Update a feed in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Update a feed in Carbon Black Cloud.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**feed_id** |  required  | Feed ID | string | 
**feed_name** |  required  | Feed Name | string | 
**feed_provider_url** |  required  | Feed Provider URL | string | 
**feed_summary** |  required  | Feed Summary | string | 
**feed_category** |  required  | Feed Category | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |  
action_result.message | string |  |  
action_result.data.\*.id | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |    

## action: 'update watchlist'
Update a watchlist in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Update a watchlist in Carbon Black Cloud.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**watchlist_id** |  required  | Watchlist ID | string | 
**watchlist_name** |  required  | Watchlist Name | string | 
**watchlist_description** |  optional  | Description | string | 
**watchlist_tags_enabled** |  optional  | Enable Tags | boolean | 
**watchlist_alerts_enabled** |  optional  | Enable Alerts | boolean | 
**add_report_ids** |  optional  | Comma Separated Report IDs | string | 
**remove_report_ids** |  optional  | Comma Separated Report IDs | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |  
action_result.message | string |  |  
action_result.data.\*.id | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |    

## action: 'get scheduled task'
Get Scheduled Task Created in Carbon Black Cloud

Type: **investigate**  
Read only: **True**

Get Scheduled Task Created in Carbon Black Cloud.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**device_id** |  required  | CBC Device ID | string |  `cbc device id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.event_channel | string |  |  
action_result.data.\*.datetime | string |  |  
action_result.data.\*.task | string |  |  
action_result.data.\*.severity | numeric |  |  
action_result.data.\*.provider_name | string |  |  
action_result.data.\*.provider_guid | string |  |  
action_result.data.\*.host | string |  |  
action_result.data.\*.event_id | numeric |  |  
action_result.data.\*.keywords | string |  |  
action_result.data.\*.data | string |  |  
action_result.data.\*.process_pid | numeric |  |  
action_result.data.\*.thread_id | numeric |  |  
action_result.data.\*.time_range | string |  |  
action_result.data.\*.timestamp | string |  |  
action_result.data.\*.xpath | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.status | string |  |  
action_result.message | string |  |    

## action: 'get asset info'
Get Asset Info

Type: **investigate**  
Read only: **True**

Get asset info.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**device_id** |  required  | CBC Device ID | string |  `cbc device id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.id | string |  |  
action_result.data.\*.name | string |  |  
action_result.data.\*.os_version | string |  |  
action_result.data.\*.last_internal_ip_address | string |  |  
action_result.data.\*.last_external_ip_address | string |  |  
action_result.data.\*.status | string |  |  
action_result.data.\*.last_contact_time | string |  |  
action_result.data.\*.sensor_version | string |  |  
action_result.data.\*.sensor_states | string |  |  
action_result.status | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.status | string |  |  
action_result.message | string |  |    

## action: 'get cleared eventlogs'
Get Cleared Event Logs

Type: **investigate**  
Read only: **False**

Get cleared event logs from Carbon Black Cloud LiveQuery.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**device_id** |  required  | Device ID | string |  `cbc device id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.datetime | string |  |  
action_result.data.\*.domain | string |  |  
action_result.data.\*.user | string |  |  
action_result.data.\*.sid | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.status | string |  |  
action_result.message | string |  |    

## action: 'list persistence locations'
List Windows Persistence Locations

Type: **investigate**  
Read only: **True**

List Windows Persistence Locations.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**device_id** |  required  | CBC Device ID | string |  `cbc device id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.path | string |  |  
action_result.data.\*.name | string |  |  
action_result.data.\*.source | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.status | string |  |  
action_result.message | string |  |    

## action: 'get rdp info'
Get RDP Connection Information

Type: **investigate**  
Read only: **False**

Get RDP Connection Information from Carbon Black Cloud LiveQuery.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**device_id** |  required  | Device ID | string |  `cbc device id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.process_pid | string |  |  
action_result.data.\*.process_name | string |  |  
action_result.data.\*.process_cmdline | string |  |  
action_result.data.\*.local_address | string |  |  
action_result.data.\*.remote_address | string |  |  
action_result.data.\*.local_port | string |  |  
action_result.data.\*.remote_port | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.status | string |  |  
action_result.message | string |  |    

## action: 'list logged users'
List Logged In Users

Type: **investigate**  
Read only: **False**

List Logged In Users from Carbon Black Cloud LiveQuery.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**device_id** |  required  | Device ID | string |  `cbc device id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.login_type | string |  |  
action_result.data.\*.user | string |  |  
action_result.data.\*.device_name | string |  |  
action_result.data.\*.host | string |  |  
action_result.data.\*.time | string |  |  
action_result.data.\*.process_pid | string |  |  
action_result.data.\*.sid | string |  |  
action_result.data.\*.registry_hive | string |  |  
action_result.data.\*.process_name | string |  |  
action_result.data.\*.cmdline | string |  |  
summary.total_objects_successful | numeric |  |  
summary.total_objects | numeric |  |  
action_result.status | string |  |  
action_result.message | string |  |  
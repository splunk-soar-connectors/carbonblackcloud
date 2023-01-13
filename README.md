[comment]: # "Auto-generated SOAR connector documentation"
# Carbon Black Cloud

Publisher: VMware  
Connector Version: 1\.0\.1  
Product Vendor: VMware  
Product Name: Carbon Black Cloud  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 5\.3\.0  

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
**cbc\_url** |  required  | string | Carbon Black Cloud instance URL
**org\_key** |  required  | string | Carbon Black Cloud Org Key
**api\_id** |  required  | string | API ID
**api\_secret\_key** |  required  | password | API Secret Key
**fetch\_cb\_analytics** |  required  | boolean | Fetch CB\_ANALYTICS alerts
**fetch\_device\_control** |  required  | boolean | Fetch DEVICE\_CONTROL alerts
**fetch\_watchlist** |  required  | boolean | Fetch WATCHLIST alerts \(requires Enterprise EDR\)
**fetch\_container\_runtime** |  required  | boolean | Fetch CONTAINER\_RUNTIME alerts
**min\_severity** |  required  | numeric | Minimum alerts severity

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity with the supplied configuration  
[on poll](#action-on-poll) - Callback action for the on\_poll ingest functionality  
[normalize artifact](#action-normalize-artifact) - Normalize artifact ingested by Splunk App for Splunk Phantom  
[dismiss alert](#action-dismiss-alert) - Dismiss Carbon Black Cloud alert  
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

## action: 'test connectivity'
Validate the asset configuration for connectivity with the supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'on poll'
Callback action for the on\_poll ingest functionality

Type: **ingest**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**container\_id** |  optional  | Container IDs to limit the ingestion to | string | 
**start\_time** |  optional  | Start of time range, in epoch time \(milliseconds\) | numeric | 
**end\_time** |  optional  | End of time range, in epoch time \(milliseconds\) | numeric | 
**container\_count** |  optional  | Maximum number of container records to query for\. | numeric | 
**artifact\_count** |  optional  | Maximum number of artifact records to query for\. | numeric | 

#### Action Output
No Output  

## action: 'normalize artifact'
Normalize artifact ingested by Splunk App for Splunk Phantom

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**raw** |  optional  | Artifact \_raw data | string |  `cbc alert` 
**artifact\_id** |  optional  | Artifact ID to process | numeric |  `phantom artifact id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric | 
action\_result\.parameter\.artifact\_id | string |  `phantom artifact id` 
action\_result\.summary | string | 
action\_result\.message | string |   

## action: 'dismiss alert'
Dismiss Carbon Black Cloud alert

Type: **correct**  
Read only: **False**

Dismiss Alert in Carbon Black Cloud\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**alert\_id** |  required  | Carbon Black Cloud Alert ID | string |  `cbc alert id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.alert\_id | string | 
action\_result\.status | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric | 
action\_result\.message | string |   

## action: 'get enriched event'
Get Enriched Event

Type: **investigate**  
Read only: **False**

Get enriched event from Carbon Black Cloud\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**alert\_id** |  required  | CBC Alert ID | string |  `cbc alert id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.details\.event\_id | string | 
action\_result\.data\.\*\.details\.event\_type | string | 
action\_result\.data\.\*\.details\.event\_description | string | 
action\_result\.data\.\*\.details\.alert\_id | string | 
action\_result\.data\.\*\.details\.alert\_category | string | 
action\_result\.data\.\*\.details\.backend\_timestamp | string | 
action\_result\.data\.\*\.details\.device\_id | string | 
action\_result\.data\.\*\.details\.device\_name | string | 
action\_result\.data\.\*\.details\.device\_os | string | 
action\_result\.data\.\*\.details\.device\_policy | string | 
action\_result\.data\.\*\.details\.process\_name | string | 
action\_result\.data\.\*\.details\.process\_hash | string | 
action\_result\.data\.\*\.details\.parent\_pid | string | 
action\_result\.data\.\*\.details\.process\_pid | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric | 
action\_result\.status | string | 
action\_result\.message | string |   

## action: 'get file'
Get File

Type: **investigate**  
Read only: **True**

Get file From Carbon Black Cloud endpoint\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**device\_id** |  required  | CBC Device ID | string |  `cbc device id` 
**file\_name** |  required  | File Name | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.vault\_id | string | 
action\_result\.data\.\*\.file\_name | string | 
action\_result\.data\.\*\.device\_id | string |  `cbc device id` 
action\_result\.status | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric | 
action\_result\.message | string |   

## action: 'delete file'
Delete File

Type: **contain**  
Read only: **True**

Delete file from Carbon Black Cloud endpoint\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**device\_id** |  required  | CBC Device ID | string |  `cbc device id` 
**file\_name** |  required  | File Name | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.device\_id | string | 
action\_result\.data\.\*\.file\_name | string | 
action\_result\.status | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric | 
action\_result\.message | string |   

## action: 'get binary file'
Get Binary File

Type: **investigate**  
Read only: **True**

Get binary file From Carbon Black Cloud endpoint\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**file\_hash** |  required  | Binary file sha256 hash | string |  `cbc process hash` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.vault\_id | string | 
action\_result\.data\.\*\.file\_hash | string |  `cbc process hash` 
action\_result\.data\.\*\.file\_name | string | 
action\_result\.status | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric | 
action\_result\.message | string |   

## action: 'kill process'
Kill process on Carbon Black Cloud endpoint

Type: **contain**  
Read only: **False**

Kill process on a Carbon Black Cloud endpoint by PID, process name, process hash or GUID\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**device\_id** |  required  | CBC Device ID | string |  `cbc device id` 
**process\_pid** |  optional  | Process PID | numeric |  `pid` 
**process\_name** |  optional  | Process Name | string |  `process name` 
**process\_hash** |  optional  | Process Hash | string |  `cbc process hash` 
**process\_guid** |  optional  | Process GUID | string |  `cbc process guid` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.process\_pid | string |  `pid` 
action\_result\.data\.\*\.process\_name | string |  `process name` 
action\_result\.data\.\*\.process\_killed | boolean | 
action\_result\.status | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric | 
action\_result\.message | string |   

## action: 'get binary metadata'
Get binary metadata from Carbon Black Cloud

Type: **investigate**  
Read only: **True**

Get binary metadata from Carbon Black Cloud\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**file\_hash** |  required  | Binary file sha256 hash | string |  `cbc process hash` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.sha256 | string | 
action\_result\.data\.\*\.architecture | string | 
action\_result\.data\.\*\.available\_file\_size | string | 
action\_result\.data\.\*\.charset\_id | string | 
action\_result\.data\.\*\.comments | string | 
action\_result\.data\.\*\.company\_name | string | 
action\_result\.data\.\*\.copyright | string | 
action\_result\.data\.\*\.file\_available | string | 
action\_result\.data\.\*\.file\_description | string | 
action\_result\.data\.\*\.file\_size | string | 
action\_result\.data\.\*\.file\_version | string | 
action\_result\.data\.\*\.internal\_name | string | 
action\_result\.data\.\*\.lang\_id | string | 
action\_result\.data\.\*\.md5 | string | 
action\_result\.data\.\*\.original\_filename | string | 
action\_result\.data\.\*\.os\_type | string | 
action\_result\.data\.\*\.private\_build | string | 
action\_result\.data\.\*\.product\_description | string | 
action\_result\.data\.\*\.product\_name | string | 
action\_result\.data\.\*\.product\_version | string | 
action\_result\.data\.\*\.special\_build | string | 
action\_result\.data\.\*\.trademark | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric | 
action\_result\.status | string | 
action\_result\.message | string |   

## action: 'get process metadata'
Get Process Metadata

Type: **investigate**  
Read only: **True**

Get process metadata from Carbon Black Cloud\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**process\_guid** |  required  | Process GUID | string |  `cbc process guid` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.details\.process\_name | string | 
action\_result\.data\.\*\.details\.process\_sha256 | string | 
action\_result\.data\.\*\.details\.process\_pid | string | 
action\_result\.data\.\*\.details\.process\_cmdline | string | 
action\_result\.data\.\*\.details\.parent\_pid | string | 
action\_result\.data\.\*\.details\.alert\_id | string | 
action\_result\.data\.\*\.details\.alert\_category | string | 
action\_result\.data\.\*\.details\.backend\_timestamp | string | 
action\_result\.data\.\*\.details\.device\_id | string | 
action\_result\.data\.\*\.details\.device\_name | string | 
action\_result\.data\.\*\.details\.device\_os | string | 
action\_result\.data\.\*\.details\.device\_policy | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric | 
action\_result\.status | string | 
action\_result\.message | string |   

## action: 'quarantine device'
Quarantine device in Carbon Black Cloud

Type: **contain**  
Read only: **False**

Quarantine device in Carbon Black Cloud\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**device\_id** |  required  | CBC Device ID | string |  `cbc device id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.device\_id | string | 
action\_result\.status | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric | 
action\_result\.message | string |   

## action: 'unquarantine device'
Unquarantine device in Carbon Black Cloud

Type: **contain**  
Read only: **False**

Unquarantine device in Carbon Black Cloud\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**device\_id** |  required  | CBC Device ID | string |  `cbc device id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.device\_id | string | 
action\_result\.status | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric | 
action\_result\.message | string |   

## action: 'ban hash'
Ban process by hash in Carbon Black Cloud

Type: **contain**  
Read only: **False**

Ban process by hash in Carbon Black Cloud\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**process\_hash** |  required  | CBC Process Hash | string |  `cbc process hash` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.process\_hash | string | 
action\_result\.status | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric | 
action\_result\.message | string |   

## action: 'unban hash'
Unban process by hash in Carbon Black Cloud

Type: **contain**  
Read only: **False**

Unban process by hash in Carbon Black Cloud\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**process\_hash** |  required  | CBC Process Hash | string |  `cbc process hash` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.process\_hash | string | 
action\_result\.status | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric | 
action\_result\.message | string |   

## action: 'list policies'
List device policies in Carbon Black Cloud

Type: **investigate**  
Read only: **True**

List device policies in Carbon Black Cloud\.

#### Action Parameters
No parameters are required for this action

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.id | numeric | 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.description | string | 
action\_result\.data\.\*\.num\_devices | string | 
action\_result\.data\.\*\.priority\_level | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric | 
action\_result\.status | string | 
action\_result\.message | string |   

## action: 'set device policy'
Set device policy of a Carbon Black Cloud endpoint

Type: **contain**  
Read only: **True**

Set device policy of a Carbon Black Cloud endpoint\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**device\_id** |  required  | CBC Device ID | string |  `cbc device id` 
**policy\_id** |  optional  | Policy ID | string | 
**policy\_name** |  optional  | Policy Name | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.policy\_id | string | 
action\_result\.data\.\*\.policy\_name | string | 
action\_result\.data\.\*\.device\_id | string | 
action\_result\.status | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric | 
action\_result\.status | string | 
action\_result\.message | string |   

## action: 'add ioc'
Add IOC to feed/watchlist in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Add IOC to feed/watchlist in Carbon Black Cloud\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**feed\_id** |  optional  | Feed ID | string | 
**watchlist\_id** |  optional  | Watchlist ID | string | 
**report\_id** |  required  | Report ID | string | 
**ioc\_id** |  optional  | IOC ID | string | 
**cbc\_field** |  required  | CBC IOC Field | string | 
**ioc\_value** |  required  | CBC IOC Value | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.data\.\*\.ioc\_id | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric |   

## action: 'remove watchlist ioc'
Remove IOC from watchlist in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Remove IOC from watchlist in Carbon Black Cloud\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**watchlist\_id** |  required  | Watchlist ID | string | 
**report\_id** |  required  | Report ID | string | 
**ioc\_id** |  optional  | IOC ID | string | 
**ioc\_value** |  optional  | IOC Value | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric | 
action\_result\.status | string | 
action\_result\.message | string |   

## action: 'remove feed ioc'
Remove IOC from feed in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Remove IOC from feed in Carbon Black Cloud\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**feed\_id** |  required  | Feed ID | string | 
**report\_id** |  required  | Report ID | string | 
**ioc\_id** |  optional  | IOC ID | string | 
**ioc\_value** |  optional  | IOC Value | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric | 
action\_result\.status | string | 
action\_result\.message | string |   

## action: 'list processes'
List processes on a device in Carbon Black Cloud

Type: **investigate**  
Read only: **False**

List processes on a device in Carbon Black Cloud\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**device\_id** |  required  | CBC Device ID | string |  `cbc device id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.process\_pid | numeric |  `pid` 
action\_result\.data\.\*\.process\_path | string |  `process name` 
action\_result\.data\.\*\.sid | string | 
action\_result\.data\.\*\.parent\_pid | numeric |  `pid` 
action\_result\.data\.\*\.process\_cmdline | string | 
action\_result\.data\.\*\.process\_username | string | 
action\_result\.data\.\*\.process\_create\_time | numeric | 
action\_result\.data\.\*\.parent\_create\_time | numeric | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric | 
action\_result\.status | string | 
action\_result\.message | string |   

## action: 'execute command'
Execute command on a device in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Execute command on a device in Carbon Black Cloud\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**device\_id** |  required  | CBC Device ID | string |  `cbc device id` 
**command\_line** |  required  | Command Line | string | 
**timeout** |  optional  | Execution timeout \(seconds\) | numeric | 
**work\_dir** |  optional  | Working directory | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.device\_id | string | 
action\_result\.data\.\*\.command\_line | string | 
action\_result\.data\.\*\.stdout | string | 
action\_result\.status | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric | 
action\_result\.message | string |   

## action: 'create report'
Create a report in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Create a report in Carbon Black Cloud\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**feed\_id** |  optional  | Feed ID | string | 
**report\_save\_as\_watchlist** |  optional  | Save as a Watchlist Report | boolean | 
**report\_name** |  required  | Report Name | string | 
**report\_severity** |  required  | Report Severity | numeric | 
**report\_summary** |  required  | Report Summary | string | 
**report\_tags** |  optional  | Comma Separated Report Tags | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.data\.\*\.id | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric |   

## action: 'delete report'
Delete a report in Carbon Black Cloud feed or watchlist

Type: **correct**  
Read only: **True**

Delete a report in Carbon Black Cloud feed or watchlist\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**report\_id** |  required  | Report ID | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.message | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric |   

## action: 'create feed'
Create a feed in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Create a feed in Carbon Black Cloud\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**feed\_name** |  required  | Feed Name | string | 
**feed\_provider\_url** |  required  | Feed Provider URL | string | 
**feed\_summary** |  required  | Feed Summary | string | 
**feed\_category** |  required  | Feed Category | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.data\.\*\.id | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric |   

## action: 'create watchlist'
Create a watchlist in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Create a watchlist in Carbon Black Cloud\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**watchlist\_name** |  required  | Watchlist Name | string | 
**watchlist\_description** |  optional  | Description | string | 
**watchlist\_tags\_enabled** |  optional  | Enable Tags | boolean | 
**watchlist\_alerts\_enabled** |  optional  | Enable Alerts | boolean | 
**watchlist\_report\_ids** |  optional  | Report IDs \(CSV\) | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.data\.\*\.id | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric |   

## action: 'delete feed'
Delete a feed in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Delete a feed in Carbon Black Cloud\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**feed\_id** |  required  | Feed ID | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.message | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric |   

## action: 'delete watchlist'
Delete a watchlist in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Delete a watchlist in Carbon Black Cloud\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**watchlist\_id** |  required  | Watchlist ID | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.message | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric |   

## action: 'retrieve watchlist'
Retrieve a watchlist in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Retrieve a watchlist in Carbon Black Cloud\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**watchlist\_id** |  required  | Watchlist ID | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.id | string | 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.description | string | 
action\_result\.data\.\*\.tags\_enabled | string | 
action\_result\.data\.\*\.alerts\_enabled | string | 
action\_result\.data\.\*\.create\_timestamp | string | 
action\_result\.data\.\*\.last\_update\_timestamp | string | 
action\_result\.data\.\*\.report\_ids | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric | 
action\_result\.status | string | 
action\_result\.message | string |   

## action: 'retrieve feed'
Retrieve a feed in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Retrieve a feed in Carbon Black Cloud\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**feed\_id** |  required  | Feed ID | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.id | string | 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.access | string | 
action\_result\.data\.\*\.summary | string | 
action\_result\.data\.\*\.category | string | 
action\_result\.data\.\*\.provider\_url | string | 
action\_result\.data\.\*\.reports\_count | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric | 
action\_result\.status | string | 
action\_result\.message | string |   

## action: 'retrieve iocs'
Retrieve IOCs for a given report in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Retrieve IOCs for a given report in Carbon Black Cloud\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**watchlist\_id** |  optional  | Watchlist ID | string | 
**feed\_id** |  optional  | Feed ID | string | 
**report\_id** |  required  | Report ID | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.id | string | 
action\_result\.data\.\*\.match\_type | string | 
action\_result\.data\.\*\.field | string | 
action\_result\.data\.\*\.values | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric | 
action\_result\.status | string | 
action\_result\.message | string |   

## action: 'update feed'
Update a feed in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Update a feed in Carbon Black Cloud\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**feed\_id** |  required  | Feed ID | string | 
**feed\_name** |  required  | Feed Name | string | 
**feed\_provider\_url** |  required  | Feed Provider URL | string | 
**feed\_summary** |  required  | Feed Summary | string | 
**feed\_category** |  required  | Feed Category | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.data\.\*\.id | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric |   

## action: 'update watchlist'
Update a watchlist in Carbon Black Cloud

Type: **contain**  
Read only: **True**

Update a watchlist in Carbon Black Cloud\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**watchlist\_id** |  required  | Watchlist ID | string | 
**watchlist\_name** |  required  | Watchlist Name | string | 
**watchlist\_description** |  optional  | Description | string | 
**watchlist\_tags\_enabled** |  optional  | Enable Tags | boolean | 
**watchlist\_alerts\_enabled** |  optional  | Enable Alerts | boolean | 
**add\_report\_ids** |  optional  | Comma Separated Report IDs | string | 
**remove\_report\_ids** |  optional  | Comma Separated Report IDs | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.data\.\*\.id | string | 
summary\.total\_objects\_successful | numeric | 
summary\.total\_objects | numeric | 

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
    -   Alerts (org.alerts.close) - EXECUTE
    -   Applications (org.reputations) - CREATE, DELETE
    -   Background Tasks (jobs.status) - READ
    -   Custom Detections (org.watchlists) - CREATE, READ, UPDATE, DELETE
    -   Custom Detections (org.feeds) - CREATE, READ, UPDATE, DELETE
    -   Device (device.quarantine) - EXECUTE
    -   Device (device) - READ
    -   Device (device.policy) - UPDATE
    -   Live Response File (org.liveresponse.file) - READ, DELETE
    -   Live Response Process (org.liveresponse.process) - EXECUTE, READ, DELETE
    -   Live Response Session (org.liveresponse.session) - CREATE, READ, DELETE
    -   Live Query (livequery.manage) - CREATE, READ, UPDATE, DELETE
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
    alerts(requires Enterprise EDR), CONTAINER_RUNTIME alerts, HOST_BASED_FIREWALL alerts, INTRUSION_DETECTION_SYSTEM (requires Enterprise EDR) alerts). Select minimum alerts severity.
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

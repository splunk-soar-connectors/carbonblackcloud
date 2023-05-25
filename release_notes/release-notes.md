## Version 1.1.0

- New actions that operate on Carbon Black Cloud objects:
    - `dismiss future alerts` - Dismiss all future Carbon Black Cloud alerts
    - `get asset info` - Get Asset Info
    - `get cleared eventlogs` - Get Cleared Event Logs
    - `get rdp info` - Get RDP Connection Information
    - `get scheduled task` - Get Scheduled Task Created in Carbon Black Cloud
    - `list logged users` - List Logged In Users from Carbon Black Cloud LiveQuery
    - `list persistence locations` - List Windows Persistence Locations


## Version 1.0.1

- Carbon Black Cloud Alerts ingestion via the REST API:
    - Configurable alert types
    - Configurable minimum alert severity
    - Proxy support (via either global or per-asset **HTTPS_PROXY** environment variable)
- A number of actions that operate on Carbon Black Cloud objects:
    - `update watchlist` - Update a watchlist in Carbon Black Cloud
    - `update feed` - Update a feed in Carbon Black Cloud
    - `retrieve iocs` - Retrieve IOCs for a given report in Carbon Black Cloud
    - `retrieve feed` - Retrieve a feed in Carbon Black Cloud
    - `retrieve watchlist` - Retrieve a watchlist in Carbon Black Cloud
    - `delete watchlist` - Delete a watchlist in Carbon Black Cloud
    - `delete feed` - Delete a feed in Carbon Black Cloud
    - `create watchlist` - Create a watchlist in Carbon Black Cloud
    - `create feed` - Create a feed in Carbon Black Cloud
    - `delete report` - Delete a report in Carbon Black Cloud feed or watchlist
    - `create report` - Create a report in Carbon Black Cloud
    - `execute command` - Execute command on a device in Carbon Black Cloud
    - `list processes` - List processes on a device in Carbon Black Cloud
    - `remove feed ioc` - Remove IOC from feed in Carbon Black Cloud
    - `remove watchlist ioc` - Remove IOC from watchlist in Carbon Black Cloud
    - `add ioc` - Add IOC to feed/watchlist in Carbon Black Cloud
    - `set device policy` - Set device policy of a Carbon Black Cloud endpoint
    - `list policies` - List device policies in Carbon Black Cloud
    - `unban hash` - Unban process by hash in Carbon Black Cloud
    - `ban hash` - Ban process by hash in Carbon Black Cloud
    - `unquarantine device` - Unquarantine device in Carbon Black Cloud
    - `quarantine device` - Quarantine device in Carbon Black Cloud
    - `get process metadata` - Get Process Metadata
    - `get binary metadata` - Get binary metadata from Carbon Black Cloud
    - `kill process` - Kill process on Carbon Black Cloud endpoint
    - `get binary file` - Get Binary File
    - `delete file` - Delete File
    - `get file` - Get File
    - `get enriched event` - Get Enriched Event
    - `dismiss alert` - Dismiss Carbon Black Cloud alert
- The `normalize artifact` action to normalize artifacts ingested by the Splunk App for Splunk SOAR
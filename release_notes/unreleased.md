* New Features:
	* Migration from Alerts v6 to Alerts v7.
	* New actions that operate on Carbon Black Cloud objects:
		* get cron jobs - Get Cron Jobs in Carbon Black Cloud
		* get observations - Get Observations
	* Updated action:
		* get scheduled task - Get Scheduled Task Created in Carbon Black Cloud
	* Decommissioned action:
		* get enriched event - Get Enriched Event
	* Added two new types of alerts (INTRUSION_DETECTION_SYSTEM and HOST_BASED_FIREWALL) to ingest.
* Breaking Changes:
	* Alerts ingest has been changed to Alert API v7. Some fields in the earlier versions have been renamed or removed from the new versions.
	* An additional permission is needed to close alerts: Background Tasks - jobs.status - READ).
	* The Alert Action get enriched event has been deprecated and will be deactivated July 31, 2024 . The action get observations has been added and can enrich more Alert types.
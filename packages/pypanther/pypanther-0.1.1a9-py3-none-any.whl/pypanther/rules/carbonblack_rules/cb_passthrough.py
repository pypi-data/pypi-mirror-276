from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.log_types import LogType

carbon_black_alert_v2_passthrough_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="True Positive",
        ExpectedResult=True,
        Log={
            "p_log_type": "CarbonBlack.AlertV2",
            "alert_notes_present": False,
            "alert_url": "https://d5.carbonblack.net/alerts?orgKey=ABCD1234&s%5Bc%5D%5Bquery_string%5D=id%3A9728f0c8-7810-fb20-15d0-343031500435",
            "attack_tactic": "TA0002",
            "backend_timestamp": "2023-10-04 08:47:36.268000000",
            "backend_update_timestamp": "2023-10-04 08:47:36.268000000",
            "blocked_effective_reputation": "TRUSTED_WHITE_LIST",
            "blocked_name": "c:\\windows\\system32\\cmd.exe",
            "blocked_sha256": "b99d61d874728edc0918ca0eb10eab93d381e7367e377406e65963366c874450",
            "childproc_cmdline": 'C:\\Windows\\system32\\cmd.exe /c ""C:\\Users\\bob.ross\\Downloads\\u0007irreg\\AirRegNCmd.cmd" N18906"',
            "childproc_effective_reputation": "TRUSTED_WHITE_LIST",
            "childproc_guid": "ABCD1234-0a5089d3-00002004-00000000-1d9f69f13af9c8b",
            "childproc_name": "c:\\windows\\system32\\cmd.exe",
            "childproc_sha256": "b99d61d874728edc0918ca0eb10eab93d381e7367e377406e65963366c874450",
            "childproc_username": "DESKTOP-A1B2C3\\bob.ross",
            "detection_timestamp": "2023-10-04 08:46:44.508000000",
            "determination": {"change_timestamp": "2023-10-04 08:47:36.268000000", "value": "NONE"},
            "device_external_ip": "12.34.56.78",
            "device_id": 173050323,
            "device_internal_ip": "192.168.31.23",
            "device_location": "OFFSITE",
            "device_name": "DESKTOP-A1B2C3",
            "device_os": "WINDOWS",
            "device_policy": "Standard",
            "device_policy_id": 390195,
            "device_target_value": "MEDIUM",
            "device_username": "bob.ross@gmail.com",
            "first_event_timestamp": "2023-10-04 08:42:17.182000000",
            "id": "9728f0c8-7810-fb20-15d0-343031500435",
            "is_updated": False,
            "last_event_timestamp": "2023-10-04 08:45:49.524000000",
            "mdr_alert": False,
            "mdr_alert_notes_present": False,
            "org_key": "ABCD1234",
            "parent_effective_reputation": "LOCAL_WHITE",
            "parent_guid": "ABCD1234-0a5089d3-000013f8-00000000-1d9f69f13af9c8b",
            "parent_name": "c:\\windows\\explorer.exe",
            "parent_pid": 5112,
            "parent_reputation": "TRUSTED_WHITE_LIST",
            "parent_sha256": "9c06462b5d1b85517a8ed4b5754c21e6beca5c9a02e42efa8b0e1049431c2972",
            "parent_username": "DESKTOP-A1B2C3\\bob.ross",
            "policy_applied": "APPLIED",
            "primary_event_id": "8e8f7f9f629211ee87ce374372b370f0",
            "process_cmdline": '"C:\\Windows\\System32\\WindowsPowerShell\\u000b1.0\\powershell.exe" ',
            "process_effective_reputation": "TRUSTED_WHITE_LIST",
            "process_guid": "ABCD1234-0a5089d3-000029a8-00000000-1d9f69f13af9c8b",
            "process_issuer": [""],
            "process_md5": "dfd66604ca0898e8e26df7b1635b6326",
            "process_name": "c:\\windows\\system32\\windowspowershell\\u000b1.0\\powershell.exe",
            "process_pid": 10664,
            "process_publisher": [""],
            "process_reputation": "TRUSTED_WHITE_LIST",
            "process_sha256": "d23b67799a0da0143e395ba5db906a22ab08fac4bd5581e275b1e0f1b3fac55c",
            "process_username": "DESKTOP-A1B2C3\\bob.ross",
            "reason": "The application utweb.exe was detected running. A Terminate Policy Action was applied.",
            "reason_code": "T_POL_TERM : utweb.exe",
            "run_state": "RAN",
            "sensor_action": "ALLOW",
            "severity": 3,
            "threat_id": "f1088650549018a6dab7e582a9d3b826",
            "ttps": [
                "POLICY_TERMINATE",
                "NETWORK_ACCESS",
                "MITRE_T1059_003_WIN_CMD_SHELL",
                "ACTIVE_CLIENT",
                "INTERNATIONAL_SITE",
                "MITRE_T1059_001_POWERSHELL",
                "MITRE_T1059_CMD_LINE_OR_SCRIPT_INTER",
                "UNKNOWN_APP",
                "RUN_CMD_SHELL",
            ],
            "type": "CB_ANALYTICS",
            "version": "2.0.0",
            "workflow": {
                "change_timestamp": "2023-10-04 08:47:36.268000000",
                "changed_by": "ALERT_CREATION",
                "changed_by_type": "SYSTEM",
                "closure_reason": "NO_REASON",
                "status": "OPEN",
            },
        },
    ),
    PantherRuleTest(
        Name="Alert Updated",
        ExpectedResult=False,
        Log={
            "p_log_type": "CarbonBlack.AlertV2",
            "alert_notes_present": False,
            "alert_url": "https://d5.carbonblack.net/alerts?orgKey=ABCD1234&s%5Bc%5D%5Bquery_string%5D=id%3A9728f0c8-7810-fb20-15d0-343031500435",
            "attack_tactic": "TA0002",
            "backend_timestamp": "2023-10-04 08:47:36.268000000",
            "backend_update_timestamp": "2023-10-04 08:47:36.268000000",
            "blocked_effective_reputation": "TRUSTED_WHITE_LIST",
            "blocked_name": "c:\\windows\\system32\\cmd.exe",
            "blocked_sha256": "b99d61d874728edc0918ca0eb10eab93d381e7367e377406e65963366c874450",
            "childproc_cmdline": 'C:\\Windows\\system32\\cmd.exe /c ""C:\\Users\\bob.ross\\Downloads\\u0007irreg\\AirRegNCmd.cmd" N18906"',
            "childproc_effective_reputation": "TRUSTED_WHITE_LIST",
            "childproc_guid": "ABCD1234-0a5089d3-00002004-00000000-1d9f69f13af9c8b",
            "childproc_name": "c:\\windows\\system32\\cmd.exe",
            "childproc_sha256": "b99d61d874728edc0918ca0eb10eab93d381e7367e377406e65963366c874450",
            "childproc_username": "DESKTOP-A1B2C3\\bob.ross",
            "detection_timestamp": "2023-10-04 08:46:44.508000000",
            "determination": {"change_timestamp": "2023-10-04 08:47:36.268000000", "value": "NONE"},
            "device_external_ip": "12.34.56.78",
            "device_id": 173050323,
            "device_internal_ip": "192.168.31.23",
            "device_location": "OFFSITE",
            "device_name": "DESKTOP-A1B2C3",
            "device_os": "WINDOWS",
            "device_policy": "Standard",
            "device_policy_id": 390195,
            "device_target_value": "MEDIUM",
            "device_username": "bob.ross@gmail.com",
            "first_event_timestamp": "2023-10-04 08:42:17.182000000",
            "id": "9728f0c8-7810-fb20-15d0-343031500435",
            "is_updated": False,
            "last_event_timestamp": "2023-10-04 08:45:49.524000000",
            "mdr_alert": False,
            "mdr_alert_notes_present": False,
            "org_key": "ABCD1234",
            "parent_effective_reputation": "LOCAL_WHITE",
            "parent_guid": "ABCD1234-0a5089d3-000013f8-00000000-1d9f69f13af9c8b",
            "parent_name": "c:\\windows\\explorer.exe",
            "parent_pid": 5112,
            "parent_reputation": "TRUSTED_WHITE_LIST",
            "parent_sha256": "9c06462b5d1b85517a8ed4b5754c21e6beca5c9a02e42efa8b0e1049431c2972",
            "parent_username": "DESKTOP-A1B2C3\\bob.ross",
            "policy_applied": "APPLIED",
            "primary_event_id": "8e8f7f9f629211ee87ce374372b370f0",
            "process_cmdline": '"C:\\Windows\\System32\\WindowsPowerShell\\u000b1.0\\powershell.exe" ',
            "process_effective_reputation": "TRUSTED_WHITE_LIST",
            "process_guid": "ABCD1234-0a5089d3-000029a8-00000000-1d9f69f13af9c8b",
            "process_issuer": [""],
            "process_md5": "dfd66604ca0898e8e26df7b1635b6326",
            "process_name": "c:\\windows\\system32\\windowspowershell\\u000b1.0\\powershell.exe",
            "process_pid": 10664,
            "process_publisher": [""],
            "process_reputation": "TRUSTED_WHITE_LIST",
            "process_sha256": "d23b67799a0da0143e395ba5db906a22ab08fac4bd5581e275b1e0f1b3fac55c",
            "process_username": "DESKTOP-A1B2C3\\bob.ross",
            "reason": "The application utweb.exe was detected running. A Terminate Policy Action was applied.",
            "reason_code": "T_POL_TERM : utweb.exe",
            "run_state": "RAN",
            "sensor_action": "ALLOW",
            "severity": 3,
            "threat_id": "f1088650549018a6dab7e582a9d3b826",
            "ttps": [
                "POLICY_TERMINATE",
                "NETWORK_ACCESS",
                "MITRE_T1059_003_WIN_CMD_SHELL",
                "ACTIVE_CLIENT",
                "INTERNATIONAL_SITE",
                "MITRE_T1059_001_POWERSHELL",
                "MITRE_T1059_CMD_LINE_OR_SCRIPT_INTER",
                "UNKNOWN_APP",
                "RUN_CMD_SHELL",
            ],
            "type": "CB_ANALYTICS",
            "version": "2.0.0",
            "workflow": {
                "change_timestamp": "2023-10-04 08:47:36.268000000",
                "changed_by": "admin",
                "changed_by_type": "USER",
                "closure_reason": "RESOLVED",
                "status": "CLOSED",
            },
        },
    ),
]


class CarbonBlackAlertV2Passthrough(PantherRule):
    RuleID = "CarbonBlack.AlertV2.Passthrough-prototype"
    Description = "This rule enriches and contextualizes security alerts generated by Carbon Black.  The alert title and description are dynamically updated based on data included in the alert log."
    DisplayName = "Carbon Black Passthrough Rule"
    Runbook = "Review the Carbon Black alert details to determine what malicious behavior was detected, and whether or not it was blocked.  Use the Reference link to view the alert in the Carbon Black console and take remediating actions if necessary."
    Reference = "https://docs.vmware.com/en/VMware-Carbon-Black-Cloud/services/carbon-black-cloud-user-guide/GUID-0B68199D-6411-45D1-AE0D-2AB9B7A28513.html"
    LogTypes = [LogType.CarbonBlack_AlertV2]
    Severity = PantherSeverity.Medium
    DedupPeriodMinutes = 30
    SummaryAttributes = [
        "attack_tactic",
        "blocked_name",
        "device_name",
        "device_username",
        "primary_event_id",
        "reason",
        "threat_id",
    ]
    Tests = carbon_black_alert_v2_passthrough_tests

    def rule(self, event):
        return event.deep_get("workflow", "changed_by") == "ALERT_CREATION"

    def title(self, event):
        return f"{event.get('attack_tactic', 'CB')}: {event.get('device_username', '<no-user-found>')} on {event.get('device_name', '<no-device-found>')}: {event.get('reason', '<no-reason-found>')}"

    def description(self, event):
        return event.get("reason", "<no-reason-found>")

    def severity(self, event):
        sev = event.get("severity")
        if sev >= 8:
            return "CRITICAL"
        if sev >= 6:
            return "HIGH"
        if sev >= 4:
            return "MEDIUM"
        if sev >= 2:
            return "LOW"
        return "INFO"

    def reference(self, event):
        return event.get("alert_url")

    def dedup(self, event):
        return event.get("id")

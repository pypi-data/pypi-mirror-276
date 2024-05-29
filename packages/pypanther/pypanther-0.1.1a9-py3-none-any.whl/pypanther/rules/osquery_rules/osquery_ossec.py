from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.log_types import LogType

osquery_ossec_rootkit_detected_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Rootkit Detected",
        ExpectedResult=True,
        Log={
            "action": "added",
            "calendarTime": "Tue Sep 11 16:14:21 2018 UTC",
            "columns": {
                "build_distro": "10.12",
                "build_platform": "darwin",
                "config_hash": "1111",
                "config_valid": "1",
                "counter": "14",
                "global_state": "0",
                "extensions": "active",
                "instance_id": "1111",
                "pid": "223",
                "resident_size": "54894592",
                "start_time": "1536634519",
                "system_time": "12472",
                "user_time": "31800",
                "uuid": "37821E12-CC8A-5AA3-A90C-FAB28A5BF8F9",
                "version": "3.2.6",
                "watcher": "92",
            },
            "counter": "255",
            "decorations": {"host_uuid": "1111", "environment": "corp"},
            "epoch": "0",
            "hostIdentifier": "test.lan",
            "log_type": "result",
            "name": "pack_ossec-rootkit_pwned",
            "unixTime": "1536682461",
        },
    ),
    PantherRuleTest(
        Name="Rootkit Not Detected",
        ExpectedResult=False,
        Log={
            "action": "added",
            "calendarTime": "Tue Sep 11 16:14:21 2018 UTC",
            "columns": {
                "build_distro": "10.12",
                "build_platform": "darwin",
                "config_hash": "1111",
                "config_valid": "1",
                "counter": "14",
                "global_state": "2",
                "extensions": "active",
                "instance_id": "1111",
                "pid": "223",
                "resident_size": "54894592",
                "start_time": "1536634519",
                "system_time": "12472",
                "user_time": "31800",
                "uuid": "37821E12-CC8A-5AA3-A90C-FAB28A5BF8F9",
                "version": "3.2.6",
                "watcher": "92",
            },
            "counter": "255",
            "decorations": {"host_uuid": "1111", "environment": "corp"},
            "epoch": "0",
            "hostIdentifier": "test.lan",
            "log_type": "result",
            "name": "pack_osquery-response_alf",
            "unixTime": "1536682461",
        },
    ),
]


class OsqueryOSSECRootkitDetected(PantherRule):
    RuleID = "Osquery.OSSECRootkitDetected-prototype"
    DisplayName = "OSSEC Rootkit Detected via Osquery"
    LogTypes = [LogType.Osquery_Differential]
    Tags = ["Osquery", "Malware", "Defense Evasion:Rootkit"]
    Reports = {"MITRE ATT&CK": ["TA0005:T1014"]}
    Severity = PantherSeverity.Medium
    Description = "Checks if any results are returned for the Osquery OSSEC Rootkit pack.\n"
    Runbook = "Verify the presence of the rootkit and re-image the machine.\n"
    Reference = "https://panther.com/blog/osquery-log-analysis/"
    SummaryAttributes = ["name", "hostIdentifier", "action"]
    Tests = osquery_ossec_rootkit_detected_tests

    def rule(self, event):
        return "ossec-rootkit" in event.get("name", "") and event.get("action") == "added"

    def title(self, event):
        return f"OSSEC rootkit found on [{event.get('hostIdentifier')}]"

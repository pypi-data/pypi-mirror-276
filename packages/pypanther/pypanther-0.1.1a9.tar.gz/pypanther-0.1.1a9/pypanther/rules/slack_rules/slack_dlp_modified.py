from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import slack_alert_context
from pypanther.log_types import LogType

slack_audit_logs_dlp_modified_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Native DLP Rule Deactivated",
        ExpectedResult=True,
        Log={
            "action": "native_dlp_rule_deactivated",
            "actor": {
                "type": "user",
                "user": {
                    "email": "user@example.com",
                    "id": "A012B3CDEFG",
                    "name": "username",
                    "team": "T01234N56GB",
                },
            },
            "context": {
                "ip_address": "1.2.3.4",
                "location": {
                    "domain": "test-workspace",
                    "id": "T01234N56GB",
                    "name": "test-workspace",
                    "type": "workspace",
                },
                "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            },
        },
    ),
    PantherRuleTest(
        Name="Native DLP Violation Deleted",
        ExpectedResult=True,
        Log={
            "action": "native_dlp_violation_deleted",
            "actor": {
                "type": "user",
                "user": {
                    "email": "user@example.com",
                    "id": "A012B3CDEFG",
                    "name": "username",
                    "team": "T01234N56GB",
                },
            },
            "context": {
                "ip_address": "1.2.3.4",
                "location": {
                    "domain": "test-workspace",
                    "id": "T01234N56GB",
                    "name": "test-workspace",
                    "type": "workspace",
                },
                "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            },
        },
    ),
    PantherRuleTest(
        Name="User Logout",
        ExpectedResult=False,
        Log={
            "action": "user_logout",
            "actor": {
                "type": "user",
                "user": {
                    "email": "user@example.com",
                    "id": "W012J3FEWAU",
                    "name": "primary-owner",
                    "team": "T01234N56GB",
                },
            },
            "context": {
                "ip_address": "1.2.3.4",
                "location": {
                    "domain": "test-workspace-1",
                    "id": "T01234N56GB",
                    "name": "test-workspace-1",
                    "type": "workspace",
                },
                "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            },
            "date_create": "2022-07-28 15:22:32",
            "entity": {
                "type": "user",
                "user": {
                    "email": "user@example.com",
                    "id": "W012J3FEWAU",
                    "name": "primary-owner",
                    "team": "T01234N56GB",
                },
            },
            "id": "72cac009-9eb3-4dde-bac6-ee49a32a1789",
        },
    ),
]


class SlackAuditLogsDLPModified(PantherRule):
    RuleID = "Slack.AuditLogs.DLPModified-prototype"
    DisplayName = "Slack DLP Modified"
    LogTypes = [LogType.Slack_AuditLogs]
    Tags = [
        "Slack",
        "Defense Evasion",
        "Impair Defenses",
        "Disable or Modify Tools",
        "Indicator Removal",
    ]
    Reports = {"MITRE ATT&CK": ["TA0005:T1562.001", "TA0005:T1070"]}
    Severity = PantherSeverity.High
    Description = "Detects when a Data Loss Prevention (DLP) rule has been deactivated or a violation has been deleted\n"
    Reference = "https://slack.com/intl/en-gb/help/articles/12914005852819-Slack-Connect--Data-loss-prevention"
    SummaryAttributes = ["action", "p_any_ip_addresses", "p_any_emails"]
    Tests = slack_audit_logs_dlp_modified_tests
    DLP_ACTIONS = ["native_dlp_rule_deactivated", "native_dlp_violation_deleted"]
    # DLP violations can be removed by security engineers in the case of FPs
    # We still want to alert on these, however those should not constitute a High severity

    def rule(self, event):
        return event.get("action") in self.DLP_ACTIONS

    def title(self, event):
        if event.get("action") == "native_dlp_rule_deactivated":
            return "Slack DLP Rule Deactivated"
        return "Slack DLP Violation Deleted"

    def severity(self, event):
        if event.get("action") == "native_dlp_violation_deleted":
            return "Medium"
        return "High"

    def alert_context(self, event):
        return slack_alert_context(event)

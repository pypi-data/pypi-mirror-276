from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import slack_alert_context
from pypanther.log_types import LogType

slack_audit_logs_intune_mdm_disabled_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Intune Disabled",
        ExpectedResult=True,
        Log={
            "action": "intune_disabled",
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


class SlackAuditLogsIntuneMDMDisabled(PantherRule):
    RuleID = "Slack.AuditLogs.IntuneMDMDisabled-prototype"
    DisplayName = "Slack Intune MDM Disabled"
    LogTypes = [LogType.Slack_AuditLogs]
    Tags = ["Slack", "Defense Evasion", "Impair Defenses", "Disable or Modify Tools"]
    Reports = {"MITRE ATT&CK": ["TA0005:T1562.001"]}
    Severity = PantherSeverity.Critical
    Description = "Detects the disabling of Microsoft Intune Enterprise MDM within Slack"
    Reference = "https://slack.com/intl/en-gb/help/articles/6495319642387-Set-up-Slack-for-Intune-mobile-apps"
    SummaryAttributes = ["p_any_ip_addresses", "p_any_emails"]
    Tests = slack_audit_logs_intune_mdm_disabled_tests

    def rule(self, event):
        return event.get("action") == "intune_disabled"

    def alert_context(self, event):
        return slack_alert_context(event)

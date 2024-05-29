from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import slack_alert_context
from pypanther.log_types import LogType

slack_audit_logs_ekm_slackbot_unenrolled_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="EKM Slackbot Unenrolled",
        ExpectedResult=True,
        Log={
            "action": "ekm_slackbot_unenroll_notification_sent",
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


class SlackAuditLogsEKMSlackbotUnenrolled(PantherRule):
    RuleID = "Slack.AuditLogs.EKMSlackbotUnenrolled-prototype"
    DisplayName = "Slack EKM Slackbot Unenrolled"
    LogTypes = [LogType.Slack_AuditLogs]
    Tags = ["Slack", "Impact", "Service Stop"]
    Reports = {"MITRE ATT&CK": ["TA0040:T1489"]}
    Severity = PantherSeverity.High
    Description = "Detects when a workspace is longer enrolled in EKM"
    Reference = (
        "https://slack.com/intl/en-gb/help/articles/360019110974-Slack-Enterprise-Key-Management"
    )
    SummaryAttributes = ["p_any_ip_addresses", "p_any_emails"]
    Tests = slack_audit_logs_ekm_slackbot_unenrolled_tests

    def rule(self, event):
        # Only alert on the `ekm_slackbot_unenroll_notification_sent` action
        return event.get("action") == "ekm_slackbot_unenroll_notification_sent"

    def alert_context(self, event):
        return slack_alert_context(event)

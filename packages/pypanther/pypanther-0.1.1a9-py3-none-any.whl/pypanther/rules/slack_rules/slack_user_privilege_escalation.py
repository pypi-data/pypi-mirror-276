from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import deep_get, slack_alert_context
from pypanther.log_types import LogType

slack_audit_logs_user_privilege_escalation_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Owner Transferred",
        ExpectedResult=True,
        Log={
            "action": "owner_transferred",
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
        Name="Permissions Assigned",
        ExpectedResult=True,
        Log={
            "action": "permissions_assigned",
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
        Name="Role Changed to Admin",
        ExpectedResult=True,
        Log={
            "action": "role_change_to_admin",
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
        Name="Role Changed to Owner",
        ExpectedResult=True,
        Log={
            "action": "role_change_to_owner",
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


class SlackAuditLogsUserPrivilegeEscalation(PantherRule):
    RuleID = "Slack.AuditLogs.UserPrivilegeEscalation-prototype"
    DisplayName = "Slack User Privilege Escalation"
    LogTypes = [LogType.Slack_AuditLogs]
    Tags = ["Slack", "Privilege Escalation", "Account Manipulation", "Additional Cloud Roles"]
    Reports = {"MITRE ATT&CK": ["TA0004:T1098.003"]}
    Severity = PantherSeverity.High
    Description = "Detects when a Slack user gains escalated privileges"
    Reference = "https://slack.com/intl/en-gb/help/articles/201314026-Permissions-by-role-in-Slack"
    SummaryAttributes = ["p_any_ip_addresses", "p_any_emails"]
    Tests = slack_audit_logs_user_privilege_escalation_tests
    USER_PRIV_ESC_ACTIONS = {
        "owner_transferred": "Slack Owner Transferred",
        "permissions_assigned": "Slack User Assigned Permissions",
        "role_change_to_admin": "Slack User Made Admin",
        "role_change_to_owner": "Slack User Made Owner",
    }

    def rule(self, event):
        return event.get("action") in self.USER_PRIV_ESC_ACTIONS

    def title(self, event):
        username = deep_get(event, "actor", "user", "name", default="<unknown-actor>")
        email = deep_get(event, "actor", "user", "email", default="<unknown-email>")
        if event.get("action") == "owner_transferred":
            return f"Slack Owner Transferred from {username} ({email})"
        if event.get("action") == "permissions_assigned":
            return f"Slack User, {username} ({email}), assigned permissions"
        if event.get("action") == "role_change_to_admin":
            return f"Slack User, {username} ({email}), promoted to admin"
        if event.get("action") == "role_change_to_owner":
            return f"Slack User, {username} ({email}), promoted to Owner"
        return (
            f"Slack User Privilege Escalation event {event.get('action')} on {username} ({email})"
        )

    def severity(self, event):
        # Downgrade severity for users assigned permissions
        if event.get("action") == "permissions_assigned":
            return "Medium"
        return "Critical"

    def alert_context(self, event):
        return slack_alert_context(event)

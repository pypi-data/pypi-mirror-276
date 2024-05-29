from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.log_types import LogType

okta_support_access_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Support Access Granted",
        ExpectedResult=True,
        Log={
            "published": "2022-03-22 14:21:53.225",
            "eventType": "user.session.impersonation.grant",
            "version": "0",
            "severity": "INFO",
            "legacyEventType": "core.user.impersonation.grant.enabled",
            "displayMessage": "Enable impersonation grant",
            "actor": {
                "alternateId": "homer@springfield.gov",
                "displayName": "Homer Simpson",
                "id": "111111",
                "type": "User",
            },
            "client": {
                "device": "Computer",
                "ipAddress": "1.1.1.1",
                "userAgent": {
                    "browser": "CHROME",
                    "os": "Mac OS X",
                    "rawUserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36",
                },
                "zone": "null",
            },
            "p_log_type": "Okta.SystemLog",
        },
    ),
    PantherRuleTest(
        Name="Login Event",
        ExpectedResult=False,
        Log={
            "published": "2022-03-22 14:21:53.225",
            "eventType": "user.session.start",
            "version": "0",
            "severity": "INFO",
            "actor": {
                "alternateId": "homer@springfield.gov",
                "displayName": "Homer Simpson",
                "id": "111111",
                "type": "User",
            },
            "client": {
                "device": "Computer",
                "ipAddress": "1.1.1.1",
                "userAgent": {
                    "browser": "CHROME",
                    "os": "Mac OS X",
                    "rawUserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36",
                },
                "zone": "null",
            },
            "p_log_type": "Okta.SystemLog",
        },
    ),
]


class OktaSupportAccess(PantherRule):
    RuleID = "Okta.Support.Access-prototype"
    DisplayName = "Okta Support Access Granted"
    LogTypes = [LogType.Okta_SystemLog]
    Tags = [
        "Identity & Access Management",
        "DataModel",
        "Okta",
        "Initial Access:Trusted Relationship",
    ]
    Reports = {"MITRE ATT&CK": ["TA0001:T1199"]}
    Severity = PantherSeverity.Medium
    Description = "An admin user has granted access to Okta Support to your account"
    Reference = "https://help.okta.com/en/prod/Content/Topics/Settings/settings-support-access.htm"
    Runbook = "Contact Admin to ensure this was sanctioned activity"
    DedupPeriodMinutes = 15
    SummaryAttributes = ["eventType", "severity", "displayMessage", "p_any_ip_addresses"]
    Tests = okta_support_access_tests
    OKTA_SUPPORT_ACCESS_EVENTS = [
        "user.session.impersonation.grant",
        "user.session.impersonation.initiate",
    ]

    def rule(self, event):
        return event.get("eventType") in self.OKTA_SUPPORT_ACCESS_EVENTS

    def title(self, event):
        return f"Okta Support Access Granted by {event.udm('actor_user')}"

    def alert_context(self, event):
        context = {
            "user": event.udm("actor_user"),
            "ip": event.udm("source_ip"),
            "event": event.get("eventType"),
        }
        return context

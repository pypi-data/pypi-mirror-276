import re
from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import deep_get, okta_alert_context
from pypanther.log_types import LogType

okta_admin_role_assigned_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Admin Access Assigned",
        ExpectedResult=True,
        Log={
            "uuid": "2a992f80-d1ad-4f62-900e-8c68bb72a21b",
            "published": "2020-11-25 21:27:03.496000000",
            "eventType": "user.account.privilege.grant",
            "version": "0",
            "severity": "INFO",
            "legacyEventType": "core.user.admin_privilege.granted",
            "displayMessage": "Grant user privilege",
            "actor": {
                "id": "00uu1uuuuIlllaaaa356",
                "type": "User",
                "alternateId": "jack@acme.io",
                "displayName": "Jack Naglieri",
            },
            "client": {
                "userAgent": {
                    "browser": "CHROME",
                    "os": "Mac OS X",
                    "rawUserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
                },
                "geographicalContext": {
                    "geolocation": {"lat": 37.7852, "lon": -122.3874},
                    "city": "San Francisco",
                    "state": "California",
                    "country": "United States",
                    "postalCode": "94105",
                },
                "zone": "null",
                "ipAddress": "136.24.229.58",
                "device": "Computer",
            },
            "request": {},
            "outcome": {"result": "SUCCESS"},
            "target": [
                {
                    "id": "00u6eup97mAJZWYmP357",
                    "type": "User",
                    "alternateId": "alice@acme.io",
                    "displayName": "Alice Green",
                }
            ],
            "transaction": {},
            "debugContext": {
                "debugData": {
                    "privilegeGranted": "Organization administrator, Application administrator (all)",
                    "requestUri": "/api/internal/administrators/00u6eu8c68bb72a21b57",
                    "threatSuspected": "false",
                    "url": "/api/internal/administrators/00u6eu8c68bb72a21b57",
                    "requestId": "X777JJ9sssQQHHrrrQTyYQAABBE",
                }
            },
            "authenticationContext": {},
            "securityContext": {},
        },
    ),
    PantherRuleTest(
        Name="Super Admin Access Assigned (High sev)",
        ExpectedResult=True,
        Log={
            "uuid": "2a992f80-d1ad-4f62-900e-8c68bb72a21b",
            "published": "2020-11-25 21:27:03.496000000",
            "eventType": "user.account.privilege.grant",
            "version": "0",
            "severity": "INFO",
            "legacyEventType": "core.user.admin_privilege.granted",
            "displayMessage": "Grant user privilege",
            "actor": {
                "id": "00uu1uuuuIlllaaaa356",
                "type": "User",
                "alternateId": "jack@acme.io",
                "displayName": "Jack Naglieri",
            },
            "client": {
                "userAgent": {
                    "browser": "CHROME",
                    "os": "Mac OS X",
                    "rawUserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
                },
                "geographicalContext": {
                    "geolocation": {"lat": 37.7852, "lon": -122.3874},
                    "city": "San Francisco",
                    "state": "California",
                    "country": "United States",
                    "postalCode": "94105",
                },
                "zone": "null",
                "ipAddress": "136.24.229.58",
                "device": "Computer",
            },
            "request": {},
            "outcome": {"result": "SUCCESS"},
            "target": [
                {
                    "id": "00u6eup97mAJZWYmP357",
                    "type": "User",
                    "alternateId": "alice@acme.io",
                    "displayName": "Alice Green",
                }
            ],
            "transaction": {},
            "debugContext": {
                "debugData": {
                    "privilegeGranted": "Super administrator, Read only admin",
                    "requestUri": "/api/internal/administrators/00u6eu8c68bb72a21b57",
                    "threatSuspected": "false",
                    "url": "/api/internal/administrators/00u6eu8c68bb72a21b57",
                    "requestId": "X777JJ9sssQQHHrrrQTyYQAABBE",
                }
            },
            "authenticationContext": {},
            "securityContext": {},
        },
    ),
]


class OktaAdminRoleAssigned(PantherRule):
    RuleID = "Okta.AdminRoleAssigned-prototype"
    DisplayName = "Okta Admin Role Assigned"
    LogTypes = [LogType.Okta_SystemLog]
    Tags = ["Identity & Access Management", "Okta", "Privilege Escalation:Valid Accounts"]
    Reports = {"MITRE ATT&CK": ["TA0004:T1078"]}
    Severity = PantherSeverity.Info
    Description = "A user has been granted administrative privileges in Okta"
    Reference = (
        "https://help.okta.com/en/prod/Content/Topics/Security/administrators-admin-comparison.htm"
    )
    Runbook = "Reach out to the user if needed to validate the activity"
    DedupPeriodMinutes = 15
    SummaryAttributes = ["eventType", "severity", "displayMessage", "p_any_ip_addresses"]
    Tests = okta_admin_role_assigned_tests
    ADMIN_PATTERN = re.compile("[aA]dministrator")

    def rule(self, event):
        return (
            event.get("eventType", None) == "user.account.privilege.grant"
            and deep_get(event, "outcome", "result") == "SUCCESS"
            and bool(
                self.ADMIN_PATTERN.search(
                    deep_get(event, "debugContext", "debugData", "privilegeGranted", default="")
                )
            )
        )

    def dedup(self, event):
        return deep_get(
            event, "debugContext", "debugData", "requestId", default="<UNKNOWN_REQUEST_ID>"
        )

    def title(self, event):
        target = event.get("target", [{}])
        display_name = target[0].get("displayName", "MISSING DISPLAY NAME") if target else ""
        alternate_id = target[0].get("alternateId", "MISSING ALTERNATE ID") if target else ""
        privilege = deep_get(
            event, "debugContext", "debugData", "privilegeGranted", default="<UNKNOWN_PRIVILEGE>"
        )
        return f"{deep_get(event, 'actor', 'displayName')} <{deep_get(event, 'actor', 'alternateId')}> granted [{privilege}] privileges to {display_name} <{alternate_id}>"

    def alert_context(self, event):
        return okta_alert_context(event)

    def severity(self, event):
        if "Super administrator" in deep_get(
            event, "debugContext", "debugData", "privilegeGranted", default=""
        ):
            return "HIGH"
        return "INFO"

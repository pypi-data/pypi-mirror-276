from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.log_types import LogType

teleport_local_user_login_without_mfa_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="User logged in with MFA",
        ExpectedResult=False,
        Log={
            "addr.remote": "[2001:db8:feed:face:c0ff:eeb0:baf00:00d]:65123",
            "cluster_name": "teleport.example.com",
            "code": "T1000I",
            "ei": 0,
            "event": "user.login",
            "method": "local",
            "mfa_device": {
                "mfa_device_name": "1Password",
                "mfa_device_type": "WebAuthn",
                "mfa_device_uuid": "88888888-4444-4444-4444-222222222222",
            },
            "success": True,
            "time": "2023-09-20T19:00:00.123456Z",
            "uid": "88888888-4444-4444-4444-222222222222",
            "user": "max.mustermann",
            "user_agent": "Examplecorp Spacedeck-web/99.9 (Hackintosh; ARM Cortex A1000)",
        },
    ),
    PantherRuleTest(
        Name="User logged in without MFA",
        ExpectedResult=False,
        Log={
            "addr.remote": "[2001:db8:face:face:face:face:face:face]:65123",
            "cluster_name": "teleport.example.com",
            "code": "T1000I",
            "ei": 0,
            "event": "user.login",
            "method": "local",
            "success": True,
            "time": "2023-09-20T19:00:00.123456Z",
            "uid": "88888888-4444-4444-4444-222222222222",
            "user": "max.mustermann",
            "user_agent": "Examplecorp Spacedeck-web/99.9 (Hackintosh; ARM Cortex A1000)",
        },
    ),
]


class TeleportLocalUserLoginWithoutMFA(PantherRule):
    RuleID = "Teleport.LocalUserLoginWithoutMFA-prototype"
    DisplayName = "User Logged in wihout MFA"
    LogTypes = [LogType.Gravitational_TeleportAudit]
    Tags = ["Teleport"]
    Severity = PantherSeverity.High
    Description = "A local User logged in without MFA"
    Reports = {"MITRE ATT&CK": ["TA0001:T1078"]}
    Reference = "https://goteleport.com/docs/management/admin/"
    Runbook = "A local user logged in without Multi-Factor Authentication\n"
    SummaryAttributes = ["event", "code", "user", "success", "mfa_device"]
    Tests = teleport_local_user_login_without_mfa_tests
    SENSITIVE_LOCAL_USERS = ["breakglass"]

    def rule(self, event):
        return (
            event.get("event") == "user.login"
            and event.get("success") == "true"
            and (event.get("method") == "local")
            and (not event.get("mfa_device"))
        )

    def severity(self, event):
        if event.get("user") in self.SENSITIVE_LOCAL_USERS:
            return "HIGH"
        return "MEDIUM"

    def title(self, event):
        return f"User [{event.get('user', '<UNKNOWN_USER>')}] logged into [{event.get('cluster_name', '<UNNAMED_CLUSTER>')}] locally without using MFA"

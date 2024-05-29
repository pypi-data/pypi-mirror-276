from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import deep_get
from pypanther.log_types import LogType

g_suite_workspace_password_enforce_strong_disabled_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Workspace Admin Disabled Strong Password Enforcement",
        ExpectedResult=True,
        Log={
            "actor": {
                "callerType": "USER",
                "email": "user@example.io",
                "profileId": "110111111111111111111",
            },
            "id": {
                "applicationName": "admin",
                "customerId": "D12345",
                "time": "2022-12-11 01:33:56.306000000",
                "uniqueQualifier": "-6444444444444444444",
            },
            "ipAddress": "12.12.12.12",
            "kind": "admin#reports#activity",
            "name": "CHANGE_APPLICATION_SETTING",
            "parameters": {
                "APPLICATION_EDITION": "enterprise",
                "APPLICATION_NAME": "Security",
                "NEW_VALUE": "off",
                "OLD_VALUE": "on",
                "ORG_UNIT_NAME": "Example IO",
                "SETTING_NAME": "Password Management - Enforce strong password",
            },
            "type": "APPLICATION_SETTINGS",
        },
    ),
    PantherRuleTest(
        Name="Admin Set Default Calendar SHARING_OUTSIDE_DOMAIN Setting to READ_ONLY_ACCESS",
        ExpectedResult=False,
        Log={
            "actor": {"callerType": "USER", "email": "example@example.io", "profileId": "12345"},
            "id": {
                "applicationName": "admin",
                "customerId": "D12345",
                "time": "2022-12-11 01:06:26.303000000",
                "uniqueQualifier": "-12345",
            },
            "ipAddress": "12.12.12.12",
            "kind": "admin#reports#activity",
            "name": "CHANGE_CALENDAR_SETTING",
            "parameters": {
                "DOMAIN_NAME": "example.io",
                "NEW_VALUE": "READ_ONLY_ACCESS",
                "OLD_VALUE": "DEFAULT",
                "ORG_UNIT_NAME": "Example IO",
                "SETTING_NAME": "SHARING_OUTSIDE_DOMAIN",
            },
            "type": "CALENDAR_SETTINGS",
        },
    ),
    PantherRuleTest(
        Name="ListObject Type",
        ExpectedResult=False,
        Log={
            "actor": {"email": "user@example.io", "profileId": "118111111111111111111"},
            "id": {
                "applicationName": "drive",
                "customerId": "D12345",
                "time": "2022-12-20 17:27:47.080000000",
                "uniqueQualifier": "-7312729053723258069",
            },
            "ipAddress": "12.12.12.12",
            "kind": "admin#reports#activity",
            "name": "rename",
            "parameters": {
                "actor_is_collaborator_account": None,
                "billable": True,
                "doc_id": "1GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",
                "doc_title": "Document Title- Found Here",
                "doc_type": "presentation",
                "is_encrypted": None,
                "new_value": ["Document Title- Found Here"],
                "old_value": ["Document Title- Old"],
                "owner": "user@example.io",
                "owner_is_shared_drive": None,
                "owner_is_team_drive": None,
                "primary_event": True,
                "visibility": "private",
            },
            "type": "access",
        },
    ),
]


class GSuiteWorkspacePasswordEnforceStrongDisabled(PantherRule):
    RuleID = "GSuite.Workspace.PasswordEnforceStrongDisabled-prototype"
    DisplayName = "GSuite Workspace Strong Password Enforcement Has Been Disabled"
    LogTypes = [LogType.GSuite_ActivityEvent]
    Tags = ["GSuite"]
    Severity = PantherSeverity.High
    Reports = {"MITRE ATT&CK": ["TA0006:T1110"]}
    Description = "A Workspace Admin Has Disabled The Enforcement Of Strong Passwords\n"
    Reference = "https://support.google.com/a/answer/139399?hl=en"
    Runbook = "Verify the intent of this Password Strength Setting Change. If intent cannot be verified, then a search on the actor's other activities is advised.\n"
    SummaryAttributes = ["actor:email"]
    Tests = g_suite_workspace_password_enforce_strong_disabled_tests

    def rule(self, event):
        if deep_get(event, "id", "applicationName", default="").lower() != "admin":
            return False
        if all(
            [
                event.get("name", "") == "CHANGE_APPLICATION_SETTING",
                event.get("type", "") == "APPLICATION_SETTINGS",
                deep_get(event, "parameters", "NEW_VALUE", default="").lower() == "off",
                deep_get(event, "parameters", "SETTING_NAME", default="")
                == "Password Management - Enforce strong password",
            ]
        ):
            return True
        return False

    def title(self, event):
        return f"GSuite Workspace Strong Password Enforcement Has Been Disabled By [{deep_get(event, 'actor', 'email', default='<NO_ACTOR_FOUND>')}]"

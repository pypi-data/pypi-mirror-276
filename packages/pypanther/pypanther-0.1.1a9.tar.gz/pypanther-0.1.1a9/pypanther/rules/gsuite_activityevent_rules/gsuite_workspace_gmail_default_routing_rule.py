from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import deep_get
from pypanther.log_types import LogType

g_suite_workspace_gmail_default_routing_rule_modified_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Workspace Admin Creates Default Routing Rule",
        ExpectedResult=True,
        Log={
            "actor": {
                "callerType": "USER",
                "email": "user@example.io",
                "profileId": "110555555555555555555",
            },
            "id": {
                "applicationName": "admin",
                "customerId": "D12345",
                "time": "2022-12-11 00:50:03.493000000",
                "uniqueQualifier": "-6333333333333333333",
            },
            "ipAddress": "12.12.12.12",
            "kind": "admin#reports#activity",
            "name": "CREATE_GMAIL_SETTING",
            "parameters": {
                "SETTING_NAME": "MESSAGE_SECURITY_RULE",
                "USER_DEFINED_SETTING_NAME": "44444",
            },
            "type": "EMAIL_SETTINGS",
        },
    ),
    PantherRuleTest(
        Name="Workspace Admin Deletes Default Routing Rule",
        ExpectedResult=True,
        Log={
            "actor": {
                "callerType": "USER",
                "email": "user@example.io",
                "profileId": "110555555555555555555",
            },
            "id": {
                "applicationName": "admin",
                "customerId": "D12345",
                "time": "2022-12-11 00:50:41.760000000",
                "uniqueQualifier": "-5015136739334825037",
            },
            "ipAddress": "12.12.12.12",
            "kind": "admin#reports#activity",
            "name": "DELETE_GMAIL_SETTING",
            "parameters": {
                "SETTING_NAME": "MESSAGE_SECURITY_RULE",
                "USER_DEFINED_SETTING_NAME": "44444",
            },
            "type": "EMAIL_SETTINGS",
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


class GSuiteWorkspaceGmailDefaultRoutingRuleModified(PantherRule):
    RuleID = "GSuite.Workspace.GmailDefaultRoutingRuleModified-prototype"
    DisplayName = "GSuite Workspace Gmail Default Routing Rule Modified"
    LogTypes = [LogType.GSuite_ActivityEvent]
    Tags = ["GSuite"]
    Reports = {"MITRE ATT&CK": ["TA0003:T1098"]}
    Severity = PantherSeverity.High
    Description = "A Workspace Admin Has Modified A Default Routing Rule In Gmail\n"
    Reference = "https://support.google.com/a/answer/2368153?hl=en"
    Runbook = "Administrators use Default Routing to set up how inbound email is delivered within an organization. The configuration of the default routing rule needs to be inspected in order to verify the intent of the rule is benign.\nIf this change was not planned, inspect the other actions taken by this actor.\n"
    SummaryAttributes = ["actor:email"]
    Tests = g_suite_workspace_gmail_default_routing_rule_modified_tests

    def rule(self, event):
        if all(
            [
                event.get("type", "") == "EMAIL_SETTINGS",
                event.get("name", "").endswith("_GMAIL_SETTING"),
                deep_get(event, "parameters", "SETTING_NAME", default="")
                == "MESSAGE_SECURITY_RULE",
            ]
        ):
            return True
        return False

    def title(self, event):
        # Gmail records the event name as DELETE_GMAIL_SETTING/CREATE_GMAIL_SETTING
        # We shouldn't be able to enter title() unless event[name] ends with
        #  _GMAIL_SETTING, and as such change_type assumes the happy path.
        change_type = f"{event.get('name', '').split('_')[0].lower()}d"
        return f"GSuite Gmail Default Routing Rule Was [{change_type}] by [{deep_get(event, 'actor', 'email', default='<UNKNOWN_EMAIL>')}]"

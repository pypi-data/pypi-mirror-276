from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.log_types import LogType

google_workspace_apps_marketplace_new_domain_application_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Change Email Setting Default",
        ExpectedResult=False,
        Log={
            "actor": {"callerType": "USER", "email": "example@example.io", "profileId": "12345"},
            "id": {
                "applicationName": "admin",
                "customerId": "D1234",
                "time": "2022-12-10 23:33:04.667000000",
                "uniqueQualifier": "-12345",
            },
            "ipAddress": "12.12.12.12",
            "kind": "admin#reports#activity",
            "name": "CHANGE_EMAIL_SETTING",
            "parameters": {
                "NEW_VALUE": "1",
                "OLD_VALUE": "DEFAULT",
                "ORG_UNIT_NAME": "EXAMPLE IO",
                "SETTING_NAME": "ENABLE_G_SUITE_MARKETPLACE",
            },
            "type": "EMAIL_SETTINGS",
        },
    ),
    PantherRuleTest(
        Name="DocuSign for Google",
        ExpectedResult=True,
        Log={
            "actor": {"callerType": "USER", "email": "example@example.io", "profileId": "12345"},
            "id": {
                "applicationName": "admin",
                "customerId": "D12345",
                "time": "2022-12-10 23:05:39.508000000",
                "uniqueQualifier": "-12345",
            },
            "kind": "admin#reports#activity",
            "name": "ADD_APPLICATION",
            "parameters": {
                "APP_ID": "469176070494",
                "APPLICATION_ENABLED": "true",
                "APPLICATION_NAME": "DocuSign eSignature for Google",
            },
            "type": "DOMAIN_SETTINGS",
        },
    ),
    PantherRuleTest(
        Name="Microsoft Apps for Google",
        ExpectedResult=True,
        Log={
            "actor": {"callerType": "USER", "email": "example@example.io", "profileId": "12345"},
            "id": {
                "applicationName": "admin",
                "customerId": "D12345",
                "time": "2022-12-10 23:05:39.508000000",
                "uniqueQualifier": "-12345",
            },
            "kind": "admin#reports#activity",
            "name": "ADD_APPLICATION",
            "parameters": {
                "APP_ID": "469176070494",
                "APPLICATION_ENABLED": "true",
                "APPLICATION_NAME": "Microsoft Applications for Google",
            },
            "type": "DOMAIN_SETTINGS",
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


class GoogleWorkspaceAppsMarketplaceNewDomainApplication(PantherRule):
    Description = "A Google Workspace User configured a new domain application from the Google Workspace Apps Marketplace."
    DisplayName = "Google Workspace Apps Marketplace New Domain Application"
    Runbook = "Confirm this was the intended behavior."
    Reference = "https://developers.google.com/workspace/marketplace/overview"
    Severity = PantherSeverity.Medium
    LogTypes = [LogType.GSuite_ActivityEvent]
    RuleID = "Google.Workspace.Apps.Marketplace.New.Domain.Application-prototype"
    Tests = google_workspace_apps_marketplace_new_domain_application_tests

    def rule(self, event):
        # Return True to match the log event and trigger an alert.
        return (
            event.get("name") == "ADD_APPLICATION"
            and event.get("parameters", {}).get("APPLICATION_ENABLED", "<NO_APPLICATION_FOUND>")
            == "true"
        )

    def title(self, event):
        # (Optional) Return a string which will be shown as the alert title.
        # If no 'dedup' function is defined, the return value of this method
        # will act as deduplication string.
        return f"Google Workspace User [{event.get('actor', {}).get('email', '<NO_EMAIL_PROVIDED>')}] enabled a new Google Workspace Marketplace application [{event.get('parameters', {}).get('APPLICATION_NAME', '<NO_APPLICATION_NAME_FOUND>')}]"

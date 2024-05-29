from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_notion_helpers import notion_alert_context
from pypanther.log_types import LogType

notion_workspace_scim_token_generated_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="other event",
        ExpectedResult=False,
        Log={
            "event": {
                "id": "...",
                "timestamp": "2023-06-02T20:16:41.217Z",
                "workspace_id": "123",
                "actor": {
                    "id": "..",
                    "object": "user",
                    "type": "person",
                    "person": {"email": "homer.simpson@yourcompany.io"},
                },
                "ip_address": "...",
                "platform": "mac-desktop",
                "type": "workspace.content_exported",
                "workspace.content_exported": {},
            }
        },
    ),
    PantherRuleTest(
        Name="Token Generated",
        ExpectedResult=True,
        Log={
            "event": {
                "id": "...",
                "timestamp": "2023-06-02T20:21:01.873Z",
                "workspace_id": "123",
                "actor": {
                    "id": "..",
                    "object": "user",
                    "type": "person",
                    "person": {"email": "homer.simpson@yourcompany.com"},
                },
                "ip_address": "...",
                "platform": "mac-desktop",
                "type": "workspace.scim_token_generated",
                "workspace.scim_token_generated": {},
            }
        },
    ),
]


class NotionWorkspaceSCIMTokenGenerated(PantherRule):
    RuleID = "Notion.Workspace.SCIM.Token.Generated-prototype"
    DisplayName = "Notion SCIM Token Generated"
    LogTypes = [LogType.Notion_AuditLogs]
    Tags = ["Notion", "Application Security", "Supply Chain Attack"]
    Description = "A Notion User generated a SCIM token."
    Severity = PantherSeverity.Medium
    Runbook = "Possible Initial Access. Follow up with the Notion User to determine if this was done for a valid business reason."
    Reference = "https://www.notion.so/help/provision-users-and-groups-with-scim"
    Tests = notion_workspace_scim_token_generated_tests

    def rule(self, event):
        event_type = event.deep_get("event", "type", default="<NO_EVENT_TYPE_FOUND>")
        return event_type == "workspace.scim_token_generated"

    def title(self, event):
        user = event.deep_get("event", "actor", "person", "email", default="<NO_USER_FOUND>")
        workspace_id = event.deep_get("event", "workspace_id", default="<NO_WORKSPACE_ID_FOUND>")
        return f"Notion User [{user}] generated a SCIM token for workspace id [{workspace_id}]."

    def alert_context(self, event):
        return notion_alert_context(event)

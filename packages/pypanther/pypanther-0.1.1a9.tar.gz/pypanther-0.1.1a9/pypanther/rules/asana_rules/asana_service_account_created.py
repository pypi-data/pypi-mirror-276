from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import deep_get
from pypanther.log_types import LogType

asana_service_account_created_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="New domain created",
        ExpectedResult=False,
        Log={
            "actor": {
                "actor_type": "user",
                "email": "homer.simpson@example.io",
                "gid": "12345",
                "name": "Homer Simpson",
            },
            "context": {
                "client_ip_address": "12.12.12.12",
                "context_type": "web",
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            },
            "created_at": "2022-12-16 19:30:26.15",
            "details": {"new_value": "test.com"},
            "event_category": "admin_settings",
            "event_type": "workspace_associated_email_domain_added",
            "gid": "12345",
            "resource": {"gid": "12345", "name": "Example IO", "resource_type": "workspace"},
        },
    ),
    PantherRuleTest(
        Name="Slack svc acct",
        ExpectedResult=True,
        Log={
            "actor": {
                "actor_type": "user",
                "email": "homer.simpson@panther.io",
                "gid": "12345",
                "name": "Homer Simpson",
            },
            "context": {
                "client_ip_address": "12.12.12.12",
                "context_type": "web",
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            },
            "created_at": "2022-12-16 19:28:18.396",
            "details": {},
            "event_category": "apps",
            "event_type": "service_account_created",
            "gid": "12345",
            "resource": {"gid": "12345", "name": "Slack Service Account", "resource_type": "user"},
        },
    ),
    PantherRuleTest(
        Name="Datadog svc acct",
        ExpectedResult=True,
        Log={
            "actor": {
                "actor_type": "user",
                "email": "homer.simpson@panther.io",
                "gid": "12345",
                "name": "Homer Simpson",
            },
            "context": {
                "client_ip_address": "12.12.12.12",
                "context_type": "web",
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            },
            "created_at": "2022-12-16 19:28:18.396",
            "details": {},
            "event_category": "apps",
            "event_type": "service_account_created",
            "gid": "12345",
            "resource": {
                "gid": "12345",
                "name": "Datadog Service Account",
                "resource_type": "user",
            },
        },
    ),
]


class AsanaServiceAccountCreated(PantherRule):
    Description = "An Asana service account was created by someone in your organization."
    DisplayName = "Asana Service Account Created"
    Runbook = "Confirm this user acted with valid business intent and determine whether this activity was authorized."
    Reference = "https://help.asana.com/hc/en-us/articles/14217496838427-Service-Accounts"
    Severity = PantherSeverity.Medium
    LogTypes = [LogType.Asana_Audit]
    RuleID = "Asana.Service.Account.Created-prototype"
    Tests = asana_service_account_created_tests

    def rule(self, event):
        return event.get("event_type", "<NO_EVENT_TYPE_FOUND>") == "service_account_created"

    def title(self, event):
        actor_email = deep_get(event, "actor", "email", default="<ACTOR_NOT_FOUND>")
        svc_acct_name = deep_get(event, "resource", "name", default="<SVC_ACCT_NAME_NOT_FOUND>")
        return f"Asana user [{actor_email}] created a new service account [{svc_acct_name}]."

from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.log_types import LogType

zendesk_new_api_token_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Zendesk - API Token Updated",
        ExpectedResult=False,
        Log={
            "url": "https://myzendek.zendesk.com/api/v2/audit_logs/111222333444.json",
            "id": 123456789123,
            "action_label": "Updated",
            "actor_id": 123,
            "actor_name": "John Doe",
            "source_id": 123,
            "source_type": "api_token",
            "source_label": "API token: a new description",
            "action": "update",
            "change_description": "description changed from not set to a new description",
            "ip_address": "127.0.0.1",
            "created_at": "2021-05-28T18:39:50Z",
            "p_log_type": "Zendesk.Audit",
        },
    ),
    PantherRuleTest(
        Name="Zendesk - API Token Created",
        ExpectedResult=True,
        Log={
            "url": "https://myzendek.zendesk.com/api/v2/audit_logs/111222333444.json",
            "id": 123456789123,
            "action_label": "Created",
            "actor_id": 123,
            "actor_name": "John Doe",
            "source_id": 123,
            "source_type": "api_token",
            "source_label": "API token",
            "action": "create",
            "change_description": "",
            "ip_address": "127.0.0.1",
            "created_at": "2021-05-28T18:39:50Z",
            "p_log_type": "Zendesk.Audit",
        },
    ),
]


class ZendeskNewAPIToken(PantherRule):
    RuleID = "Zendesk.NewAPIToken-prototype"
    DisplayName = "Zendesk API Token Created"
    LogTypes = [LogType.Zendesk_Audit]
    Severity = PantherSeverity.High
    Tags = ["Zendesk", "Credential Access:Steal Application Access Token"]
    Reports = {"MITRE ATT&CK": ["TA0006:T1528"]}
    Description = "A user created a new API token to be used with Zendesk."
    Runbook = "Validate the api token was created for valid use case, otherwise delete the token immediately."
    Reference = "https://support.zendesk.com/hc/en-us/articles/4408889192858-Managing-access-to-the-Zendesk-API#topic_bsw_lfg_mmb:~:text=enable%20token%20access.-,Generating%20API%20tokens,-To%20generate%20an"
    SummaryAttributes = ["p_any_ip_addresses"]
    Tests = zendesk_new_api_token_tests
    API_TOKEN_ACTIONS = {"create", "destroy"}

    def rule(self, event):
        return (
            event.get("source_type") == "api_token"
            and event.get("action", "") in self.API_TOKEN_ACTIONS
        )

    def title(self, event):
        action = event.get("action", "<UNKNOWN_ACTION>")
        return (
            f"[{event.get('p_log_type')}]: User [{event.udm('actor_user')}] {action} an api token"
        )

    def severity(self, event):
        if event.get("action", "") == "destroy":
            return "INFO"
        return "HIGH"

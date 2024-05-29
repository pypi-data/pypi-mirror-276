from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import deep_get
from pypanther.helpers.panther_tailscale_helpers import (
    is_tailscale_admin_console_event,
    tailscale_alert_context,
)
from pypanther.log_types import LogType

tailscale_magic_dns_disabled_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Magic DNS Disabled",
        ExpectedResult=True,
        Log={
            "event": {
                "action": "DISABLE",
                "actor": {
                    "displayName": "Homer Simpson",
                    "id": "uodc9f3CNTRL",
                    "loginName": "homer.simpson@yourcompany.io",
                    "type": "USER",
                },
                "eventGroupID": "017676eb3de31cd31c0be96b965c2970",
                "origin": "ADMIN_CONSOLE",
                "target": {
                    "id": "yoururl.com",
                    "name": "yoururl.com",
                    "property": "MAGIC_DNS",
                    "type": "TAILNET",
                },
            },
            "fields": {"recorded": "2023-07-19 16:10:38.825360311"},
            "p_any_actor_ids": ["uodc9f3CNTRL"],
            "p_any_emails": ["homer.simpson@yourcompany.io"],
            "p_any_usernames": ["homer.simpson"],
            "p_event_time": "2023-07-19 16:10:38.365000",
            "p_log_type": "Tailscale.Audit",
            "p_parse_time": "2023-07-19 16:13:56.849016",
            "p_row_id": "5e197fb53834e39eeab7feb9198904",
            "p_schema_version": 0,
            "p_source_id": "5d65e24a-7ebb-403b-803c-51396e03d201",
            "p_source_label": "Tailscale Audit and Network Logs",
            "p_udm": {},
            "time": "2023-07-19 16:10:38.365000000",
        },
    ),
    PantherRuleTest(
        Name="Other Event",
        ExpectedResult=False,
        Log={
            "event": {
                "action": "CREATE",
                "actor": {
                    "displayName": "Homer Simpson",
                    "id": "uodc9f3CNTRL",
                    "loginName": "homer.simpson@yourcompany.io",
                    "type": "USER",
                },
                "eventGroupID": "9f880e02981e341447958344b7b4071f",
                "new": {},
                "origin": "ADMIN_CONSOLE",
                "target": {"id": "k6r3fm3CNTRL", "name": "API key", "type": "API_KEY"},
            },
            "fields": {"recorded": "2023-07-19 16:11:41.778839718"},
            "p_any_actor_ids": ["uodc9f3CNTRL"],
            "p_any_emails": ["homer.simpson@yourcompany.io"],
            "p_any_usernames": ["homersimpson"],
            "p_event_time": "2023-07-19 16:11:41.601000",
            "p_log_type": "Tailscale.Audit",
            "p_parse_time": "2023-07-19 16:14:56.865276",
            "p_row_id": "02eaf97ec9caaaabff8882ba19ad1d",
            "p_schema_version": 0,
            "p_source_id": "5d65e24a-7ebb-403b-803c-51396e03d201",
            "p_source_label": "Tailscale Audit and Network Logs",
            "p_udm": {},
            "time": "2023-07-19 16:11:41.601000000",
        },
    ),
]


class TailscaleMagicDNSDisabled(PantherRule):
    Description = "A Tailscale User disabled magic dns settings in your organization's tenant."
    DisplayName = "Tailscale Magic DNS Disabled"
    Runbook = "Assess if this was done by the user for a valid business reason. Be vigilant to re-enable this setting as it's in the best security interest for your organization's security posture."
    Reference = "https://tailscale.com/kb/1081/magicdns/"
    Severity = PantherSeverity.High
    LogTypes = [LogType.Tailscale_Audit]
    RuleID = "Tailscale.Magic.DNS.Disabled-prototype"
    Tests = tailscale_magic_dns_disabled_tests

    def rule(self, event):
        action = deep_get(event, "event", "action", default="<NO_ACTION_FOUND>")
        target_property = deep_get(
            event, "event", "target", "property", default="<NO_TARGET_PROPERTY_FOUND>"
        )
        return all(
            [
                action == "DISABLE",
                target_property == "MAGIC_DNS",
                is_tailscale_admin_console_event(event),
            ]
        )

    def title(self, event):
        user = deep_get(event, "event", "actor", "loginName", default="<NO_USER_FOUND>")
        target_id = deep_get(event, "event", "target", "id", default="<NO_TARGET_ID_FOUND>")
        return f"Tailscale user [{user}] disabled Magic DNS for [{target_id}] in your organization’s tenant."

    def alert_context(self, event):
        return tailscale_alert_context(event)

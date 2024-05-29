from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import deep_get
from pypanther.log_types import LogType

asana_team_privacy_public_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Team made public",
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
            "created_at": "2022-12-16 19:35:21.026",
            "details": {"new_value": "public"},
            "event_category": "access_control",
            "event_type": "team_privacy_settings_changed",
            "gid": "12345",
            "resource": {"gid": "12345", "name": "Example Team Name", "resource_type": "team"},
            "p_log_type": "Asana.Audit",
        },
    ),
    PantherRuleTest(
        Name="Other event",
        ExpectedResult=False,
        Log={
            "actor": {
                "actor_type": "user",
                "email": "homer.simpsons@simpsons.com",
                "gid": "1234567890",
                "name": "Homer Simpson",
            },
            "context": {
                "client_ip_address": "1.2.3.4",
                "context_type": "web",
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            },
            "created_at": "2023-02-01 18:05:08.413",
            "details": {"method": ["SAML"]},
            "event_category": "logins",
            "event_type": "user_login_succeeded",
            "gid": "123456789",
            "resource": {
                "email": "homer.simpsons@simpsons.com",
                "gid": "1234567890",
                "name": "Homer Simpson",
                "resource_type": "user",
            },
            "p_log_type": "Asana.Audit",
        },
    ),
]


class AsanaTeamPrivacyPublic(PantherRule):
    Description = "An Asana team's privacy setting was changed to public to the organization (not public to internet)"
    DisplayName = "Asana Team Privacy Public"
    Reference = "https://help.asana.com/hc/en-us/articles/14211433439387-Team-permissions"
    Severity = PantherSeverity.Low
    LogTypes = [LogType.Asana_Audit]
    RuleID = "Asana.Team.Privacy.Public-prototype"
    Tests = asana_team_privacy_public_tests

    def rule(self, event):
        return (
            event.get("event_type") == "team_privacy_settings_changed"
            and deep_get(event, "details", "new_value") == "public"
        )

    def title(self, event):
        team = deep_get(event, "resource", "name", default="<TEAM_NOT_FOUND>")
        actor = deep_get(event, "actor", "email", default="<ACTOR_NOT_FOUND>")
        return f"Asana team [{team}] has been made public to the org by [{actor}]."

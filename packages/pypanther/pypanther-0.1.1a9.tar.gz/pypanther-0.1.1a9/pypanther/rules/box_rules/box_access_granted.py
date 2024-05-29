from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import deep_get
from pypanther.log_types import LogType

box_access_granted_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Regular Event",
        ExpectedResult=False,
        Log={
            "type": "event",
            "additional_details": '{"key": "value"}',
            "created_by": {
                "id": "12345678",
                "type": "user",
                "login": "cat@example",
                "name": "Bob Cat",
            },
            "event_type": "DELETE",
        },
    ),
    PantherRuleTest(
        Name="Access Granted",
        ExpectedResult=True,
        Log={
            "type": "event",
            "additional_details": '{"key": "value"}',
            "created_by": {
                "id": "12345678",
                "type": "user",
                "login": "cat@example",
                "name": "Bob Cat",
            },
            "event_type": "ACCESS_GRANTED",
            "source": {
                "id": "12345678",
                "type": "user",
                "login": "user@example",
                "name": "Bob Cat",
            },
        },
    ),
]


class BoxAccessGranted(PantherRule):
    RuleID = "Box.Access.Granted-prototype"
    DisplayName = "Box Access Granted"
    LogTypes = [LogType.Box_Event]
    Tags = ["Box"]
    Severity = PantherSeverity.Low
    Description = "A user granted access to their box account to Box technical support from account settings.\n"
    Reference = "https://support.box.com/hc/en-us/articles/7039943421715-Enabling-and-Disabling-Access-for-Box-Support"
    Runbook = "Investigate whether the user purposefully granted access to their account.\n"
    SummaryAttributes = ["p_any_ip_addresses"]
    Tests = box_access_granted_tests

    def rule(self, event):
        return event.get("event_type") == "ACCESS_GRANTED"

    def title(self, event):
        return f"User [{deep_get(event, 'created_by', 'name', default='<UNKNOWN_USER>')}] granted access to their account"

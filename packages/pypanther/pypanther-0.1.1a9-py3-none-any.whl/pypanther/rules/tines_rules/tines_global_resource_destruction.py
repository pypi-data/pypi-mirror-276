from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import deep_get
from pypanther.helpers.panther_tines_helpers import tines_alert_context
from pypanther.log_types import LogType

tines_global_resource_destruction_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Detection Trigger",
        ExpectedResult=True,
        Log={
            "created_at": "2023-06-13 15:14:46",
            "id": 1234,
            "operation_name": "GlobalResourceDestruction",
            "p_source_label": "tines-log-source-name",
            "request_ip": "98.224.225.84",
            "request_user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (  KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "tenant_id": "1337",
            "user_email": "user@email.com",
            "user_id": "7331",
            "user_name": "Tines User Person",
        },
    ),
    PantherRuleTest(
        Name="Tines Login",
        ExpectedResult=False,
        Log={
            "created_at": "2023-05-17 14:45:19",
            "id": 7888888,
            "operation_name": "Login",
            "p_source_label": "tines-log-source-name",
            "request_ip": "12.12.12.12",
            "request_user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "tenant_id": "8888",
            "user_email": "user@company.com",
            "user_id": "17171",
            "user_name": "user at company dot com",
        },
    ),
]


class TinesGlobalResourceDestruction(PantherRule):
    RuleID = "Tines.Global.Resource.Destruction-prototype"
    DisplayName = "Tines Global Resource Destruction"
    SummaryAttributes = ["user_id", "operation_name", "tenant_id", "request_ip"]
    LogTypes = [LogType.Tines_Audit]
    Tags = ["Tines"]
    Severity = PantherSeverity.Low
    Description = "A Tines user has destroyed a global resource."
    Runbook = "Possible data destruction. Please reach out to the user and confirm this was done for valid business reasons."
    Reference = "https://www.tines.com/docs/resources"
    Tests = tines_global_resource_destruction_tests

    def rule(self, event):
        return (
            deep_get(event, "operation_name", default="<NO_OPERATION_NAME>")
            == "GlobalResourceDestruction"
        )

    def title(self, event):
        operation = deep_get(event, "operation_name", default="<NO_OPERATION_NAME>")
        user = deep_get(event, "user_email", default="<NO_USER_EMAIL>")
        tines_instance = deep_get(event, "p_source_label", default="<NO_SOURCE_LABEL>")
        return f"Tines [{operation}] performed by [{user}] on [{tines_instance}]."

    def alert_context(self, event):
        return tines_alert_context(event)

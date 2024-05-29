from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import deep_walk
from pypanther.log_types import LogType

netskope_unauthorized_api_calls_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="True positive",
        ExpectedResult=True,
        Log={
            "_id": "1e589befa3da30132362f32a",
            "_insertion_epoch_timestamp": 1702318213,
            "audit_log_event": "Rest API V2 Call",
            "count": 1,
            "is_netskope_personnel": False,
            "organization_unit": "",
            "severity_level": 2,
            "supporting_data": {
                "data_type": "incidents",
                "data_values": [
                    403,
                    "POST",
                    "/api/v2/incidents/uba/getuci",
                    "trid=ccb898fgrhvdd0v0lebg",
                ],
            },
            "timestamp": "2023-12-11 18:10:13.000000000",
            "type": "admin_audit_logs",
            "ur_normalized": "service-account",
            "user": "service-account",
        },
    ),
    PantherRuleTest(
        Name="True negative",
        ExpectedResult=False,
        Log={
            "_id": "1e589befa3da30132362f32a",
            "_insertion_epoch_timestamp": 1702318213,
            "audit_log_event": "Rest API V2 Call",
            "count": 1,
            "is_netskope_personnel": False,
            "organization_unit": "",
            "severity_level": 2,
            "supporting_data": {
                "data_type": "incidents",
                "data_values": [
                    200,
                    "POST",
                    "/api/v2/incidents/uba/getuci",
                    "trid=ccb898fgrhvdd0v0lebg",
                ],
            },
            "timestamp": "2023-12-11 18:10:13.000000000",
            "type": "admin_audit_logs",
            "ur_normalized": "service-account",
            "user": "service-account",
        },
    ),
]


class NetskopeUnauthorizedAPICalls(PantherRule):
    RuleID = "Netskope.UnauthorizedAPICalls-prototype"
    DisplayName = "Netskope Many Unauthorized API Calls"
    LogTypes = [LogType.Netskope_Audit]
    Tags = ["Netskope", "Configuration Required", "Brute Force"]
    Reports = {"MITRE ATT&CK": ["TA0006:T1110"]}
    Severity = PantherSeverity.High
    Description = "Many unauthorized API calls were observed for a user in a short period of time."
    Threshold = 10
    Runbook = "An account is making many unauthorized API calls.  This could indicate brute force activity, or expired service account credentials."
    Reference = "https://docs.netskope.com/en/netskope-help/data-security/netskope-private-access/private-access-rest-apis/"
    Tests = netskope_unauthorized_api_calls_tests

    def rule(self, event):
        data_values = deep_walk(event, "supporting_data", "data_values")
        if data_values and data_values[0] == 403:
            return True
        return False

    def title(self, event):
        user = event.get("user", "<USER_NOT_FOUND>")
        return f"Many unauthorized API calls from user [{user}]"

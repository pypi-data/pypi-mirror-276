from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import deep_get
from pypanther.helpers.panther_tines_helpers import tines_alert_context
from pypanther.log_types import LogType

tines_custom_certificate_authority_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Tines Login",
        ExpectedResult=False,
        Log={
            "created_at": "2023-05-17 14:45:19",
            "id": 7888888,
            "operation_name": "Login",
            "request_ip": "12.12.12.12",
            "request_user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "tenant_id": "8888",
            "user_email": "user@company.com",
            "user_id": "17171",
            "user_name": "user at company dot com",
        },
    ),
    PantherRuleTest(
        Name="Tines Custom CA set",
        ExpectedResult=True,
        Log={
            "created_at": "2023-05-18 22:54:11",
            "id": 7111111,
            "inputs": {},
            "operation_name": "CustomCertificateAuthoritySet",
            "request_ip": "12.12.12.12",
            "request_user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "tenant_id": "8888",
            "user_email": "user@company.com",
            "user_id": "17171",
            "user_name": "user at company dot com",
        },
    ),
]


class TinesCustomCertificateAuthority(PantherRule):
    RuleID = "Tines.Custom.CertificateAuthority-prototype"
    DisplayName = "Tines Custom CertificateAuthority setting changed"
    LogTypes = [LogType.Tines_Audit]
    Tags = ["Tines", "IAM - Credential Security"]
    Reference = "https://www.tines.com/docs/admin/custom-certificate-authority"
    Severity = PantherSeverity.High
    Description = "Detects when Tines Custom CertificateAuthority settings are changed\n"
    SummaryAttributes = ["user_id", "operation_name", "tenant_id", "request_ip"]
    Tests = tines_custom_certificate_authority_tests
    ACTIONS = ["CustomCertificateAuthoritySet"]

    def rule(self, event):
        action = deep_get(event, "operation_name", default="<NO_OPERATION_NAME>")
        return action in self.ACTIONS

    def title(self, event):
        action = deep_get(event, "operation_name", default="<NO_OPERATION_NAME>")
        return f"Tines: [{action}] by [{deep_get(event, 'user_email', default='<NO_USEREMAIL>')}]"

    def alert_context(self, event):
        return tines_alert_context(event)

    def dedup(self, event):
        return f"{deep_get(event, 'user_id', default='<NO_USERID>')}_{deep_get(event, 'operation_name', default='<NO_OPERATION>')}"

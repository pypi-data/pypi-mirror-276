from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.gcp_base_helpers import gcp_alert_context
from pypanther.helpers.panther_base_helpers import deep_walk
from pypanther.log_types import LogType

gcp_service_account_access_denied_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="service-account.access-denied-should-alert",
        ExpectedResult=True,
        Log={
            "insertid": "xxxxxxxxxxxx",
            "logname": "projects/test-project-123456/logs/cloudaudit.googleapis.com%2Factivity",
            "protoPayload": {
                "at_sign_type": "type.googleapis.com/google.cloud.audit.AuditLog",
                "authenticationInfo": {
                    "principalEmail": "test-no-perms@test-project-123456.iam.gserviceaccount.com",
                    "principalSubject": "serviceAccount:test-no-perms@test-project-123456.iam.gserviceaccount.com",
                    "serviceAccountKeyName": "//iam.googleapis.com/projects/test-project-123456/serviceAccounts/test-no-perms@test-project-123456.iam.gserviceaccount.com/keys/a0064fe0ef82b9e256b8b093d927ee842a19da34",
                },
                "authorizationInfo": [
                    {
                        "permission": "iam.serviceAccounts.create",
                        "resource": "projects/test-project-123456",
                        "resourceAttributes": {},
                    }
                ],
                "methodName": "google.iam.admin.v1.CreateServiceAccount",
                "request": {
                    "@type": "type.googleapis.com/google.iam.admin.v1.CreateServiceAccountRequest",
                    "account_id": "test123",
                    "name": "projects/test-project-123456",
                    "service_account": {},
                },
                "requestMetadata": {
                    "callerIP": "12.12.12.12",
                    "callerSuppliedUserAgent": "google-cloud-sdk gcloud/431.0.0 command/gcloud.iam.service-accounts.create invocation-id/b2ea5dab8c9b4bff8bc15ab299dff79e environment/devshell environment-version/None client-os/LINUX client-os-ver/5.15.107 client-pltf-arch/x86_64 interactive/True from-script/False python/3.9.2 term/screen (Linux 5.15.107+),gzip(gfe)",
                    "destinationAttributes": {},
                    "requestAttributes": {"auth": {}, "time": "2023-05-24T21:12:55.211301546Z"},
                },
                "resourceName": "projects/test-project-123456",
                "response": {"@type": "type.googleapis.com/google.iam.admin.v1.ServiceAccount"},
                "serviceName": "iam.googleapis.com",
                "status": {
                    "code": 7,
                    "details": [
                        {
                            "@type": "type.googleapis.com/google.rpc.ErrorInfo",
                            "domain": "iam.googleapis.com",
                            "metadata": {"permission": "iam.serviceAccounts.create"},
                            "reason": "IAM_PERMISSION_DENIED",
                        }
                    ],
                    "message": "Permission 'iam.serviceAccounts.create' denied on resource (or it may not exist).",
                },
            },
            "receivetimestamp": "2023-05-24 21:12:55.964",
            "resource": {
                "labels": {"email_id": "", "project_id": "test-project-123456", "unique_id": ""},
                "type": "service_account",
            },
            "severity": "ERROR",
            "timestamp": "2023-05-24 21:12:55.145",
        },
    ),
    PantherRuleTest(
        Name="service-account.access-grated-should-not-alert",
        ExpectedResult=False,
        Log={
            "insertId": "xxxxxxxxxxxx",
            "logName": "projects/test-project-123456/logs/cloudaudit.googleapis.com%2Factivity",
            "protoPayload": {
                "at_sign_type": "type.googleapis.com/google.cloud.audit.AuditLog",
                "authenticationInfo": {},
                "authorizationInfo": [
                    {
                        "granted": True,
                        "permission": "iam.serviceAccounts.create",
                        "resource": "projects/test-project-123456",
                        "resourceAttributes": {},
                    }
                ],
                "methodName": "google.iam.admin.v1.CreateServiceAccount",
                "request": {
                    "@type": "type.googleapis.com/google.iam.admin.v1.CreateServiceAccountRequest",
                    "account_id": "appengine-default",
                    "name": "projects/test-project-123456",
                    "service_account": {
                        "display_name": "App Engine default service account",
                        "email": "test-project-123456@appspot.gserviceaccount.com",
                    },
                },
                "requestMetadata": {
                    "callerIP": "private",
                    "destinationAttributes": {},
                    "requestAttributes": {"auth": {}, "time": "2023-05-23T19:27:42.510877536Z"},
                },
                "resourceName": "projects/test-project-123456",
                "response": {
                    "@type": "type.googleapis.com/google.iam.admin.v1.ServiceAccount",
                    "display_name": "App Engine default service account",
                    "email": "test-project-123456@appspot.gserviceaccount.com",
                    "etag": "MDEwMjE5MjA=",
                    "name": "projects/test-project-123456/serviceAccounts/test-project-123456@appspot.gserviceaccount.com",
                    "oauth2_client_id": "114240096070638624820",
                    "project_id": "test-project-123456",
                    "unique_id": "114240096070638624820",
                },
                "serviceName": "iam.googleapis.com",
                "status": {"message": "OK"},
            },
            "receiveTimestamp": "2023-05-23 19:27:44.037",
            "resource": {
                "labels": {
                    "email_id": "test-project-123456@appspot.gserviceaccount.com",
                    "project_id": "test-project-123456",
                    "unique_id": "114240096070638624820",
                },
                "type": "service_account",
            },
            "severity": "NOTICE",
            "timestamp": "2023-05-23 19:27:42.492",
        },
    ),
]


class GCPServiceAccountAccessDenied(PantherRule):
    DedupPeriodMinutes = 5
    Threshold = 30
    DisplayName = "GCP Service Account Access Denied"
    RuleID = "GCP.Service.Account.Access.Denied-prototype"
    Severity = PantherSeverity.Low
    LogTypes = [LogType.GCP_AuditLog]
    Tags = ["GCP", "Service Account", "Access"]
    Description = "This rule detects deletions of GCP Log Buckets or Sinks.\n"
    Runbook = "Ensure that the bucket or sink deletion was expected. Adversaries may do this to cover their tracks.\n"
    Reference = "https://cloud.google.com/iam/docs/service-account-overview"
    Tests = gcp_service_account_access_denied_tests

    def rule(self, event):
        reason = deep_walk(event, "protoPayload", "status", "details", "reason", default="")
        return reason == "IAM_PERMISSION_DENIED"

    def title(self, event):
        actor = deep_walk(
            event,
            "protoPayload",
            "authenticationInfo",
            "principalEmail",
            default="<ACTOR_NOT_FOUND>",
        )
        return f"[GCP]: [{actor}] performed multiple requests resulting in [IAM_PERMISSION_DENIED]"

    def alert_context(self, event):
        return gcp_alert_context(event)

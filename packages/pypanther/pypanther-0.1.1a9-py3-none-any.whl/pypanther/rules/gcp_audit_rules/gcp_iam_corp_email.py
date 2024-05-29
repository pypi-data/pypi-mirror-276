from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import deep_get
from pypanther.log_types import LogType

gcpiam_corporate_email_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Gmail account added",
        ExpectedResult=True,
        Log={
            "protoPayload": {
                "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
                "status": {},
                "authenticationInfo": {"principalEmail": "test@runpanther.com"},
                "requestMetadata": {
                    "callerIp": "136.24.229.58",
                    "callerSuppliedUserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36,gzip(gfe)",
                    "requestAttributes": {},
                    "destinationAttributes": {},
                },
                "serviceName": "cloudresourcemanager.googleapis.com",
                "methodName": "SetIamPolicy",
                "authorizationInfo": [
                    {
                        "resource": "projects/western-verve-123456",
                        "permission": "resourcemanager.projects.setIamPolicy",
                        "granted": True,
                        "resourceAttributes": {},
                    },
                    {
                        "resource": "projects/western-verve-123456",
                        "permission": "resourcemanager.projects.setIamPolicy",
                        "granted": True,
                        "resourceAttributes": {},
                    },
                ],
                "resourceName": "projects/western-verve-123456",
                "serviceData": {
                    "@type": "type.googleapis.com/google.iam.v1.logging.AuditData",
                    "policyDelta": {
                        "bindingDeltas": [
                            {
                                "action": "ADD",
                                "role": "roles/viewer",
                                "member": "user:username@gmail.com",
                            }
                        ]
                    },
                },
                "request": {
                    "resource": "western-verve-123456",
                    "@type": "type.googleapis.com/google.iam.v1.SetIamPolicyRequest",
                    "policy": {
                        "bindings": [
                            {
                                "members": ["user:user-two@gmail.com"],
                                "role": "roles/appengine.serviceAdmin",
                            },
                            {
                                "members": [
                                    "serviceAccount:service-951849100836@compute-system.iam.gserviceaccount.com"
                                ],
                                "role": "roles/compute.serviceAgent",
                            },
                            {
                                "role": "roles/editor",
                                "members": [
                                    "serviceAccount:951849100836-compute@developer.gserviceaccount.com",
                                    "serviceAccount:951849100836@cloudservices.gserviceaccount.com",
                                ],
                            },
                            {"members": ["user:test@runpanther.com"], "role": "roles/owner"},
                            {"members": ["user:user-two@gmail.com"], "role": "roles/pubsub.admin"},
                            {
                                "members": [
                                    "serviceAccount:pubsub-reader@western-verve-123456.iam.gserviceaccount.com"
                                ],
                                "role": "roles/pubsub.subscriber",
                            },
                            {
                                "members": [
                                    "serviceAccount:pubsub-reader@western-verve-123456.iam.gserviceaccount.com"
                                ],
                                "role": "roles/pubsub.viewer",
                            },
                            {
                                "role": "roles/resourcemanager.organizationAdmin",
                                "members": ["user:test@runpanther.com"],
                            },
                            {"members": ["user:username@gmail.com"], "role": "roles/viewer"},
                        ],
                        "etag": "BwWk8zJlg2o=",
                    },
                },
                "response": {
                    "etag": "BwWlp7rH6tY=",
                    "bindings": [
                        {
                            "members": ["user:user-two@gmail.com"],
                            "role": "roles/appengine.serviceAdmin",
                        },
                        {
                            "members": [
                                "serviceAccount:service-951849100836@compute-system.iam.gserviceaccount.com"
                            ],
                            "role": "roles/compute.serviceAgent",
                        },
                        {
                            "members": [
                                "serviceAccount:951849100836-compute@developer.gserviceaccount.com",
                                "serviceAccount:951849100836@cloudservices.gserviceaccount.com",
                            ],
                            "role": "roles/editor",
                        },
                        {"members": ["user:test@runpanther.com"], "role": "roles/owner"},
                        {"role": "roles/pubsub.admin", "members": ["user:user-two@gmail.com"]},
                        {
                            "role": "roles/pubsub.subscriber",
                            "members": [
                                "serviceAccount:pubsub-reader@western-verve-123456.iam.gserviceaccount.com"
                            ],
                        },
                        {
                            "members": [
                                "serviceAccount:pubsub-reader@western-verve-123456.iam.gserviceaccount.com"
                            ],
                            "role": "roles/pubsub.viewer",
                        },
                        {
                            "members": ["user:test@runpanther.com"],
                            "role": "roles/resourcemanager.organizationAdmin",
                        },
                        {"members": ["user:username@gmail.com"], "role": "roles/viewer"},
                    ],
                    "@type": "type.googleapis.com/google.iam.v1.Policy",
                },
            },
            "insertId": "mrbji0dal80",
            "resource": {"type": "project", "labels": {"project_id": "western-verve-123456"}},
            "timestamp": "2020-05-15T03:51:35.019Z",
            "severity": "NOTICE",
            "logName": "projects/western-verve-123456/logs/cloudaudit.googleapis.com%2Factivity",
            "receiveTimestamp": "2020-05-15T03:51:35.977314225Z",
        },
    ),
    PantherRuleTest(
        Name="Runpanther account added",
        ExpectedResult=False,
        Log={
            "protoPayload": {
                "@type": "type.googleapis.com/google.cloud.audit.AuditLog",
                "status": {},
                "authenticationInfo": {"principalEmail": "test@runpanther.com"},
                "requestMetadata": {
                    "callerIp": "136.24.229.58",
                    "callerSuppliedUserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36,gzip(gfe)",
                    "requestAttributes": {},
                    "destinationAttributes": {},
                },
                "serviceName": "cloudresourcemanager.googleapis.com",
                "methodName": "SetIamPolicy",
                "authorizationInfo": [
                    {
                        "resource": "projects/western-verve-123456",
                        "permission": "resourcemanager.projects.setIamPolicy",
                        "granted": True,
                        "resourceAttributes": {},
                    },
                    {
                        "resource": "projects/western-verve-123456",
                        "permission": "resourcemanager.projects.setIamPolicy",
                        "granted": True,
                        "resourceAttributes": {},
                    },
                ],
                "resourceName": "projects/western-verve-123456",
                "serviceData": {
                    "@type": "type.googleapis.com/google.iam.v1.logging.AuditData",
                    "policyDelta": {
                        "bindingDeltas": [
                            {
                                "action": "ADD",
                                "role": "roles/viewer",
                                "member": "user:username@runpanther.com",
                            }
                        ]
                    },
                },
                "request": {
                    "resource": "western-verve-123456",
                    "@type": "type.googleapis.com/google.iam.v1.SetIamPolicyRequest",
                    "policy": {
                        "bindings": [
                            {
                                "members": ["user:user-two@gmail.com"],
                                "role": "roles/appengine.serviceAdmin",
                            },
                            {
                                "members": [
                                    "serviceAccount:service-951849100836@compute-system.iam.gserviceaccount.com"
                                ],
                                "role": "roles/compute.serviceAgent",
                            },
                            {
                                "role": "roles/editor",
                                "members": [
                                    "serviceAccount:951849100836-compute@developer.gserviceaccount.com",
                                    "serviceAccount:951849100836@cloudservices.gserviceaccount.com",
                                ],
                            },
                            {"members": ["user:test@runpanther.com"], "role": "roles/owner"},
                            {"members": ["user:user-two@gmail.com"], "role": "roles/pubsub.admin"},
                            {
                                "members": [
                                    "serviceAccount:pubsub-reader@western-verve-123456.iam.gserviceaccount.com"
                                ],
                                "role": "roles/pubsub.subscriber",
                            },
                            {
                                "members": [
                                    "serviceAccount:pubsub-reader@western-verve-123456.iam.gserviceaccount.com"
                                ],
                                "role": "roles/pubsub.viewer",
                            },
                            {
                                "role": "roles/resourcemanager.organizationAdmin",
                                "members": ["user:test@runpanther.com"],
                            },
                            {"members": ["user:username@gmail.com"], "role": "roles/viewer"},
                        ],
                        "etag": "BwWk8zJlg2o=",
                    },
                },
                "response": {
                    "etag": "BwWlp7rH6tY=",
                    "bindings": [
                        {
                            "members": ["user:user-two@gmail.com"],
                            "role": "roles/appengine.serviceAdmin",
                        },
                        {
                            "members": [
                                "serviceAccount:service-951849100836@compute-system.iam.gserviceaccount.com"
                            ],
                            "role": "roles/compute.serviceAgent",
                        },
                        {
                            "members": [
                                "serviceAccount:951849100836-compute@developer.gserviceaccount.com",
                                "serviceAccount:951849100836@cloudservices.gserviceaccount.com",
                            ],
                            "role": "roles/editor",
                        },
                        {"members": ["user:test@runpanther.com"], "role": "roles/owner"},
                        {"role": "roles/pubsub.admin", "members": ["user:user-two@gmail.com"]},
                        {
                            "role": "roles/pubsub.subscriber",
                            "members": [
                                "serviceAccount:pubsub-reader@western-verve-123456.iam.gserviceaccount.com"
                            ],
                        },
                        {
                            "members": [
                                "serviceAccount:pubsub-reader@western-verve-123456.iam.gserviceaccount.com"
                            ],
                            "role": "roles/pubsub.viewer",
                        },
                        {
                            "members": ["user:test@runpanther.com"],
                            "role": "roles/resourcemanager.organizationAdmin",
                        },
                        {"members": ["user:username@gmail.com"], "role": "roles/viewer"},
                    ],
                    "@type": "type.googleapis.com/google.iam.v1.Policy",
                },
            },
            "insertId": "mrbji0dal80",
            "resource": {"type": "project", "labels": {"project_id": "western-verve-123456"}},
            "timestamp": "2020-05-15T03:51:35.019Z",
            "severity": "NOTICE",
            "logName": "projects/western-verve-123456/logs/cloudaudit.googleapis.com%2Factivity",
            "receiveTimestamp": "2020-05-15T03:51:35.977314225Z",
        },
    ),
]


class GCPIAMCorporateEmail(PantherRule):
    RuleID = "GCP.IAM.CorporateEmail-prototype"
    DisplayName = "GCP Corporate Email Not Used"
    DedupPeriodMinutes = 720
    LogTypes = [LogType.GCP_AuditLog]
    Tags = ["GCP", "Identity & Access Management", "Persistence:Create Account"]
    Reports = {"MITRE ATT&CK": ["TA0003:T1136"], "CIS": ["1.1"]}
    Severity = PantherSeverity.Low
    Description = "A Gmail account is being used instead of a corporate email"
    Runbook = "Remove the user"
    Reference = "https://cloud.google.com/iam/docs/service-account-overview"
    SummaryAttributes = ["severity", "p_any_ip_addresses", "p_any_domain_names"]
    Tests = gcpiam_corporate_email_tests

    def rule(self, event):
        if deep_get(event, "protoPayload", "methodName") != "SetIamPolicy":
            return False
        service_data = deep_get(event, "protoPayload", "serviceData")
        if not service_data:
            return False
        # Reference: bit.ly/2WsJdZS
        binding_deltas = deep_get(service_data, "policyDelta", "bindingDeltas")
        if not binding_deltas:
            return False
        for delta in binding_deltas:
            if delta.get("action") != "ADD":
                continue
            if delta.get("member", "").endswith("@gmail.com"):
                return True
        return False

    def title(self, event):
        return f"A GCP IAM account has been created with a Gmail email in {deep_get(event, 'resource', 'labels', 'project_id', default='<UNKNOWN_PROJECT>')}"

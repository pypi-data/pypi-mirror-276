from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import deep_get
from pypanther.log_types import LogType

gcpvpc_flow_logs_disabled_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Disable Flow Logs Event",
        ExpectedResult=True,
        Log={
            "insertId": "123456",
            "logName": "projects/gcp-project/logs/cloudaudit.googleapis.com%2Factivity",
            "operation": {
                "first": True,
                "id": "operation-abc-123",
                "last": True,
                "producer": "compute.googleapis.com",
            },
            "p_any_ip_addresses": ["1.2.3.4"],
            "p_event_time": "2023-03-08 18:52:58.322",
            "p_log_type": "GCP.AuditLog",
            "p_parse_time": "2023-03-08 18:54:14.597",
            "p_source_label": "gcplogsource",
            "protoPayload": {
                "at_sign_type": "type.googleapis.com/google.cloud.audit.AuditLog",
                "authenticationInfo": {"principalEmail": "user1@company.io"},
                "authorizationInfo": [
                    {
                        "granted": True,
                        "permission": "compute.subnetworks.update",
                        "resourceAttributes": {
                            "name": "projects/gcp-project/regions/us-central1/subnetworks/default",
                            "service": "compute",
                            "type": "compute.subnetworks",
                        },
                    }
                ],
                "methodName": "v1.compute.subnetworks.patch",
                "request": {
                    "@type": "type.googleapis.com/compute.subnetworks.patch",
                    "enableFlowLogs": False,
                    "fingerprint": "/�/��\x03��",
                },
                "requestMetadata": {
                    "callerIP": "1.2.3.4",
                    "callerSuppliedUserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36,gzip(gfe),gzip(gfe)",
                    "destinationAttributes": {},
                    "requestAttributes": {
                        "auth": {},
                        "reason": "8uSywAYQGg5Db2xpc2V1bSBGbG93cw",
                        "time": "2023-03-08T18:52:58.731721Z",
                    },
                },
                "resourceName": "projects/gcp-project/regions/us-central1/subnetworks/default",
                "response": {
                    "@type": "type.googleapis.com/operation",
                    "endTime": "2023-03-08T10:52:58.700-08:00",
                    "id": "123456",
                    "insertTime": "2023-03-08T10:52:58.699-08:00",
                    "name": "operation-1678301578299-5f668096688bc-0635b6ef-4d0122bb",
                    "operationType": "compute.subnetworks.patch",
                    "progress": "100",
                    "region": "https://www.googleapis.com/compute/v1/projects/gcp-project/regions/us-central1",
                    "selfLink": "https://www.googleapis.com/compute/v1/projects/gcp-project/regions/us-central1/operations/1234",
                    "selfLinkWithId": "https://www.googleapis.com/compute/v1/projects/gcp-project/regions/us-central1/operations/1234",
                    "startTime": "2023-03-08T10:52:58.700-08:00",
                    "status": "DONE",
                    "targetId": "123456",
                    "targetLink": "https://www.googleapis.com/compute/v1/projects/gcp-project/regions/us-central1/subnetworks/default",
                    "user": "user1@company.io",
                },
                "serviceName": "compute.googleapis.com",
            },
            "receiveTimestamp": "2023-03-08 18:52:58.991",
            "resource": {
                "labels": {
                    "location": "us-central1",
                    "project_id": "gcp-project",
                    "subnetwork_id": "123456",
                    "subnetwork_name": "default",
                },
                "type": "gce_subnetwork",
            },
            "severity": "NOTICE",
            "timestamp": "2023-03-08 18:52:58.322",
        },
    ),
    PantherRuleTest(
        Name="Enable Flow Logs Event",
        ExpectedResult=False,
        Log={
            "insertId": "12345",
            "logName": "projects/test-project/logs/cloudaudit.googleapis.com%2Factivity",
            "operation": {
                "first": True,
                "id": "operation-abcdefg-1234567",
                "last": True,
                "producer": "compute.googleapis.com",
            },
            "p_any_ip_addresses": ["1.2.3.4"],
            "p_event_time": "2023-03-08 18:52:52.114",
            "p_log_type": "GCP.AuditLog",
            "p_parse_time": "2023-03-08 18:54:14.595",
            "p_row_id": "5e7586fcbb73fdeed985ebeb16bd0c",
            "p_source_id": "4fc88a5a-2d51-4279-9c4a-08fa7cc52566",
            "p_source_label": "gcplogsource",
            "protoPayload": {
                "at_sign_type": "type.googleapis.com/google.cloud.audit.AuditLog",
                "authenticationInfo": {"principalEmail": "user1@company.io"},
                "authorizationInfo": [
                    {
                        "granted": True,
                        "permission": "compute.subnetworks.update",
                        "resourceAttributes": {
                            "name": "projects/test-project/regions/us-central1/subnetworks/default",
                            "service": "compute",
                            "type": "compute.subnetworks",
                        },
                    }
                ],
                "methodName": "v1.compute.subnetworks.patch",
                "request": {
                    "@type": "type.googleapis.com/compute.subnetworks.patch",
                    "fingerprint": "/�/��\x03��",
                    "logConfig": {"enable": True},
                },
                "requestMetadata": {
                    "callerIP": "1.2.3.4",
                    "callerSuppliedUserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36,gzip(gfe),gzip(gfe)",
                    "destinationAttributes": {},
                    "requestAttributes": {
                        "auth": {},
                        "reason": "8uSywAYQGg5Db2xpc2V1bSBGbG93cw",
                        "time": "2023-03-08T18:52:52.558899Z",
                    },
                },
                "resourceName": "projects/test-project/regions/us-central1/subnetworks/default",
                "response": {
                    "@type": "type.googleapis.com/operation",
                    "endTime": "2023-03-08T10:52:52.510-08:00",
                    "id": "9876543210",
                    "insertTime": "2023-03-08T10:52:52.509-08:00",
                    "name": "operation-abcdefg-1234567",
                    "operationType": "compute.subnetworks.patch",
                    "progress": "100",
                    "region": "https://www.googleapis.com/compute/v1/projects/test-project/regions/us-central1",
                    "selfLink": "https://www.googleapis.com/compute/v1/projects/test-project/regions/us-central1/operations/operation-abcdefg-1234567",
                    "selfLinkWithId": "https://www.googleapis.com/compute/v1/projects/test-project/regions/us-central1/operations/9876543210",
                    "startTime": "2023-03-08T10:52:52.510-08:00",
                    "status": "DONE",
                    "targetId": "567854321",
                    "targetLink": "https://www.googleapis.com/compute/v1/projects/test-project/regions/us-central1/subnetworks/default",
                    "user": "user1@company.io",
                },
                "serviceName": "compute.googleapis.com",
            },
            "receiveTimestamp": "2023-03-08 18:52:52.72",
            "resource": {
                "labels": {
                    "location": "us-central1",
                    "project_id": "test-project",
                    "subnetwork_id": "567854321",
                    "subnetwork_name": "default",
                },
                "type": "gce_subnetwork",
            },
            "severity": "NOTICE",
            "timestamp": "2023-03-08 18:52:52.114",
        },
    ),
]


class GCPVPCFlowLogsDisabled(PantherRule):
    Description = "VPC flow logs were disabled for a subnet."
    DisplayName = "GCP VPC Flow Logs Disabled"
    Reference = "https://cloud.google.com/vpc/docs/using-flow-logs"
    Severity = PantherSeverity.Medium
    LogTypes = [LogType.GCP_AuditLog]
    RuleID = "GCP.VPC.Flow.Logs.Disabled-prototype"
    Tests = gcpvpc_flow_logs_disabled_tests

    def rule(self, event):
        return all(
            [
                event.get("protoPayload"),
                deep_get(event, "protoPayload", "methodName", default="")
                == "v1.compute.subnetworks.patch",
                deep_get(event, "protoPayload", "request", "enableFlowLogs") is False,
            ]
        )

    def title(self, event):
        actor = deep_get(
            event,
            "protoPayload",
            "authenticationInfo",
            "principalEmail",
            default="<ACTOR_NOT_FOUND>",
        )
        resource = deep_get(event, "protoPayload", "resourceName", default="<RESOURCE_NOT_FOUND>")
        return f"GCP: [{actor}] disabled VPC Flow Logs for [{resource}]"

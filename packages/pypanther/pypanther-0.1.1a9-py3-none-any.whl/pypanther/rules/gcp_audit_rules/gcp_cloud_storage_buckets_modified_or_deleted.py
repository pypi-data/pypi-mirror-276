from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import deep_get
from pypanther.log_types import LogType

gcp_cloud_storage_buckets_modified_or_deleted_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="other event",
        ExpectedResult=False,
        Log={
            "insertid": "ezyd47c12y",
            "logname": "projects/gcp-project1/logs/cloudaudit.googleapis.com%2Factivity",
            "p_any_ip_addresses": ["1.2.3.4"],
            "p_event_time": "2023-03-09 16:41:30.524",
            "p_log_type": "GCP.AuditLog",
            "p_parse_time": "2023-03-09 16:44:14.617",
            "p_row_id": "1234567909689348911",
            "p_source_id": "4fc88a5a-2d51-4279-9c4a-08fa7cc52566",
            "p_source_label": "gcplogsource",
            "protoPayload": {
                "at_sign_type": "type.googleapis.com/google.cloud.audit.AuditLog",
                "authenticationInfo": {"principalEmail": "test@company.io"},
                "authorizationInfo": [
                    {
                        "granted": True,
                        "permission": "logging.sinks.update",
                        "resource": "projects/gcp-project1/sinks/log-sink",
                        "resourceAttributes": {
                            "name": "projects/gcp-project1/sinks/log-sink",
                            "service": "logging.googleapis.com",
                        },
                    }
                ],
                "methodName": "google.logging.v2.ConfigServiceV2.UpdateSink",
                "request": {
                    "@type": "type.googleapis.com/google.logging.v2.UpdateSinkRequest",
                    "sink": {
                        "destination": "pubsub.googleapis.com/projects/gcp-project1/topics/gcp-topic1",
                        "exclusions": [
                            {"filter": "protoPayload.serviceName = 'k8s.io", "name": "excludek8s"}
                        ],
                        "name": "log-sink",
                        "writerIdentity": "serviceAccount:p197946410614-915152@gcp-sa-logging.iam.gserviceaccount.com",
                    },
                    "sinkName": "projects/gcp-project1/sinks/log-sink",
                    "uniqueWriterIdentity": True,
                    "updateMask": "exclusions",
                },
                "requestMetadata": {
                    "callerIP": "1.2.3.4",
                    "callerSuppliedUserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36,gzip(gfe),gzip(gfe)",
                    "destinationAttributes": {},
                    "requestAttributes": {"auth": {}, "time": "2023-03-09T16:41:30.540045105Z"},
                },
                "resourceName": "projects/gcp-project1/sinks/log-sink",
                "serviceName": "logging.googleapis.com",
                "status": {},
            },
            "receivetimestamp": "2023-03-09 16:41:32.21",
            "resource": {
                "labels": {"destination": "", "name": "log-sink", "project_id": "gcp-project1"},
                "type": "logging_sink",
            },
            "severity": "NOTICE",
            "timestamp": "2023-03-09 16:41:30.524",
        },
    ),
    PantherRuleTest(
        Name="bucket update",
        ExpectedResult=True,
        Log={
            "insertId": "asdf1234asdfg",
            "logName": "projects/gcp-project1/logs/cloudaudit.googleapis.com%2Factivity",
            "p_any_ip_addresses": ["1.2.3.4"],
            "p_event_time": "2023-03-09 10:05:23.603",
            "p_log_type": "GCP.AuditLog",
            "p_parse_time": "2023-03-09 10:07:14.731",
            "p_row_id": "7ad218d42253b7e6f78cc0ed1635",
            "p_source_id": "4fc88a5a-2d51-4279-9c4a-08fa7cc52566",
            "p_source_label": "gcplogsource",
            "protoPayload": {
                "at_sign_type": "type.googleapis.com/google.cloud.audit.AuditLog",
                "authenticationInfo": {"principalEmail": "user@company.io"},
                "authorizationInfo": [
                    {
                        "granted": True,
                        "permission": "storage.buckets.update",
                        "resource": "projects/_/buckets/my-bucket",
                        "resourceAttributes": {},
                    }
                ],
                "methodName": "storage.buckets.update",
                "requestMetadata": {
                    "callerIP": "1.2.3.4",
                    "callerSuppliedUserAgent": "apitools Python/3.9.11 gsutil/5.11 (darwin) analytics/enabled interactive/True command/notification google-cloud-sdk/394.0.0,gzip(gfe)",
                    "destinationAttributes": {},
                    "requestAttributes": {"auth": {}, "time": "2023-03-09T10:05:23.610372568Z"},
                },
                "resourceName": "projects/_/buckets/my-bucket",
                "serviceName": "storage.googleapis.com",
                "status": {},
            },
            "receiveTimestamp": "2023-03-09 10:05:25.146",
            "resource": {
                "labels": {
                    "bucket_name": "my-bucket",
                    "location": "us-east1",
                    "project_id": "gcp-project1",
                },
                "type": "gcs_bucket",
            },
            "severity": "NOTICE",
            "timestamp": "2023-03-09 10:05:23.603",
        },
    ),
]


class GCPCloudStorageBucketsModifiedOrDeleted(PantherRule):
    Description = "Detects GCP cloud storage bucket updates and deletes."
    DisplayName = "GCP Cloud Storage Buckets Modified Or Deleted"
    Reference = "https://cloud.google.com/storage/docs/buckets"
    Severity = PantherSeverity.Low
    LogTypes = [LogType.GCP_AuditLog]
    RuleID = "GCP.Cloud.Storage.Buckets.Modified.Or.Deleted-prototype"
    Tests = gcp_cloud_storage_buckets_modified_or_deleted_tests
    BUCKET_OPERATIONS = ["storage.buckets.delete", "storage.buckets.update"]

    def rule(self, event):
        return all(
            [
                deep_get(event, "protoPayload", "serviceName", default="")
                == "storage.googleapis.com",
                deep_get(event, "protoPayload", "methodName", default="") in self.BUCKET_OPERATIONS,
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
        operation = deep_get(event, "protoPayload", "methodName", default="<OPERATION_NOT_FOUND>")
        project = deep_get(event, "resource", "labels", "project_id", default="<PROJECT_NOT_FOUND>")
        bucket = deep_get(event, "resource", "labels", "bucket_name", default="<BUCKET_NOT_FOUND>")
        return (
            f"GCP: [{actor}] performed a [{operation}] on bucket [{bucket}] in project [{project}]."
        )

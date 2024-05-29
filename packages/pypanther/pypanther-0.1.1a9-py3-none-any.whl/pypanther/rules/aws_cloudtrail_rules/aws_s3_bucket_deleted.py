from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import aws_rule_context, deep_get
from pypanther.helpers.panther_default import aws_cloudtrail_success
from pypanther.log_types import LogType

awss3_bucket_deleted_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="An S3 Bucket was deleted",
        ExpectedResult=True,
        Log={
            "eventVersion": "1.05",
            "errorCode": "",
            "userIdentity": {
                "type": "AssumedRole",
                "principalId": "AAAAAAAAAAAAAAAAAAAAA:user_name",
                "arn": "arn:aws:sts::123456789012:assumed-role/BucketAdministrator/user_name",
                "accountId": "123456789012",
                "accessKeyId": "AAAAAAAAAAAAAAAAAAAAA",
                "sessionContext": {
                    "attributes": {
                        "mfaAuthenticated": "true",
                        "creationDate": "2020-02-14T00:11:28Z",
                    },
                    "sessionIssuer": {
                        "type": "Role",
                        "principalId": "AAAAAAAAAAAAAAAAAAAAA",
                        "arn": "arn:aws:iam::123456789012:role/BucketAdministrator",
                        "accountId": "123456789012",
                        "userName": "BucketAdministrator",
                    },
                },
            },
            "eventTime": "2020-02-14T00:43:54Z",
            "eventSource": "s3.amazonaws.com",
            "eventName": "DeleteBucket",
            "awsRegion": "us-east-2",
            "sourceIPAddress": "157.130.196.214",
            "userAgent": "[S3Console/0.4, aws-internal/3 aws-sdk-java/1.11.666 Linux/4.9.184-0.1.ac.235.83.329.metal1.x86_64 OpenJDK_64-Bit_Server_VM/25.232-b09 java/1.8.0_232 vendor/Oracle_Corporation]",
            "requestParameters": {"host": ["s3-us-east-2.amazonaws.com"], "bucketName": "secrets"},
            "responseElements": None,
            "additionalEventData": {
                "SignatureVersion": "SigV4",
                "CipherSuite": "ECDHE-RSA-AES128-SHA",
                "AuthenticationMethod": "AuthHeader",
                "vpcEndpointId": "vpce-aaa333c9",
            },
            "requestID": "EEEE5AAAAAA44444",
            "eventID": "6795ef5c-7777-4444-8888-cabb7f252bd3",
            "eventType": "AwsApiCall",
            "recipientAccountId": "123456789012",
            "vpcEndpointId": "vpce-aaa333c9",
        },
    ),
    PantherRuleTest(
        Name="S3 Bucket Deletion Failed",
        ExpectedResult=False,
        Log={
            "eventName": "DeleteBucket",
            "errorCode": "BucketNotEmpty",
            "errorMessage": "The bucket you tried to delete is not empty",
            "awsRegion": "us-east-2",
            "sourceIPAddress": "157.130.196.214",
            "userAgent": "[S3Console/0.4, aws-internal/3 aws-sdk-java/1.11.666 Linux/4.9.184-0.1.ac.235.83.329.metal1.x86_64 OpenJDK_64-Bit_Server_VM/25.232-b09 java/1.8.0_232 vendor/Oracle_Corporation]",
            "responseElements": None,
            "requestID": "EEEE5AAAAAA44444",
            "userIdentity": {},
            "eventID": "6795ef5c-7777-4444-8888-cabb7f252bd3",
            "eventType": "AwsApiCall",
            "recipientAccountId": "123456789012",
            "vpcEndpointId": "vpce-aaa333c9",
        },
    ),
    PantherRuleTest(
        Name="An S3 Object Deleted",
        ExpectedResult=False,
        Log={
            "eventName": "DeleteObject",
            "awsRegion": "us-east-2",
            "sourceIPAddress": "157.130.196.214",
            "userAgent": "[S3Console/0.4, aws-internal/3 aws-sdk-java/1.11.666 Linux/4.9.184-0.1.ac.235.83.329.metal1.x86_64 OpenJDK_64-Bit_Server_VM/25.232-b09 java/1.8.0_232 vendor/Oracle_Corporation]",
            "responseElements": None,
            "requestID": "EEEE5AAAAAA44444",
            "eventID": "6795ef5c-7777-4444-8888-cabb7f252bd3",
            "userIdentity": {},
            "eventType": "AwsApiCall",
            "recipientAccountId": "123456789012",
            "vpcEndpointId": "vpce-aaa333c9",
        },
    ),
]


class AWSS3BucketDeleted(PantherRule):
    RuleID = "AWS.S3.BucketDeleted-prototype"
    DisplayName = "S3 Bucket Deleted"
    LogTypes = [LogType.AWS_CloudTrail]
    Tags = ["AWS", "Impact:Data Destruction"]
    Reports = {"MITRE ATT&CK": ["TA0040:T1485"]}
    Severity = PantherSeverity.Info
    Description = "A S3 Bucket, Policy, or Website was deleted"
    Runbook = "Explore if this bucket deletion was potentially destructive"
    Reference = "https://docs.aws.amazon.com/AmazonS3/latest/userguide/DeletingObjects.html"
    SummaryAttributes = ["sourceIpAddress", "userAgent", "recipientAccountId", "vpcEndpointId"]
    Tests = awss3_bucket_deleted_tests

    def rule(self, event):
        # Capture DeleteBucket, DeleteBucketPolicy, DeleteBucketWebsite
        return event.get("eventName").startswith("DeleteBucket") and aws_cloudtrail_success(event)

    def helper_strip_role_session_id(self, user_identity_arn):
        # The Arn structure is arn:aws:sts::123456789012:assumed-role/RoleName/<sessionId>
        arn_parts = user_identity_arn.split("/")
        if arn_parts:
            return "/".join(arn_parts[:2])
        return user_identity_arn

    def dedup(self, event):
        user_identity = event.get("userIdentity", {})
        if user_identity.get("type") == "AssumedRole":
            return self.helper_strip_role_session_id(user_identity.get("arn", ""))
        return user_identity.get("arn")

    def title(self, event):
        return f"{deep_get(event, 'userIdentity', 'type')} [{self.dedup(event)}] destroyed a bucket"

    def alert_context(self, event):
        return aws_rule_context(event)

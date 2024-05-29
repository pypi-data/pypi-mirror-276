from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import aws_rule_context
from pypanther.helpers.panther_default import aws_cloudtrail_success
from pypanther.log_types import LogType

aws_cloud_trail_iam_anything_changed_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="IAM Change",
        ExpectedResult=True,
        Log={
            "awsRegion": "us-east-1",
            "eventID": "1111",
            "eventName": "AttachRolePolicy",
            "eventSource": "iam.amazonaws.com",
            "eventTime": "2019-01-01T00:00:00Z",
            "eventType": "AwsApiCall",
            "eventVersion": "1.05",
            "recipientAccountId": "123456789012",
            "requestID": "1111",
            "requestParameters": {
                "policyArn": "arn:aws:iam::aws:policy/example-policy",
                "roleName": "LambdaFunctionRole-1111",
            },
            "responseElements": None,
            "sourceIPAddress": "111.111.111.111",
            "userAgent": "cloudformation.amazonaws.com",
            "userIdentity": {
                "accesKeyId": "1111",
                "accessKeyId": "1111",
                "accountId": "123456789012",
                "arn": "arn:aws:sts::123456789012:assumed-role/example-role/example-user",
                "invokedBy": "cloudformation.amazonaws.com",
                "principalId": "1111:example-user",
                "sessionContext": {
                    "attributes": {
                        "creationDate": "2019-01-01T00:00:00Z",
                        "mfaAuthenticated": "true",
                    },
                    "sessionIssuer": {
                        "accountId": "123456789012",
                        "arn": "arn:aws:iam::123456789012:role/example-role",
                        "principalId": "1111",
                        "type": "Role",
                        "userName": "example-user",
                    },
                },
                "type": "AssumedRole",
            },
        },
    ),
    PantherRuleTest(
        Name="IAM Read Only Activity",
        ExpectedResult=False,
        Log={
            "awsRegion": "us-east-1",
            "eventID": "1111",
            "eventName": "DescribePolicy",
            "eventSource": "iam.amazonaws.com",
            "eventTime": "2019-01-01T00:00:00Z",
            "eventType": "AwsApiCall",
            "eventVersion": "1.05",
            "recipientAccountId": "123456789012",
            "requestID": "1111",
            "requestParameters": {"roleName": "LambdaFunctionRole-1111"},
            "responseElements": None,
            "sourceIPAddress": "111.111.111.111",
            "userAgent": "cloudformation.amazonaws.com",
            "userIdentity": {
                "accesKeyId": "1111",
                "accessKeyId": "1111",
                "accountId": "123456789012",
                "arn": "arn:aws:sts::123456789012:assumed-role/example-role/example-user",
                "invokedBy": "cloudformation.amazonaws.com",
                "principalId": "1111:example-user",
                "sessionContext": {
                    "attributes": {
                        "creationDate": "2019-01-01T00:00:00Z",
                        "mfaAuthenticated": "true",
                    },
                    "sessionIssuer": {
                        "accountId": "123456789012",
                        "arn": "arn:aws:iam::123456789012:role/example-role",
                        "principalId": "1111",
                        "type": "Role",
                        "userName": "example-user",
                    },
                },
                "type": "AssumedRole",
            },
        },
    ),
    PantherRuleTest(
        Name="Error Making IAM Change",
        ExpectedResult=False,
        Log={
            "awsRegion": "us-east-1",
            "errorCode": "NoSuchEntity",
            "eventID": "1111",
            "eventName": "AttachRolePolicy",
            "eventSource": "iam.amazonaws.com",
            "eventTime": "2019-01-01T00:00:00Z",
            "eventType": "AwsApiCall",
            "eventVersion": "1.05",
            "recipientAccountId": "123456789012",
            "requestID": "1111",
            "requestParameters": {
                "policyArn": "arn:aws:iam::aws:policy/example-policy",
                "roleName": "LambdaFunctionRole-1111",
            },
            "responseElements": None,
            "sourceIPAddress": "111.111.111.111",
            "userAgent": "cloudformation.amazonaws.com",
            "userIdentity": {
                "accesKeyId": "1111",
                "accessKeyId": "1111",
                "accountId": "123456789012",
                "arn": "arn:aws:sts::123456789012:assumed-role/example-role/example-user",
                "invokedBy": "cloudformation.amazonaws.com",
                "principalId": "1111:example-user",
                "sessionContext": {
                    "attributes": {
                        "creationDate": "2019-01-01T00:00:00Z",
                        "mfaAuthenticated": "true",
                    },
                    "sessionIssuer": {
                        "accountId": "123456789012",
                        "arn": "arn:aws:iam::123456789012:role/example-role",
                        "principalId": "1111",
                        "type": "Role",
                        "userName": "example-user",
                    },
                },
                "type": "AssumedRole",
            },
        },
    ),
]


class AWSCloudTrailIAMAnythingChanged(PantherRule):
    RuleID = "AWS.CloudTrail.IAMAnythingChanged-prototype"
    DisplayName = "IAM Change"
    LogTypes = [LogType.AWS_CloudTrail]
    Tags = ["AWS", "Identity and Access Management"]
    Severity = PantherSeverity.Info
    DedupPeriodMinutes = 720
    Description = "A change occurred in the IAM configuration. This could be a resource being created, deleted, or modified. This is a high level view of changes, helfpul to indicate how dynamic a certain IAM environment is.\n"
    Runbook = "Ensure this was an approved IAM configuration change.\n"
    Reference = "https://docs.aws.amazon.com/IAM/latest/UserGuide/cloudtrail-integration.html"
    SummaryAttributes = [
        "eventName",
        "userAgent",
        "sourceIpAddress",
        "recipientAccountId",
        "p_any_aws_arns",
    ]
    Tests = aws_cloud_trail_iam_anything_changed_tests
    IAM_CHANGE_ACTIONS = [
        "Add",
        "Attach",
        "Change",
        "Create",
        "Deactivate",
        "Delete",
        "Detach",
        "Enable",
        "Put",
        "Remove",
        "Set",
        "Update",
        "Upload",
    ]

    def rule(self, event):
        # Only check IAM events, as the next check is relatively computationally
        # expensive and can often be skipped
        if not aws_cloudtrail_success(event) or event.get("eventSource") != "iam.amazonaws.com":
            return False
        return any(
            (event.get("eventName", "").startswith(action) for action in self.IAM_CHANGE_ACTIONS)
        )

    def alert_context(self, event):
        return aws_rule_context(event)

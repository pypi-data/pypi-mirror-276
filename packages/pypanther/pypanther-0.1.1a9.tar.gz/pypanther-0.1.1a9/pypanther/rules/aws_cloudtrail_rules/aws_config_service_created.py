from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import aws_rule_context
from pypanther.helpers.panther_default import aws_cloudtrail_success
from pypanther.log_types import LogType

aws_config_service_created_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Config Recorder Delivery Channel Created",
        ExpectedResult=True,
        Log={
            "eventVersion": "1.05",
            "userIdentity": {
                "type": "AssumedRole",
                "principalId": "1111:tester",
                "arn": "arn:aws:sts::123456789012:assumed-role/tester",
                "accountId": "123456789012",
                "accessKeyId": "1",
                "sessionContext": {
                    "sessionIssuer": {
                        "type": "Role",
                        "principalId": "1111",
                        "arn": "arn:aws:iam::123456789012:role/tester",
                        "accountId": "123456789012",
                        "userName": "tester",
                    },
                    "webIdFederationData": {},
                    "attributes": {
                        "mfaAuthenticated": "true",
                        "creationDate": "2019-01-01T00:00:00Z",
                    },
                },
            },
            "eventTime": "2019-01-01T00:00:00Z",
            "eventSource": "config.amazonaws.com",
            "eventName": "PutDeliveryChannel",
            "awsRegion": "us-west-2",
            "sourceIPAddress": "111.111.111.111",
            "userAgent": "console.amazonaws.com",
            "requestParameters": {"configurationRecorderName": "default"},
            "responseElements": None,
            "requestID": "1",
            "eventID": "1",
            "eventType": "AwsApiCall",
            "recipientAccountId": "123456789012",
        },
    ),
    PantherRuleTest(
        Name="Config Recorder Deleted",
        ExpectedResult=False,
        Log={
            "eventVersion": "1.05",
            "userIdentity": {
                "type": "AssumedRole",
                "principalId": "1111:tester",
                "arn": "arn:aws:sts::123456789012:assumed-role/tester",
                "accountId": "123456789012",
                "accessKeyId": "1",
                "sessionContext": {
                    "sessionIssuer": {
                        "type": "Role",
                        "principalId": "1111",
                        "arn": "arn:aws:iam::123456789012:role/tester",
                        "accountId": "123456789012",
                        "userName": "tester",
                    },
                    "webIdFederationData": {},
                    "attributes": {
                        "mfaAuthenticated": "true",
                        "creationDate": "2019-01-01T00:00:00Z",
                    },
                },
            },
            "eventTime": "2019-01-01T00:00:00Z",
            "eventSource": "config.amazonaws.com",
            "eventName": "DeleteDeliveryChannel",
            "awsRegion": "us-west-2",
            "sourceIPAddress": "111.111.111.111",
            "userAgent": "console.amazonaws.com",
            "requestParameters": {"configurationRecorderName": "default"},
            "responseElements": None,
            "requestID": "1",
            "eventID": "1",
            "eventType": "AwsApiCall",
            "recipientAccountId": "123456789012",
        },
    ),
    PantherRuleTest(
        Name="Error Creating Config Recorder Delivery Channel",
        ExpectedResult=False,
        Log={
            "eventVersion": "1.05",
            "errorCode": "InvalidDeliveryChannelNameException",
            "userIdentity": {
                "type": "AssumedRole",
                "principalId": "1111:tester",
                "arn": "arn:aws:sts::123456789012:assumed-role/tester",
                "accountId": "123456789012",
                "accessKeyId": "1",
                "sessionContext": {
                    "sessionIssuer": {
                        "type": "Role",
                        "principalId": "1111",
                        "arn": "arn:aws:iam::123456789012:role/tester",
                        "accountId": "123456789012",
                        "userName": "tester",
                    },
                    "webIdFederationData": {},
                    "attributes": {
                        "mfaAuthenticated": "true",
                        "creationDate": "2019-01-01T00:00:00Z",
                    },
                },
            },
            "eventTime": "2019-01-01T00:00:00Z",
            "eventSource": "config.amazonaws.com",
            "eventName": "PutDeliveryChannel",
            "awsRegion": "us-west-2",
            "sourceIPAddress": "111.111.111.111",
            "userAgent": "console.amazonaws.com",
            "requestParameters": {"configurationRecorderName": "default"},
            "responseElements": None,
            "requestID": "1",
            "eventID": "1",
            "eventType": "AwsApiCall",
            "recipientAccountId": "123456789012",
        },
    ),
]


class AWSConfigServiceCreated(PantherRule):
    RuleID = "AWS.ConfigService.Created-prototype"
    DisplayName = "AWS Config Service Created"
    LogTypes = [LogType.AWS_CloudTrail]
    Tags = ["AWS", "Security Control", "Discovery:Cloud Service Discovery"]
    Reports = {"CIS": ["3.9"], "MITRE ATT&CK": ["TA0007:T1526"]}
    Severity = PantherSeverity.Info
    Description = "An AWS Config Recorder or Delivery Channel was created\n"
    Runbook = "Verify that the Config Service changes were authorized. If not, revert them and investigate who caused the change. Consider altering permissions to prevent this from happening again in the future.\n"
    Reference = "https://aws.amazon.com/config/"
    SummaryAttributes = [
        "eventName",
        "userAgent",
        "sourceIpAddress",
        "recipientAccountId",
        "p_any_aws_arns",
    ]
    Tests = aws_config_service_created_tests
    # API calls that are indicative of an AWS Config Service change
    CONFIG_SERVICE_CREATE_EVENTS = {
        "PutDeliveryChannel",
        "PutConfigurationRecorder",
        "StartConfigurationRecorder",
    }

    def rule(self, event):
        return (
            aws_cloudtrail_success(event)
            and event.get("eventName") in self.CONFIG_SERVICE_CREATE_EVENTS
        )

    def alert_context(self, event):
        return aws_rule_context(event)

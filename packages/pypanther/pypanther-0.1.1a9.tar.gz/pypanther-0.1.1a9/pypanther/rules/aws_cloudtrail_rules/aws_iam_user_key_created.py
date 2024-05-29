from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import aws_rule_context, deep_get
from pypanther.helpers.panther_default import aws_cloudtrail_success
from pypanther.log_types import LogType

awsiam_backdoor_user_keys_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="user1 create keys for user1",
        ExpectedResult=False,
        Log={
            "awsRegion": "us-east-1",
            "eventCategory": "Management",
            "eventID": "12345",
            "eventName": "CreateAccessKey",
            "eventSource": "iam.amazonaws.com",
            "eventTime": "2022-09-27 17:09:18",
            "eventType": "AwsApiCall",
            "eventVersion": "1.08",
            "managementEvent": True,
            "readOnly": False,
            "recipientAccountId": "123456789",
            "requestParameters": {"userName": "user1"},
            "responseElements": {
                "accessKey": {
                    "accessKeyId": "ABCDEFG",
                    "createDate": "Sep 27, 2022 5:09:18 PM",
                    "status": "Active",
                    "userName": "user1",
                }
            },
            "sourceIPAddress": "cloudformation.amazonaws.com",
            "userAgent": "cloudformation.amazonaws.com",
            "userIdentity": {
                "accessKeyId": "ABCDEFGH",
                "accountId": "123456789",
                "arn": "arn:aws:iam::123456789:user/user1",
                "invokedBy": "cloudformation.amazonaws.com",
                "principalId": "ABCDEFGH",
                "sessionContext": {
                    "attributes": {
                        "creationDate": "2022-09-27T17:08:35Z",
                        "mfaAuthenticated": "false",
                    },
                    "sessionIssuer": {},
                    "webIdFederationData": {},
                },
                "type": "IAMUser",
                "userName": "user1",
            },
        },
    ),
    PantherRuleTest(
        Name="user1 create keys for user2",
        ExpectedResult=True,
        Log={
            "awsRegion": "us-east-1",
            "eventCategory": "Management",
            "eventID": "12345",
            "eventName": "CreateAccessKey",
            "eventSource": "iam.amazonaws.com",
            "eventTime": "2022-09-27 17:09:18",
            "eventType": "AwsApiCall",
            "eventVersion": "1.08",
            "managementEvent": True,
            "readOnly": False,
            "recipientAccountId": "123456789",
            "requestParameters": {"userName": "user2"},
            "responseElements": {
                "accessKey": {
                    "accessKeyId": "ABCDEFG",
                    "createDate": "Sep 27, 2022 5:09:18 PM",
                    "status": "Active",
                    "userName": "user2",
                }
            },
            "sourceIPAddress": "cloudformation.amazonaws.com",
            "userAgent": "cloudformation.amazonaws.com",
            "userIdentity": {
                "accessKeyId": "ABCDEFGH",
                "accountId": "123456789",
                "arn": "arn:aws:iam::123456789:user/user1",
                "invokedBy": "cloudformation.amazonaws.com",
                "principalId": "ABCDEFGH",
                "sessionContext": {
                    "attributes": {
                        "creationDate": "2022-09-27T17:08:35Z",
                        "mfaAuthenticated": "false",
                    },
                    "sessionIssuer": {},
                    "webIdFederationData": {},
                },
                "type": "IAMUser",
                "userName": "user1",
            },
        },
    ),
    PantherRuleTest(
        Name="jackson create keys for jack",
        ExpectedResult=True,
        Log={
            "awsRegion": "us-east-1",
            "eventCategory": "Management",
            "eventID": "12345",
            "eventName": "CreateAccessKey",
            "eventSource": "iam.amazonaws.com",
            "eventTime": "2022-09-27 17:09:18",
            "eventType": "AwsApiCall",
            "eventVersion": "1.08",
            "managementEvent": True,
            "readOnly": False,
            "recipientAccountId": "123456789",
            "requestParameters": {"userName": "jack"},
            "responseElements": {
                "accessKey": {
                    "accessKeyId": "ABCDEFG",
                    "createDate": "Sep 27, 2022 5:09:18 PM",
                    "status": "Active",
                    "userName": "jack",
                }
            },
            "sourceIPAddress": "cloudformation.amazonaws.com",
            "userAgent": "cloudformation.amazonaws.com",
            "userIdentity": {
                "accessKeyId": "ABCDEFGH",
                "accountId": "123456789",
                "arn": "arn:aws:iam::123456789:user/jackson",
                "invokedBy": "cloudformation.amazonaws.com",
                "principalId": "ABCDEFGH",
                "sessionContext": {
                    "attributes": {
                        "creationDate": "2022-09-27T17:08:35Z",
                        "mfaAuthenticated": "false",
                    },
                    "sessionIssuer": {},
                    "webIdFederationData": {},
                },
                "type": "IAMUser",
                "userName": "user1",
            },
        },
    ),
    PantherRuleTest(
        Name="jack create keys for jackson",
        ExpectedResult=True,
        Log={
            "awsRegion": "us-east-1",
            "eventCategory": "Management",
            "eventID": "12345",
            "eventName": "CreateAccessKey",
            "eventSource": "iam.amazonaws.com",
            "eventTime": "2022-09-27 17:09:18",
            "eventType": "AwsApiCall",
            "eventVersion": "1.08",
            "managementEvent": True,
            "readOnly": False,
            "recipientAccountId": "123456789",
            "requestParameters": {"userName": "jackson"},
            "responseElements": {
                "accessKey": {
                    "accessKeyId": "ABCDEFG",
                    "createDate": "Sep 27, 2022 5:09:18 PM",
                    "status": "Active",
                    "userName": "jackson",
                }
            },
            "sourceIPAddress": "cloudformation.amazonaws.com",
            "userAgent": "cloudformation.amazonaws.com",
            "userIdentity": {
                "accessKeyId": "ABCDEFGH",
                "accountId": "123456789",
                "arn": "arn:aws:iam::123456789:user/jack",
                "invokedBy": "cloudformation.amazonaws.com",
                "principalId": "ABCDEFGH",
                "sessionContext": {
                    "attributes": {
                        "creationDate": "2022-09-27T17:08:35Z",
                        "mfaAuthenticated": "false",
                    },
                    "sessionIssuer": {},
                    "webIdFederationData": {},
                },
                "type": "IAMUser",
                "userName": "user1",
            },
        },
    ),
    PantherRuleTest(
        Name="CreateKey returns error code",
        ExpectedResult=False,
        Log={
            "awsRegion": "us-east-1",
            "errorCode": "LimitExceededException",
            "errorMessage": "Cannot exceed quota for AccessKeysPerUser: 2",
            "eventCategory": "Management",
            "eventID": "efffffff-bbbb-4444-bbbb-ffffffffffff",
            "eventName": "CreateAccessKey",
            "eventSource": "iam.amazonaws.com",
            "eventTime": "2023-01-03 01:52:07.000000000",
            "eventType": "AwsApiCall",
            "eventVersion": "1.08",
            "managementEvent": True,
            "readOnly": False,
            "recipientAccountId": "123456789012",
            "requestID": "84eeeeee-eeee-eeee-eeee-eeeeeeeeeeee",
            "sourceIPAddress": "12.12.12.12",
            "tlsDetails": {
                "cipherSuite": "ECDHE-RSA-AES128-GCM-SHA256",
                "clientProvidedHostHeader": "iam.amazonaws.com",
                "tlsVersion": "TLSv1.2",
            },
            "userAgent": "aws-sdk-go-v2/1.14.0 os/macos lang/go/1.17.6 md/GOOS/darwin md/GOARCH/arm64 api/iam/1.17.0",
            "userIdentity": {
                "accessKeyId": "ASIA5ZXAKGI33TI7QQGW",
                "accountId": "123456789012",
                "arn": "arn:aws:iam::123456789012:user/some_iam_user",
                "principalId": "AIDA55555555555555555",
                "sessionContext": {
                    "attributes": {
                        "creationDate": "2023-01-03T01:52:07Z",
                        "mfaAuthenticated": "true",
                    },
                    "sessionIssuer": {},
                    "webIdFederationData": {},
                },
                "type": "IAMUser",
                "userName": "some_iam_user",
            },
        },
    ),
]


class AWSIAMBackdoorUserKeys(PantherRule):
    Description = "Detects AWS API key creation for a user by another user. Backdoored users can be used to obtain persistence in the AWS environment."
    DisplayName = "AWS User API Key Created"
    Reports = {"MITRE ATT&CK": ["TA0003:T1098", "TA0005:T1108", "TA0005:T1550", "TA0008:T1550"]}
    Reference = "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html"
    Severity = PantherSeverity.Medium
    LogTypes = [LogType.AWS_CloudTrail]
    RuleID = "AWS.IAM.Backdoor.User.Keys-prototype"
    Tests = awsiam_backdoor_user_keys_tests

    def rule(self, event):
        return (
            aws_cloudtrail_success(event)
            and event.get("eventSource") == "iam.amazonaws.com"
            and (event.get("eventName") == "CreateAccessKey")
            and (
                not deep_get(event, "userIdentity", "arn", default="").endswith(
                    f"user/{deep_get(event, 'responseElements', 'accessKey', 'userName', default='')}"
                )
            )
        )

    def title(self, event):
        return f"[{deep_get(event, 'userIdentity', 'arn')}] created API keys for [{deep_get(event, 'responseElements', 'accessKey', 'userName', default='')}]"

    def dedup(self, event):
        return f"{deep_get(event, 'userIdentity', 'arn')}"

    def alert_context(self, event):
        return aws_rule_context(event)

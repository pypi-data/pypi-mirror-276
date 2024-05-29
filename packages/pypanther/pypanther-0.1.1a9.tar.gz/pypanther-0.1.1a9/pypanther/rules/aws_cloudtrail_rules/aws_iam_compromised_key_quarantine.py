from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.log_types import LogType

aws_cloud_trail_iam_compromised_key_quarantine_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="AttachUserPolicy AWSCompromisedKeyQuarantineV2-true",
        ExpectedResult=True,
        Log={
            "eventVersion": "1.08",
            "userIdentity": {
                "type": "AssumedRole",
                "principalId": "FAKE_PRINCIPAL:user.name",
                "arn": "arn:aws:sts::123456789012:assumed-role/a-role/user.name",
                "accountId": "123456789012",
                "accessKeyId": "FAKE_ACCESS_KEY",
                "sessionContext": {
                    "sessionIssuer": {
                        "type": "Role",
                        "principalId": "FAKE_PRINCIPAL",
                        "arn": "arn:aws:iam::123456789012:role/a-role",
                        "accountId": "123456789012",
                        "userName": "a-role",
                    },
                    "webIdFederationData": {},
                    "attributes": {
                        "creationDate": "2023-11-21T22:28:31Z",
                        "mfaAuthenticated": "false",
                    },
                },
            },
            "eventTime": "2023-11-21T23:23:52Z",
            "eventSource": "iam.amazonaws.com",
            "eventName": "AttachUserPolicy",
            "awsRegion": "us-east-1",
            "sourceIPAddress": "1.2.3.4",
            "userAgent": "AWS Internal",
            "requestParameters": {
                "userName": "test-user",
                "policyArn": "arn:aws:iam::aws:policy/AWSCompromisedKeyQuarantineV2",
            },
            "responseElements": None,
            "requestID": "a2468e00-2b3c-4696-8056-327a624b5887",
            "eventID": "e7bb4b23-66e1-4656-b607-f575fde3b790",
            "readOnly": False,
            "eventType": "AwsApiCall",
            "managementEvent": True,
            "recipientAccountId": "123456789012",
            "eventCategory": "Management",
            "sessionCredentialFromConsole": "true",
        },
    ),
    PantherRuleTest(
        Name="PutUserPolicy-false",
        ExpectedResult=False,
        Log={
            "eventVersion": "1.08",
            "userIdentity": {
                "type": "AssumedRole",
                "principalId": "FAKE_PRINCIPAL:evan.gibler",
                "arn": "arn:aws:sts::123456789012:assumed-role/a-role/user.name",
                "accountId": "123456789012",
                "accessKeyId": "FAKE_ACCESS_KEY",
                "sessionContext": {
                    "sessionIssuer": {
                        "type": "Role",
                        "principalId": "FAKE_PRINCIPAL",
                        "arn": "arn:aws:iam::123456789012:role/a-role",
                        "accountId": "123456789012",
                        "userName": "a-role",
                    },
                    "webIdFederationData": {},
                    "attributes": {
                        "creationDate": "2023-11-21T22:28:31Z",
                        "mfaAuthenticated": "false",
                    },
                },
            },
            "eventTime": "2023-11-21T23:31:17Z",
            "eventSource": "iam.amazonaws.com",
            "eventName": "PutUserPolicy",
            "awsRegion": "us-east-1",
            "sourceIPAddress": "136.32.237.81",
            "userAgent": "AWS Internal",
            "requestParameters": {
                "userName": "test-user",
                "policyName": "TestUserDenyAll",
                "policyDocument": '{\n\t"Version": "2012-10-17",\n\t"Statement": [\n\t\t{\n\t\t\t"Sid": "TestUserDenyAll",\n\t\t\t"Effect": "Deny",\n\t\t\t"Action": ["*"],\n\t\t\t"Resource": ["*"]\n\t\t}\n\t]\n}',
            },
            "responseElements": None,
            "requestID": "2f59fa44-615c-40b7-a31f-01401e523663",
            "eventID": "7ee6ba6e-1943-417a-a6a3-3a2b0292cdac",
            "readOnly": False,
            "eventType": "AwsApiCall",
            "managementEvent": True,
            "recipientAccountId": "123456789012",
            "eventCategory": "Management",
            "sessionCredentialFromConsole": "true",
        },
    ),
]


class AWSCloudTrailIAMCompromisedKeyQuarantine(PantherRule):
    LogTypes = [LogType.AWS_CloudTrail]
    Description = "Detects when an IAM user has the AWSCompromisedKeyQuarantineV2 policy attached to their account."
    DisplayName = "AWS Compromised IAM Key Quarantine"
    RuleID = "AWS.CloudTrail.IAMCompromisedKeyQuarantine-prototype"
    Severity = PantherSeverity.High
    Tags = [
        "AWS",
        "Identity and Access Management",
        "Initial Access:Valid Accounts",
        "Credential Access:Unsecured Credentials",
    ]
    Reports = {"MITRE ATT&CK": ["TA0001:T1078.004", "TA0006:T1552.001"]}
    Runbook = "Check the quarantined IAM entity's key usage for signs of compromise and follow the instructions outlined in the AWS support case opened regarding this event.\n"
    Reference = "https://unit42.paloaltonetworks.com/malicious-operations-of-exposed-iam-keys-cryptojacking/"
    Tests = aws_cloud_trail_iam_compromised_key_quarantine_tests
    IAM_ACTIONS = {"AttachUserPolicy", "AttachGroupPolicy", "AttachRolePolicy"}
    QUARANTINE_MANAGED_POLICY = "arn:aws:iam::aws:policy/AWSCompromisedKeyQuarantineV2"

    def rule(self, event):
        return all(
            [
                event.get("eventSource", "") == "iam.amazonaws.com",
                event.get("eventName", "") in self.IAM_ACTIONS,
                event.deep_get("requestParameters", "policyArn", default="")
                == self.QUARANTINE_MANAGED_POLICY,
            ]
        )

    def title(self, event):
        account_id = event.deep_get("recipientAccountId", default="<ACCOUNT_ID_NOT_FOUND>")
        user_name = event.deep_get("requestParameters", "userName", default="<USER_NAME_NOT_FOUND>")
        return f"Compromised Key quarantined for [{user_name}] in AWS Account [{account_id}]"

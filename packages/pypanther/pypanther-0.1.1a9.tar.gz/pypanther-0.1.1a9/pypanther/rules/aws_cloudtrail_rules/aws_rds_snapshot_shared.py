from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import aws_rule_context
from pypanther.log_types import LogType

awsrds_snapshot_shared_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Snapshot shared with another account",
        ExpectedResult=True,
        Log={
            "eventVersion": "1.08",
            "userIdentity": {
                "type": "AssumedRole",
                "principalId": "AROA2DFDF0C1FDFCAD2B2:fake.user",
                "arn": "arn:aws:sts::123456789012:assumed-role/AWSReservedSSO_DevAdmin_635426549a280cc6/fake.user",
                "accountId": "123456789012",
                "accessKeyId": "ASIAFFA5AFEC02FFCD8ED",
                "sessionContext": {
                    "sessionIssuer": {
                        "type": "Role",
                        "principalId": "AROA2DFDF0C1FDFCAD2B2",
                        "arn": "arn:aws:iam::123456789012:role/aws-reserved/sso.amazonaws.com/us-west-2/AWSReservedSSO_DevAdmin_635426549a280cc6",
                        "accountId": "123456789012",
                        "userName": "AWSReservedSSO_DevAdmin_635426549a280cc6",
                    },
                    "webIdFederationData": {},
                    "attributes": {
                        "creationDate": "2023-12-12T19:43:57Z",
                        "mfaAuthenticated": "false",
                    },
                },
            },
            "eventTime": "2023-12-12T20:12:22Z",
            "eventSource": "rds.amazonaws.com",
            "eventName": "ModifyDBSnapshotAttribute",
            "awsRegion": "us-west-2",
            "sourceIPAddress": "1.2.3.4",
            "userAgent": "68319f60-9dec-43b2-9702-de3a08c9d8a3",
            "requestParameters": {
                "dBSnapshotIdentifier": "exfiltration",
                "attributeName": "restore",
                "valuesToAdd": ["193672423079"],
            },
            "responseElements": {
                "dBSnapshotIdentifier": "exfiltration",
                "dBSnapshotAttributes": [
                    {"attributeName": "restore", "attributeValues": ["193672423079"]}
                ],
            },
            "requestID": "b7f91314-eb8b-4be5-995d-6b97d70dfb3b",
            "eventID": "86581591-0f39-4eae-9a8d-b2224a3c91fa",
            "readOnly": False,
            "eventType": "AwsApiCall",
            "managementEvent": True,
            "recipientAccountId": "123456789012",
            "eventCategory": "Management",
            "tlsDetails": {
                "tlsVersion": "TLSv1.3",
                "cipherSuite": "TLS_AES_128_GCM_SHA256",
                "clientProvidedHostHeader": "rds.us-west-2.amazonaws.com",
            },
        },
    ),
    PantherRuleTest(
        Name="Snapshot shared with no accounts",
        ExpectedResult=False,
        Log={
            "eventVersion": "1.08",
            "userIdentity": {
                "type": "AssumedRole",
                "principalId": "AROA2DFDF0C1FDFCAD2B2:fake.user",
                "arn": "arn:aws:sts::123456789012:assumed-role/AWSReservedSSO_DevAdmin_635426549a280cc6/fake.user",
                "accountId": "123456789012",
                "accessKeyId": "ASIAFFA5AFEC02FFCD8ED",
                "sessionContext": {
                    "sessionIssuer": {
                        "type": "Role",
                        "principalId": "AROA2DFDF0C1FDFCAD2B2",
                        "arn": "arn:aws:iam::123456789012:role/aws-reserved/sso.amazonaws.com/us-west-2/AWSReservedSSO_DevAdmin_635426549a280cc6",
                        "accountId": "123456789012",
                        "userName": "AWSReservedSSO_DevAdmin_635426549a280cc6",
                    },
                    "webIdFederationData": {},
                    "attributes": {
                        "creationDate": "2023-12-12T19:43:57Z",
                        "mfaAuthenticated": "false",
                    },
                },
            },
            "eventTime": "2023-12-12T20:12:22Z",
            "eventSource": "rds.amazonaws.com",
            "eventName": "ModifyDBSnapshotAttribute",
            "awsRegion": "us-west-2",
            "sourceIPAddress": "1.2.3.4",
            "userAgent": "68319f60-9dec-43b2-9702-de3a08c9d8a3",
            "requestParameters": {
                "dBSnapshotIdentifier": "exfiltration",
                "attributeName": "restore",
                "valuesToAdd": [],
            },
            "responseElements": {
                "dBSnapshotIdentifier": "exfiltration",
                "dBSnapshotAttributes": [{"attributeName": "restore", "attributeValues": []}],
            },
            "requestID": "b7f91314-eb8b-4be5-995d-6b97d70dfb3b",
            "eventID": "86581591-0f39-4eae-9a8d-b2224a3c91fa",
            "readOnly": False,
            "eventType": "AwsApiCall",
            "managementEvent": True,
            "recipientAccountId": "123456789012",
            "eventCategory": "Management",
            "tlsDetails": {
                "tlsVersion": "TLSv1.3",
                "cipherSuite": "TLS_AES_128_GCM_SHA256",
                "clientProvidedHostHeader": "rds.us-west-2.amazonaws.com",
            },
        },
    ),
]


class AWSRDSSnapshotShared(PantherRule):
    RuleID = "AWS.RDS.SnapshotShared-prototype"
    DisplayName = "AWS RDS Snapshot Shared"
    LogTypes = [LogType.AWS_CloudTrail]
    Tags = ["AWS", "Exfiltration", "Transfer Data to Cloud Account"]
    Severity = PantherSeverity.High
    Reports = {"MITRE ATT&CK": ["TA0010:T1537"]}
    Description = "An RDS snapshot was shared with another account. This could be an indicator of exfiltration.\n"
    Runbook = "Ensure that the snapshot was shared intentionally and with an approved account. If not, remove the snapshot and quarantine the compromised IAM user.\n"
    Reference = "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ShareSnapshot.html"
    SummaryAttributes = ["eventSource", "recipientAccountId", "awsRegion", "p_any_aws_arns"]
    Tests = awsrds_snapshot_shared_tests

    def rule(self, event):
        if all(
            [
                event.get("eventSource", "") == "rds.amazonaws.com",
                event.get("eventName", "") == "ModifyDBSnapshotAttribute"
                or event.get("eventName", "") == "ModifyDBClusterSnapshotAttribute",
                event.deep_get("requestParameters", "attributeName") == "restore",
            ]
        ):
            current_account_id = event.deep_get("userIdentity", "accountId", default="")
            shared_account_ids = event.deep_get("requestParameters", "valuesToAdd", default=[])
            if shared_account_ids:
                return any(
                    (
                        account_id
                        for account_id in shared_account_ids
                        if account_id != current_account_id
                    )
                )
            return False
        return False

    def title(self, event):
        account_id = event.get("recipientAccountId", default="<ACCOUNT_ID_NOT_FOUND>")
        rds_instance_id = event.deep_get(
            "responseElements", "dBInstanceIdentifier", default="<DB_INSTANCE_ID_NOT_FOUND>"
        )
        return f"RDS Snapshot Shared in [{account_id}] for RDS instance [{rds_instance_id}]"

    def alert_context(self, event):
        return aws_rule_context(event)

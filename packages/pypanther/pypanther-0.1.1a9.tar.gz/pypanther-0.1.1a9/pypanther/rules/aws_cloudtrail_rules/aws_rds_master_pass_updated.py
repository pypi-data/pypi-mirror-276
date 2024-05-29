from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import deep_get
from pypanther.log_types import LogType

awsrds_master_password_updated_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Allocated storage modified",
        ExpectedResult=False,
        Log={
            "awsRegion": "us-west-1",
            "eventCategory": "Management",
            "eventID": "cb82857f-302d-4d6c-b516-589ec39dee7c",
            "eventName": "ModifyDBInstance",
            "eventSource": "rds.amazonaws.com",
            "eventTime": "2022-09-24 00:38:26",
            "eventType": "AwsApiCall",
            "eventVersion": "1.08",
            "managementEvent": True,
            "p_any_aws_account_ids": ["123456789012"],
            "p_any_aws_arns": [
                "arn:aws:iam::123456789012:role/Admin",
                "arn:aws:kms:us-west-1:123456789012:key/e2c16323-1c31-45fb-adda-07e5c9f78997",
                "arn:aws:rds:us-west-1:123456789012:db:my-database",
                "arn:aws:sts::123456789012:assumed-role/Admin/Jack",
            ],
            "p_any_domain_names": ["AWS Internal"],
            "p_any_trace_ids": ["ASIASWJRT64ZWCAMGCWI"],
            "p_event_time": "2022-09-24 00:38:26",
            "p_log_type": "AWS.CloudTrail",
            "p_parse_time": "2022-09-24 00:42:44.436",
            "p_row_id": "da110a31e6a4cfa7c8a888cb13f59305",
            "p_source_id": "125a8146-e3ea-454b-aed7-9e08e735b670",
            "p_source_label": "CloudTrail",
            "readOnly": False,
            "recipientAccountId": "123456789012",
            "requestID": "bd420698-bbb7-4ec3-b109-190e03adc1f4",
            "requestParameters": {
                "allocatedStorage": 22,
                "allowMajorVersionUpgrade": False,
                "applyImmediately": True,
                "dBInstanceIdentifier": "my-database",
                "maxAllocatedStorage": 1000,
            },
            "responseElements": {
                "allocatedStorage": 20,
                "associatedRoles": [],
                "autoMinorVersionUpgrade": True,
                "availabilityZone": "us-west-1b",
                "backupRetentionPeriod": 0,
                "backupTarget": "region",
                "cACertificateIdentifier": "rds-ca-2019",
                "copyTagsToSnapshot": True,
                "customerOwnedIpEnabled": False,
                "dBInstanceArn": "arn:aws:rds:us-west-1:123456789012:db:my-database",
                "dBInstanceClass": "db.t3.micro",
                "dBInstanceIdentifier": "my-database",
                "dBInstanceStatus": "available",
                "dBName": "test",
                "dBParameterGroups": [
                    {"dBParameterGroupName": "default.mysql8.0", "parameterApplyStatus": "in-sync"}
                ],
                "dBSecurityGroups": [],
                "dBSubnetGroup": {
                    "dBSubnetGroupDescription": "Created from the RDS Management Console",
                    "dBSubnetGroupName": "default-vpc-f9999999",
                    "subnetGroupStatus": "Complete",
                    "subnets": [
                        {
                            "subnetAvailabilityZone": {"name": "us-west-1c"},
                            "subnetIdentifier": "subnet-8cb458ea",
                            "subnetOutpost": {},
                            "subnetStatus": "Active",
                        },
                        {
                            "subnetAvailabilityZone": {"name": "us-west-1b"},
                            "subnetIdentifier": "subnet-8382bbd8",
                            "subnetOutpost": {},
                            "subnetStatus": "Active",
                        },
                    ],
                    "vpcId": "vpc-f9999999",
                },
                "dbInstancePort": 0,
                "dbiResourceId": "db-FEVDSUCWJ43PXONVT6ZU2TK4WY",
                "deletionProtection": False,
                "domainMemberships": [],
                "enabledCloudwatchLogsExports": ["audit", "error", "general"],
                "endpoint": {
                    "address": "my-database.cbsugyyyyyyy.us-west-1.rds.amazonaws.com",
                    "hostedZoneId": "Z10WI91S59XXQN",
                    "port": 3306,
                },
                "engine": "mysql",
                "engineVersion": "8.0.28",
                "httpEndpointEnabled": False,
                "iAMDatabaseAuthenticationEnabled": False,
                "instanceCreateTime": "Sep 23, 2022 11:25:46 PM",
                "kmsKeyId": "arn:aws:kms:us-west-1:123456789012:key/e2c16323-1c31-45fb-adda-07e5c9f78997",
                "licenseModel": "general-public-license",
                "masterUsername": "admin",
                "maxAllocatedStorage": 1000,
                "monitoringInterval": 0,
                "multiAZ": False,
                "networkType": "IPV4",
                "optionGroupMemberships": [
                    {"optionGroupName": "default:mysql-8-0", "status": "in-sync"}
                ],
                "pendingModifiedValues": {"allocatedStorage": 22},
                "performanceInsightsEnabled": False,
                "preferredBackupWindow": "11:52-12:22",
                "preferredMaintenanceWindow": "tue:13:03-tue:13:33",
                "publiclyAccessible": True,
                "readReplicaDBInstanceIdentifiers": [],
                "storageEncrypted": True,
                "storageThroughput": 0,
                "storageType": "gp2",
                "tagList": [],
                "vpcSecurityGroups": [{"status": "active", "vpcSecurityGroupId": "sg-d963a5a4"}],
            },
            "sessionCredentialFromConsole": True,
            "sourceIPAddress": "AWS Internal",
            "userAgent": "AWS Internal",
            "userIdentity": {
                "accessKeyId": "ASIASWJRT64ZWCAMGCWI",
                "accountId": "123456789012",
                "arn": "arn:aws:sts::123456789012:assumed-role/Admin/Jack",
                "principalId": "AROAJ4ULUNLE6DYF4PCOK:jack",
                "sessionContext": {
                    "attributes": {
                        "creationDate": "2022-09-23T23:17:13Z",
                        "mfaAuthenticated": "true",
                    },
                    "sessionIssuer": {
                        "accountId": "123456789012",
                        "arn": "arn:aws:iam::123456789012:role/Admin",
                        "principalId": "AROAJ4ULUNLE6DYF4PCOK",
                        "type": "Role",
                        "userName": "Admin",
                    },
                    "webIdFederationData": {},
                },
                "type": "AssumedRole",
            },
        },
    ),
    PantherRuleTest(
        Name="Master pass modified",
        ExpectedResult=True,
        Log={
            "awsRegion": "us-west-1",
            "eventCategory": "Management",
            "eventID": "09191e37-4632-4722-82bf-50288436cf47",
            "eventName": "ModifyDBInstance",
            "eventSource": "rds.amazonaws.com",
            "eventTime": "2022-09-24 00:28:15",
            "eventType": "AwsApiCall",
            "eventVersion": "1.08",
            "managementEvent": True,
            "p_any_aws_account_ids": ["123456789012"],
            "p_any_aws_arns": [
                "arn:aws:iam::123456789012:role/Admin",
                "arn:aws:kms:us-west-1:123456789012:key/e2c16323-1c31-45fb-adda-07e5c9f78997",
                "arn:aws:rds:us-west-1:123456789012:db:my-database",
                "arn:aws:sts::123456789012:assumed-role/Admin/Jack",
            ],
            "p_any_domain_names": ["AWS Internal"],
            "p_any_trace_ids": ["ASIASWJRT64ZWCAMGCWI"],
            "p_event_time": "2022-09-24 00:28:15",
            "p_log_type": "AWS.CloudTrail",
            "p_parse_time": "2022-09-24 00:32:43.679",
            "p_row_id": "eea2890fafffb7b88fae80cb138a08",
            "p_source_id": "b00eb354-da7a-49dd-9cc6-32535e32096a",
            "p_source_label": "CloudTrail",
            "readOnly": False,
            "recipientAccountId": "123456789012",
            "requestID": "93fba047-0282-4c53-b3a6-1c3bb684f563",
            "requestParameters": {
                "allowMajorVersionUpgrade": False,
                "applyImmediately": True,
                "dBInstanceIdentifier": "my-database",
                "masterUserPassword": "****",
                "maxAllocatedStorage": 1000,
            },
            "responseElements": {
                "allocatedStorage": 20,
                "associatedRoles": [],
                "autoMinorVersionUpgrade": True,
                "availabilityZone": "us-west-1b",
                "backupRetentionPeriod": 0,
                "backupTarget": "region",
                "cACertificateIdentifier": "rds-ca-2019",
                "copyTagsToSnapshot": True,
                "customerOwnedIpEnabled": False,
                "dBInstanceArn": "arn:aws:rds:us-west-1:123456789012:db:my-database",
                "dBInstanceClass": "db.t3.micro",
                "dBInstanceIdentifier": "my-database",
                "dBInstanceStatus": "available",
                "dBName": "test",
                "dBParameterGroups": [
                    {"dBParameterGroupName": "default.mysql8.0", "parameterApplyStatus": "in-sync"}
                ],
                "dBSecurityGroups": [],
                "dBSubnetGroup": {
                    "dBSubnetGroupDescription": "Created from the RDS Management Console",
                    "dBSubnetGroupName": "default-vpc-f9999999",
                    "subnetGroupStatus": "Complete",
                    "subnets": [
                        {
                            "subnetAvailabilityZone": {"name": "us-west-1c"},
                            "subnetIdentifier": "subnet-8cb458ea",
                            "subnetOutpost": {},
                            "subnetStatus": "Active",
                        },
                        {
                            "subnetAvailabilityZone": {"name": "us-west-1b"},
                            "subnetIdentifier": "subnet-8382bbd8",
                            "subnetOutpost": {},
                            "subnetStatus": "Active",
                        },
                    ],
                    "vpcId": "vpc-f9999999",
                },
                "dbInstancePort": 0,
                "dbiResourceId": "db-FEVDSUCWJ43PXONVT6ZU2TK4WY",
                "deletionProtection": False,
                "domainMemberships": [],
                "enabledCloudwatchLogsExports": ["audit", "error", "general"],
                "endpoint": {
                    "address": "my-database.cbsugyyyyyyy.us-west-1.rds.amazonaws.com",
                    "hostedZoneId": "Z10WI91S59XXQN",
                    "port": 3306,
                },
                "engine": "mysql",
                "engineVersion": "8.0.28",
                "httpEndpointEnabled": False,
                "iAMDatabaseAuthenticationEnabled": False,
                "instanceCreateTime": "Sep 23, 2022 11:25:46 PM",
                "kmsKeyId": "arn:aws:kms:us-west-1:123456789012:key/e2c16323-1c31-45fb-adda-07e5c9f78997",
                "licenseModel": "general-public-license",
                "masterUsername": "admin",
                "maxAllocatedStorage": 1000,
                "monitoringInterval": 0,
                "multiAZ": False,
                "networkType": "IPV4",
                "optionGroupMemberships": [
                    {"optionGroupName": "default:mysql-8-0", "status": "in-sync"}
                ],
                "pendingModifiedValues": {"masterUserPassword": "****"},
                "performanceInsightsEnabled": False,
                "preferredBackupWindow": "11:52-12:22",
                "preferredMaintenanceWindow": "tue:13:03-tue:13:33",
                "publiclyAccessible": True,
                "readReplicaDBInstanceIdentifiers": [],
                "storageEncrypted": True,
                "storageThroughput": 0,
                "storageType": "gp2",
                "tagList": [],
                "vpcSecurityGroups": [{"status": "active", "vpcSecurityGroupId": "sg-d963a5a4"}],
            },
            "sessionCredentialFromConsole": True,
            "sourceIPAddress": "AWS Internal",
            "userAgent": "AWS Internal",
            "userIdentity": {
                "accessKeyId": "ASIASWJRT64ZWCAMGCWI",
                "accountId": "123456789012",
                "arn": "arn:aws:sts::123456789012:assumed-role/Admin/Jack",
                "principalId": "AROAJ4ULUNLE6DYF4PCOK:jack",
                "sessionContext": {
                    "attributes": {
                        "creationDate": "2022-09-23T23:17:13Z",
                        "mfaAuthenticated": "true",
                    },
                    "sessionIssuer": {
                        "accountId": "123456789012",
                        "arn": "arn:aws:iam::123456789012:role/Admin",
                        "principalId": "AROAJ4ULUNLE6DYF4PCOK",
                        "type": "Role",
                        "userName": "Admin",
                    },
                    "webIdFederationData": {},
                },
                "type": "AssumedRole",
            },
        },
    ),
]


class AWSRDSMasterPasswordUpdated(PantherRule):
    Description = "A sensitive database operation that should be performed carefully or rarely"
    DisplayName = "AWS RDS Master Password Updated"
    Reference = (
        "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.DBInstance.Modifying.html"
    )
    Severity = PantherSeverity.Low
    Reports = {"MITRE ATT&CK": ["TA0003:T1098"]}
    SummaryAttributes = [
        "awsRegion",
        "userIdentity:arn",
        "responseElements:dBInstanceIdentifier",
        "p_any_aws_arns",
        "p_any_aws_account_ids",
    ]
    LogTypes = [LogType.AWS_CloudTrail]
    RuleID = "AWS.RDS.MasterPasswordUpdated-prototype"
    Tests = awsrds_master_password_updated_tests

    def rule(self, event):
        return (
            event.get("eventName") == "ModifyDBInstance"
            and event.get("eventSource") == "rds.amazonaws.com"
            and bool(
                deep_get(event, "responseElements", "pendingModifiedValues", "masterUserPassword")
            )
        )

    def title(self, event):
        return f"RDS Master Password Updated on [{deep_get(event, 'responseElements', 'dBInstanceArn')}]"

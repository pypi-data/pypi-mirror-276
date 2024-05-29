from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import aws_rule_context, deep_get
from pypanther.log_types import LogType

awsec2_traffic_mirroring_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="CreateTrafficMirrorFilter",
        ExpectedResult=True,
        Log={
            "awsRegion": "us-east-1",
            "eventCategory": "Management",
            "eventID": "a3c6297b-3320-4d32-b224-cc45ee75d561",
            "eventName": "CreateTrafficMirrorFilter",
            "eventSource": "ec2.amazonaws.com",
            "eventTime": "2022-11-15 22:58:13",
            "eventType": "AwsApiCall",
            "eventVersion": "1.08",
            "managementEvent": True,
            "p_any_aws_account_ids": ["123451234513"],
            "p_any_aws_arns": [
                "arn:aws:iam::123451234513:role/MakeStuffPublic",
                "arn:aws:sts::123451234513:assumed-role/MakeStuffPublic",
            ],
            "p_any_domain_names": ["AWS Internal"],
            "p_any_trace_ids": ["ASIA57JLR4M2ZZDJUXY3"],
            "p_any_usernames": ["MakeStuffPublic"],
            "p_event_time": "2022-11-15 22:58:13",
            "p_log_type": "AWS.CloudTrail",
            "p_parse_time": "2022-11-15 23:00:37.355",
            "p_row_id": "82670d2e7575bbd0e8fc97d014b5a80c",
            "p_source_id": "125a8146-e3ea-454b-aed7-9e08e735b670",
            "p_source_label": "Panther Identity Org CloudTrail",
            "readOnly": False,
            "recipientAccountId": "123451234515",
            "requestID": "200a9157-dff7-4578-87d6-205b01d90a56",
            "requestParameters": {
                "CreateTrafficMirrorFilterRequest": {
                    "ClientToken": "5b7eff74-2b70-4f92-8aa1-9c716bf151aa"
                }
            },
            "responseElements": {
                "CreateTrafficMirrorFilterResponse": {
                    "clientToken": "5b7eff74-2b70-4f92-8aa1-9c716bf151aa",
                    "requestId": "200a9157-dff7-4578-87d6-205b01d90a56",
                    "trafficMirrorFilter": {
                        "egressFilterRuleSet": "",
                        "ingressFilterRuleSet": "",
                        "networkServiceSet": "",
                        "tagSet": "",
                        "trafficMirrorFilterId": "tmf-010db9a7d8056cc2d",
                    },
                    "xmlns": "http://ec2.amazonaws.com/doc/2016-11-15/",
                }
            },
            "sessionCredentialFromConsole": True,
            "sourceIPAddress": "AWS Internal",
            "userAgent": "AWS Internal",
            "userIdentity": {
                "accessKeyId": "ASIA57JLR4M2ZZDJUXY3",
                "accountId": "123451234516",
                "arn": "arn:aws:sts::123123123123:assumed-role/MakeStuffPublic",
                "principalId": "AROA57JLR4M2SBAPVC4BO",
                "sessionContext": {
                    "attributes": {
                        "creationDate": "2022-11-15T22:38:17Z",
                        "mfaAuthenticated": "true",
                    },
                    "sessionIssuer": {
                        "accountId": "123123123123",
                        "arn": "arn:aws:iam::123123123123:role/MakeStuffPublic",
                        "principalId": "AROA57JLR4M2SBAPVC4BO",
                        "type": "Role",
                        "userName": "MakeStuffPublic",
                    },
                    "webIdFederationData": {},
                },
                "type": "AssumedRole",
            },
        },
    ),
    PantherRuleTest(
        Name="CreateTrafficMirrorFilterRule",
        ExpectedResult=True,
        Log={
            "awsRegion": "us-east-1",
            "eventCategory": "Management",
            "eventID": "61b6e2d6-788c-4b8d-9b6f-1ce17539e05e",
            "eventName": "CreateTrafficMirrorFilterRule",
            "eventSource": "ec2.amazonaws.com",
            "eventTime": "2022-11-15 22:58:13",
            "eventType": "AwsApiCall",
            "eventVersion": "1.08",
            "managementEvent": True,
            "p_any_aws_account_ids": ["123451234512"],
            "p_any_aws_arns": [
                "arn:aws:iam::123451234513:role/MakeStuffPublic",
                "arn:aws:sts::123451234513:assumed-role/MakeStuffPublic",
            ],
            "p_any_domain_names": ["AWS Internal"],
            "p_any_trace_ids": ["ASIA57JLR4M2ZZDJUXY3"],
            "p_any_usernames": ["MakeStuffPublic"],
            "p_event_time": "2022-11-15 22:58:13",
            "p_log_type": "AWS.CloudTrail",
            "p_parse_time": "2022-11-15 23:00:37.356",
            "p_row_id": "82670d2e7575bbd0e8fc97d014b6a80c",
            "p_source_id": "125a8146-e3ea-454b-aed7-9e08e735b670",
            "p_source_label": "Panther Identity Org CloudTrail",
            "readOnly": False,
            "recipientAccountId": "123451234566",
            "requestID": "92220f15-633f-4b9c-a544-57b9b8228ec3",
            "requestParameters": {
                "CreateTrafficMirrorFilterRuleRequest": {
                    "ClientToken": "b59974fd-e63c-489a-9011-4386f541e2e7",
                    "DestinationCidrBlock": "0.0.0.0/0",
                    "Protocol": 6,
                    "RuleAction": "accept",
                    "RuleNumber": 100,
                    "SourceCidrBlock": "0.0.0.0/0",
                    "TrafficDirection": "egress",
                    "TrafficMirrorFilterId": "tmf-010db9a7d8056cc2d",
                }
            },
            "responseElements": {
                "CreateTrafficMirrorFilterRuleResponse": {
                    "clientToken": "b59974fd-e63c-489a-9011-4386f541e2e7",
                    "requestId": "92220f15-633f-4b9c-a544-57b9b8228ec3",
                    "trafficMirrorFilterRule": {
                        "destinationCidrBlock": "0.0.0.0/0",
                        "protocol": 6,
                        "ruleAction": "accept",
                        "ruleNumber": 100,
                        "sourceCidrBlock": "0.0.0.0/0",
                        "trafficDirection": "egress",
                        "trafficMirrorFilterId": "tmf-010db9a7d8056cc2d",
                        "trafficMirrorFilterRuleId": "tmfr-01669e70d44b9705a",
                    },
                    "xmlns": "http://ec2.amazonaws.com/doc/2016-11-15/",
                }
            },
            "sessionCredentialFromConsole": True,
            "sourceIPAddress": "AWS Internal",
            "userAgent": "AWS Internal",
            "userIdentity": {
                "accessKeyId": "ASIA57JLR4M2ZZDJUXY3",
                "accountId": "123123123123",
                "arn": "arn:aws:sts::123123123123:assumed-role/MakeStuffPublic",
                "principalId": "AROA57JLR4M2SBAPVC4BO:MakeStuffPublic",
                "sessionContext": {
                    "attributes": {
                        "creationDate": "2022-11-15T22:38:17Z",
                        "mfaAuthenticated": "true",
                    },
                    "sessionIssuer": {
                        "accountId": "123123123123",
                        "arn": "arn:aws:iam::123123123123:role/MakeStuffPublic",
                        "principalId": "AROA57JLR4M2SBAPVC4BO",
                        "type": "Role",
                        "userName": "MakeStuffPublic",
                    },
                    "webIdFederationData": {},
                },
                "type": "AssumedRole",
            },
        },
    ),
    PantherRuleTest(
        Name="CreateTrafficMirrorSession",
        ExpectedResult=True,
        Log={
            "awsRegion": "us-east-1",
            "errorCode": "Client.NetworkInterfaceNotSupported",
            "errorMessage": "eni-0c61fbc84fca4138f must be attached to a supported instance",
            "eventCategory": "Management",
            "eventID": "5298b707-aa6b-4e4d-86c6-761ee19bb095",
            "eventName": "CreateTrafficMirrorSession",
            "eventSource": "ec2.amazonaws.com",
            "eventTime": "2022-11-15 22:58:35",
            "eventType": "AwsApiCall",
            "eventVersion": "1.08",
            "managementEvent": True,
            "p_any_aws_account_ids": ["123123123123"],
            "p_any_aws_arns": [
                "arn:aws:iam::123451234513:role/MakeStuffPublic",
                "arn:aws:sts::123451234513:assumed-role/MakeStuffPublic",
            ],
            "p_any_domain_names": ["AWS Internal"],
            "p_any_trace_ids": ["ASIA57JLR4M2ZZDJUXY3"],
            "p_any_usernames": ["MakeStuffPublic"],
            "p_event_time": "2022-11-15 22:58:35",
            "p_log_type": "AWS.CloudTrail",
            "p_parse_time": "2022-11-15 23:00:37.356",
            "p_row_id": "82670d2e7575bbd0e8fc97d014bba80c",
            "p_source_id": "125a8146-e3ea-454b-aed7-9e08e735b670",
            "p_source_label": "Panther Identity Org CloudTrail",
            "readOnly": False,
            "recipientAccountId": "123123123123",
            "requestID": "6eda0d2f-6688-4877-ae3d-0d982d7e7aaf",
            "requestParameters": {
                "CreateTrafficMirrorSessionRequest": {
                    "ClientToken": "c773e3fd-0611-4fb0-a436-67fbef29031e",
                    "NetworkInterfaceId": "eni-0c61fbc84fca4138f",
                    "SessionNumber": 1,
                    "TrafficMirrorFilterId": "tmf-010db9a7d8056cc2d",
                    "TrafficMirrorTargetId": "tmt-0fd4b591901182794",
                }
            },
            "sessionCredentialFromConsole": True,
            "sourceIPAddress": "AWS Internal",
            "userAgent": "AWS Internal",
            "userIdentity": {
                "accessKeyId": "ASIA57JLR4M2ZZDJUXY3",
                "accountId": "123123123123",
                "arn": "arn:aws:sts::123123123123:assumed-role/MakeStuffPublic",
                "principalId": "AROA57JLR4M2SBAPVC4BO:MakeStuffPublic",
                "sessionContext": {
                    "attributes": {
                        "creationDate": "2022-11-15T22:38:17Z",
                        "mfaAuthenticated": "true",
                    },
                    "sessionIssuer": {
                        "accountId": "123123123123",
                        "arn": "arn:aws:iam::123123123123:role/MakeStuffPublic",
                        "principalId": "AROA57JLR4M2SBAPVC4BO",
                        "type": "Role",
                        "userName": "MakeStuffPublic",
                    },
                    "webIdFederationData": {},
                },
                "type": "AssumedRole",
            },
        },
    ),
    PantherRuleTest(
        Name="CreateTrafficMirrorTarget",
        ExpectedResult=True,
        Log={
            "awsRegion": "us-east-1",
            "eventCategory": "Management",
            "eventID": "1ca9056c-efe7-4415-bb35-bbee893b9bd0",
            "eventName": "CreateTrafficMirrorTarget",
            "eventSource": "ec2.amazonaws.com",
            "eventTime": "2022-11-15 23:05:21",
            "eventType": "AwsApiCall",
            "eventVersion": "1.08",
            "managementEvent": True,
            "p_any_aws_account_ids": ["123123123123"],
            "p_any_aws_arns": [
                "arn:aws:iam::123451234513:role/MakeStuffPublic",
                "arn:aws:sts::123451234513:assumed-role/MakeStuffPublic",
            ],
            "p_any_domain_names": ["AWS Internal"],
            "p_any_trace_ids": ["ASIA57JLR4M2ZZDJUXY3"],
            "p_any_usernames": ["MakeStuffPublic"],
            "p_event_time": "2022-11-15 23:05:21",
            "p_log_type": "AWS.CloudTrail",
            "p_parse_time": "2022-11-15 23:07:31.858",
            "p_row_id": "de31c1202c72c6b6ff8698d014ba931a",
            "p_source_id": "125a8146-e3ea-454b-aed7-9e08e735b670",
            "p_source_label": "Panther Identity Org CloudTrail",
            "readOnly": False,
            "recipientAccountId": "123123123123",
            "requestID": "4698f691-c987-412d-b11d-e4aa285394d1",
            "requestParameters": {
                "CreateTrafficMirrorTargetRequest": {
                    "ClientToken": "fc50f178-783d-4420-b788-345988244b83",
                    "NetworkInterfaceId": "eni-0fd6cc8547555878f",
                }
            },
            "responseElements": {
                "CreateTrafficMirrorTargetResponse": {
                    "clientToken": "fc50f178-783d-4420-b788-345988244b83",
                    "requestId": "4698f691-c987-412d-b11d-e4aa285394d1",
                    "trafficMirrorTarget": {
                        "networkInterfaceId": "eni-0fd6cc8547555878f",
                        "ownerId": 123123123123.0,
                        "tagSet": "",
                        "trafficMirrorTargetId": "tmt-0a45c694b91bcea54",
                        "type": "network-interface",
                    },
                    "xmlns": "http://ec2.amazonaws.com/doc/2016-11-15/",
                }
            },
            "sessionCredentialFromConsole": True,
            "sourceIPAddress": "AWS Internal",
            "userAgent": "AWS Internal",
            "userIdentity": {
                "accessKeyId": "ASIA57JLR4M2ZZDJUXY3",
                "accountId": "123123123123",
                "arn": "arn:aws:sts::123123123123:assumed-role/MakeStuffPublic",
                "principalId": "AROA57JLR4M2SBAPVC4BO",
                "sessionContext": {
                    "attributes": {
                        "creationDate": "2022-11-15T22:38:17Z",
                        "mfaAuthenticated": "true",
                    },
                    "sessionIssuer": {
                        "accountId": "123123123123",
                        "arn": "arn:aws:iam::123123123123:role/MakeStuffPublic",
                        "principalId": "AROA57JLR4M2SBAPVC4BO",
                        "type": "Role",
                        "userName": "MakeStuffPublic",
                    },
                    "webIdFederationData": {},
                },
                "type": "AssumedRole",
            },
        },
    ),
    PantherRuleTest(
        Name="DeleteTrafficMirrorTarget",
        ExpectedResult=True,
        Log={
            "awsRegion": "us-east-1",
            "eventCategory": "Management",
            "eventID": "2212e8b1-b053-4388-9d3a-1bf963b1f075",
            "eventName": "DeleteTrafficMirrorTarget",
            "eventSource": "ec2.amazonaws.com",
            "eventTime": "2022-11-15 23:05:38",
            "eventType": "AwsApiCall",
            "eventVersion": "1.08",
            "managementEvent": True,
            "p_any_aws_account_ids": ["123123123123"],
            "p_any_aws_arns": [
                "arn:aws:iam::123451234513:role/MakeStuffPublic",
                "arn:aws:sts::123451234513:assumed-role/MakeStuffPublic",
            ],
            "p_any_domain_names": ["AWS Internal"],
            "p_any_trace_ids": ["ASIA57JLR4M2ZZDJUXY3"],
            "p_any_usernames": ["MakeStuffPublic"],
            "p_event_time": "2022-11-15 23:05:38",
            "p_log_type": "AWS.CloudTrail",
            "p_parse_time": "2022-11-15 23:07:31.858",
            "p_row_id": "de31c1202c72c6b6ff8698d014bf931a",
            "p_source_id": "125a8146-e3ea-454b-aed7-9e08e735b670",
            "p_source_label": "Panther Identity Org CloudTrail",
            "readOnly": False,
            "recipientAccountId": "123123123123",
            "requestID": "b56e2421-1fed-4052-b3ac-82daf374964c",
            "requestParameters": {
                "DeleteTrafficMirrorTargetRequest": {
                    "TrafficMirrorTargetId": "tmt-0fd4b591901182794"
                }
            },
            "responseElements": {
                "DeleteTrafficMirrorTargetResponse": {
                    "requestId": "b56e2421-1fed-4052-b3ac-82daf374964c",
                    "trafficMirrorTargetId": "tmt-0fd4b591901182794",
                    "xmlns": "http://ec2.amazonaws.com/doc/2016-11-15/",
                }
            },
            "sessionCredentialFromConsole": True,
            "sourceIPAddress": "AWS Internal",
            "userAgent": "AWS Internal",
            "userIdentity": {
                "accessKeyId": "ASIA57JLR4M2ZZDJUXY3",
                "accountId": "123123123123",
                "arn": "arn:aws:sts::123123123123:assumed-role/MakeStuffPublic",
                "principalId": "AROA57JLR4M2SBAPVC4BO",
                "sessionContext": {
                    "attributes": {
                        "creationDate": "2022-11-15T22:38:17Z",
                        "mfaAuthenticated": "true",
                    },
                    "sessionIssuer": {
                        "accountId": "123123123123",
                        "arn": "arn:aws:iam::123123123123:role/MakeStuffPublic",
                        "principalId": "AROA57JLR4M2SBAPVC4BO",
                        "type": "Role",
                        "userName": "MakeStuffPublic",
                    },
                    "webIdFederationData": {},
                },
                "type": "AssumedRole",
            },
        },
    ),
    PantherRuleTest(
        Name="DescribeTrafficMirrorTargets",
        ExpectedResult=True,
        Log={
            "awsRegion": "us-east-1",
            "eventCategory": "Management",
            "eventID": "43b5d650-dfdf-41a7-9b57-831e5cf1d190",
            "eventName": "DescribeTrafficMirrorTargets",
            "eventSource": "ec2.amazonaws.com",
            "eventTime": "2022-11-15 23:05:39",
            "eventType": "AwsApiCall",
            "eventVersion": "1.08",
            "managementEvent": True,
            "p_any_aws_account_ids": ["123123123123"],
            "p_any_aws_arns": [
                "arn:aws:iam::123451234513:role/MakeStuffPublic",
                "arn:aws:sts::123451234513:assumed-role/MakeStuffPublic",
            ],
            "p_any_domain_names": ["AWS Internal"],
            "p_any_trace_ids": ["ASIA57JLR4M2ZZDJUXY3"],
            "p_any_usernames": ["MakeStuffPublic"],
            "p_event_time": "2022-11-15 23:05:39",
            "p_log_type": "AWS.CloudTrail",
            "p_parse_time": "2022-11-15 23:07:31.858",
            "p_row_id": "de31c1202c72c6b6ff8698d014c0931a",
            "p_source_id": "125a8146-e3ea-454b-aed7-9e08e735b670",
            "p_source_label": "Panther Identity Org CloudTrail",
            "readOnly": True,
            "recipientAccountId": "123123123123",
            "requestID": "6aa42f9d-b623-4d7e-b1b5-1647ac4d7f8e",
            "requestParameters": {"DescribeTrafficMirrorTargetsRequest": {"MaxResults": 1000}},
            "sessionCredentialFromConsole": True,
            "sourceIPAddress": "AWS Internal",
            "userAgent": "AWS Internal",
            "userIdentity": {
                "accessKeyId": "ASIA57JLR4M2ZZDJUXY3",
                "accountId": "123123123123",
                "arn": "arn:aws:sts::123123123123:assumed-role/MakeStuffPublic",
                "principalId": "AROA57JLR4M2SBAPVC4BO",
                "sessionContext": {
                    "attributes": {
                        "creationDate": "2022-11-15T22:38:17Z",
                        "mfaAuthenticated": "true",
                    },
                    "sessionIssuer": {
                        "accountId": "123123123123",
                        "arn": "arn:aws:iam::123123123123:role/MakeStuffPublic",
                        "principalId": "AROA57JLR4M2SBAPVC4BO",
                        "type": "Role",
                        "userName": "MakeStuffPublic",
                    },
                    "webIdFederationData": {},
                },
                "type": "AssumedRole",
            },
        },
    ),
    PantherRuleTest(
        Name="ModifyTrafficMirrorSession",
        ExpectedResult=True,
        Log={
            "awsRegion": "us-east-1",
            "eventCategory": "Management",
            "eventID": "66c0fb61-804e-4cee-9f2e-c1d23c406a78",
            "eventName": "ModifyTrafficMirrorSession",
            "eventSource": "ec2.amazonaws.com",
            "eventTime": "2022-11-15 23:10:17",
            "eventType": "AwsApiCall",
            "eventVersion": "1.08",
            "managementEvent": True,
            "p_any_aws_account_ids": ["123123123123"],
            "p_any_aws_arns": [
                "arn:aws:iam::123451234513:role/MakeStuffPublic",
                "arn:aws:sts::123451234513:assumed-role/MakeStuffPublic",
            ],
            "p_any_domain_names": ["AWS Internal"],
            "p_any_trace_ids": ["ASIA57JLR4M2ZZDJUXY3"],
            "p_any_usernames": ["MakeStuffPublic"],
            "p_event_time": "2022-11-15 23:10:17",
            "p_log_type": "AWS.CloudTrail",
            "p_parse_time": "2022-11-15 23:13:49.967",
            "p_row_id": "9a217340fc13a7ff8b9b9ad014e0e205",
            "p_source_id": "125a8146-e3ea-454b-aed7-9e08e735b670",
            "p_source_label": "Panther Identity Org CloudTrail",
            "readOnly": False,
            "recipientAccountId": "123123123123",
            "requestID": "a39291d0-81b6-470f-ae0d-0f028d5676ce",
            "requestParameters": {
                "ModifyTrafficMirrorSessionRequest": {
                    "RemoveField": [
                        {"content": "description", "tag": 1},
                        {"content": "packet-length", "tag": 2},
                    ],
                    "SessionNumber": 2,
                    "TrafficMirrorFilterId": "tmf-010db9a7d8056cc2d",
                    "TrafficMirrorSessionId": "tms-05e1e21760419ecb6",
                    "TrafficMirrorTargetId": "tmt-0a45c694b91bcea54",
                    "VirtualNetworkId": 12348395.0,
                }
            },
            "responseElements": {
                "ModifyTrafficMirrorSessionResponse": {
                    "requestId": "a39291d0-81b6-470f-ae0d-0f028d5676ce",
                    "trafficMirrorSession": {
                        "networkInterfaceId": "eni-08dd7ebbda3b01770",
                        "ownerId": 123123123123.0,
                        "sessionNumber": 2,
                        "tagSet": "",
                        "trafficMirrorFilterId": "tmf-010db9a7d8056cc2d",
                        "trafficMirrorSessionId": "tms-05e1e21760419ecb6",
                        "trafficMirrorTargetId": "tmt-0a45c694b91bcea54",
                        "virtualNetworkId": 12348395.0,
                    },
                    "xmlns": "http://ec2.amazonaws.com/doc/2016-11-15/",
                }
            },
            "sessionCredentialFromConsole": True,
            "sourceIPAddress": "AWS Internal",
            "userAgent": "AWS Internal",
            "userIdentity": {
                "accessKeyId": "ASIA57JLR4M2ZZDJUXY3",
                "accountId": "123123123",
                "arn": "arn:aws:sts::123123123123:assumed-role/MakeStuffPublic",
                "principalId": "AROA57JLR4M2SBAPVC4BO",
                "sessionContext": {
                    "attributes": {
                        "creationDate": "2022-11-15T22:38:17Z",
                        "mfaAuthenticated": "true",
                    },
                    "sessionIssuer": {
                        "accountId": "123123123123",
                        "arn": "arn:aws:iam::123123123123:role/MakeStuffPublic",
                        "principalId": "AROA57JLR4M2SBAPVC4BO",
                        "type": "Role",
                        "userName": "MakeStuffPublic",
                    },
                    "webIdFederationData": {},
                },
                "type": "AssumedRole",
            },
        },
    ),
    PantherRuleTest(
        Name="UnrelatedEvent",
        ExpectedResult=False,
        Log={
            "awsRegion": "us-east-1",
            "eventCategory": "Management",
            "eventID": "982f8066-640d-40fb-b433-ba15e14fee40",
            "eventName": "UpdateProjectVisibility",
            "eventSource": "codebuild.amazonaws.com",
            "eventTime": "2021-08-18T14:54:53Z",
            "eventType": "AwsApiCall",
            "eventVersion": "1.08",
            "managementEvent": True,
            "readOnly": False,
            "recipientAccountId": "111122223333",
            "requestID": "4397365f-c790-4c23-9fe6-97e13a16ea84",
            "requestParameters": {
                "projectArn": "arn:aws:codebuild:us-east-1:111122223333:project/testproject1234",
                "projectVisibility": "PUBLIC_READ",
                "resourceAccessRole": "arn:aws:iam::111122223333:role/service-role/test",
            },
            "responseElements": None,
            "sourceIPAddress": "1.1.1.1",
            "userAgent": "aws-internal/3 aws-sdk-java/1.11.1030 Linux/5.4.116-64.217.amzn2int.x86_64 OpenJDK_64-Bit_Server_VM/25.302-b08 java/1.8.0_302 vendor/Oracle_Corporation cfg/retry-mode/legacy",
            "userIdentity": {
                "accessKeyId": "ASIAXXXXXXXXXXXX",
                "accountId": "111122223333",
                "arn": "arn:aws:sts::111122223333:assumed-role/MakeStuffPublic",
                "principalId": "111111111111",
                "sessionContext": {
                    "attributes": {
                        "creationDate": "2021-08-18T14:54:10Z",
                        "mfaAuthenticated": "false",
                    },
                    "sessionIssuer": {},
                    "webIdFederationData": {},
                },
                "type": "AssumedRole",
            },
        },
    ),
    PantherRuleTest(
        Name="AWS Config Runs DescribeTrafficMirrorTargets",
        ExpectedResult=False,
        Log={
            "awsRegion": "us-west-2",
            "eventCategory": "Management",
            "eventID": "c98e81a7-15ee-4888-bbbb-cccccccccccc",
            "eventName": "DescribeTrafficMirrorTargets",
            "eventSource": "ec2.amazonaws.com",
            "eventTime": "2023-02-10 18:08:33",
            "eventType": "AwsApiCall",
            "eventVersion": "1.08",
            "managementEvent": True,
            "readOnly": True,
            "recipientAccountId": "123456789012",
            "requestID": "1531eeee-5ddd-4fff-8111-844444444444",
            "requestParameters": {"DescribeTrafficMirrorTargetsRequest": {"MaxResults": 1000}},
            "sourceIPAddress": "config.amazonaws.com",
            "userAgent": "config.amazonaws.com",
            "userIdentity": {
                "accountId": "123456789012",
                "arn": "arn:aws:sts::123456789012:assumed-role/SomeAWSConfig/ConfigResourceCompositionSession",
                "invokedBy": "config.amazonaws.com",
                "principalId": "AROAAAAAAAAAAAAAAAAAA:ConfigResourceCompositionSession",
                "sessionContext": {
                    "attributes": {
                        "creationDate": "2023-02-13T18:08:33Z",
                        "mfaAuthenticated": "false",
                    },
                    "sessionIssuer": {
                        "accountId": "123456789012",
                        "arn": "arn:aws:iam::123456789012:role/PantherAWSConfig",
                        "principalId": "AROAAAAAAAAAAAAAAAAAA",
                        "type": "Role",
                        "userName": "PantherAWSConfig",
                    },
                    "webIdFederationData": {},
                },
                "type": "AssumedRole",
            },
        },
    ),
]


class AWSEC2TrafficMirroring(PantherRule):
    Description = "This rule captures multiple traffic mirroring events in AWS Cloudtrail."
    DisplayName = "AWS EC2 Traffic Mirroring"
    Reference = "https://attack.mitre.org/techniques/T1040/"
    Runbook = "Examine other activities done by this user to determine whether or not activity is suspicious. If your network traffic is not encrypted, we recommend changing the severity to high or critical."
    Severity = PantherSeverity.Medium
    Tags = ["AWS", "Cloudtrail", "MITRE"]
    LogTypes = [LogType.AWS_CloudTrail]
    RuleID = "AWS.EC2.Traffic.Mirroring-prototype"
    SummaryAttributes = ["userIdentity.type"]
    Tests = awsec2_traffic_mirroring_tests

    def rule(self, event):
        # Return True to match the log event and trigger an alert.
        event_names = [
            "CreateTrafficMirrorFilter",
            "CreateTrafficMirrorFilterRule",
            "CreateTrafficMirrorSession",
            "CreateTrafficMirrorTarget",
            "DeleteTrafficMirrorFilter",
            "DeleteTrafficMirrorFilterRule",
            "DeleteTrafficMirrorSession",
            "DeleteTrafficMirrorTarget",
            "DescribeTrafficMirrorFilters",
            "DescribeTrafficMirrorSessions",
            "DescribeTrafficMirrorTargets",
            "ModifyTrafficMirrorFilterNetworkServices",
            "ModifyTrafficMirrorFilterRule",
            "ModifyTrafficMirrorSession",
        ]
        if deep_get(event, "userIdentity", "invokedBy", default="").endswith(".amazonaws.com"):
            return False
        return (
            event.get("eventSource", "") == "ec2.amazonaws.com"
            and event.get("eventName", "") in event_names
        )

    def title(self, event):
        # (Optional) Return a string which will be shown as the alert title.
        # If no 'dedup' function is defined, the return value of this method will
        # act as deduplication string.
        return f"{event.get('userIdentity', {}).get('arn', 'no-type')} ec2 activity found for {event.get('eventName')} in account {event.get('recipientAccountId')} in region {event.get('awsRegion')}."

    def dedup(self, event):
        #  (Optional) Return a string which will be used to deduplicate similar alerts.
        # Dedupe based on user identity, to not include multiple events from the same identity.
        return f"{event.get('userIdentity', {}).get('arn', 'no-user-identity-provided')}"

    def alert_context(self, event):
        #  (Optional) Return a dictionary with additional data to be included
        #  in the alert sent to the SNS/SQS/Webhook destination
        return aws_rule_context(event)

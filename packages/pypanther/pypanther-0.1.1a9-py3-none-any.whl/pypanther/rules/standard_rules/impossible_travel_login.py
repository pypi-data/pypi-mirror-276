from datetime import datetime, timedelta
from json import dumps, loads
from typing import List

from panther_detection_helpers.caching import get_string_set, put_string_set

import pypanther.helpers.panther_event_type_helpers as event_type
from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity, RuleMock
from pypanther.helpers.panther_base_helpers import deep_get
from pypanther.helpers.panther_lookuptable_helpers import LookupTableMatches
from pypanther.helpers.panther_oss_helpers import km_between_ipinfo_loc, resolve_timestamp_string
from pypanther.log_types import LogType

standard_impossible_travel_login_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="CloudTrail not ConsoleLogin",
        ExpectedResult=False,
        Log={"eventType": "logout", "p_log_type": "AWS.CloudTrail"},
    ),
    PantherRuleTest(
        Name="CloudTrail ConsoleLogin no history",
        ExpectedResult=False,
        Mocks=[
            RuleMock(ObjectName="put_string_set", ReturnValue=""),
            RuleMock(ObjectName="get_string_set", ReturnValue=""),
        ],
        Log={
            "additionalEventData": {"MFAUsed": "No", "MobileVersion": "No"},
            "awsRegion": "us-east-1",
            "eventCategory": "Management",
            "eventName": "ConsoleLogin",
            "eventSource": "signin.amazonaws.com",
            "eventTime": "2023-05-26 20:14:51",
            "eventType": "AwsConsoleSignIn",
            "eventVersion": "1.08",
            "managementEvent": True,
            "p_event_time": "2023-05-26 20:14:51",
            "p_enrichment": {
                "ipinfo_location": {
                    "sourceIPAddress": {
                        "city": "Auckland",
                        "country": "NZ",
                        "lat": "-36.84853",
                        "lng": "174.76349",
                        "p_match": "12.12.12.12",
                        "postal_code": "1010",
                        "region": "Auckland",
                        "region_code": "AUK",
                        "timezone": "Pacific/Auckland",
                    }
                }
            },
            "p_log_type": "AWS.CloudTrail",
            "p_parse_time": "2023-05-26 20:19:14.002",
            "p_source_label": "LogSource Name",
            "readOnly": False,
            "recipientAccountId": "123456789012",
            "responseElements": {"ConsoleLogin": "Success"},
            "sourceIPAddress": "12.12.12.12",
            "tlsDetails": {
                "cipherSuite": "TLS_AES_128_GCM_SHA256",
                "clientProvidedHostHeader": "signin.aws.amazon.com",
                "tlsVersion": "TLSv1.3",
            },
            "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "userIdentity": {
                "type": "IAMUser",
                "principalId": "1111",
                "arn": "arn:aws:iam::123456789012:user/tester",
                "accountId": "123456789012",
                "userName": "tester",
            },
        },
    ),
    PantherRuleTest(
        Name="CloudTrail ConsoleLogin with history",
        ExpectedResult=True,
        Mocks=[
            RuleMock(ObjectName="put_string_set", ReturnValue=""),
            RuleMock(
                ObjectName="get_string_set",
                ReturnValue='[\n {\n  "p_event_time": "2023-05-26 18:14:51",\n  "city": "New York City",\n  "country": "US",\n  "lat": "40.71427",\n  "lng": "-74.00597",\n  "postal_code": "10004",\n  "region": "New York",\n  "region_code": "NY",\n  "timezone": "America/New_York"\n }\n]',
            ),
        ],
        Log={
            "additionalEventData": {"MFAUsed": "No", "MobileVersion": "No"},
            "awsRegion": "us-east-1",
            "eventCategory": "Management",
            "eventName": "ConsoleLogin",
            "eventSource": "signin.amazonaws.com",
            "eventTime": "2023-05-26 20:14:51",
            "eventType": "AwsConsoleSignIn",
            "eventVersion": "1.08",
            "managementEvent": True,
            "p_event_time": "2023-05-26 20:14:51",
            "p_enrichment": {
                "ipinfo_location": {
                    "sourceIPAddress": {
                        "city": "Auckland",
                        "country": "NZ",
                        "lat": "-36.84853",
                        "lng": "174.76349",
                        "p_match": "12.12.12.12",
                        "postal_code": "1010",
                        "region": "Auckland",
                        "region_code": "AUK",
                        "timezone": "Pacific/Auckland",
                    }
                }
            },
            "p_log_type": "AWS.CloudTrail",
            "p_parse_time": "2023-05-26 20:19:14.002",
            "p_source_label": "LogSource Name",
            "readOnly": False,
            "recipientAccountId": "123456789012",
            "responseElements": {"ConsoleLogin": "Success"},
            "sourceIPAddress": "12.12.12.12",
            "tlsDetails": {
                "cipherSuite": "TLS_AES_128_GCM_SHA256",
                "clientProvidedHostHeader": "signin.aws.amazon.com",
                "tlsVersion": "TLSv1.3",
            },
            "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "userIdentity": {
                "type": "IAMUser",
                "principalId": "1111",
                "arn": "arn:aws:iam::123456789012:user/tester",
                "accountId": "123456789012",
                "userName": "tester",
            },
        },
    ),
    PantherRuleTest(
        Name="Okta Not sign-in",
        ExpectedResult=False,
        Log={"eventType": "logout", "p_log_type": "Okta.SystemLog"},
    ),
    PantherRuleTest(
        Name="Okta sign-in with history and impossible travel",
        ExpectedResult=True,
        Mocks=[
            RuleMock(ObjectName="put_string_set", ReturnValue=""),
            RuleMock(
                ObjectName="get_string_set",
                ReturnValue='[\n {\n  "p_event_time": "2023-05-26 18:14:51",\n  "city": "New York City",\n  "country": "US",\n  "lat": "40.71427",\n  "lng": "-74.00597",\n  "postal_code": "10004",\n  "region": "New York",\n  "region_code": "NY",\n  "timezone": "America/New_York"\n }\n]',
            ),
        ],
        Log={
            "actor": {
                "alternateId": "homer.simpson@company.com",
                "displayName": "Homer Simpson",
                "id": "00uwuwuwuwuwuwuwuwuw",
                "type": "User",
            },
            "authenticationContext": {"authenticationStep": 0, "externalSessionId": "idx1234"},
            "client": {
                "device": "Computer",
                "ipAddress": "12.12.12.12",
                "userAgent": {
                    "browser": "CHROME",
                    "os": "Mac OS X",
                    "rawUserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                },
                "zone": "null",
            },
            "debugContext": {"debugData": {}},
            "device": {},
            "displayMessage": "User login to Okta",
            "eventType": "user.session.start",
            "legacyEventType": "core.user_auth.login_success",
            "outcome": {"result": "SUCCESS"},
            "p_event_time": "2023-05-26 20:18:51",
            "p_enrichment": {
                "ipinfo_location": {
                    "client.ipAddress": {
                        "city": "Auckland",
                        "country": "NZ",
                        "lat": "-36.84853",
                        "lng": "174.76349",
                        "p_match": "12.12.12.12",
                        "postal_code": "1010",
                        "region": "Auckland",
                        "region_code": "AUK",
                        "timezone": "Pacific/Auckland",
                    }
                }
            },
            "p_log_type": "Okta.SystemLog",
            "p_source_label": "Okta Logs",
            "p_parse_time": "2023-05-26 20:22:51.888",
            "published": "2023-05-26 20:18:51.888",
            "request": {"ipChain": []},
            "securityContext": {},
            "severity": "INFO",
            "target": [],
            "transaction": {},
            "uuid": "79999999-ffff-eeee-bbbb-222222222222",
            "version": "0",
        },
    ),
    PantherRuleTest(
        Name="Okta sign-in with history and impossible travel, Apple Private Relay",
        ExpectedResult=True,
        Mocks=[
            RuleMock(ObjectName="put_string_set", ReturnValue=""),
            RuleMock(
                ObjectName="get_string_set",
                ReturnValue='[\n {\n  "p_event_time": "2023-05-26 18:14:51",\n  "city": "New York City",\n  "country": "US",\n  "lat": "40.71427",\n  "lng": "-74.00597",\n  "postal_code": "10004",\n  "region": "New York",\n  "region_code": "NY",\n  "timezone": "America/New_York"\n }\n]',
            ),
        ],
        Log={
            "actor": {
                "alternateId": "homer.simpson@company.com",
                "displayName": "Homer Simpson",
                "id": "00uwuwuwuwuwuwuwuwuw",
                "type": "User",
            },
            "authenticationContext": {"authenticationStep": 0, "externalSessionId": "idx1234"},
            "client": {
                "device": "Computer",
                "ipAddress": "12.12.12.12",
                "userAgent": {
                    "browser": "CHROME",
                    "os": "Mac OS X",
                    "rawUserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                },
                "zone": "null",
            },
            "debugContext": {"debugData": {}},
            "device": {},
            "displayMessage": "User login to Okta",
            "eventType": "user.session.start",
            "legacyEventType": "core.user_auth.login_success",
            "outcome": {"result": "SUCCESS"},
            "p_event_time": "2023-05-26 20:18:51",
            "p_enrichment": {
                "ipinfo_location": {
                    "client.ipAddress": {
                        "city": "Los Angeles",
                        "country": "US",
                        "lat": "34.05223",
                        "lng": "-118.24368",
                        "p_match": "12.12.12.12",
                        "postal_code": "90009",
                        "region": "California",
                        "region_code": "CA",
                        "timezone": "America/Los_Angeles",
                    }
                },
                "ipinfo_privacy": {
                    "client.ipAddress": {
                        "hosting": True,
                        "p_match": "12.12.12.12",
                        "proxy": False,
                        "relay": True,
                        "service": "Apple Private Relay",
                        "tor": False,
                        "vpn": False,
                    }
                },
            },
            "p_log_type": "Okta.SystemLog",
            "p_source_label": "Okta Logs",
            "p_parse_time": "2023-05-26 20:22:51.888",
            "published": "2023-05-26 20:18:51.888",
            "request": {"ipChain": []},
            "securityContext": {},
            "severity": "INFO",
            "target": [],
            "transaction": {},
            "uuid": "79999999-ffff-eeee-bbbb-222222222222",
            "version": "0",
        },
    ),
    PantherRuleTest(
        Name="Okta sign-in with history and impossible travel, VPN with service",
        ExpectedResult=True,
        Mocks=[
            RuleMock(ObjectName="put_string_set", ReturnValue=""),
            RuleMock(
                ObjectName="get_string_set",
                ReturnValue='[\n {\n  "p_event_time": "2023-05-26 18:14:51",\n  "city": "New York City",\n  "country": "US",\n  "lat": "40.71427",\n  "lng": "-74.00597",\n  "postal_code": "10004",\n  "region": "New York",\n  "region_code": "NY",\n  "timezone": "America/New_York"\n }\n]',
            ),
        ],
        Log={
            "actor": {
                "alternateId": "homer.simpson@company.com",
                "displayName": "Homer Simpson",
                "id": "00uwuwuwuwuwuwuwuwuw",
                "type": "User",
            },
            "authenticationContext": {"authenticationStep": 0, "externalSessionId": "idx1234"},
            "client": {
                "device": "Computer",
                "ipAddress": "12.12.12.12",
                "userAgent": {
                    "browser": "CHROME",
                    "os": "Mac OS X",
                    "rawUserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                },
                "zone": "null",
            },
            "debugContext": {"debugData": {}},
            "device": {},
            "displayMessage": "User login to Okta",
            "eventType": "user.session.start",
            "legacyEventType": "core.user_auth.login_success",
            "outcome": {"result": "SUCCESS"},
            "p_event_time": "2023-05-26 20:18:51",
            "p_enrichment": {
                "ipinfo_location": {
                    "client.ipAddress": {
                        "city": "Los Angeles",
                        "country": "US",
                        "lat": "34.05223",
                        "lng": "-118.24368",
                        "p_match": "12.12.12.12",
                        "postal_code": "90009",
                        "region": "California",
                        "region_code": "CA",
                        "timezone": "America/Los_Angeles",
                    }
                },
                "ipinfo_privacy": {
                    "client.ipAddress": {
                        "hosting": False,
                        "p_match": "12.12.12.12",
                        "proxy": False,
                        "relay": False,
                        "service": "Private Internet Access",
                        "tor": False,
                        "vpn": True,
                    }
                },
            },
            "p_log_type": "Okta.SystemLog",
            "p_source_label": "Okta Logs",
            "p_parse_time": "2023-05-26 20:22:51.888",
            "published": "2023-05-26 20:18:51.888",
            "request": {"ipChain": []},
            "securityContext": {},
            "severity": "INFO",
            "target": [],
            "transaction": {},
            "uuid": "79999999-ffff-eeee-bbbb-222222222222",
            "version": "0",
        },
    ),
    PantherRuleTest(
        Name="Okta sign-in with history and impossible travel, VPN with no service",
        ExpectedResult=True,
        Mocks=[
            RuleMock(ObjectName="put_string_set", ReturnValue=""),
            RuleMock(
                ObjectName="get_string_set",
                ReturnValue='[\n {\n  "p_event_time": "2023-05-26 18:14:51",\n  "city": "New York City",\n  "country": "US",\n  "lat": "40.71427",\n  "lng": "-74.00597",\n  "postal_code": "10004",\n  "region": "New York",\n  "region_code": "NY",\n  "timezone": "America/New_York"\n }\n]',
            ),
        ],
        Log={
            "actor": {
                "alternateId": "homer.simpson@company.com",
                "displayName": "Homer Simpson",
                "id": "00uwuwuwuwuwuwuwuwuw",
                "type": "User",
            },
            "authenticationContext": {"authenticationStep": 0, "externalSessionId": "idx1234"},
            "client": {
                "device": "Computer",
                "ipAddress": "12.12.12.12",
                "userAgent": {
                    "browser": "CHROME",
                    "os": "Mac OS X",
                    "rawUserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                },
                "zone": "null",
            },
            "debugContext": {"debugData": {}},
            "device": {},
            "displayMessage": "User login to Okta",
            "eventType": "user.session.start",
            "legacyEventType": "core.user_auth.login_success",
            "outcome": {"result": "SUCCESS"},
            "p_event_time": "2023-05-26 20:18:51",
            "p_enrichment": {
                "ipinfo_location": {
                    "client.ipAddress": {
                        "city": "Los Angeles",
                        "country": "US",
                        "lat": "34.05223",
                        "lng": "-118.24368",
                        "p_match": "12.12.12.12",
                        "postal_code": "90009",
                        "region": "California",
                        "region_code": "CA",
                        "timezone": "America/Los_Angeles",
                    }
                },
                "ipinfo_privacy": {
                    "client.ipAddress": {
                        "hosting": False,
                        "proxy": False,
                        "relay": False,
                        "service": "",
                        "tor": False,
                        "vpn": True,
                    }
                },
            },
            "p_log_type": "Okta.SystemLog",
            "p_source_label": "Okta Logs",
            "p_parse_time": "2023-05-26 20:22:51.888",
            "published": "2023-05-26 20:18:51.888",
            "request": {"ipChain": []},
            "securityContext": {},
            "severity": "INFO",
            "target": [],
            "transaction": {},
            "uuid": "79999999-ffff-eeee-bbbb-222222222222",
            "version": "0",
        },
    ),
    PantherRuleTest(
        Name="Short Distances and Short Timedeltas",
        ExpectedResult=True,
        Mocks=[
            RuleMock(ObjectName="put_string_set", ReturnValue=""),
            RuleMock(
                ObjectName="get_string_set",
                ReturnValue='[\n  {\n    "city": "Los Angeles",\n    "country": "US",\n    "lat": "34.05223",\n    "lng": "-118.24368",\n    "p_event_time": "2023-06-12T22:23:51.964000",\n    "postal_code": "90009",\n    "region": "California",\n    "region_code": "CA",\n    "timezone": "America/Los_Angeles"\n  }\n]',
            ),
        ],
        Log={
            "actor": {
                "alternateId": "homer.simpson@company.com",
                "displayName": "Homer Simpson",
                "id": "00uwuwuwuwuwuwuwuwuw",
                "type": "User",
            },
            "authenticationContext": {"authenticationStep": 0, "externalSessionId": "idx1234"},
            "client": {
                "device": "Computer",
                "ipAddress": "12.12.12.11",
                "userAgent": {
                    "browser": "CHROME",
                    "os": "Mac OS X",
                    "rawUserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                },
                "zone": "null",
            },
            "debugContext": {"debugData": {}},
            "device": {},
            "displayMessage": "User login to Okta",
            "eventType": "user.session.start",
            "legacyEventType": "core.user_auth.login_success",
            "outcome": {"result": "SUCCESS"},
            "p_event_time": "2023-06-12T22:26:01.951000",
            "p_enrichment": {
                "ipinfo_location": {
                    "client.ipAddress": {
                        "p_match": "12.12.12.11",
                        "city": "Anaheim",
                        "country": "US",
                        "lat": "33.8085",
                        "lng": "-117.9228",
                        "p_event_time": "2023-06-12T22:26:01.951000",
                        "postal_code": "92802",
                        "region": "California",
                        "region_code": "CA",
                        "timezone": "America/Los_Angeles",
                    }
                }
            },
            "p_log_type": "Okta.SystemLog",
            "p_source_label": "Okta Logs",
            "p_parse_time": "2023-06-12T22:29:01.951000",
            "published": "2023-06-12 22:26:01.951000",
            "request": {"ipChain": []},
            "securityContext": {},
            "severity": "INFO",
            "target": [],
            "transaction": {},
            "uuid": "79999999-ffff-eeee-bbbb-222222222222",
            "version": "0",
        },
    ),
    PantherRuleTest(
        Name="Asana ImpossibleTravel",
        ExpectedResult=True,
        Mocks=[
            RuleMock(ObjectName="put_string_set", ReturnValue=""),
            RuleMock(
                ObjectName="get_string_set",
                ReturnValue='[\n {\n  "p_event_time": "2023-06-12T21:26:01.951000",\n  "city": "New York City",\n  "country": "US",\n  "lat": "40.71427",\n  "lng": "-74.00597",\n  "postal_code": "10004",\n  "region": "New York",\n  "region_code": "NY",\n  "timezone": "America/New_York"\n }\n]',
            ),
        ],
        Log={
            "actor": {
                "actor_type": "user",
                "email": "homer.simpsons@simpsons.com",
                "gid": "1234567890",
                "name": "Homer Simpson",
            },
            "context": {
                "client_ip_address": "1.2.3.4",
                "context_type": "web",
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            },
            "created_at": "2023-05-26 18:24:51.413",
            "details": {"method": ["SAML"]},
            "event_category": "logins",
            "event_type": "user_login_succeeded",
            "gid": "123456789",
            "resource": {
                "email": "homer.simpsons@simpsons.com",
                "gid": "1234567890",
                "name": "Homer Simpson",
                "resource_type": "user",
            },
            "p_log_type": "Asana.Audit",
            "p_source_label": "Asana Logs",
            "p_enrichment": {
                "ipinfo_privacy": {"context.client_ip_address": {"p_match": "1.2.3.4"}},
                "ipinfo_location": {
                    "context.client_ip_address": {
                        "p_match": "1.2.3.4",
                        "city": "Anaheim",
                        "country": "US",
                        "lat": "33.8085",
                        "lng": "-117.9228",
                        "p_event_time": "2023-06-12T22:26:01.951000",
                        "postal_code": "92802",
                        "region": "California",
                        "region_code": "CA",
                        "timezone": "America/Los_Angeles",
                    }
                },
            },
            "p_event_time": "2023-06-12T22:26:01.951000",
        },
    ),
    PantherRuleTest(
        Name="Notion Impossible Travel",
        ExpectedResult=True,
        Mocks=[
            RuleMock(ObjectName="put_string_set", ReturnValue=""),
            RuleMock(
                ObjectName="get_string_set",
                ReturnValue='[\n  {\n    "p_event_time": "2023-10-03T18:26:01.951000",\n    "source_ip": "192.168.100.100",\n    "city": "Minas Tirith",\n    "country": "Gondor",\n    "lat": "0.00000",\n    "lng": "0.00000",\n    "p_match": "192.168.100.100",\n    "postal_code": "55555",\n    "region": "Pellenor",\n    "region_code": "PL",\n    "timezone": "Middle Earth/Pellenor"\n  }\n]',
            ),
        ],
        Log={
            "event": {
                "actor": {
                    "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                    "object": "user",
                    "person": {"email": "aragorn.elessar@lotr.com"},
                    "type": "person",
                },
                "details": {"authType": "saml"},
                "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "ip_address": "192.168.100.100",
                "timestamp": "2023-10-03T19:02:28.044000Z",
                "type": "user.login",
                "workspace_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            },
            "p_enrichment": {
                "ipinfo_location": {
                    "event.ip_address": {
                        "city": "Barad-Dur",
                        "lat": "100.00000",
                        "lng": "0.00000",
                        "country": "Mordor",
                        "postal_code": "55555",
                        "p_match": "192.168.100.100",
                        "region": "Mount Doom",
                        "region_code": "MD",
                        "timezone": "Middle Earth/Mordor",
                    }
                }
            },
            "p_event_time": "2023-10-03T19:02:28.044000Z",
            "p_log_type": "Notion.AuditLogs",
            "p_source_label": "Notion-Panther-Labs",
        },
    ),
    PantherRuleTest(
        Name="First hit from VPN should not fail",
        ExpectedResult=False,
        Mocks=[
            RuleMock(ObjectName="put_string_set", ReturnValue=""),
            RuleMock(ObjectName="get_string_set", ReturnValue=""),
        ],
        Log={
            "actor": {
                "alternateId": "homer.simpson@company.com",
                "displayName": "Homer Simpson",
                "id": "00uwuwuwuwuwuwuwuwuw",
                "type": "User",
            },
            "authenticationContext": {"authenticationStep": 0, "externalSessionId": "idx1234"},
            "client": {
                "device": "Computer",
                "ipAddress": "12.12.12.12",
                "userAgent": {
                    "browser": "CHROME",
                    "os": "Mac OS X",
                    "rawUserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                },
                "zone": "null",
            },
            "debugContext": {"debugData": {}},
            "device": {},
            "displayMessage": "User login to Okta",
            "eventType": "user.session.start",
            "legacyEventType": "core.user_auth.login_success",
            "outcome": {"result": "SUCCESS"},
            "p_event_time": "2023-05-26 20:18:51",
            "p_enrichment": {
                "ipinfo_location": {
                    "client.ipAddress": {
                        "city": "Los Angeles",
                        "country": "US",
                        "lat": "34.05223",
                        "lng": "-118.24368",
                        "p_match": "12.12.12.12",
                        "postal_code": "90009",
                        "region": "California",
                        "region_code": "CA",
                        "timezone": "America/Los_Angeles",
                    }
                },
                "ipinfo_privacy": {
                    "client.ipAddress": {
                        "hosting": True,
                        "p_match": "12.12.12.12",
                        "proxy": False,
                        "relay": True,
                        "service": "Apple Private Relay",
                        "tor": False,
                        "vpn": False,
                    }
                },
            },
            "p_log_type": "Okta.SystemLog",
            "p_source_label": "Okta Logs",
            "p_parse_time": "2023-05-26 20:22:51.888",
            "published": "2023-05-26 20:18:51.888",
            "request": {"ipChain": []},
            "securityContext": {},
            "severity": "INFO",
            "target": [],
            "transaction": {},
            "uuid": "79999999-ffff-eeee-bbbb-222222222222",
            "version": "0",
        },
    ),
]


class StandardImpossibleTravelLogin(PantherRule):
    RuleID = "Standard.ImpossibleTravel.Login-prototype"
    DisplayName = "Impossible Travel for Login Action"
    LogTypes = [
        LogType.Asana_Audit,
        LogType.AWS_CloudTrail,
        LogType.Notion_AuditLogs,
        LogType.Okta_SystemLog,
    ]
    Tags = ["Identity & Access Management", "Initial Access:Valid Accounts"]
    Reports = {"MITRE ATT&CK": ["TA0001:T1078"]}
    Severity = PantherSeverity.High
    Description = (
        "A user has subsequent logins from two geographic locations that are very far apart"
    )
    Runbook = "Reach out to the user if needed to validate the activity, then lock the account. \nIf the user responds that the geolocation on the new location is incorrect, you can directly report the inaccuracy via  https://ipinfo.io/corrections\n"
    Reference = "https://expertinsights.com/insights/what-are-impossible-travel-logins/#:~:text=An%20impossible%20travel%20login%20is,of%20the%20logins%20is%20fraudulent"
    SummaryAttributes = ["p_any_usernames", "p_any_ip_addresses", "p_any_domain_names"]
    Tests = standard_impossible_travel_login_tests

    def gen_key(self, event):
        """
        gen_key uses the data_model for the logtype to cache
        an entry that is specific to the Log Source ID

        The data_model needs to answer to "actor_user"
        """
        rule_name = deep_get(event, "p_source_label")
        actor = event.udm("actor_user")
        if None in [rule_name, actor]:
            return None
        return f"{rule_name.replace(' ', '')}..{actor}"

    def rule(self, event):
        # too-many-return-statements due to error checking
        # pylint: disable=global-statement,too-many-return-statements,too-complex
        self.EVENT_CITY_TRACKING = {}
        self.CACHE_KEY = None
        self.IS_VPN = False
        self.IS_PRIVATE_RELAY = False
        # Only evaluate successful logins
        if event.udm("event_type") != event_type.SUCCESSFUL_LOGIN:
            return False
        p_event_datetime = resolve_timestamp_string(deep_get(event, "p_event_time"))
        if p_event_datetime is None:
            # we couldn't go from p_event_time to a datetime object
            # we need to do this in order to make later time comparisons generic
            return False
        new_login_stats = {
            "p_event_time": p_event_datetime.isoformat(),
            "source_ip": event.udm("source_ip"),
        }
        #
        src_ip_enrichments = LookupTableMatches().p_matches(event, event.udm("source_ip"))
        # stuff everything from ipinfo_location into the new_login_stats
        # new_login_stats is the value that we will cache for this key
        ipinfo_location = deep_get(src_ip_enrichments, "ipinfo_location")
        if ipinfo_location is None:
            return False
        new_login_stats.update(ipinfo_location)
        # Bail out if we have a None value in set as it causes false positives
        if None in new_login_stats.values():
            return False
        ## Check for VPN or Private Relay
        ipinfo_privacy = deep_get(src_ip_enrichments, "ipinfo_privacy")
        if ipinfo_privacy is not None:
            ###  Do VPN/private relay
            self.IS_PRIVATE_RELAY = all(
                [
                    deep_get(ipinfo_privacy, "relay", default=False),
                    deep_get(ipinfo_privacy, "service", default="") == "Apple Private Relay",
                ]
            )
            # We've found that some places, like WeWork locations,
            #   have the VPN attribute set to true, but do not have a
            #   service name entry.
            # We have noticed VPN connections with commercial VPN
            #   offerings have the VPN attribute set to true, and
            #   do have a service name entry
            self.IS_VPN = all(
                [
                    deep_get(ipinfo_privacy, "vpn", default=False),
                    deep_get(ipinfo_privacy, "service", default="") != "",
                ]
            )
        if self.IS_VPN or self.IS_PRIVATE_RELAY:
            new_login_stats.update(
                {
                    "is_vpn": f"{self.IS_VPN}",
                    "is_apple_priv_relay": f"{self.IS_PRIVATE_RELAY}",
                    "service_name": f"{deep_get(ipinfo_privacy, 'service', default='<NO_SERVICE>')}",
                    "NOTE": "APPLE PRIVATE RELAY AND VPN LOGINS ARE NOT CACHED FOR COMPARISON",
                }
            )
        # Generate a unique cache key for each user per log type
        self.CACHE_KEY = self.gen_key(event)
        if self.CACHE_KEY is None:
            # We can't save without a cache key
            return False
        # Retrieve the prior login info from the cache, if any
        last_login = get_string_set(self.CACHE_KEY)
        # If we haven't seen this user login in the past 1 day,
        # store this login for future use and don't alert
        if not last_login:
            if not (self.IS_PRIVATE_RELAY or self.IS_VPN):
                put_string_set(
                    key=self.CACHE_KEY,
                    val=[dumps(new_login_stats)],
                    epoch_seconds=int((datetime.utcnow() + timedelta(days=1)).timestamp()),
                )
            return False
        # Load the last login from the cache into an object we can compare
        # str check is in place for unit test mocking
        if isinstance(last_login, str):
            tmp_last_login = loads(last_login)
            last_login = []
            for l_l in tmp_last_login:
                last_login.append(dumps(l_l))
        last_login_stats = loads(last_login.pop())
        distance = km_between_ipinfo_loc(last_login_stats, new_login_stats)
        old_time = resolve_timestamp_string(deep_get(last_login_stats, "p_event_time"))
        new_time = resolve_timestamp_string(deep_get(new_login_stats, "p_event_time"))
        time_delta = (new_time - old_time).total_seconds() / 3600  # seconds in an hour
        # Don't let time_delta be 0 (divide by zero error below)
        time_delta = time_delta or 0.0001
        # Calculate speed in Kilometers / Hour
        speed = distance / time_delta
        # Calculation is complete, write the current login to the cache
        # Only if non-VPN non-relay!
        if not self.IS_PRIVATE_RELAY and (not self.IS_VPN):
            put_string_set(
                key=self.CACHE_KEY,
                val=[dumps(new_login_stats)],
                epoch_seconds=int((datetime.utcnow() + timedelta(days=1)).timestamp()),
            )
        self.EVENT_CITY_TRACKING["previous"] = last_login_stats
        self.EVENT_CITY_TRACKING["current"] = new_login_stats
        self.EVENT_CITY_TRACKING["speed"] = int(speed)
        self.EVENT_CITY_TRACKING["speed_units"] = "km/h"
        self.EVENT_CITY_TRACKING["distance"] = int(distance)
        self.EVENT_CITY_TRACKING["distance_units"] = "km"
        return speed > 900  # Boeing 747 cruising speed

    def title(self, event):
        #
        log_source = deep_get(event, "p_source_label", default="<NO_SOURCE_LABEL>")
        old_city = deep_get(self.EVENT_CITY_TRACKING, "previous", "city", default="<NO_PREV_CITY>")
        new_city = deep_get(self.EVENT_CITY_TRACKING, "current", "city", default="<NO_PREV_CITY>")
        speed = deep_get(self.EVENT_CITY_TRACKING, "speed", default="<NO_SPEED>")
        distance = deep_get(self.EVENT_CITY_TRACKING, "distance", default="<NO_DISTANCE>")
        return f"Impossible Travel: [{event.udm('actor_user')}] in [{log_source}] went [{speed}] km/h for [{distance}] km between [{old_city}] and [{new_city}]"

    def dedup(self, event):  # pylint: disable=W0613
        return self.CACHE_KEY

    def alert_context(self, event):
        context = {"actor_user": event.udm("actor_user")}
        context.update(self.EVENT_CITY_TRACKING)
        return context

    def severity(self, _):
        if self.IS_VPN or self.IS_PRIVATE_RELAY:
            return "INFO"
        # time = distance/speed
        distance = deep_get(self.EVENT_CITY_TRACKING, "distance", default=None)
        speed = deep_get(self.EVENT_CITY_TRACKING, "speed", default=None)
        if speed and distance:
            time = distance / speed
            # time of 0.1666 is 10 minutes
            if time < 0.1666 and distance < 50:
                # This is likely a GEOIP inaccuracy
                return "LOW"
        return "HIGH"

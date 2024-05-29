from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import deep_get, deep_walk, okta_alert_context
from pypanther.log_types import LogType

okta_new_behavior_accessing_admin_console_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="New Behavior Accessing Admin Console (behavior)",
        ExpectedResult=True,
        Log={
            "actor": {
                "alternateId": "homer.simpson@duff.com",
                "displayName": "Homer Simpson",
                "id": "00abc123",
                "type": "User",
            },
            "authenticationcontext": {"authenticationStep": 0, "externalSessionId": "100-abc-9999"},
            "client": {
                "device": "Computer",
                "geographicalContext": {
                    "city": "Springfield",
                    "country": "United States",
                    "geolocation": {"lat": 20, "lon": -25},
                    "postalCode": "12345",
                    "state": "Ohio",
                },
                "ipAddress": "1.3.2.4",
                "userAgent": {
                    "browser": "CHROME",
                    "os": "Mac OS X",
                    "rawUserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
                },
                "zone": "null",
            },
            "device": {"name": "Evil Computer"},
            "debugcontext": {
                "debugData": {
                    "requestId": "AbCdEf12G",
                    "requestUri": "/api/v1/users/AbCdEfG/lifecycle/reset_factors",
                    "url": "/api/v1/users/AbCdEfG/lifecycle/reset_factors?",
                    "behaviors": {
                        "New Geo-Location=NEGATIVE": None,
                        "New Device=POSITIVE": None,
                        "New IP=POSITIVE": None,
                        "New State=NEGATIVE": None,
                        "New Country=NEGATIVE": None,
                        "Velocity=NEGATIVE": None,
                        "New City=NEGATIVE": None,
                    },
                }
            },
            "displaymessage": "Evaluation of sign-on policy",
            "eventtype": "policy.evaluate_sign_on",
            "outcome": {
                "reason": "Sign-on policy evaluation resulted in CHALLENGE",
                "result": "CHALLENGE",
            },
            "published": "2022-06-22 18:18:29.015",
            "request": {
                "ipChain": [
                    {
                        "geographicalContext": {
                            "city": "Springfield",
                            "country": "United States",
                            "geolocation": {"lat": 20, "lon": -25},
                            "postalCode": "12345",
                            "state": "Ohio",
                            "ip": "1.3.2.4",
                            "version": "V4",
                        }
                    }
                ]
            },
            "securitycontext": {
                "asNumber": 701,
                "asOrg": "verizon",
                "domain": "verizon.net",
                "isProxy": False,
                "isp": "verizon",
            },
            "severity": "INFO",
            "target": [
                {
                    "alternateId": "Okta Admin Console",
                    "displayName": "Okta Admin Console",
                    "type": "AppInstance",
                },
                {
                    "alternateId": "peter.griffin@company.com",
                    "displayName": "Peter Griffin",
                    "id": "0002222AAAA",
                    "type": "User",
                },
            ],
            "transaction": {"detail": {}, "id": "ABcDeFgG", "type": "WEB"},
            "uuid": "AbC-123-XyZ",
            "version": "0",
        },
    ),
    PantherRuleTest(
        Name="New Behavior Accessing Admin Console (logSecurityDataOnly)",
        ExpectedResult=True,
        Log={
            "actor": {
                "alternateId": "homer.simpson@duff.com",
                "displayName": "Homer Simpson",
                "id": "00abc123",
                "type": "User",
            },
            "authenticationcontext": {"authenticationStep": 0, "externalSessionId": "100-abc-9999"},
            "client": {
                "device": "Computer",
                "geographicalContext": {
                    "city": "Springfield",
                    "country": "United States",
                    "geolocation": {"lat": 20, "lon": -25},
                    "postalCode": "12345",
                    "state": "Ohio",
                },
                "ipAddress": "1.3.2.4",
                "userAgent": {
                    "browser": "CHROME",
                    "os": "Mac OS X",
                    "rawUserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
                },
                "zone": "null",
            },
            "device": {"name": "Evil Computer"},
            "debugcontext": {
                "debugData": {
                    "requestId": "AbCdEf12G",
                    "requestUri": "/api/v1/users/AbCdEfG/lifecycle/reset_factors",
                    "url": "/api/v1/users/AbCdEfG/lifecycle/reset_factors?",
                    "logOnlySecurityData": {
                        "risk": {"level": "LOW"},
                        "behaviors": {
                            "New Geo-Location": "NEGATIVE",
                            "New Device": "POSITIVE",
                            "New IP": "POSITIVE",
                            "New State": "NEGATIVE",
                            "New Country": "NEGATIVE",
                            "Velocity": "NEGATIVE",
                            "New City": "NEGATIVE",
                        },
                    },
                }
            },
            "displaymessage": "Evaluation of sign-on policy",
            "eventtype": "policy.evaluate_sign_on",
            "outcome": {
                "reason": "Sign-on policy evaluation resulted in CHALLENGE",
                "result": "CHALLENGE",
            },
            "published": "2022-06-22 18:18:29.015",
            "request": {
                "ipChain": [
                    {
                        "geographicalContext": {
                            "city": "Springfield",
                            "country": "United States",
                            "geolocation": {"lat": 20, "lon": -25},
                            "postalCode": "12345",
                            "state": "Ohio",
                            "ip": "1.3.2.4",
                            "version": "V4",
                        }
                    }
                ]
            },
            "securitycontext": {
                "asNumber": 701,
                "asOrg": "verizon",
                "domain": "verizon.net",
                "isProxy": False,
                "isp": "verizon",
            },
            "severity": "INFO",
            "target": [
                {
                    "alternateId": "Okta Admin Console",
                    "displayName": "Okta Admin Console",
                    "type": "AppInstance",
                },
                {
                    "alternateId": "peter.griffin@company.com",
                    "displayName": "Peter Griffin",
                    "id": "0002222AAAA",
                    "type": "User",
                },
            ],
            "transaction": {"detail": {}, "id": "ABcDeFgG", "type": "WEB"},
            "uuid": "AbC-123-XyZ",
            "version": "0",
        },
    ),
    PantherRuleTest(
        Name="Not New Behavior",
        ExpectedResult=False,
        Log={
            "actor": {
                "alternateId": "homer.simpson@duff.com",
                "displayName": "Homer Simpson",
                "id": "00abc123",
                "type": "User",
            },
            "authenticationcontext": {"authenticationStep": 0, "externalSessionId": "100-abc-9999"},
            "client": {
                "device": "Computer",
                "geographicalContext": {
                    "city": "Springfield",
                    "country": "United States",
                    "geolocation": {"lat": 20, "lon": -25},
                    "postalCode": "12345",
                    "state": "Ohio",
                },
                "ipAddress": "1.3.2.4",
                "userAgent": {
                    "browser": "CHROME",
                    "os": "Mac OS X",
                    "rawUserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
                },
                "zone": "null",
            },
            "debugcontext": {
                "debugData": {
                    "requestId": "AbCdEf12G",
                    "requestUri": "/api/v1/users/AbCdEfG/lifecycle/reset_factors",
                    "url": "/api/v1/users/AbCdEfG/lifecycle/reset_factors?",
                    "logOnlySecurityData": {
                        "risk": {"level": "LOW"},
                        "behaviors": {
                            "New Geo-Location": "NEGATIVE",
                            "New Device": "NEGATIVE",
                            "New IP": "NEGATIVE",
                            "New State": "NEGATIVE",
                            "New Country": "NEGATIVE",
                            "Velocity": "NEGATIVE",
                            "New City": "NEGATIVE",
                        },
                    },
                }
            },
            "displaymessage": "Evaluation of sign-on policy",
            "eventtype": "policy.evaluate_sign_on",
            "outcome": {
                "reason": "Sign-on policy evaluation resulted in CHALLENGE",
                "result": "CHALLENGE",
            },
            "published": "2022-06-22 18:18:29.015",
            "request": {
                "ipChain": [
                    {
                        "geographicalContext": {
                            "city": "Springfield",
                            "country": "United States",
                            "geolocation": {"lat": 20, "lon": -25},
                            "postalCode": "12345",
                            "state": "Ohio",
                            "ip": "1.3.2.4",
                            "version": "V4",
                        }
                    }
                ]
            },
            "securitycontext": {
                "asNumber": 701,
                "asOrg": "verizon",
                "domain": "verizon.net",
                "isProxy": False,
                "isp": "verizon",
            },
            "severity": "INFO",
            "target": [
                {
                    "alternateId": "Okta Admin Console",
                    "displayName": "Okta Admin Console",
                    "type": "AppInstance",
                },
                {
                    "alternateId": "peter.griffin@company.com",
                    "displayName": "Peter Griffin",
                    "id": "0002222AAAA",
                    "type": "User",
                },
            ],
            "transaction": {"detail": {}, "id": "ABcDeFgG", "type": "WEB"},
            "uuid": "AbC-123-XyZ",
            "version": "0",
        },
    ),
]


class OktaNewBehaviorAccessingAdminConsole(PantherRule):
    RuleID = "Okta.New.Behavior.Accessing.Admin.Console-prototype"
    DisplayName = "Okta New Behaviors Acessing Admin Console"
    LogTypes = [LogType.Okta_SystemLog]
    Reports = {"MITRE ATT&CK": ["TA0001:T1078.004"]}
    Severity = PantherSeverity.High
    Description = "New Behaviors Observed while Accessing Okta Admin Console. A user attempted to access the Okta Admin Console from a new device with a new IP.\n"
    Runbook = "Configure Authentication Policies (Application Sign-on Policies) for access to privileged applications, including the Admin Console, to require re-authentication “at every sign-in”. Turn on and test New Device and Suspicious Activity end-user notifications.\n"
    Reference = "https://sec.okta.com/articles/2023/08/cross-tenant-impersonation-prevention-and-detection\n"
    Tests = okta_new_behavior_accessing_admin_console_tests

    def rule(self, event):
        if event.get("eventtype") != "policy.evaluate_sign_on":
            return False
        if "Okta Admin Console" not in deep_walk(event, "target", "displayName", default=""):
            return False
        behaviors = deep_get(event, "debugContext", "debugData", "behaviors")
        if behaviors:
            return "New Device=POSITIVE" in behaviors and "New IP=POSITIVE" in behaviors
        return (
            deep_get(
                event, "debugContext", "debugData", "logOnlySecurityData", "behaviors", "New Device"
            )
            == "POSITIVE"
            and deep_get(
                event, "debugContext", "debugData", "logOnlySecurityData", "behaviors", "New IP"
            )
            == "POSITIVE"
        )

    def title(self, event):
        return f"{deep_get(event, 'actor', 'displayName', default='<displayName-not-found>')} <{deep_get(event, 'actor', 'alternateId', default='alternateId-not-found')}> accessed Okta Admin Console using new behaviors: New IP: {deep_get(event, 'client', 'ipAddress', default='<ipAddress-not-found>')} New Device: {deep_get(event, 'device', 'name', default='<deviceName-not-found>')}"

    def alert_context(self, event):
        return okta_alert_context(event)

from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import okta_alert_context
from pypanther.log_types import LogType

okta_group_admin_role_assigned_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Group Privilege Grant",
        ExpectedResult=True,
        Log={
            "actor": {
                "alternateId": "homer.simpson@duff.com",
                "displayName": "Homer Simpsons",
                "id": "00ABC123",
                "type": "User",
            },
            "authenticationcontext": {"authenticationStep": 0, "externalSessionId": "xyz1234"},
            "client": {
                "device": "Computer",
                "geographicalContext": {
                    "city": "Springfield",
                    "country": "United States",
                    "geolocation": {"lat": 11.111, "lon": -70},
                    "postalCode": "1234",
                    "state": "California",
                },
                "ipAddress": "1.2.3.4",
                "userAgent": {
                    "browser": "CHROME",
                    "os": "Mac OS X",
                    "rawUserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                },
                "zone": "null",
            },
            "debugcontext": {
                "debugData": {
                    "authnRequestId": "ABC123",
                    "deviceFingerprint": "009988771ABC",
                    "dtHash": "123abc1234",
                    "requestId": "abc-111-adf",
                    "requestUri": "/idp/idx/identify",
                    "threatSuspected": "false",
                    "url": "/idp/idx/identify?",
                }
            },
            "displaymessage": "Group Privilege granted",
            "eventtype": "group.privilege.grant",
            "legacyeventtype": "group.privilege.grant",
            "outcome": {"result": "FAILURE"},
            "published": "2022-12-13 00:58:19.811",
            "request": {
                "ipChain": [
                    {
                        "geographicalContext": {
                            "city": "Springfield",
                            "country": "United States",
                            "geolocation": {"lat": 11.111, "lon": -70},
                            "postalCode": "1234",
                            "state": "California",
                        },
                        "ip": "1.2.3.4",
                        "version": "V4",
                    }
                ]
            },
            "securitycontext": {
                "asNumber": 11351,
                "asOrg": "charter communications inc",
                "domain": "rr.com",
                "isProxy": False,
                "isp": "charter communications inc",
            },
            "severity": "WARN",
            "target": [
                {
                    "alternateId": "App (123)",
                    "displayName": "App (123)",
                    "id": "12345",
                    "type": "AppInstance",
                }
            ],
            "transaction": {"detail": {}, "id": "aaa-bbb-123", "type": "WEB"},
            "uuid": "aa-11-22-33-44-bb",
            "version": "0",
        },
    ),
    PantherRuleTest(
        Name="Non Event",
        ExpectedResult=False,
        Log={
            "actor": {
                "alternateId": "homer.simpson@duff.com",
                "displayName": "Homer Simpsons",
                "id": "00ABC123",
                "type": "User",
            },
            "authenticationcontext": {"authenticationStep": 0, "externalSessionId": "xyz1234"},
            "client": {
                "device": "Computer",
                "geographicalContext": {
                    "city": "Springfield",
                    "country": "United States",
                    "geolocation": {"lat": 11.111, "lon": -70},
                    "postalCode": "1234",
                    "state": "California",
                },
                "ipAddress": "1.2.3.4",
                "userAgent": {
                    "browser": "CHROME",
                    "os": "Mac OS X",
                    "rawUserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                },
                "zone": "null",
            },
            "debugcontext": {
                "debugData": {
                    "authnRequestId": "ABC123",
                    "deviceFingerprint": "009988771ABC",
                    "dtHash": "123abc1234",
                    "requestId": "abc-111-adf",
                    "requestUri": "/idp/idx/identify",
                    "threatSuspected": "false",
                    "url": "/idp/idx/identify?",
                }
            },
            "displaymessage": "User attempted to reuse tokens",
            "eventtype": "app.token.reuse",
            "legacyeventtype": "app.token.reuse",
            "outcome": {"result": "FAILURE"},
            "published": "2022-12-13 00:58:19.811",
            "request": {
                "ipChain": [
                    {
                        "geographicalContext": {
                            "city": "Springfield",
                            "country": "United States",
                            "geolocation": {"lat": 11.111, "lon": -70},
                            "postalCode": "1234",
                            "state": "California",
                        },
                        "ip": "1.2.3.4",
                        "version": "V4",
                    }
                ]
            },
            "securitycontext": {
                "asNumber": 11351,
                "asOrg": "charter communications inc",
                "domain": "rr.com",
                "isProxy": False,
                "isp": "charter communications inc",
            },
            "severity": "WARN",
            "target": [
                {
                    "alternateId": "App (123)",
                    "displayName": "App (123)",
                    "id": "12345",
                    "type": "AppInstance",
                }
            ],
            "transaction": {"detail": {}, "id": "aaa-bbb-123", "type": "WEB"},
            "uuid": "aa-11-22-33-44-bb",
            "version": "0",
        },
    ),
]


class OktaGroupAdminRoleAssigned(PantherRule):
    Description = "Detect when an admin role is assigned to a group"
    DisplayName = "Okta Group Admin Role Assigned"
    Reference = "https://support.okta.com/help/s/article/How-to-assign-Administrator-roles-to-groups?language=en_US#:~:text=Log%20in%20to%20the%20Admin,user%20and%20click%20Save%20changes"
    Severity = PantherSeverity.High
    LogTypes = [LogType.Okta_SystemLog]
    RuleID = "Okta.Group.Admin.Role.Assigned-prototype"
    Tests = okta_group_admin_role_assigned_tests

    def rule(self, event):
        return event.get("eventtype", "") == "group.privilege.grant"

    def title(self, event):
        # pylint: disable=W0613
        return f"Okta Admin Privileges Assigned to Group [{event.get('target', [{}])[0].get('alternateId', '<id-not-found>')}]"

    def alert_context(self, event):
        return okta_alert_context(event)

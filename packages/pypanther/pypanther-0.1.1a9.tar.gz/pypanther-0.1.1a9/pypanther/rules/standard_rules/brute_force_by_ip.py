from json import loads
from typing import List

import pypanther.helpers.panther_event_type_helpers as event_type
from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity, RuleMock
from pypanther.helpers.panther_default import lookup_aws_account_name
from pypanther.helpers.panther_oss_helpers import add_parse_delay, geoinfo_from_ip
from pypanther.log_types import LogType

standard_brute_force_by_ip_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="AWS.CloudTrail - Successful Login",
        ExpectedResult=False,
        Log={
            "eventVersion": "1.05",
            "userIdentity": {
                "type": "IAMUser",
                "principalId": "1111",
                "arn": "arn:aws:iam::123456789012:user/tester",
                "accountId": "123456789012",
                "userName": "testuser",
            },
            "eventTime": "2019-01-01T00:00:00Z",
            "eventSource": "signin.amazonaws.com",
            "eventName": "ConsoleLogin",
            "awsRegion": "us-east-1",
            "sourceIPAddress": "111.111.111.111",
            "userAgent": "Mozilla",
            "requestParameters": None,
            "responseElements": {"ConsoleLogin": "Success"},
            "additionalEventData": {
                "LoginTo": "https://console.aws.amazon.com/console/",
                "MobileVersion": "No",
                "MFAUsed": "No",
            },
            "eventID": "1",
            "eventType": "AwsConsoleSignIn",
            "recipientAccountId": "123456789012",
            "p_log_type": "AWS.CloudTrail",
            "p_parse_time": "2021-06-04 10:02:33.650807",
            "p_event_time": "2021-06-04 09:59:53.650807",
        },
    ),
    PantherRuleTest(
        Name="AWS.CloudTrail - Failed Login",
        ExpectedResult=True,
        Mocks=[
            RuleMock(
                ObjectName="geoinfo_from_ip",
                ReturnValue='{ "ip": "111.111.111.111", "region": "UnitTestRegion", "city": "UnitTestCityNew", "country": "UnitTestCountry", "hostname": "somedomain.com", "org": "Some Org" }',
            )
        ],
        Log={
            "eventVersion": "1.05",
            "userIdentity": {
                "type": "IAMUser",
                "principalId": "1111",
                "arn": "arn:aws:iam::123456789012:user/tester",
                "accountId": "123456789012",
                "userName": "tester",
            },
            "eventTime": "2019-01-01T00:00:00Z",
            "eventSource": "signin.amazonaws.com",
            "eventName": "ConsoleLogin",
            "awsRegion": "us-east-1",
            "sourceIPAddress": "111.111.111.111",
            "userAgent": "Mozilla",
            "requestParameters": None,
            "responseElements": {"ConsoleLogin": "Failure"},
            "additionalEventData": {
                "LoginTo": "https://console.aws.amazon.com/console/",
                "MobileVersion": "No",
                "MFAUsed": "No",
            },
            "eventID": "1",
            "eventType": "AwsConsoleSignIn",
            "recipientAccountId": "123456789012",
            "p_log_type": "AWS.CloudTrail",
            "p_parse_time": "2021-06-04 10:02:33.650807",
            "p_event_time": "2021-06-04 09:59:53.650807",
        },
    ),
    PantherRuleTest(
        Name="Box - Regular Event",
        ExpectedResult=False,
        Log={
            "type": "event",
            "additional_details": '{"key": "value"}',
            "created_by": {
                "id": "12345678",
                "type": "user",
                "login": "cat@example",
                "name": "Bob Cat",
            },
            "ip_address": "111.111.111.111",
            "event_type": "DELETE",
            "p_log_type": "Box.Event",
            "p_parse_time": "2021-06-04 10:02:33.650807",
            "p_event_time": "2021-06-04 09:59:53.650807",
        },
    ),
    PantherRuleTest(
        Name="Box - Login Failed",
        ExpectedResult=True,
        Mocks=[
            RuleMock(
                ObjectName="geoinfo_from_ip",
                ReturnValue='{ "ip": "111.111.111.111", "region": "UnitTestRegion", "city": "UnitTestCityNew", "country": "UnitTestCountry", "hostname": "somedomain.com", "org": "Some Org" }',
            )
        ],
        Log={
            "type": "event",
            "additional_details": '{"key": "value"}',
            "created_by": {
                "id": "12345678",
                "type": "user",
                "login": "cat@example",
                "name": "Bob Cat",
            },
            "event_type": "FAILED_LOGIN",
            "source": {"id": "12345678", "type": "user", "name": "Bob Cat"},
            "ip_address": "111.111.111.111",
            "p_log_type": "Box.Event",
            "p_parse_time": "2021-06-04 10:02:33.650807",
            "p_event_time": "2021-06-04 09:59:53.650807",
        },
    ),
    PantherRuleTest(
        Name="GSuite - Normal Login Event",
        ExpectedResult=False,
        Log={
            "id": {"applicationName": "login"},
            "ipAddress": "111.111.111.111",
            "events": [{"type": "login", "name": "login_success"}],
            "p_log_type": "GSuite.Reports",
            "p_parse_time": "2021-06-04 10:02:33.650807",
            "p_event_time": "2021-06-04 09:59:53.650807",
        },
    ),
    PantherRuleTest(
        Name="GSuite - Failed Login Event",
        ExpectedResult=True,
        Mocks=[
            RuleMock(
                ObjectName="geoinfo_from_ip",
                ReturnValue='{ "ip": "111.111.111.111", "region": "UnitTestRegion", "city": "UnitTestCityNew", "country": "UnitTestCountry", "hostname": "somedomain.com", "org": "Some Org" }',
            )
        ],
        Log={
            "actor": {"email": "bob@example.com"},
            "id": {"applicationName": "login"},
            "ipAddress": "111.111.111.111",
            "events": [{"type": "login", "name": "login_failure"}],
            "p_log_type": "GSuite.Reports",
            "p_parse_time": "2021-06-04 10:02:33.650807",
            "p_event_time": "2021-06-04 09:59:53.650807",
        },
    ),
    PantherRuleTest(
        Name="Okta - Successful Login",
        ExpectedResult=False,
        Log={
            "actor": {
                "alternateId": "admin",
                "displayName": "unknown",
                "id": "unknown",
                "type": "User",
            },
            "client": {"ipAddress": "111.111.111.111"},
            "eventType": "user.session.start",
            "outcome": {"reason": "VERIFICATION_ERROR", "result": "SUCCESS"},
            "p_log_type": "Okta.SystemLog",
            "p_parse_time": "2021-06-04 10:02:33.650807",
            "p_event_time": "2021-06-04 09:59:53.650807",
        },
    ),
    PantherRuleTest(
        Name="Okta - Failed Login",
        ExpectedResult=True,
        Mocks=[
            RuleMock(
                ObjectName="geoinfo_from_ip",
                ReturnValue='{ "ip": "111.111.111.111", "region": "UnitTestRegion", "city": "UnitTestCityNew", "country": "UnitTestCountry", "hostname": "somedomain.com", "org": "Some Org" }',
            )
        ],
        Log={
            "actor": {
                "alternateId": "admin",
                "displayName": "unknown",
                "id": "unknown",
                "type": "User",
            },
            "client": {"ipAddress": "111.111.111.111"},
            "eventType": "user.session.start",
            "outcome": {"reason": "VERIFICATION_ERROR", "result": "FAILURE"},
            "p_log_type": "Okta.SystemLog",
            "p_parse_time": "2021-06-04 10:02:33.650807",
            "p_event_time": "2021-06-04 09:59:53.650807",
        },
    ),
    PantherRuleTest(
        Name="OneLogin - Normal Login Event",
        ExpectedResult=False,
        Log={
            "event_type_id": 8,
            "actor_user_id": 123456,
            "actor_user_name": "Bob Cat",
            "user_id": 123456,
            "user_name": "Bob Cat",
            "ipaddr": "111.111.111.111",
            "p_log_type": "OneLogin.Events",
            "p_parse_time": "2021-06-04 10:02:33.650807",
            "p_event_time": "2021-06-04 09:59:53.650807",
        },
    ),
    PantherRuleTest(
        Name="OneLogin - Failed Login Event",
        ExpectedResult=True,
        Mocks=[
            RuleMock(
                ObjectName="geoinfo_from_ip",
                ReturnValue='{ "ip": "111.111.111.111", "region": "UnitTestRegion", "city": "UnitTestCityNew", "country": "UnitTestCountry", "hostname": "somedomain.com", "org": "Some Org" }',
            )
        ],
        Log={
            "event_type_id": 6,
            "actor_user_id": 123456,
            "actor_user_name": "Bob Cat",
            "user_id": 123456,
            "user_name": "Bob Cat",
            "ipaddr": "1.2.3.4",
            "p_log_type": "OneLogin.Events",
            "p_parse_time": "2021-06-04 10:02:33.650807",
            "p_event_time": "2021-06-04 09:59:53.650807",
        },
    ),
    PantherRuleTest(
        Name="GCP - Non Login Event",
        ExpectedResult=False,
        Log={
            "protoPayload": {
                "at_sign_type": "type.googleapis.com/google.cloud.audit.AuditLog",
                "serviceName": "cloudresourcemanager.googleapis.com",
                "methodName": "SetIamPolicy",
                "authenticationInfo": {"principalEmail": "bob@example.com"},
                "requestMetadata": {"callerIP": "111.111.111.111"},
                "serviceData": {
                    "@type": "type.googleapis.com/google.iam.v1.logging.AuditData",
                    "policyDelta": {
                        "bindingDeltas": [
                            {
                                "action": "ADD",
                                "member": "cat@example.com",
                                "role": "roles/resourcemanager.organizationAdmin",
                            }
                        ]
                    },
                },
            },
            "p_log_type": "GCP.AuditLog",
            "p_parse_time": "2021-06-04 10:02:33.650807",
            "p_event_time": "2021-06-04 09:59:53.650807",
        },
    ),
    PantherRuleTest(
        Name="Asana - Failed Login",
        ExpectedResult=True,
        Mocks=[
            RuleMock(
                ObjectName="geoinfo_from_ip",
                ReturnValue='{ "ip": "111.111.111.111", "region": "UnitTestRegion", "city": "UnitTestCityNew", "country": "UnitTestCountry", "hostname": "somedomain.com", "org": "Some Org" }',
            )
        ],
        Log={
            "actor": {
                "actor_type": "user",
                "email": "homer@springfield.com",
                "gid": "2222222",
                "name": "Homer",
            },
            "context": {"client_ip_address": "8.8.8.8", "context_type": "web"},
            "created_at": "2021-10-21T23:38:10.364Z",
            "details": {"method": ["ONE_TIME_KEY"]},
            "event_category": "logins",
            "event_type": "user_login_failed",
            "gid": "222222222",
            "resource": {
                "email": "homer@springfield.com",
                "gid": "2222222",
                "name": "homer",
                "resource_type": "user",
            },
            "p_log_type": "Asana.Audit",
            "p_parse_time": "2021-06-04 10:02:33.650807",
            "p_event_time": "2021-06-04 09:59:53.650807",
        },
    ),
    PantherRuleTest(
        Name="Asana - Normal Login",
        ExpectedResult=False,
        Log={
            "actor": {
                "actor_type": "user",
                "email": "homer@springfield.com",
                "gid": "2222222",
                "name": "Homer",
            },
            "context": {"client_ip_address": "8.8.8.8", "context_type": "web"},
            "created_at": "2021-10-21T23:38:10.364Z",
            "details": {"method": ["ONE_TIME_KEY"]},
            "event_category": "logins",
            "event_type": "user_login_succeeded",
            "gid": "222222222",
            "resource": {
                "email": "homer@springfield.com",
                "gid": "2222222",
                "name": "homer",
                "resource_type": "user",
            },
            "p_log_type": "Asana.Audit",
            "p_parse_time": "2021-06-04 10:02:33.650807",
            "p_event_time": "2021-06-04 09:59:53.650807",
        },
    ),
    PantherRuleTest(
        Name="1Password - Regular Login",
        ExpectedResult=False,
        Log={
            "uuid": "1234",
            "session_uuid": "5678",
            "timestamp": "2021-12-03 19:52:52",
            "category": "success",
            "type": "credentials_ok",
            "country": "US",
            "target_user": {
                "email": "homer@springfield.gov",
                "name": "Homer Simpson",
                "uuid": "1234",
            },
            "client": {
                "app_name": "1Password Browser Extension",
                "app_version": "20184",
                "ip_address": "1.1.1.1",
                "os_name": "Solaris",
                "os_version": "10",
                "platform_name": "Chrome",
                "platform_version": "96.0.4664.55",
            },
            "p_log_type": "OnePassword.SignInAttempt",
        },
    ),
    PantherRuleTest(
        Name="1Password - Failed Login",
        ExpectedResult=True,
        Mocks=[
            RuleMock(
                ObjectName="geoinfo_from_ip",
                ReturnValue='{ "ip": "111.111.111.111", "region": "UnitTestRegion", "city": "UnitTestCityNew", "country": "UnitTestCountry", "hostname": "somedomain.com", "org": "Some Org" }',
            )
        ],
        Log={
            "uuid": "1234",
            "session_uuid": "5678",
            "timestamp": "2021-12-03 19:52:52",
            "category": "credentials_failed",
            "type": "password_secret_bad",
            "country": "US",
            "target_user": {
                "email": "homer@springfield.gov",
                "name": "Homer Simpson",
                "uuid": "1234",
            },
            "client": {
                "app_name": "1Password Browser Extension",
                "app_version": "20184",
                "ip_address": "111.111.111.111",
                "os_name": "Solaris",
                "os_version": "10",
                "platform_name": "Chrome",
                "platform_version": "96.0.4664.55",
            },
            "p_log_type": "OnePassword.SignInAttempt",
            "p_parse_time": "2021-06-04 10:02:33.650807",
            "p_event_time": "2021-06-04 09:59:53.650807",
        },
    ),
]


class StandardBruteForceByIP(PantherRule):
    RuleID = "Standard.BruteForceByIP-prototype"
    DisplayName = "Brute Force By IP"
    LogTypes = [
        LogType.Asana_Audit,
        LogType.Atlassian_Audit,
        LogType.AWS_CloudTrail,
        LogType.Box_Event,
        LogType.GSuite_Reports,
        LogType.Okta_SystemLog,
        LogType.OneLogin_Events,
        LogType.OnePassword_SignInAttempt,
    ]
    Severity = PantherSeverity.Info
    Tags = ["DataModel", "Credential Access:Brute Force"]
    Threshold = 20
    Reports = {"MITRE ATT&CK": ["TA0006:T1110"]}
    Description = "An actor user was denied login access more times than the configured threshold."
    Runbook = "Analyze the IP they came from, and other actions taken before/after. Check if a user from this ip eventually authenticated successfully."
    Reference = "https://owasp.org/www-community/controls/Blocking_Brute_Force_Attacks"
    SummaryAttributes = ["p_any_ip_addresses"]
    Tests = standard_brute_force_by_ip_tests

    def rule(self, event):
        # filter events on unified data model field
        return event.udm("event_type") == event_type.FAILED_LOGIN

    def title(self, event):
        # use unified data model field in title
        log_type = event.get("p_log_type")
        title_str = (
            f"{log_type}: User [{event.udm('actor_user')}] has exceeded the failed logins threshold"
        )
        if log_type == "AWS.CloudTrail":
            title_str += f" in [{lookup_aws_account_name(event.get('recipientAccountId'))}]"
        return title_str

    def alert_context(self, event):
        geoinfo = geoinfo_from_ip(event.udm("source_ip"))
        if isinstance(geoinfo, str):
            geoinfo = loads(geoinfo)
        context = {}
        context["geolocation"] = (
            f"{geoinfo.get('city')}, {geoinfo.get('region')} in {geoinfo.get('country')}"
        )
        context["ip"] = geoinfo.get("ip")
        context["reverse_lookup"] = geoinfo.get("hostname", "No reverse lookup hostname")
        context["ip_org"] = geoinfo.get("org", "No organization listed")
        context = add_parse_delay(event, context)
        return context

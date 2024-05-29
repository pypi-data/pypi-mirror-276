import re
from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_auth0_helpers import auth0_alert_context, is_auth0_config_event
from pypanther.helpers.panther_base_helpers import deep_get
from pypanther.log_types import LogType

auth0_user_invitation_created_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Test-org",
        ExpectedResult=True,
        Log={
            "data": {
                "_id": "90020230616045255729813000000000000001223372038324184656",
                "client_id": "6xNLmMWZMYvMO3ZjQoN8siUWAbg3pnpA",
                "client_name": "",
                "date": "2023-06-16T04:52:50.663Z",
                "description": "Create invitations to organization",
                "details": {
                    "request": {
                        "auth": {
                            "credentials": {"jti": "81a67a5a3b2c4fb5cc2fcf38349456dd"},
                            "strategy": "jwt",
                            "user": {
                                "email": "bob@panther.com",
                                "name": "Bob",
                                "user_id": "google-oauth2|115547599209686809398",
                            },
                        },
                        "body": {
                            "client_id": "KwJItGFu62zryEc4c8t5BQuwB1qdeDFa",
                            "invitee": {"email": "larry@example.com"},
                            "inviter": {"name": "Larry Jones"},
                        },
                        "channel": "https://manage.auth0.com/",
                        "ip": "123.123.123.123",
                        "method": "post",
                        "path": "/api/v2/organizations/org_tFmw9RlOUjoSkOf1/invitations",
                        "query": {},
                        "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                    },
                    "response": {
                        "body": {
                            "client_id": "KwJItGFu62zryEc4c8t5BQuwB1qdeDFa",
                            "id": "uinv_DeLuEdgf3hjxRd0z",
                            "invitee": {"email": "frank@example.com"},
                            "inviter": {"name": "Bob Jones"},
                        },
                        "statusCode": 201,
                    },
                },
                "id": "90020230616045255729813000000000000001223372038324184656",
                "ip": "123.123.123.123",
                "isMobile": False,
                "log_id": "90020230616045255729813000000000000001223372038324184656",
                "type": "sapi",
                "user_agent": "Chrome 114.0.0 / Mac OS X 10.15.7",
                "user_id": "google-oauth2|115547599209686809398",
            },
            "p_any_ip_addresses": ["12.12.12.12"],
            "p_any_usernames": ["auth0|6459776e974703f3a65dc258"],
            "p_event_time": "2023-05-15 16:13:53.609",
            "p_log_type": "Auth0.Events",
            "p_parse_time": "2023-05-15 16:15:28.555",
            "p_row_id": "e20ac28001d19ac6df97b99618d4a207",
            "p_schema_version": 0,
            "p_source_id": "b9031579-b2c5-45c2-b15c-632b995a4e36",
            "p_source_label": "Auth0 Org Label",
        },
    ),
    PantherRuleTest(
        Name="Test-org-regex-fail",
        ExpectedResult=False,
        Log={
            "data": {
                "_id": "90020230616045255729813000000000000001223372038324184656",
                "client_id": "6xNLmMWZMYvMO3ZjQoN8siUWAbg3pnpA",
                "client_name": "",
                "date": "2023-06-16T04:52:50.663Z",
                "description": "Create invitations to organization",
                "details": {
                    "request": {
                        "auth": {
                            "credentials": {"jti": "81a67a5a3b2c4fb5cc2fcf38349456dd"},
                            "strategy": "jwt",
                            "user": {
                                "email": "bob@panther.com",
                                "name": "Bob",
                                "user_id": "google-oauth2|115547599209686809398",
                            },
                        },
                        "body": {
                            "client_id": "KwJItGFu62zryEc4c8t5BQuwB1qdeDFa",
                            "invitee": {"email": "larry@example.com"},
                            "inviter": {"name": "Larry Jones"},
                        },
                        "channel": "https://manage.auth0.com/",
                        "ip": "123.123.123.123",
                        "method": "post",
                        "path": "/api/v2/organizations/more/org_tFmw9RlOUjoSkOf1/invitations",
                        "query": {},
                        "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                    },
                    "response": {
                        "body": {
                            "client_id": "KwJItGFu62zryEc4c8t5BQuwB1qdeDFa",
                            "id": "uinv_DeLuEdgf3hjxRd0z",
                            "invitee": {"email": "frank@example.com"},
                            "inviter": {"name": "Bob Jones"},
                        },
                        "statusCode": 201,
                    },
                },
                "id": "90020230616045255729813000000000000001223372038324184656",
                "ip": "35.167.74.121",
                "isMobile": False,
                "log_id": "90020230616045255729813000000000000001223372038324184656",
                "type": "sapi",
                "user_agent": "Chrome 114.0.0 / Mac OS X 10.15.7",
                "user_id": "google-oauth2|115547599209686809398",
            },
            "p_any_ip_addresses": ["12.12.12.12"],
            "p_any_usernames": ["auth0|6459776e974703f3a65dc258"],
            "p_event_time": "2023-05-15 16:13:53.609",
            "p_log_type": "Auth0.Events",
            "p_parse_time": "2023-05-15 16:15:28.555",
            "p_row_id": "e20ac28001d19ac6df97b99618d4a207",
            "p_schema_version": 0,
            "p_source_id": "b9031579-b2c5-45c2-b15c-632b995a4e36",
            "p_source_label": "Auth0 Tenant Label",
        },
    ),
    PantherRuleTest(
        Name="Test-other-endpoint",
        ExpectedResult=False,
        Log={
            "data": {
                "client_id": "1HXWWGKk1Zj3JF8GvMrnCSirccDs4qvr",
                "client_name": "",
                "date": "2023-05-15 16:13:53.609000000",
                "description": "Create tenant invitations for a given client",
                "details": {
                    "request": {
                        "auth": {
                            "credentials": {
                                "jti": "dc1843dbe925a1ed2e707452c2123913",
                                "scopes": ["create:actions", "create:actions_log_sessions"],
                            },
                            "strategy": "jwt",
                            "user": {
                                "email": "homer.simpson@yourcompany.io",
                                "name": "homer.simpson@yourcompany.io",
                                "user_id": "auth0|6459776e974703f3a65dc258",
                            },
                        },
                        "body": {"owners": ["marge.simpson@yourcompany.io"], "roles": ["owner"]},
                        "channel": "https://manage.auth0.com/",
                        "ip": "12.12.12.12",
                        "method": "post",
                        "path": "/api/v2/some-other-endpoint",
                        "query": {},
                        "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                    },
                    "response": {
                        "body": [
                            {
                                "email": "marge.simpson@yourcompany.io",
                                "expires_at": "2023-05-18T16:13:53.600Z",
                                "invitation_id": "inv_TEyzbreI336AHrfU",
                            }
                        ],
                        "statusCode": 201,
                    },
                },
                "ip": "12.12.12.12",
                "log_id": "90020230515161358744602000000000000001223372037485092159",
                "type": "sapi",
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                "user_id": "auth0|6459776e974703f3a65dc258",
            },
            "log_id": "90020230515161358744602000000000000001223372037485092159",
            "p_any_ip_addresses": ["12.12.12.12"],
            "p_any_usernames": ["auth0|6459776e974703f3a65dc258"],
            "p_event_time": "2023-05-15 16:13:53.609",
            "p_log_type": "Auth0.Events",
            "p_parse_time": "2023-05-15 16:15:28.555",
            "p_row_id": "e20ac28001d19ac6df97b99618d4a207",
            "p_schema_version": 0,
            "p_source_id": "b9031579-b2c5-45c2-b15c-632b995a4e36",
            "p_source_label": "Org Auth0 Tenant Label",
        },
    ),
    PantherRuleTest(
        Name="Test-no-invitee",
        ExpectedResult=True,
        Log={
            "data": {
                "client_id": "1HXWWGKk1Zj3JF8GvMrnCSirccDs4qvr",
                "client_name": "",
                "date": "2023-05-15 16:13:53.609000000",
                "description": "Create tenant invitations for a given client",
                "details": {
                    "request": {
                        "auth": {
                            "credentials": {
                                "jti": "dc1843dbe925a1ed2e707452c2123913",
                                "scopes": ["create:actions", "create:actions_log_sessions"],
                            },
                            "strategy": "jwt",
                            "user": {
                                "email": "homer.simpson@yourcompany.io",
                                "name": "homer.simpson@yourcompany.io",
                                "user_id": "auth0|6459776e974703f3a65dc258",
                            },
                        },
                        "body": None,
                        "channel": "https://manage.auth0.com/",
                        "ip": "12.12.12.12",
                        "method": "post",
                        "path": "/api/v2/tenants/invitations",
                        "query": {},
                        "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                    },
                    "response": {
                        "body": [
                            {
                                "email": "marge.simpson@yourcompany.io",
                                "expires_at": "2023-05-18T16:13:53.600Z",
                                "invitation_id": "inv_TEyzbreI336AHrfU",
                            }
                        ],
                        "statusCode": 201,
                    },
                },
                "ip": "12.12.12.12",
                "log_id": "90020230515161358744602000000000000001223372037485092159",
                "type": "sapi",
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                "user_id": "auth0|6459776e974703f3a65dc258",
            },
            "log_id": "90020230515161358744602000000000000001223372037485092159",
            "p_any_ip_addresses": ["12.12.12.12"],
            "p_any_usernames": ["auth0|6459776e974703f3a65dc258"],
            "p_event_time": "2023-05-15 16:13:53.609",
            "p_log_type": "Auth0.Events",
            "p_parse_time": "2023-05-15 16:15:28.555",
            "p_row_id": "e20ac28001d19ac6df97b99618d4a207",
            "p_schema_version": 0,
            "p_source_id": "b9031579-b2c5-45c2-b15c-632b995a4e36",
            "p_source_label": "Auth0 Tenant Label",
        },
    ),
    PantherRuleTest(
        Name="Test-tenant",
        ExpectedResult=True,
        Log={
            "data": {
                "client_id": "1HXWWGKk1Zj3JF8GvMrnCSirccDs4qvr",
                "client_name": "",
                "date": "2023-05-15 16:13:53.609000000",
                "description": "Create tenant invitations for a given client",
                "details": {
                    "request": {
                        "auth": {
                            "credentials": {
                                "jti": "dc1843dbe925a1ed2e707452c2123913",
                                "scopes": ["create:actions", "create:actions_log_sessions"],
                            },
                            "strategy": "jwt",
                            "user": {
                                "email": "homer.simpson@yourcompany.io",
                                "name": "homer.simpson@yourcompany.io",
                                "user_id": "auth0|6459776e974703f3a65dc258",
                            },
                        },
                        "body": {"owners": ["marge.simpson@yourcompany.io"], "roles": ["owner"]},
                        "channel": "https://manage.auth0.com/",
                        "ip": "12.12.12.12",
                        "method": "post",
                        "path": "/api/v2/tenants/invitations",
                        "query": {},
                        "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                    },
                    "response": {
                        "body": [
                            {
                                "email": "marge.simpson@yourcompany.io",
                                "expires_at": "2023-05-18T16:13:53.600Z",
                                "invitation_id": "inv_TEyzbreI336AHrfU",
                            }
                        ],
                        "statusCode": 201,
                    },
                },
                "ip": "12.12.12.12",
                "log_id": "90020230515161358744602000000000000001223372037485092159",
                "type": "sapi",
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                "user_id": "auth0|6459776e974703f3a65dc258",
            },
            "log_id": "90020230515161358744602000000000000001223372037485092159",
            "p_any_ip_addresses": ["12.12.12.12"],
            "p_any_usernames": ["auth0|6459776e974703f3a65dc258"],
            "p_event_time": "2023-05-15 16:13:53.609",
            "p_log_type": "Auth0.Events",
            "p_parse_time": "2023-05-15 16:15:28.555",
            "p_row_id": "e20ac28001d19ac6df97b99618d4a207",
            "p_schema_version": 0,
            "p_source_id": "b9031579-b2c5-45c2-b15c-632b995a4e36",
            "p_source_label": "Auth0 Tenant Label",
        },
    ),
]


class Auth0UserInvitationCreated(PantherRule):
    DisplayName = "Auth0 User Invitation Created"
    Reference = (
        "https://auth0.com/docs/manage-users/organizations/configure-organizations/invite-members"
    )
    Severity = PantherSeverity.Info
    LogTypes = [LogType.Auth0_Events]
    RuleID = "Auth0.User.Invitation.Created-prototype"
    Tests = auth0_user_invitation_created_tests
    org_re = re.compile("^/api/v2/organizations/[^/\\s]+/invitations$")

    def rule(self, event):
        if not any([True, is_auth0_config_event(event)]):
            return False
        return self.invitation_type(event) is not None

    def title(self, event):
        inv_type = self.invitation_type(event)
        if inv_type == "tenant":
            try:
                invitee = deep_get(
                    event, "data", "details", "request", "body", "owners", default=[]
                )[0]
            except IndexError:
                invitee = "<NO_INVITEE>"
        elif inv_type == "organization":
            invitee = deep_get(event, "data", "details", "request", "body", "invitee", "email")
        else:
            invitee = "<NO_INVITEE>"
        inviter = deep_get(
            event, "data", "details", "request", "auth", "user", "email", default="<NO_INVITER>"
        )
        source = deep_get(event, "p_source_label", default="<NO_PSOURCE>")
        return f"Auth0 User [{inviter}] invited [{invitee}] to {inv_type.title()} [{source}]]"

    def invitation_type(self, event):
        path = deep_get(event, "data", "details", "request", "path", default="")
        if path == "/api/v2/tenants/invitations":
            return "tenant"
        if self.org_re.match(path):
            return "organization"
        return None

    def alert_context(self, event):
        return auth0_alert_context(event)

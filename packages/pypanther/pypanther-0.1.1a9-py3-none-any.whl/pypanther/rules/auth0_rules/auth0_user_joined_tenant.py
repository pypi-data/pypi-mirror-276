from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_auth0_helpers import auth0_alert_context, is_auth0_config_event
from pypanther.helpers.panther_base_helpers import deep_get
from pypanther.log_types import LogType

auth0_user_joined_tenant_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="User accepted an invitation",
        ExpectedResult=True,
        Log={
            "data": {
                "client_id": "1HXWWGKk1Zj3JF8GvMrnCSirccDs4qvr",
                "client_name": "",
                "date": "2023-05-15 16:17:00.128000000",
                "description": "Update an invitation",
                "details": {
                    "request": {
                        "auth": {
                            "credentials": {
                                "jti": "9da39f3d0b369356d2f4338ff13e4e8b",
                                "scopes": ["update:tenant_invitations"],
                            },
                            "strategy": "jwt",
                            "user": {
                                "email": "homer.simpson@yourcompany.com",
                                "name": "Homer Simpson",
                                "user_id": "google-oauth2|105261262156475850461",
                            },
                        },
                        "body": {
                            "state": "accepted",
                            "user": {
                                "email": "homer.simpson@yourcompany.com",
                                "id": "google-oauth2|105261262156475850461",
                            },
                        },
                        "channel": "https://manage.auth0.com/",
                        "ip": "12.12.12.12",
                        "method": "patch",
                        "path": "/api/v2/tenants/invitations/inv_TEyzbreI336AHrfU",
                        "query": {},
                    },
                    "response": {"body": {}, "statusCode": 200},
                },
                "ip": "12.12.12.12",
                "log_id": "90020230515161703699125000000000000001223372037485126920",
                "type": "sapi",
                "user_id": "google-oauth2|105261262156475850461",
            },
            "log_id": "90020230515161703699125000000000000001223372037485126920",
            "p_any_ip_addresses": ["12.12.12.12"],
            "p_any_usernames": ["google-oauth2|105261262156475850461"],
            "p_event_time": "2023-05-15 16:17:00.128",
            "p_log_type": "Auth0.Events",
            "p_parse_time": "2023-05-15 16:18:28.605",
            "p_row_id": "6e94415d533cdcaac7ffc79618fb9b01",
            "p_schema_version": 0,
            "p_source_id": "b9031579-b2c5-45c2-b15c-632b995a4e36",
            "p_source_label": "Org Auth0 Tenant Label",
        },
    ),
    PantherRuleTest(
        Name="User declined an invitation",
        ExpectedResult=False,
        Log={
            "data": {
                "client_id": "1HXWWGKk1Zj3JF8GvMrnCSirccDs4qvr",
                "client_name": "",
                "date": "2023-05-15 16:17:00.128000000",
                "description": "Update an invitation",
                "details": {
                    "request": {
                        "auth": {
                            "credentials": {
                                "jti": "9da39f3d0b369356d2f4338ff13e4e8b",
                                "scopes": ["update:tenant_invitations"],
                            },
                            "strategy": "jwt",
                            "user": {
                                "email": "homer.simpson@yourcompany.com",
                                "name": "Homer Simpson",
                                "user_id": "google-oauth2|105261262156475850461",
                            },
                        },
                        "body": {
                            "state": "declined",
                            "user": {
                                "email": "homer.simpson@yourcompany.com",
                                "id": "google-oauth2|105261262156475850461",
                            },
                        },
                        "channel": "https://manage.auth0.com/",
                        "ip": "12.12.12.12",
                        "method": "patch",
                        "path": "/api/v2/tenants/invitations/inv_TEyzbreI336AHrfU",
                        "query": {},
                    },
                    "response": {"body": {}, "statusCode": 200},
                },
                "ip": "12.12.12.12",
                "log_id": "90020230515161703699125000000000000001223372037485126920",
                "type": "sapi",
                "user_id": "google-oauth2|105261262156475850461",
            },
            "log_id": "90020230515161703699125000000000000001223372037485126920",
            "p_any_ip_addresses": ["12.12.12.12"],
            "p_any_usernames": ["google-oauth2|105261262156475850461"],
            "p_event_time": "2023-05-15 16:17:00.128",
            "p_log_type": "Auth0.Events",
            "p_parse_time": "2023-05-15 16:18:28.605",
            "p_row_id": "6e94415d533cdcaac7ffc79618fb9b01",
            "p_schema_version": 0,
            "p_source_id": "b9031579-b2c5-45c2-b15c-632b995a4e36",
            "p_source_label": "Org Auth0 Tenant Label",
        },
    ),
    PantherRuleTest(
        Name="Other event",
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
                                "scopes": [
                                    "create:actions",
                                    "create:actions_log_sessions",
                                    "create:authentication_methods",
                                    "create:client_credentials",
                                    "create:client_grants",
                                    "create:clients",
                                    "create:connections",
                                    "create:custom_domains",
                                    "create:email_provider",
                                    "create:email_templates",
                                    "create:guardian_enrollment_tickets",
                                    "create:integrations",
                                    "create:log_streams",
                                    "create:organization_connections",
                                    "create:organization_invitations",
                                    "create:organization_member_roles",
                                    "create:organization_members",
                                    "create:organizations",
                                    "create:requested_scopes",
                                    "create:resource_servers",
                                    "create:roles",
                                    "create:rules",
                                    "create:shields",
                                    "create:signing_keys",
                                    "create:tenant_invitations",
                                    "create:test_email_dispatch",
                                    "create:users",
                                    "delete:actions",
                                    "delete:anomaly_blocks",
                                    "delete:authentication_methods",
                                    "delete:branding",
                                    "delete:client_credentials",
                                    "delete:client_grants",
                                    "delete:clients",
                                    "delete:connections",
                                    "delete:custom_domains",
                                    "delete:device_credentials",
                                    "delete:email_provider",
                                    "delete:email_templates",
                                    "delete:grants",
                                    "delete:guardian_enrollments",
                                    "delete:integrations",
                                    "delete:log_streams",
                                    "delete:organization_connections",
                                    "delete:organization_invitations",
                                    "delete:organization_member_roles",
                                    "delete:organization_members",
                                    "delete:organizations",
                                    "delete:owners",
                                    "delete:requested_scopes",
                                    "delete:resource_servers",
                                    "delete:roles",
                                    "delete:rules",
                                    "delete:rules_configs",
                                    "delete:shields",
                                    "delete:tenant_invitations",
                                    "delete:tenant_members",
                                    "delete:tenants",
                                    "delete:users",
                                    "read:actions",
                                    "read:anomaly_blocks",
                                    "read:attack_protection",
                                    "read:authentication_methods",
                                    "read:branding",
                                    "read:checks",
                                    "read:client_credentials",
                                    "read:client_grants",
                                    "read:client_keys",
                                    "read:clients",
                                    "read:connections",
                                    "read:custom_domains",
                                    "read:device_credentials",
                                    "read:email_provider",
                                    "read:email_templates",
                                    "read:email_triggers",
                                    "read:entity_counts",
                                    "read:grants",
                                    "read:guardian_factors",
                                    "read:insights",
                                    "read:integrations",
                                    "read:log_streams",
                                    "read:logs",
                                    "read:mfa_policies",
                                    "read:organization_connections",
                                    "read:organization_invitations",
                                    "read:organization_member_roles",
                                    "read:organization_members",
                                    "read:organizations",
                                    "read:prompts",
                                    "read:requested_scopes",
                                    "read:resource_servers",
                                    "read:roles",
                                    "read:rules",
                                    "read:rules_configs",
                                    "read:shields",
                                    "read:signing_keys",
                                    "read:stats",
                                    "read:tenant_invitations",
                                    "read:tenant_members",
                                    "read:tenant_settings",
                                    "read:triggers",
                                    "read:users",
                                    "run:checks",
                                    "update:actions",
                                    "update:attack_protection",
                                    "update:authentication_methods",
                                    "update:branding",
                                    "update:client_credentials",
                                    "update:client_grants",
                                    "update:client_keys",
                                    "update:clients",
                                    "update:connections",
                                    "update:custom_domains",
                                    "update:email_provider",
                                    "update:email_templates",
                                    "update:email_triggers",
                                    "update:guardian_factors",
                                    "update:integrations",
                                    "update:log_streams",
                                    "update:mfa_policies",
                                    "update:organization_connections",
                                    "update:organizations",
                                    "update:prompts",
                                    "update:requested_scopes",
                                    "update:resource_servers",
                                    "update:roles",
                                    "update:rules",
                                    "update:rules_configs",
                                    "update:shields",
                                    "update:signing_keys",
                                    "update:tenant_members",
                                    "update:tenant_settings",
                                    "update:triggers",
                                    "update:users",
                                ],
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
            "p_source_label": "Org Auth0 Tenant Label",
        },
    ),
]


class Auth0UserJoinedTenant(PantherRule):
    DisplayName = "Auth0 User Joined Tenant"
    Description = "User accepted invitation from Auth0 member to join an Auth0 tenant."
    RuleID = "Auth0.User.Joined.Tenant-prototype"
    Reference = "https://auth0.com/docs/manage-users/organizations/configure-organizations/invite-members#send-membership-invitations:~:text=.-,Send%20membership%20invitations,-You%20can"
    Severity = PantherSeverity.Info
    LogTypes = [LogType.Auth0_Events]
    Tests = auth0_user_joined_tenant_tests

    def rule(self, event):
        data_description = deep_get(
            event, "data", "description", default="<NO_DATA_DESCRIPTION_FOUND>"
        )
        scopes = deep_get(
            event,
            "data",
            "details",
            "request",
            "auth",
            "credentials",
            "scopes",
            default=["<NO_CREDENTIAL_SCOPE>"],
        )
        state = deep_get(event, "data", "details", "request", "body", "state", default="<NO_STATE>")
        return all(
            [
                data_description == "Update an invitation",
                "update:tenant_invitations" in scopes,
                state == "accepted",
                is_auth0_config_event(event),
            ]
        )

    def title(self, event):
        user = deep_get(
            event, "data", "details", "request", "auth", "user", "email", default="<NO_USER_FOUND>"
        )
        p_source_label = deep_get(event, "p_source_label", default="<NO_P_SOURCE_LABEL_FOUND>")
        return f"Auth0 User [{user}] has accepted an invitation to join your organization's tenant [{p_source_label}]."

    def alert_context(self, event):
        return auth0_alert_context(event)

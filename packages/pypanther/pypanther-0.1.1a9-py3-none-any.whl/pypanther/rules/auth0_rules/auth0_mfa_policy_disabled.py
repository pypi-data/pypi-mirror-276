from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_auth0_helpers import auth0_alert_context, is_auth0_config_event
from pypanther.helpers.panther_base_helpers import deep_get
from pypanther.log_types import LogType

auth0_mfa_policy_disabled_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Other Event",
        ExpectedResult=False,
        Log={
            "data": {
                "client_id": "1HXWWGKk1Zj3JF8GvMrnCSirccDs4qvr",
                "client_name": "",
                "date": "2023-05-15 21:55:18.060000000",
                "description": "Updates risk assessment configs",
                "details": {
                    "request": {
                        "auth": {
                            "credentials": {
                                "jti": "949869e066205b5076e6df203fdd7b9b",
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
                                "email": "user.name@yourcompany.io",
                                "name": "User Name",
                                "user_id": "google-oauth2|105261262156475850461",
                            },
                        },
                        "body": {"AfterAuthentication": False},
                        "channel": "https://manage.auth0.com/",
                        "ip": "12.12.12.12",
                        "method": "patch",
                        "path": "/api/v2/risk-assessment/config",
                        "query": {},
                        "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                    },
                    "response": {
                        "body": {
                            "AfterAuthentication": False,
                            "BeforeLoginPrompt": False,
                            "BeforeLoginPromptMonitoring": False,
                        },
                        "statusCode": 200,
                    },
                },
                "ip": "12.12.12.12",
                "log_id": "90020230515215719063964000000000000001223372037488829643",
                "type": "sapi",
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                "user_id": "google-oauth2|105261262156475850461",
            },
            "log_id": "90020230515215719063964000000000000001223372037488829643",
            "p_any_ip_addresses": ["12.12.12.12"],
            "p_any_usernames": ["google-oauth2|105261262156475850461"],
            "p_event_time": "2023-05-15 21:55:18.06",
            "p_log_type": "Auth0.Events",
            "p_parse_time": "2023-05-15 21:58:28.629",
            "p_row_id": "42b742dba9d5f3f284d49b971814",
            "p_schema_version": 0,
            "p_source_id": "b9031579-b2c5-45c2-b15c-632b995a4e36",
            "p_source_label": "Org Tenant Label",
        },
    ),
    PantherRuleTest(
        Name="MFA Policy Disabled",
        ExpectedResult=True,
        Log={
            "data": {
                "client_id": "1HXWWGKk1Zj3JF8GvMrnCSirccDs4qvr",
                "client_name": "",
                "date": "2023-05-16 17:28:11.165000000",
                "description": "Set the Multi-factor Authentication policies",
                "details": {
                    "request": {
                        "auth": {
                            "credentials": {
                                "jti": "0107c849078d8d889af711840197ba7c",
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
                                "email": "user.name@yourcompany.io",
                                "name": "User Name",
                                "user_id": "google-oauth2|105261262156475850461",
                            },
                        },
                        "body": [],
                        "channel": "https://manage.auth0.com/",
                        "ip": "12.12.12.12",
                        "method": "put",
                        "path": "/api/v2/guardian/policies",
                        "query": {},
                        "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                    },
                    "response": {"body": [], "statusCode": 200},
                },
                "ip": "12.12.12.12",
                "log_id": "90020230516172812328948000000000000001223372037498448373",
                "type": "sapi",
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                "user_id": "google-oauth2|105261262156475850461",
            },
            "log_id": "90020230516172812328948000000000000001223372037498448373",
            "p_any_ip_addresses": ["12.12.12.12"],
            "p_any_usernames": ["google-oauth2|105261262156475850461"],
            "p_event_time": "2023-05-16 17:28:11.165",
            "p_log_type": "Auth0.Events",
            "p_parse_time": "2023-05-16 17:29:28.904",
            "p_row_id": "a2d1b1713461e7a5f1b08f991886e402",
            "p_schema_version": 0,
            "p_source_id": "b9031579-b2c5-45c2-b15c-632b995a4e36",
            "p_source_label": "Org Tenant Label",
        },
    ),
]


class Auth0MFAPolicyDisabled(PantherRule):
    Description = "An Auth0 User disabled MFA for your organization's tenant."
    DisplayName = "Auth0 MFA Policy Disabled"
    Runbook = "Assess if this was done by the user for a valid business reason. Be vigilant to re-enable this setting as it's in the best security interest for your organization's security posture."
    Reference = "https://auth0.com/docs/secure/multi-factor-authentication/enable-mfa#:~:text=prompted%20for%20MFA.-,Never,-%3A%20MFA%20is%20not"
    Severity = PantherSeverity.High
    LogTypes = [LogType.Auth0_Events]
    RuleID = "Auth0.MFA.Policy.Disabled-prototype"
    Tests = auth0_mfa_policy_disabled_tests

    def rule(self, event):
        data_description = deep_get(
            event, "data", "description", default="<NO_DATA_DESCRIPTION_FOUND>"
        )
        request_path = deep_get(
            event, "data", "details", "request", "path", default="<NO_REQUEST_PATH_FOUND>"
        )
        request_body = deep_get(event, "data", "details", "request", "body", default=[-1])
        return all(
            [
                data_description == "Set the Multi-factor Authentication policies",
                request_path == "/api/v2/guardian/policies",
                request_body == [],
                is_auth0_config_event(event),
            ]
        )

    def title(self, event):
        user = deep_get(
            event, "data", "details", "request", "auth", "user", "email", default="<NO_USER_FOUND>"
        )
        p_source_label = deep_get(event, "p_source_label", default="<NO_P_SOURCE_LABEL_FOUND>")
        return f"Auth0 User [{user}] set mfa requirement settings to 'Never' for your organization's tenant [{p_source_label}]."

    def alert_context(self, event):
        return auth0_alert_context(event)

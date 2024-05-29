import json
from typing import List
from unittest.mock import MagicMock

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity, RuleMock
from pypanther.helpers.panther_base_helpers import deep_get
from pypanther.helpers.panther_base_helpers import gsuite_parameter_lookup as param_lookup
from pypanther.log_types import LogType

g_suite_drive_visibility_changed_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Access Event",
        ExpectedResult=False,
        Log={
            "p_row_id": "111222",
            "actor": {"email": "bobert@example.com"},
            "id": {"applicationName": "drive"},
            "events": [{"type": "access", "name": "upload"}],
        },
    ),
    PantherRuleTest(
        Name="ACL Change without Visibility Change",
        ExpectedResult=False,
        Log={
            "p_row_id": "111222",
            "actor": {"email": "bobert@example.com"},
            "id": {"applicationName": "drive"},
            "events": [{"type": "acl_change", "name": "shared_drive_settings_change"}],
        },
    ),
    PantherRuleTest(
        Name="Doc Became Public - Link (Unrestricted)",
        ExpectedResult=True,
        Log={
            "actor": {"email": "bobert@gmail.com"},
            "events": [
                {
                    "parameters": [
                        {"name": "visibility_change", "value": "external"},
                        {"name": "doc_title", "value": "my shared document"},
                        {"name": "target_domain", "value": "all"},
                        {"name": "visibility", "value": "people_with_link"},
                        {"name": "new_value", "multiValue": ["people_with_link"]},
                    ],
                    "name": "change_document_visibility",
                    "type": "acl_change",
                },
                {
                    "parameters": [{"name": "new_value", "multiValue": ["can_view"]}],
                    "name": "change_document_access_scope",
                    "type": "acl_change",
                },
            ],
            "id": {"applicationName": "drive"},
            "p_row_id": "111222",
        },
    ),
    PantherRuleTest(
        Name="Doc Became Public - Link (Allowlisted Domain Not Configured)",
        ExpectedResult=True,
        Log={
            "actor": {"email": "bobert@example.com"},
            "events": [
                {
                    "parameters": [
                        {"name": "visibility_change", "value": "external"},
                        {"name": "doc_title", "value": "my shared document"},
                        {"name": "target_domain", "value": "example.com"},
                        {"name": "visibility", "value": "people_within_domain_with_link"},
                        {"name": "new_value", "multiValue": ["people_with_link"]},
                    ],
                    "name": "change_document_visibility",
                    "type": "acl_change",
                },
                {
                    "parameters": [{"name": "new_value", "multiValue": ["can_view"]}],
                    "name": "change_document_access_scope",
                    "type": "acl_change",
                },
            ],
            "id": {"applicationName": "drive"},
            "p_row_id": "111222",
        },
    ),
    PantherRuleTest(
        Name="Doc Became Public - Link (Allowlisted Domain Is Configured)",
        ExpectedResult=False,
        Mocks=[RuleMock(ObjectName="ALLOWED_DOMAINS", ReturnValue='[\n  "example.com"\n]')],
        Log={
            "actor": {"email": "bobert@example.com"},
            "events": [
                {
                    "parameters": [
                        {"name": "visibility_change", "value": "external"},
                        {"name": "doc_title", "value": "my shared document"},
                        {"name": "target_domain", "value": "example.com"},
                        {"name": "visibility", "value": "people_within_domain_with_link"},
                        {"name": "new_value", "multiValue": ["people_with_link"]},
                    ],
                    "name": "change_document_visibility",
                    "type": "acl_change",
                },
                {
                    "parameters": [{"name": "new_value", "multiValue": ["can_view"]}],
                    "name": "change_document_access_scope",
                    "type": "acl_change",
                },
            ],
            "id": {"applicationName": "drive"},
            "p_row_id": "111222",
        },
    ),
    PantherRuleTest(
        Name="Doc Became Private - Link",
        ExpectedResult=False,
        Log={
            "actor": {"email": "bobert@example.com"},
            "events": [
                {
                    "parameters": [
                        {"name": "visibility_change", "value": "external"},
                        {"name": "doc_title", "value": "my shared document"},
                        {"name": "target_domain", "value": "all"},
                        {"name": "visibility", "value": "people_with_link"},
                        {"name": "new_value", "multiValue": ["private"]},
                    ],
                    "name": "change_document_visibility",
                    "type": "acl_change",
                }
            ],
            "id": {"applicationName": "drive"},
            "p_row_id": "111222",
        },
    ),
    PantherRuleTest(
        Name="Doc Became Public - User",
        ExpectedResult=True,
        Log={
            "id": {"applicationName": "drive"},
            "actor": {"email": "bobert@example.com"},
            "kind": "admin#reports#activity",
            "ipAddress": "1.1.1.1",
            "events": [
                {
                    "type": "access",
                    "name": "edit",
                    "parameters": [
                        {"name": "primary_event"},
                        {"name": "doc_title", "value": "Hosted Accounts"},
                        {"name": "visibility", "value": "shared_externally"},
                    ],
                },
                {
                    "type": "acl_change",
                    "name": "change_user_access",
                    "parameters": [
                        {"name": "primary_event", "boolValue": True},
                        {"name": "visibility_change", "value": "external"},
                        {"name": "target_user", "value": "someone@random.com"},
                        {"name": "old_value", "multiValue": ["none"]},
                        {"name": "new_value", "multiValue": ["can_view"]},
                        {"name": "old_visibility", "value": "people_within_domain_with_link"},
                        {"name": "doc_title", "value": "Hosted Accounts"},
                        {"name": "visibility", "value": "shared_externally"},
                    ],
                },
            ],
        },
    ),
    PantherRuleTest(
        Name="Doc Became Public - User (Multiple)",
        ExpectedResult=True,
        Log={
            "id": {"applicationName": "drive"},
            "actor": {"email": "bobert@example.com"},
            "kind": "admin#reports#activity",
            "ipAddress": "1.1.1.1",
            "events": [
                {
                    "type": "access",
                    "name": "edit",
                    "parameters": [
                        {"name": "primary_event"},
                        {"name": "doc_title", "value": "Hosted Accounts"},
                        {"name": "visibility", "value": "shared_externally"},
                    ],
                },
                {
                    "type": "acl_change",
                    "name": "change_user_access",
                    "parameters": [
                        {"name": "primary_event", "boolValue": True},
                        {"name": "visibility_change", "value": "external"},
                        {"name": "target_user", "value": "someone@random.com"},
                        {"name": "old_value", "multiValue": ["none"]},
                        {"name": "new_value", "multiValue": ["can_view"]},
                        {"name": "old_visibility", "value": "people_within_domain_with_link"},
                        {"name": "doc_title", "value": "Hosted Accounts"},
                        {"name": "visibility", "value": "shared_externally"},
                    ],
                },
                {
                    "type": "acl_change",
                    "name": "change_user_access",
                    "parameters": [
                        {"name": "primary_event", "boolValue": True},
                        {"name": "visibility_change", "value": "external"},
                        {"name": "target_user", "value": "someoneelse@random.com"},
                        {"name": "old_value", "multiValue": ["none"]},
                        {"name": "new_value", "multiValue": ["can_view"]},
                        {"name": "old_visibility", "value": "people_within_domain_with_link"},
                        {"name": "doc_title", "value": "Hosted Accounts"},
                        {"name": "visibility", "value": "shared_externally"},
                    ],
                },
                {
                    "type": "acl_change",
                    "name": "change_user_access",
                    "parameters": [
                        {"name": "primary_event", "boolValue": True},
                        {"name": "visibility_change", "value": "external"},
                        {"name": "target_user", "value": "notbobert@example.com"},
                        {"name": "old_value", "multiValue": ["none"]},
                        {"name": "new_value", "multiValue": ["can_view"]},
                        {"name": "old_visibility", "value": "people_within_domain_with_link"},
                        {"name": "doc_title", "value": "Hosted Accounts"},
                        {"name": "visibility", "value": "shared_externally"},
                    ],
                },
            ],
        },
    ),
    PantherRuleTest(
        Name="Doc Inherits Folder Permissions",
        ExpectedResult=False,
        Log={
            "p_row_id": "111222",
            "actor": {"email": "bobert@example.com"},
            "id": {"applicationName": "drive"},
            "events": [
                {
                    "name": "change_user_access_hierarchy_reconciled",
                    "type": "acl_change",
                    "parameters": [{"name": "visibility_change", "value": "internal"}],
                }
            ],
        },
    ),
    PantherRuleTest(
        Name="Doc Inherits Folder Permissions - Sharing Link",
        ExpectedResult=False,
        Log={
            "p_row_id": "111222",
            "actor": {"email": "bobert@example.com"},
            "id": {"applicationName": "drive"},
            "events": [
                {
                    "name": "change_document_access_scope_hierarchy_reconciled",
                    "type": "acl_change",
                    "parameters": [{"name": "visibility_change", "value": "internal"}],
                }
            ],
        },
    ),
    PantherRuleTest(
        Name="Doc Became Public - Public email provider",
        ExpectedResult=True,
        Log={
            "id": {"applicationName": "drive"},
            "actor": {"email": "bobert@example.com"},
            "kind": "admin#reports#activity",
            "ipAddress": "1.1.1.1",
            "events": [
                {
                    "type": "access",
                    "name": "edit",
                    "parameters": [
                        {"name": "primary_event"},
                        {"name": "doc_title", "value": "Hosted Accounts"},
                        {"name": "visibility", "value": "shared_externally"},
                    ],
                },
                {
                    "type": "acl_change",
                    "name": "change_user_access",
                    "parameters": [
                        {"name": "primary_event", "boolValue": True},
                        {"name": "visibility_change", "value": "external"},
                        {"name": "target_user", "value": "someone@yandex.com"},
                        {"name": "old_value", "multiValue": ["none"]},
                        {"name": "new_value", "multiValue": ["can_view"]},
                        {"name": "old_visibility", "value": "people_within_domain_with_link"},
                        {"name": "doc_title", "value": "Hosted Accounts"},
                        {"name": "visibility", "value": "shared_externally"},
                    ],
                },
            ],
        },
    ),
    PantherRuleTest(
        Name="Doc Shared With Multiple Users All From ALLOWED_DOMAINS",
        ExpectedResult=False,
        Mocks=[
            RuleMock(
                ObjectName="ALLOWED_DOMAINS", ReturnValue='[\n  "example.com", "notexample.com"\n]'
            )
        ],
        Log={
            "id": {"applicationName": "drive"},
            "actor": {"email": "bobert@example.com"},
            "kind": "admin#reports#activity",
            "ipAddress": "1.1.1.1",
            "events": [
                {
                    "type": "access",
                    "name": "edit",
                    "parameters": [
                        {"name": "primary_event"},
                        {"name": "doc_title", "value": "Hosted Accounts"},
                        {"name": "visibility", "value": "shared_externally"},
                    ],
                },
                {
                    "type": "acl_change",
                    "name": "change_user_access",
                    "parameters": [
                        {"name": "primary_event", "boolValue": True},
                        {"name": "visibility_change", "value": "external"},
                        {"name": "target_user", "value": "someone@notexample.com"},
                        {"name": "old_value", "multiValue": ["none"]},
                        {"name": "new_value", "multiValue": ["can_view"]},
                        {"name": "old_visibility", "value": "people_within_domain_with_link"},
                        {"name": "doc_title", "value": "Hosted Accounts"},
                        {"name": "visibility", "value": "shared_externally"},
                    ],
                },
                {
                    "type": "acl_change",
                    "name": "change_user_access",
                    "parameters": [
                        {"name": "primary_event", "boolValue": True},
                        {"name": "visibility_change", "value": "external"},
                        {"name": "target_user", "value": "someoneelse@example.com"},
                        {"name": "old_value", "multiValue": ["none"]},
                        {"name": "new_value", "multiValue": ["can_view"]},
                        {"name": "old_visibility", "value": "people_within_domain_with_link"},
                        {"name": "doc_title", "value": "Hosted Accounts"},
                        {"name": "visibility", "value": "shared_externally"},
                    ],
                },
                {
                    "type": "acl_change",
                    "name": "change_user_access",
                    "parameters": [
                        {"name": "primary_event", "boolValue": True},
                        {"name": "visibility_change", "value": "external"},
                        {"name": "target_user", "value": "notbobert@example.com"},
                        {"name": "old_value", "multiValue": ["none"]},
                        {"name": "new_value", "multiValue": ["can_view"]},
                        {"name": "old_visibility", "value": "people_within_domain_with_link"},
                        {"name": "doc_title", "value": "Hosted Accounts"},
                        {"name": "visibility", "value": "shared_externally"},
                    ],
                },
            ],
        },
    ),
]


class GSuiteDriveVisibilityChanged(PantherRule):
    RuleID = "GSuite.DriveVisibilityChanged-prototype"
    DisplayName = "GSuite External Drive Document"
    Enabled = False
    LogTypes = [LogType.GSuite_Reports]
    Tags = ["GSuite", "Collection:Data from Information Repositories", "Configuration Required"]
    Reports = {"MITRE ATT&CK": ["TA0009:T1213"]}
    Severity = PantherSeverity.Low
    Description = "A Google drive resource became externally accessible.\n"
    Reference = (
        "https://support.google.com/a/users/answer/12380484?hl=en&sjid=864417124752637253-EU"
    )
    Runbook = "Investigate whether the drive document is appropriate to be publicly accessible.\n"
    SummaryAttributes = ["actor:email"]
    DedupPeriodMinutes = 360
    Tests = g_suite_drive_visibility_changed_tests
    # Add any domain name(s) that you expect to share documents with in the ALLOWED_DOMAINS set
    ALLOWED_DOMAINS = set()
    PUBLIC_PROVIDERS = {
        "gmail.com",
        "yahoo.com",
        "outlook.com",
        "aol.com",
        "yandex.com",
        "protonmail.com",
        "pm.me",
        "icloud.com",
        "tutamail.com",
        "tuta.io",
        "keemail.me",
        "mail.com",
        "zohomail.com",
        "hotmail.com",
        "msn.com",
    }
    VISIBILITY = {
        "people_with_link",
        "people_within_domain_with_link",
        "public_on_the_web",
        "shared_externally",
        "unknown",
    }
    ALERT_DETAILS = {}
    # Events where documents have changed perms due to parent folder change
    INHERITANCE_EVENTS = {
        "change_user_access_hierarchy_reconciled",
        "change_document_access_scope_hierarchy_reconciled",
    }

    def init_alert_details(self, log):
        self.ALERT_DETAILS[log] = {
            "ACCESS_SCOPE": "<UNKNOWN_ACCESS_SCOPE>",
            "DOC_TITLE": "<UNKNOWN_TITLE>",
            "NEW_VISIBILITY": "<UNKNOWN_VISIBILITY>",
            "TARGET_USER_EMAILS": ["<UNKNOWN_USER>"],
            "TARGET_DOMAIN": "<UNKNOWN_DOMAIN>",
        }

    def user_is_external(self, target_user):
        # We need to type-cast ALLOWED_DOMAINS for unit testing mocks
        if isinstance(self.ALLOWED_DOMAINS, MagicMock):
            self.ALLOWED_DOMAINS = set(
                json.loads(self.ALLOWED_DOMAINS())
            )  # pylint: disable=not-callable
        for domain in self.ALLOWED_DOMAINS:
            if domain in target_user:
                return False
        return True

    def rule(self, event):
        # pylint: disable=too-complex
        if deep_get(event, "id", "applicationName") != "drive":
            return False
        # Events that have the types in INHERITANCE_EVENTS are
        # changes to documents and folders that occur due to
        # a change in the parent folder's permission. We ignore
        # these events to prevent every folder change from
        # generating multiple alerts.
        if deep_get(event, "events", "name") in self.INHERITANCE_EVENTS:
            return False
        log = event.get("p_row_id")
        self.init_alert_details(log)
        #########
        # for visibility changes that apply to a domain, not a user
        change_document_visibility = False
        # We need to type-cast ALLOWED_DOMAINS for unit testing mocks
        if isinstance(self.ALLOWED_DOMAINS, MagicMock):
            self.ALLOWED_DOMAINS = set(
                json.loads(self.ALLOWED_DOMAINS())
            )  # pylint: disable=not-callable
        for details in event.get("events", [{}]):
            if (
                details.get("type") == "acl_change"
                and details.get("name") == "change_document_visibility"
                and (param_lookup(details.get("parameters", {}), "new_value") != ["private"])
                and (
                    not param_lookup(details.get("parameters", {}), "target_domain")
                    in self.ALLOWED_DOMAINS
                )
                and (param_lookup(details.get("parameters", {}), "visibility") in self.VISIBILITY)
            ):
                self.ALERT_DETAILS[log]["TARGET_DOMAIN"] = param_lookup(
                    details.get("parameters", {}), "target_domain"
                )
                self.ALERT_DETAILS[log]["NEW_VISIBILITY"] = param_lookup(
                    details.get("parameters", {}), "visibility"
                )
                self.ALERT_DETAILS[log]["DOC_TITLE"] = param_lookup(
                    details.get("parameters", {}), "doc_title"
                )
                change_document_visibility = True
                break
        # "change_document_visibility" events are always paired with
        # "change_document_access_scope" events. the "target_domain" and
        # "visibility" attributes are equivalent.
        if change_document_visibility:
            for details in event.get("events", [{}]):
                if (
                    details.get("type") == "acl_change"
                    and details.get("name") == "change_document_access_scope"
                    and (param_lookup(details.get("parameters", {}), "new_value") != ["none"])
                ):
                    self.ALERT_DETAILS[log]["ACCESS_SCOPE"] = param_lookup(
                        details.get("parameters", {}), "new_value"
                    )
            return True
        #########
        # for visibility changes that apply to a user
        # there is a change_user_access event for each user
        # change_user_access and change_document_visibility events are
        # not found in the same report
        change_user_access = False
        for details in event.get("events", [{}]):
            if (
                details.get("type") == "acl_change"
                and details.get("name") == "change_user_access"
                and (param_lookup(details.get("parameters", {}), "new_value") != ["none"])
                and self.user_is_external(
                    param_lookup(details.get("parameters", {}), "target_user")
                )
            ):
                if self.ALERT_DETAILS[log]["TARGET_USER_EMAILS"] != ["<UNKNOWN_USER>"]:
                    self.ALERT_DETAILS[log]["TARGET_USER_EMAILS"].append(
                        param_lookup(details.get("parameters", {}), "target_user")
                    )
                else:
                    self.ALERT_DETAILS[log]["TARGET_USER_EMAILS"] = [
                        param_lookup(details.get("parameters", {}), "target_user")
                    ]
                    self.ALERT_DETAILS[log]["DOC_TITLE"] = param_lookup(
                        details.get("parameters", {}), "doc_title"
                    )
                    self.ALERT_DETAILS[log]["ACCESS_SCOPE"] = param_lookup(
                        details.get("parameters", {}), "new_value"
                    )
                change_user_access = True
        return change_user_access

    def alert_context(self, event):
        log = event.get("p_row_id")
        if self.ALERT_DETAILS[log]["TARGET_USER_EMAILS"] != ["<UNKNOWN_USER>"]:
            return {"target users": self.ALERT_DETAILS[log]["TARGET_USER_EMAILS"]}
        return {}

    def dedup(self, event):
        return deep_get(event, "actor", "email", default="<UNKNOWN_USER>")

    def title(self, event):
        log = event.get("p_row_id")
        if self.ALERT_DETAILS[log]["TARGET_USER_EMAILS"] != ["<UNKNOWN_USER>"]:
            if len(self.ALERT_DETAILS[log]["TARGET_USER_EMAILS"]) == 1:
                sharing_scope = self.ALERT_DETAILS[log]["TARGET_USER_EMAILS"][0]
            else:
                sharing_scope = "multiple users"
            if self.ALERT_DETAILS[log]["NEW_VISIBILITY"] == "shared_externally":
                sharing_scope += " (outside the document's current domain)"
        elif self.ALERT_DETAILS[log]["TARGET_DOMAIN"] == "all":
            sharing_scope = "the entire internet"
            if self.ALERT_DETAILS[log]["NEW_VISIBILITY"] == "people_with_link":
                sharing_scope += " (anyone with the link)"
            elif self.ALERT_DETAILS[log]["NEW_VISIBILITY"] == "public_on_the_web":
                sharing_scope += " (link not required)"
        else:
            sharing_scope = f"the {self.ALERT_DETAILS[log]['TARGET_DOMAIN']} domain"
            if self.ALERT_DETAILS[log]["NEW_VISIBILITY"] == "people_within_domain_with_link":
                sharing_scope += (
                    f" (anyone in {self.ALERT_DETAILS[log]['TARGET_DOMAIN']} with the link)"
                )
            elif self.ALERT_DETAILS[log]["NEW_VISIBILITY"] == "public_in_the_domain":
                sharing_scope += f" (anyone in {self.ALERT_DETAILS[log]['TARGET_DOMAIN']})"
        # alert_access_scope = ALERT_DETAILS[log]["ACCESS_SCOPE"][0].replace("can_", "")
        return f"User [{deep_get(event, 'actor', 'email', default='<UNKNOWN_USER>')}] made documents externally visible"

    def severity(self, event):
        log = event.get("p_row_id")
        if self.ALERT_DETAILS[log]["TARGET_USER_EMAILS"] != ["<UNKNOWN_USER>"]:
            for address in self.ALERT_DETAILS[log]["TARGET_USER_EMAILS"]:
                domain = address.split("@")[1]
                if domain in self.PUBLIC_PROVIDERS:
                    return "LOW"
        return "INFO"

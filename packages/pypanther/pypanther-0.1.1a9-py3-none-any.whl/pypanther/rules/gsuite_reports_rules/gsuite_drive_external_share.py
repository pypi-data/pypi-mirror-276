import datetime
from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import (
    PantherUnexpectedAlert,
    deep_get,
    pattern_match,
    pattern_match_list,
)
from pypanther.log_types import LogType

g_suite_drive_external_file_share_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Dangerous Share of Known Document with a Missing User",
        ExpectedResult=True,
        Log={
            "kind": "admin#reports#activity",
            "id": {
                "time": "2020-09-07T15:50:49.617Z",
                "uniqueQualifier": "1111111111111111111",
                "applicationName": "drive",
                "customerId": "C010qxghg",
            },
            "actor": {"email": "example@acme.com", "profileId": "1111111111111111111"},
            "events": [
                {
                    "type": "acl_change",
                    "name": "change_user_access",
                    "parameters": [
                        {"name": "primary_event", "boolValue": True},
                        {"name": "visibility_change", "value": "external"},
                        {"name": "target_user", "value": "outside@acme.com"},
                        {"name": "old_visibility", "value": "private"},
                        {"name": "doc_id", "value": "1111111111111111111"},
                        {"name": "doc_type", "value": "document"},
                        {"name": "doc_title", "value": "Document Title Primary"},
                        {"name": "visibility", "value": "shared_externally"},
                        {"name": "originating_app_id", "value": "1111111111111111111"},
                        {"name": "owner_is_shared_drive", "boolValue": False},
                        {"name": "owner_is_team_drive", "boolValue": False},
                        {"name": "old_value", "multiValue": ["none"]},
                        {"name": "new_value", "multiValue": ["can_edit"]},
                    ],
                }
            ],
        },
    ),
    PantherRuleTest(
        Name="Dangerous Share of Unknown Document",
        ExpectedResult=True,
        Log={
            "kind": "admin#reports#activity",
            "id": {
                "time": "2020-09-07T15:50:49.617Z",
                "uniqueQualifier": "1111111111111111111",
                "applicationName": "drive",
                "customerId": "C010qxghg",
            },
            "actor": {"email": "example@acme.com", "profileId": "1111111111111111111"},
            "events": [
                {
                    "type": "acl_change",
                    "name": "change_user_access",
                    "parameters": [
                        {"name": "primary_event", "boolValue": True},
                        {"name": "visibility_change", "value": "external"},
                        {"name": "target_user", "value": "alice@external.com"},
                        {"name": "old_visibility", "value": "private"},
                        {"name": "doc_id", "value": "1111111111111111111"},
                        {"name": "doc_type", "value": "document"},
                        {"name": "doc_title", "value": "Untitled document"},
                        {"name": "visibility", "value": "shared_externally"},
                        {"name": "originating_app_id", "value": "1111111111111111111"},
                        {"name": "owner_is_shared_drive", "boolValue": False},
                        {"name": "owner_is_team_drive", "boolValue": False},
                        {"name": "old_value", "multiValue": ["none"]},
                        {"name": "new_value", "multiValue": ["can_edit"]},
                    ],
                }
            ],
        },
    ),
    PantherRuleTest(
        Name="Share Allowed by Exception",
        ExpectedResult=False,
        Log={
            "kind": "admin#reports#activity",
            "id": {
                "time": "2020-07-07T15:50:49.617Z",
                "uniqueQualifier": "1111111111111111111",
                "applicationName": "drive",
                "customerId": "C010qxghg",
            },
            "actor": {"email": "alice@acme.com", "profileId": "1111111111111111111"},
            "events": [
                {
                    "type": "acl_change",
                    "name": "change_user_access",
                    "parameters": [
                        {"name": "primary_event", "boolValue": True},
                        {"name": "billable", "boolValue": True},
                        {"name": "visibility_change", "value": "external"},
                        {"name": "target_domain", "value": "acme.com"},
                        {"name": "old_visibility", "value": "private"},
                        {"name": "doc_id", "value": "1111111111111111111"},
                        {"name": "doc_type", "value": "document"},
                        {"name": "doc_title", "value": "Document Title Pattern"},
                        {"name": "visibility", "value": "shared_externally"},
                        {"name": "originating_app_id", "value": "1111111111111111111"},
                        {"name": "owner_is_shared_drive", "boolValue": False},
                        {"name": "owner_is_team_drive", "boolValue": False},
                        {"name": "old_value", "multiValue": ["none"]},
                        {"name": "new_value", "multiValue": ["people_within_domain_with_link"]},
                    ],
                }
            ],
        },
    ),
]


class GSuiteDriveExternalFileShare(PantherRule):
    RuleID = "GSuite.Drive.ExternalFileShare-prototype"
    DisplayName = "External GSuite File Share"
    Enabled = False
    LogTypes = [LogType.GSuite_Reports]
    Tags = [
        "GSuite",
        "Security Control",
        "Configuration Required",
        "Collection:Data from Information Repositories",
    ]
    Reports = {"MITRE ATT&CK": ["TA0009:T1213"]}
    Severity = PantherSeverity.High
    Description = "An employee shared a sensitive file externally with another organization"
    Runbook = "Contact the employee who made the share and make sure they redact the access. If the share was legitimate, add to the EXCEPTION_PATTERNS in the detection.\n"
    Reference = "https://support.google.com/docs/answer/2494822?hl=en&co=GENIE.Platform%3DiOS&sjid=864417124752637253-EU"
    Tests = g_suite_drive_external_file_share_tests
    COMPANY_DOMAIN = "your-company-name.com"
    # The glob pattern for the document title (lowercased)
    # All actors allowed to receive the file share
    # Allow any user
    # "all"
    # Allow any user in a specific domain
    # "*@acme.com"
    # The time limit for how long the file share stays valid
    EXCEPTION_PATTERNS = {
        "document title p*": {
            "allowed_for": {
                "alice@acme.com",
                "samuel@acme.com",
                "nathan@acme.com",
                "barry@acme.com",
            },
            "allowed_until": datetime.datetime(year=2030, month=6, day=2),
        }
    }

    def _check_acl_change_event(self, actor_email, acl_change_event):
        parameters = {
            p.get("name", ""): p.get("value") or p.get("multiValue")
            for p in acl_change_event["parameters"]
        }
        doc_title = parameters.get("doc_title", "TITLE_UNKNOWN")
        old_visibility = parameters.get("old_visibility", "OLD_VISIBILITY_UNKNOWN")
        new_visibility = parameters.get("visibility", "NEW_VISIBILITY_UNKNOWN")
        target_user = parameters.get("target_user", "USER_UNKNOWN")
        current_time = datetime.datetime.now()
        if (
            new_visibility == "shared_externally"
            and old_visibility == "private"
            and (not target_user.endswith(f"@{self.COMPANY_DOMAIN}"))
        ):
            # This is a dangerous share, check exceptions:
            for pattern, details in self.EXCEPTION_PATTERNS.items():
                doc_title_match = pattern_match(doc_title.lower(), pattern)
                allowed_for_match = pattern_match_list(actor_email, details.get("allowed_for"))
                allowed_for_all_match = details.get("allowed_for") == {"all"}
                if (
                    doc_title_match
                    and (allowed_for_match or allowed_for_all_match)
                    and (current_time < details.get("allowed_until"))
                ):
                    return False
                # No exceptions match.
                # Return the event summary (which is True) to alert & use in title.
                return {"actor": actor_email, "doc_title": doc_title, "target_user": target_user}
        return False

    def rule(self, event):
        application_name = deep_get(event, "id", "applicationName")
        events = event.get("events")
        actor_email = deep_get(event, "actor", "email", default="EMAIL_UNKNOWN")
        if (
            application_name == "drive"
            and events
            and ("acl_change" in set((e["type"] for e in events)))
        ):
            # If any of the events in this record are a dangerous file share, alert:
            return any(
                (
                    self._check_acl_change_event(actor_email, acl_change_event)
                    for acl_change_event in events
                )
            )
        return False

    def title(self, event):
        events = event.get("events", [])
        actor_email = deep_get(event, "actor", "email", default="EMAIL_UNKNOWN")
        matching_events = [
            self._check_acl_change_event(actor_email, acl_change_event)
            for acl_change_event in events
            if self._check_acl_change_event(actor_email, acl_change_event)
        ]
        if matching_events:
            len_events = len(matching_events)
            first_event = matching_events[0]
            actor = first_event.get("actor", "ACTOR_UNKNOWN")
            doc_title = first_event.get("doc_title", "DOC_TITLE_UNKNOWN")
            target_user = first_event.get("target_user", "USER_UNKNOWN")
            if len(matching_events) > 1:
                return (
                    f"Multiple dangerous shares ({len_events}) by [{actor}], including "
                    + f'"{doc_title}" to {target_user}'
                )
            return f'Dangerous file share by [{actor}]: "{doc_title}" to {target_user}'
        raise PantherUnexpectedAlert("No matching events, but DangerousShares still fired")

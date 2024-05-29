import re
from fnmatch import fnmatch
from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import m365_alert_context
from pypanther.log_types import LogType

microsoft365_external_document_sharing_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Allowed Domain",
        ExpectedResult=False,
        Log={
            "AppAccessContext": {"AADSessionId": "aa-bb-cc", "CorrelationId": "dd-ee-ff"},
            "ClientIP": "1.2.3.4",
            "CreationTime": "2022-12-12 19:31:41",
            "EventData": "<Type>Edit</Type><MembersCanShareApplied>False</MembersCanShareApplied>",
            "EventSource": "SharePoint",
            "Id": "111-aa-234",
            "ItemType": "File",
            "ObjectId": "https://yourorg.sharepoint.com/personal/user_yourorg/Documents/importantsecrets.docx",
            "Operation": "AddedToSecureLink",
            "OrganizationId": "11-22-abc",
            "RecordType": 14,
            "Site": "aa-bb-dd-ee-ff",
            "SiteUrl": "https://yourorg.sharepoint.com/personal/user_yourorg",
            "SourceFileExtension": "docx",
            "SourceFileName": "importantsecrets.docx",
            "SourceRelativeUrl": "Documents/importantsecrets.docx",
            "TargetUserOrGroupName": "OUTSIDER@ALLOWEDDOMAIN.COM",
            "TargetUserOrGroupType": "Guest",
            "UserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "UserId": "my.user@yourorg.onmicrosoft.com",
            "UserKey": "i:0h.f|membership|12345@live.com",
            "UserType": 0,
            "Workload": "OneDrive",
        },
    ),
    PantherRuleTest(
        Name="Allowed Folder",
        ExpectedResult=False,
        Log={
            "AppAccessContext": {"AADSessionId": "aa-bb-cc", "CorrelationId": "dd-ee-ff"},
            "ClientIP": "1.2.3.4",
            "CreationTime": "2022-12-12 19:31:41",
            "EventData": "<Type>Edit</Type><MembersCanShareApplied>False</MembersCanShareApplied>",
            "EventSource": "SharePoint",
            "Id": "111-aa-234",
            "ItemType": "File",
            "ObjectId": "https://yourorg.sharepoint.com/personal/user_yourorg/Documents/External/public.docx",
            "Operation": "AddedToSecureLink",
            "OrganizationId": "11-22-abc",
            "RecordType": 14,
            "Site": "aa-bb-dd-ee-ff",
            "SiteUrl": "https://yourorg.sharepoint.com/personal/user_yourorg",
            "SourceFileExtension": "docx",
            "SourceFileName": "public.docx",
            "SourceRelativeUrl": "Documents/External/public.docx",
            "TargetUserOrGroupName": "MARKETING@SAAS.COM",
            "TargetUserOrGroupType": "Guest",
            "UserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "UserId": "my.user@yourorg.onmicrosoft.com",
            "UserKey": "i:0h.f|membership|12345@live.com",
            "UserType": 0,
            "Workload": "OneDrive",
        },
    ),
    PantherRuleTest(
        Name="Allowed User",
        ExpectedResult=False,
        Log={
            "AppAccessContext": {"AADSessionId": "aa-bb-cc", "CorrelationId": "dd-ee-ff"},
            "ClientIP": "1.2.3.4",
            "CreationTime": "2022-12-12 19:31:41",
            "EventData": "<Type>Edit</Type><MembersCanShareApplied>False</MembersCanShareApplied>",
            "EventSource": "SharePoint",
            "Id": "111-aa-234",
            "ItemType": "File",
            "ObjectId": "https://yourorg.sharepoint.com/personal/user_yourorg/Documents/importantsecrets.docx",
            "Operation": "AddedToSecureLink",
            "OrganizationId": "11-22-abc",
            "RecordType": 14,
            "Site": "aa-bb-dd-ee-ff",
            "SiteUrl": "https://yourorg.sharepoint.com/personal/user_yourorg",
            "SourceFileExtension": "docx",
            "SourceFileName": "importantsecrets.docx",
            "SourceRelativeUrl": "Documents/importantsecrets.docx",
            "TargetUserOrGroupName": "EXCEPTION@OUTSIDER.COM",
            "TargetUserOrGroupType": "Guest",
            "UserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "UserId": "my.user@yourorg.onmicrosoft.com",
            "UserKey": "i:0h.f|membership|12345@live.com",
            "UserType": 0,
            "Workload": "OneDrive",
        },
    ),
    PantherRuleTest(
        Name="External user",
        ExpectedResult=True,
        Log={
            "AppAccessContext": {"AADSessionId": "aa-bb-cc", "CorrelationId": "dd-ee-ff"},
            "ClientIP": "1.2.3.4",
            "CreationTime": "2022-12-12 19:31:41",
            "EventData": "<Type>Edit</Type><MembersCanShareApplied>False</MembersCanShareApplied>",
            "EventSource": "SharePoint",
            "Id": "111-aa-234",
            "ItemType": "File",
            "ObjectId": "https://yourorg.sharepoint.com/personal/user_yourorg/Documents/importantsecrets.docx",
            "Operation": "AddedToSecureLink",
            "OrganizationId": "11-22-abc",
            "RecordType": 14,
            "Site": "aa-bb-dd-ee-ff",
            "SiteUrl": "https://yourorg.sharepoint.com/personal/user_yourorg",
            "SourceFileExtension": "docx",
            "SourceFileName": "importantsecrets.docx",
            "SourceRelativeUrl": "Documents/importantsecrets.docx",
            "TargetUserOrGroupName": "OUTSIDER@EXTERNAL.IO",
            "TargetUserOrGroupType": "Guest",
            "UserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "UserId": "my.user@yourorg.onmicrosoft.com",
            "UserKey": "i:0h.f|membership|12345@live.com",
            "UserType": 0,
            "Workload": "OneDrive",
        },
    ),
    PantherRuleTest(
        Name="Internal Share",
        ExpectedResult=False,
        Log={
            "AppAccessContext": {"AADSessionId": "aa-bb-cc", "CorrelationId": "dd-ee-ff"},
            "ClientIP": "1.2.3.4",
            "CreationTime": "2022-12-12 19:31:41",
            "EventData": "<Type>Edit</Type><MembersCanShareApplied>False</MembersCanShareApplied>",
            "EventSource": "SharePoint",
            "Id": "111-aa-234",
            "ItemType": "File",
            "ObjectId": "https://yourorg.sharepoint.com/personal/user_yourorg/Documents/importantsecrets.docx",
            "Operation": "AddedToSecureLink",
            "OrganizationId": "11-22-abc",
            "RecordType": 14,
            "Site": "aa-bb-dd-ee-ff",
            "SiteUrl": "https://yourorg.sharepoint.com/personal/user_yourorg",
            "SourceFileExtension": "docx",
            "SourceFileName": "importantsecrets.docx",
            "SourceRelativeUrl": "Documents/importantsecrets.docx",
            "TargetUserOrGroupName": "ANOTHERUSER@MYCOMPANY.COM",
            "TargetUserOrGroupType": "NotGuest",
            "UserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "UserId": "my.user@yourorg.onmicrosoft.com",
            "UserKey": "i:0h.f|membership|12345@live.com",
            "UserType": 0,
            "Workload": "OneDrive",
        },
    ),
]


class Microsoft365ExternalDocumentSharing(PantherRule):
    Description = "Document shared externally"
    DisplayName = "Microsoft365 External Document Sharing"
    Reports = {"MITRE ATT&CK": ["TA0009:T1039"]}
    Runbook = "Check the document metadata to ensure it is not a sensitive document."
    Reference = "https://support.microsoft.com/en-us/topic/manage-sharing-with-external-users-in-microsoft-365-small-business-2951a85f-c970-4375-aa4f-6b0d7035fe35#:~:text=Top%20of%20Page-,Turn%20external%20sharing%20on%20or%20off,-The%20ability%20to"
    Severity = PantherSeverity.Low
    LogTypes = [LogType.Microsoft365_Audit_SharePoint]
    RuleID = "Microsoft365.External.Document.Sharing-prototype"
    Tests = microsoft365_external_document_sharing_tests
    email_regex = re.compile("([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\\.[A-Z|a-z]{2,})+")
    ALLOWED_DOMAINS = ["mycompany.com", "alloweddomain.com"]  # should be in lowercase
    ALLOWED_USERS = ["exception@outsider.com"]  # should be in lowercase
    ALLOWED_PATHS = ["*/External/*", "External/*"]

    def allowed_path(self, relative_url):
        for path in self.ALLOWED_PATHS:
            if fnmatch(relative_url, path):
                return True
        return False

    def rule(self, event):
        if event.get("Operation", "") == "AnonymousLinkCreated":
            return not self.allowed_path(event.get("SourceRelativeUrl"))
        if event.get("Operation", "") == "AddedToSecureLink":
            if self.allowed_path(event.get("SourceRelativeUrl")):
                return False
            target = event.get("TargetUserOrGroupName", "")
            if target.lower() in self.ALLOWED_USERS:
                return False
            if re.fullmatch(self.email_regex, target):
                if target.split("@")[1].lower() not in self.ALLOWED_DOMAINS:
                    return True
        return False

    def title(self, event):
        return f"Microsoft365: [{event.get('SourceRelativeUrl')}] has been shared with external users by [{event.get('UserId', '<user-not-found>')}]"

    def alert_context(self, event):
        return m365_alert_context(event)

from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import get_crowdstrike_field
from pypanther.log_types import LogType

crowdstrike_real_time_response_session_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="RTS session start event",
        ExpectedResult=True,
        Log={
            "cid": "12345abcdef",
            "unknown_payload": {
                "AgentIdString": "12ab56cd",
                "CustomerIdString": "1234",
                "EventType": "Event_ExternalApiEvent",
                "ExternalApiType": "Event_RemoteResponseSessionStartEvent",
                "HostnameField": "John Macbook Pro",
                "Nonce": -4714046577736361000,
                "SessionId": "6e1181e4-4924-4761-az3d-666851jdb950",
                "StartTimestamp": 1670460538,
                "UTCTimestamp": 1670460538000,
                "UserName": "example@example.io",
                "cid": "12345abcdef",
                "eid": 118,
                "timestamp": "2022-12-08T00:48:58Z",
            },
        },
    ),
    PantherRuleTest(
        Name="RTS session not started",
        ExpectedResult=False,
        Log={
            "cid": "12345abcdef",
            "unknown_payload": {
                "AgentIdString": "12ab56cd",
                "CustomerIdString": "1234",
                "EventType": "Event_ExternalApiEvent",
                "ExternalApiType": "Event_RemoteResponseSessionEndEvent",
                "HostnameField": "John Macbook Pro",
                "Nonce": -4714046577736361000,
                "SessionId": "6e1181e4-4924-4761-az3d-666851jdb950",
                "StartTimestamp": 1670460538,
                "UTCTimestamp": 1670460538000,
                "UserName": "example@example.io",
                "cid": "12345abcdef",
                "eid": 118,
                "timestamp": "2022-12-08T00:48:58Z",
            },
        },
    ),
    PantherRuleTest(
        Name="RTS session start event (FDREvent)",
        ExpectedResult=True,
        Log={
            "event": {
                "AgentIdString": "42db160eec7948658374a28a4088f297",
                "CustomerIdString": "712bcd164963442ea43d52917cecdecc",
                "EventType": "Event_ExternalApiEvent",
                "ExternalApiType": "Event_RemoteResponseSessionStartEvent",
                "HostnameField": "US-C02TEST",
                "Nonce": "13732697495973190000",
                "SessionId": "6e1081e4-4914-4761-af3d-666851adb950",
                "StartTimestamp": "1670460538",
                "UTCTimestamp": "1670460538000",
                "UserName": "someone@runpanther.io",
                "cid": "",
                "eid": "118",
                "timestamp": "2022-12-08T00:48:58Z",
            },
            "timestamp": "2022-12-08 00:48:58.000000000",
            "aid": "42db160eec7948658374a28a4088f297",
            "cid": "712bcd164963442ea43d52917cecdecc",
            "fdr_event_type": "Event_RemoteResponseSessionStartEvent",
            "p_log_type": "Crowdstrike.FDREvent",
            "p_event_time": "2022-12-08T00:48:58Z",
            "p_any_domain_names": ["US-C02TEST"],
            "p_any_md5_hashes": [
                "42db160eec7948658374a28a4088f297",
                "712bcd164963442ea43d52917cecdecc",
            ],
            "p_any_trace_ids": [
                "42db160eec7948658374a28a4088f297",
                "712bcd164963442ea43d52917cecdecc",
            ],
            "p_any_usernames": ["someone@runpanther.io"],
            "p_any_emails": ["someone@runpanther.io"],
        },
    ),
    PantherRuleTest(
        Name="RTS session not started (FDREvent)",
        ExpectedResult=False,
        Log={
            "event": {
                "AgentIdString": "42db160eec7948658374a28a4088f297",
                "CustomerIdString": "712bcd164963442ea43d52917cecdecc",
                "EventType": "Event_ExternalApiEvent",
                "ExternalApiType": "Event_RemoteResponseSessionEndEvent",
                "HostnameField": "US-C02TEST",
                "Nonce": "13732697495973190000",
                "SessionId": "6e1081e4-4914-4761-af3d-666851adb950",
                "StartTimestamp": "1670460538",
                "UTCTimestamp": "1670460538000",
                "UserName": "someone@runpanther.io",
                "cid": "",
                "eid": "118",
                "timestamp": "2022-12-08T00:48:58Z",
            },
            "timestamp": "2022-12-08 00:48:58.000000000",
            "aid": "42db160eec7948658374a28a4088f297",
            "cid": "712bcd164963442ea43d52917cecdecc",
            "fdr_event_type": "Event_RemoteResponseSessionEndEvent",
            "p_log_type": "Crowdstrike.FDREvent",
            "p_event_time": "2022-12-08T00:48:58Z",
            "p_any_domain_names": ["US-C02TEST"],
            "p_any_md5_hashes": [
                "42db160eec7948658374a28a4088f297",
                "712bcd164963442ea43d52917cecdecc",
            ],
            "p_any_trace_ids": [
                "42db160eec7948658374a28a4088f297",
                "712bcd164963442ea43d52917cecdecc",
            ],
            "p_any_usernames": ["someone@runpanther.io"],
            "p_any_emails": ["someone@runpanther.io"],
        },
    ),
]


class CrowdstrikeRealTimeResponseSession(PantherRule):
    DisplayName = "Crowdstrike Real Time Response (RTS) Session"
    RuleID = "Crowdstrike.RealTimeResponse.Session-prototype"
    Severity = PantherSeverity.Medium
    LogTypes = [LogType.Crowdstrike_Unknown, LogType.Crowdstrike_FDREvent]
    Tags = ["Crowdstrike"]
    Description = "Alert when someone uses Crowdstrike’s RTR (real-time response) capability to access a machine remotely to run commands.\n"
    Runbook = "Validate the real-time response session started by the Actor.\n"
    Reference = "https://falcon.us-2.crowdstrike.com/documentation/71/real-time-response-and-network-containment#reviewing-real-time-response-audit-logs"
    Tests = crowdstrike_real_time_response_session_tests

    def rule(self, event):
        return (
            get_crowdstrike_field(event, "ExternalApiType", default="<unknown-ExternalApiType>")
            == "Event_RemoteResponseSessionStartEvent"
        )

    def title(self, event):
        user_name = get_crowdstrike_field(event, "UserName", default="<unknown-UserName>")
        hostname_field = get_crowdstrike_field(
            event, "HostnameField", default="<unknown-HostNameField>"
        )
        return (
            f"{user_name} started a Crowdstrike Real-Time Response (RTR) shell on {hostname_field}"
        )

    def alert_context(self, event):
        return {
            "Start Time": get_crowdstrike_field(
                event, "StartTimestamp", default="<unknown-StartTimestamp>"
            ),
            "SessionId": get_crowdstrike_field(event, "SessionId", default="<unknown-SessionId>"),
            "Actor": get_crowdstrike_field(event, "UserName", default="<unknown-UserName>"),
            "Target Host": get_crowdstrike_field(
                event, "HostnameField", default="<unknown-HostnameField>"
            ),
        }

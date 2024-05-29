from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import (
    filter_crowdstrike_fdr_event_type,
    get_crowdstrike_field,
)
from pypanther.log_types import LogType

crowdstrike_dns_request_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Denylisted Domain",
        ExpectedResult=True,
        Log={
            "event_simpleName": "DnsRequest",
            "name": "DnsRequestMacV1",
            "aid": "00000000000000000000000000000001",
            "aip": "111.111.111.111",
            "cid": "00000000000000000000000000000002",
            "id": "11111111-0000-1111-0000-111111111111",
            "event_platform": "Mac",
            "timestamp": "2021-10-01 00:00:00.000Z",
            "ConfigBuild": "1007.4.0014301.11",
            "ConfigStateHash": "507116305",
            "Entitlements": "15",
            "ContextThreadId": "0",
            "ContextTimeStamp": "2021-10-08 19:55:04.448Z",
            "ContextProcessId": "111111111111111111",
            "EffectiveTransmissionClass": 2,
            "DomainName": "baddomain.com",
            "RequestType": "1",
            "p_event_time": "2021-10-08 19:55:04.448Z",
            "p_parse_time": "2021-10-08 20:09:41.933Z",
            "p_log_type": "Crowdstrike.DNSRequest",
            "p_row_id": "2ed00000000000000000000000000001",
            "p_source_id": "11111111-1111-1111-1111-111111111111",
            "p_source_label": "Crowdstrike",
            "p_any_ip_addresses": ["111.111.111.111"],
            "p_any_domain_names": ["baddomain.com"],
            "p_any_trace_ids": [
                "00000000000000000000000000000001",
                "00000000000000000000000000000002",
            ],
        },
    ),
    PantherRuleTest(
        Name="Non-denylisted Domain",
        ExpectedResult=False,
        Log={
            "event_simpleName": "DnsRequest",
            "name": "DnsRequestMacV1",
            "aid": "00000000000000000000000000000001",
            "aip": "111.111.111.111",
            "cid": "00000000000000000000000000000002",
            "id": "11111111-0000-1111-0000-111111111111",
            "event_platform": "Mac",
            "timestamp": "2021-10-01 00:00:00.000Z",
            "ConfigBuild": "1007.4.0014301.11",
            "ConfigStateHash": "507116305",
            "Entitlements": "15",
            "ContextThreadId": "0",
            "ContextTimeStamp": "2021-10-08 19:55:04.448Z",
            "ContextProcessId": "111111111111111111",
            "EffectiveTransmissionClass": 2,
            "DomainName": "gooddomain.com",
            "RequestType": "1",
            "p_event_time": "2021-10-08 19:55:04.448Z",
            "p_parse_time": "2021-10-08 20:09:41.933Z",
            "p_log_type": "Crowdstrike.DNSRequest",
            "p_row_id": "2ed00000000000000000000000000001",
            "p_source_id": "11111111-1111-1111-1111-111111111111",
            "p_source_label": "Crowdstrike",
            "p_any_ip_addresses": ["111.111.111.111"],
            "p_any_domain_names": ["gooddomain.com"],
            "p_any_trace_ids": [
                "00000000000000000000000000000001",
                "00000000000000000000000000000002",
            ],
        },
    ),
    PantherRuleTest(
        Name="Denylisted Domain (FDREvent)",
        ExpectedResult=True,
        Log={
            "aid": "307dc41ce39744f060622095f2805249",
            "aip": "10.0.0.0",
            "cid": "0cfb1a68ef6b49fdb0d2b12725057057",
            "ConfigBuild": "1007.4.0010306.1",
            "ConfigStateHash": "156025532",
            "ContextProcessId": "289977812183778042",
            "ContextThreadId": "0",
            "ContextTimestamp": "2020-05-24 23:50:06.989",
            "Entitlements": "15",
            "event": {
                "ConfigBuild": "1007.4.0010306.1",
                "ConfigStateHash": "156025532",
                "ContextProcessId": "289977812183778042",
                "ContextThreadId": "0",
                "ContextTimeStamp": "1590364206.989",
                "DomainName": "baddomain.com",
                "Entitlements": "15",
                "RequestType": "1",
                "aid": "307dc41ce39744f060622095f2805249",
                "aip": "10.0.0.0",
                "cid": "0cfb1a68ef6b49fdb0d2b12725057057",
                "event_platform": "Mac",
                "event_simpleName": "DnsRequest",
                "id": "4be06eb8-9e19-11ea-a7b0-026c15f3d8ed",
                "name": "DnsRequestMacV1",
                "timestamp": "1590364207259",
            },
            "event_platform": "Mac",
            "event_simplename": "DnsRequest",
            "fdr_event_type": "DnsRequest",
            "id": "4be06eb8-9e19-11ea-a7b0-026c15f3d8ed",
            "name": "DnsRequestMacV1",
            "p_any_domain_names": ["baddomain.com"],
            "p_any_ip_addresses": ["10.0.0.0"],
            "p_any_md5_hashes": [
                "0cfb1a68ef6b49fdb0d2b12725057057",
                "307dc41ce39744f060622095f2805249",
            ],
            "p_any_trace_ids": [
                "0cfb1a68ef6b49fdb0d2b12725057057",
                "307dc41ce39744f060622095f2805249",
            ],
            "p_event_time": "2020-05-24 23:50:06.989",
            "p_log_type": "Crowdstrike.FDREvent",
            "p_parse_time": "2023-01-26 12:17:58.141",
            "p_row_id": "a21b385f60c08898ae918c84162d",
            "p_schema_version": 0,
            "timestamp": "2020-05-24 23:50:07.259",
        },
    ),
    PantherRuleTest(
        Name="Non-denylisted Domain (FDREvent)",
        ExpectedResult=False,
        Log={
            "aid": "307dc41ce39744f060622095f2805249",
            "aip": "10.0.0.0",
            "cid": "0cfb1a68ef6b49fdb0d2b12725057057",
            "ConfigBuild": "1007.4.0010306.1",
            "ConfigStateHash": "156025532",
            "ContextProcessId": "289977812183778042",
            "ContextThreadId": "0",
            "ContextTimeStamp": "2020-05-24 23:50:06.989",
            "Entitlements": "15",
            "event": {
                "ConfigBuild": "1007.4.0010306.1",
                "ConfigStateHash": "156025532",
                "ContextProcessId": "289977812183778042",
                "ContextThreadId": "0",
                "ContextTimeStamp": "1590364206.989",
                "DomainName": "gooddomain.com",
                "Entitlements": "15",
                "RequestType": "1",
                "aid": "307dc41ce39744f060622095f2805249",
                "aip": "10.0.0.0",
                "cid": "0cfb1a68ef6b49fdb0d2b12725057057",
                "event_platform": "Mac",
                "event_simpleName": "DnsRequest",
                "id": "4be06eb8-9e19-11ea-a7b0-026c15f3d8ed",
                "name": "DnsRequestMacV1",
                "timestamp": "1590364207259",
            },
            "event_platform": "Mac",
            "event_simplename": "DnsRequest",
            "fdr_event_type": "DnsRequest",
            "id": "4be06eb8-9e19-11ea-a7b0-026c15f3d8ed",
            "name": "DnsRequestMacV1",
            "p_any_domain_names": ["gooddomain.com"],
            "p_any_ip_addresses": ["10.0.0.0"],
            "p_any_md5_hashes": [
                "0cfb1a68ef6b49fdb0d2b12725057057",
                "307dc41ce39744f060622095f2805249",
            ],
            "p_any_trace_ids": [
                "0cfb1a68ef6b49fdb0d2b12725057057",
                "307dc41ce39744f060622095f2805249",
            ],
            "p_event_time": "2020-05-24 23:50:06.989",
            "p_log_type": "Crowdstrike.FDREvent",
            "p_parse_time": "2023-01-26 12:17:58.141",
            "p_row_id": "a21b385f60c08898ae918c84162d",
            "p_schema_version": 0,
            "timestamp": "2020-05-24 23:50:07.259",
        },
    ),
    PantherRuleTest(
        Name="Denylisted Domain (but Non-DNS type) (FDREvent)",
        ExpectedResult=False,
        Log={
            "event_simpleName": "Event_DetectionSummaryEvent",
            "name": "DnsRequestMacV1",
            "aid": "00000000000000000000000000000001",
            "aip": "111.111.111.111",
            "cid": "00000000000000000000000000000002",
            "id": "11111111-0000-1111-0000-111111111111",
            "event": {
                "aid": "00000000000000000000000000000001",
                "event_simpleName": "Event_DetectionSummaryEvent",
                "name": "DnsRequestMacV1",
                "aip": "111.111.111.111",
                "cid": "00000000000000000000000000000002",
                "id": "11111111-0000-1111-0000-111111111111",
                "event_platform": "Mac",
                "timestamp": "2021-10-01 00:00:00.000Z",
                "ConfigBuild": "1007.4.0014301.11",
                "ConfigStateHash": "507116305",
                "Entitlements": "15",
                "ContextThreadId": "0",
                "ContextTimeStamp": "2021-10-08 19:55:04.448Z",
                "ContextProcessId": "111111111111111111",
                "EffectiveTransmissionClass": 2,
                "DomainName": "baddomain.com",
                "RequestType": "1",
            },
            "event_platform": "Mac",
            "fdr_event_type": "Event_DetectionSummaryEvent",
            "timestamp": "2021-10-01 00:00:00.000Z",
            "ConfigBuild": "1007.4.0014301.11",
            "ConfigStateHash": "507116305",
            "Entitlements": "15",
            "ContextThreadId": "0",
            "ContextTimeStamp": "2021-10-08 19:55:04.448Z",
            "ContextProcessId": "111111111111111111",
            "EffectiveTransmissionClass": 2,
            "RequestType": "1",
            "p_event_time": "2021-10-08 19:55:04.448Z",
            "p_parse_time": "2021-10-08 20:09:41.933Z",
            "p_log_type": "Crowdstrike.FDREvent",
            "p_row_id": "2ed00000000000000000000000000001",
            "p_source_id": "11111111-1111-1111-1111-111111111111",
            "p_source_label": "Crowdstrike",
            "p_any_ip_addresses": ["111.111.111.111"],
            "p_any_domain_names": ["baddomain.com"],
            "p_any_trace_ids": [
                "00000000000000000000000000000001",
                "00000000000000000000000000000002",
            ],
        },
    ),
]


class CrowdstrikeDNSRequest(PantherRule):
    RuleID = "Crowdstrike.DNS.Request-prototype"
    DisplayName = "DNS request to denylisted domain"
    Enabled = False
    LogTypes = [LogType.Crowdstrike_DNSRequest, LogType.Crowdstrike_FDREvent]
    Tags = ["Crowdstrike", "Initial Access:Phishing", "Configuration Required"]
    Severity = PantherSeverity.Critical
    Reports = {"MITRE ATT&CK": ["TA0001:T1566"]}
    Description = "A DNS request was made to a domain on an explicit denylist"
    Reference = "https://docs.runpanther.io/data-onboarding/supported-logs/crowdstrike#crowdstrike-dnsrequest"
    Runbook = "Filter for host ID in title in Crowdstrike Host Management console to identify the system that queried the domain."
    DedupPeriodMinutes = 15
    SummaryAttributes = ["DomainName", "aid", "p_any_domain_names", "p_any_ip_addresses"]
    Tests = crowdstrike_dns_request_tests
    # baddomain.com is present for testing purposes. Add domains you wish to be alerted on to this list
    DENYLIST = ["baddomain.com"]

    def rule(self, event):
        # We need to run either for Crowdstrike.DnsRequest or for Crowdstrike.FDREvent with the
        # 'DnsRequest' fdr_event_type. Crowdstrike.DnsRequest is covered because of the
        # association with the type
        if filter_crowdstrike_fdr_event_type(event, "DnsRequest"):
            return False
        if get_crowdstrike_field(event, "DomainName") in self.DENYLIST:
            return True
        return False

    def title(self, event):
        return (
            f"A denylisted domain [{get_crowdstrike_field(event, 'DomainName')}] was "
            + f"queried by host {event.get('aid')}"
        )

    def dedup(self, event):
        #  Alert on every individual lookup of a bad domain, per machine
        return f"{get_crowdstrike_field(event, 'DomainName')}-{event.get('aid')}"

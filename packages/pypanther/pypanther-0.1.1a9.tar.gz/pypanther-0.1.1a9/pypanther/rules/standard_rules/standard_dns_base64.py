from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import defang_ioc, is_base64
from pypanther.log_types import LogType

standard_dns_base64_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="AWS VPC DNS (Positive)",
        ExpectedResult=True,
        Log={
            "account_id": "123456789012",
            "answers": [{"Class": "IN", "Rdata": "172.31.46.187", "Type": "A"}],
            "p_log_type": "AWS.VPCDns",
            "query_class": "IN",
            "query_name": "c29tZSBsb25nIGJhc2U2NCBzdHJpbmc=.file1.16s.us",
            "query_timestamp": "2023-04-11 01:29:20",
            "query_type": "A",
            "rcode": "NOERROR",
            "region": "us-west-2",
            "srcaddr": "172.31.46.187",
            "srcids": {"instance": "i-09d9aa4e31675db61"},
            "srcport": "36899",
            "transport": "UDP",
            "version": "1.100000",
            "vpc_id": "vpc-c26c48ba",
        },
    ),
    PantherRuleTest(
        Name="AWS VPS DNS (Negative)",
        ExpectedResult=False,
        Log={
            "account_id": "123456789012",
            "answers": [{"Class": "IN", "Rdata": "172.31.46.187", "Type": "A"}],
            "p_log_type": "AWS.VPCDns",
            "query_class": "IN",
            "query_name": "test.com",
            "query_timestamp": "2023-04-11 01:29:20",
            "query_type": "A",
            "rcode": "NOERROR",
            "region": "us-west-2",
            "srcaddr": "172.31.46.187",
            "srcids": {"instance": "i-09d9aa4e31675db61"},
            "srcport": "36899",
            "transport": "UDP",
            "version": "1.100000",
            "vpc_id": "vpc-c26c48ba",
        },
    ),
    PantherRuleTest(
        Name="AWS VPS DNS subdomain (Negative)",
        ExpectedResult=False,
        Log={
            "account_id": "123456789012",
            "answers": [{"Class": "IN", "Rdata": "172.31.46.187", "Type": "A"}],
            "p_log_type": "AWS.VPCDns",
            "query_class": "IN",
            "query_name": "=.test.com",
            "query_timestamp": "2023-04-11 01:29:20",
            "query_type": "A",
            "rcode": "NOERROR",
            "region": "us-west-2",
            "srcaddr": "172.31.46.187",
            "srcids": {"instance": "i-09d9aa4e31675db61"},
            "srcport": "36899",
            "transport": "UDP",
            "version": "1.100000",
            "vpc_id": "vpc-c26c48ba",
        },
    ),
    PantherRuleTest(
        Name="Crowdstrike DNS Request (Positive)",
        ExpectedResult=True,
        Log={
            "ConfigBuild": "1007.3.0016606.11",
            "ConfigStateHash": "1331552299",
            "ContextProcessId": "21866918",
            "ContextThreadId": "43270698197",
            "ContextTimeStamp": "2023-04-23 18:50:03.172",
            "Entitlements": "15",
            "aid": "877761efa8db44d792ddc2redacted",
            "aip": "1.1.1.1",
            "cid": "cfe698690964434083fecdredacted",
            "event": {
                "ConfigBuild": "1007.3.0016606.11",
                "ConfigStateHash": "1331552299",
                "ContextProcessId": "21866918",
                "ContextThreadId": "43270698197",
                "ContextTimeStamp": "1682275803.172",
                "DnsRequestCount": "1",
                "DomainName": "aGVsbG93b3JsZA==.example.com.",
                "DualRequest": "0",
                "EffectiveTransmissionClass": "3",
                "Entitlements": "15",
                "EventOrigin": "1",
                "InterfaceIndex": "0",
                "QueryStatus": "9003",
                "RequestType": "1",
                "aid": "877761efa8db44d792ddc2redacted",
                "aip": "1.1.1.1",
                "cid": "cfe698690964434083fecdredacted",
                "event_platform": "Win",
                "event_simpleName": "DnsRequest",
                "id": "4f006a14-0fdf-474e-bfca-021a00a935ad",
                "name": "DnsRequestV4",
                "timestamp": "1682275805712",
            },
            "event_platform": "Win",
            "event_simpleName": "DnsRequest",
            "fdr_event_type": "DnsRequest",
            "id": "4f006a14-0fdf-474e-bfca-021a00a935ad",
            "name": "DnsRequestV4",
            "p_any_domain_names": ["win8.ipv6.microsoft.com"],
            "p_any_ip_addresses": ["1.1.1.1"],
            "p_any_md5_hashes": [
                "877761efa8db44d792ddc2redacted",
                "cfe698690964434083fecdredacted",
            ],
            "p_any_trace_ids": ["877761efa8db44d792ddc2redacted", "cfe698690964434083fecdredacted"],
            "p_event_time": "2023-04-23 18:50:03.172",
            "p_log_type": "Crowdstrike.FDREvent",
            "p_parse_time": "2023-04-23 19:00:53.11",
            "p_row_id": "f2c89ec8f09cbc8ca2c1cbdf171a",
            "p_schema_version": 0,
            "p_source_id": "1f33f64c-124d-413c-a9e3-d51ccedd8e77",
            "p_source_label": "Crowdstrike-FDR-Dev",
            "timestamp": "2023-04-23 18:50:05.712",
        },
    ),
    PantherRuleTest(
        Name="Crowdstrike DNS Request (Negative)",
        ExpectedResult=False,
        Log={
            "ConfigBuild": "1007.3.0016606.11",
            "ConfigStateHash": "1331552299",
            "ContextProcessId": "21866918",
            "ContextThreadId": "43270698197",
            "ContextTimeStamp": "2023-04-23 18:50:03.172",
            "Entitlements": "15",
            "aid": "877761efa8db44d792ddc2redacted",
            "aip": "1.1.1.1",
            "cid": "cfe698690964434083fecdredacted",
            "event": {
                "ConfigBuild": "1007.3.0016606.11",
                "ConfigStateHash": "1331552299",
                "ContextProcessId": "21866918",
                "ContextThreadId": "43270698197",
                "ContextTimeStamp": "1682275803.172",
                "DnsRequestCount": "1",
                "DomainName": "win8.ipv6.microsoft.com.",
                "DualRequest": "0",
                "EffectiveTransmissionClass": "3",
                "Entitlements": "15",
                "EventOrigin": "1",
                "InterfaceIndex": "0",
                "QueryStatus": "9003",
                "RequestType": "1",
                "aid": "877761efa8db44d792ddc2redacted",
                "aip": "1.1.1.1",
                "cid": "cfe698690964434083fecdredacted",
                "event_platform": "Win",
                "event_simpleName": "DnsRequest",
                "id": "4f006a14-0fdf-474e-bfca-021a00a935ad",
                "name": "DnsRequestV4",
                "timestamp": "1682275805712",
            },
            "event_platform": "Win",
            "event_simpleName": "DnsRequest",
            "fdr_event_type": "DnsRequest",
            "id": "4f006a14-0fdf-474e-bfca-021a00a935ad",
            "name": "DnsRequestV4",
            "p_any_domain_names": ["win8.ipv6.microsoft.com"],
            "p_any_ip_addresses": ["1.1.1.1"],
            "p_any_md5_hashes": [
                "877761efa8db44d792ddc2redacted",
                "cfe698690964434083fecdredacted",
            ],
            "p_any_trace_ids": ["877761efa8db44d792ddc2redacted", "cfe698690964434083fecdredacted"],
            "p_event_time": "2023-04-23 18:50:03.172",
            "p_log_type": "Crowdstrike.FDREvent",
            "p_parse_time": "2023-04-23 19:00:53.11",
            "p_row_id": "f2c89ec8f09cbc8ca2c1cbdf171a",
            "p_schema_version": 0,
            "p_source_id": "1f33f64c-124d-413c-a9e3-d51ccedd8e77",
            "p_source_label": "Crowdstrike-FDR-Dev",
            "timestamp": "2023-04-23 18:50:05.712",
        },
    ),
    PantherRuleTest(
        Name="Cisco Umbrella DNS Request (Positive)",
        ExpectedResult=True,
        Log={
            "action": "Allow",
            "internalIp": "136.24.229.58",
            "externalIp": "136.24.229.58",
            "timestamp": "2020-05-21 19:20:25.000",
            "responseCode": "NOERROR",
            "domain": "c29tZSBsb25nIGJhc2U2NCBzdHJpbmc=.example.io.",
            "p_log_type": "CiscoUmbrella.DNS",
        },
    ),
    PantherRuleTest(
        Name="Cisco Umbrella DNS Request (Negative)",
        ExpectedResult=False,
        Log={
            "action": "Allow",
            "internalIp": "136.24.229.58",
            "externalIp": "136.24.229.58",
            "timestamp": "2020-05-21 19:20:25.000",
            "responseCode": "NOERROR",
            "domain": "c29tZSBsb25nIGJhc2.example.io.",
            "p_log_type": "CiscoUmbrella.DNS",
        },
    ),
]


class StandardDNSBase64(PantherRule):
    DisplayName = "DNS Base64 Encoded Query"
    Description = "Detects DNS queries with Base64 encoded subdomains, which could indicate an attempt to obfuscate data exfil."
    RuleID = "Standard.DNSBase64-prototype"
    Enabled = False
    Reference = "https://zofixer.com/what-is-base64-disclosure-vulnerability/"
    Severity = PantherSeverity.Medium
    LogTypes = [LogType.Crowdstrike_FDREvent, LogType.AWS_VPCDns, LogType.CiscoUmbrella_DNS]
    Tests = standard_dns_base64_tests
    DECODED = ""

    def rule(self, event):
        args = event.udm("dns_query").split(".")
        # Check if Base64 encoded arguments are present in the command line
        for arg in args:
            self.DECODED = is_base64(arg)
            if self.DECODED:
                return True
        return False

    def title(self, event):
        defang_query = defang_ioc(event.udm("dns_query"))
        return f"Base64 encoded query detected from [{event.udm('source_ip')}], [{defang_query}]"

    def alert_context(self, event):
        context = {}
        context["source ip"] = event.udm("source_ip")
        context["defanged query"] = defang_ioc(event.udm("dns_query"))
        context["decoded url part"] = self.DECODED
        return context

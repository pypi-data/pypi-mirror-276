from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import deep_get
from pypanther.log_types import LogType

gcp_access_attempts_violating_iap_access_controls_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Blocked By IAP",
        ExpectedResult=True,
        Log={
            "httprequest": {
                "latency": "0.048180s",
                "remoteIp": "1.2.3.4",
                "requestMethod": "GET",
                "requestSize": 77,
                "requestUrl": "http://6.7.8.9/",
                "responseSize": 211,
                "status": 403,
                "userAgent": "curl/7.85.0",
            },
            "insertid": "u94qwjf25yzns",
            "jsonpayload": {
                "at_sign_type": "type.googleapis.com/google.cloud.loadbalancing.type.LoadBalancerLogEntry",
                "remoteIp": "1.2.3.4",
                "statusDetails": "handled_by_identity_aware_proxy",
            },
            "logname": "projects/gcp-project1/logs/requests",
            "p_any_ip_addresses": ["6.7.8.9", "1.2.3.4"],
            "p_any_trace_ids": ["projects/gcp-project1/traces/dd43c6eb7046da54fa3724d2753262e6"],
            "p_event_time": "2023-03-09 23:19:25.712",
            "p_log_type": "GCP.HTTPLoadBalancer",
            "p_parse_time": "2023-03-09 23:21:14.47",
            "p_row_id": "be93fccee09dd2f1b0b2d9ee16d5d704",
            "p_schema_version": 0,
            "p_source_id": "964c7894-9a0d-4ddf-864f-0193438221d6",
            "p_source_label": "panther-gcp-logsource",
            "receivetimestamp": "2023-03-09 23:19:26.392",
            "resource": {
                "labels": {
                    "backend_service_name": "web-backend-service",
                    "forwarding_rule_name": "http-content-rule",
                    "project_id": "gcp-project1",
                    "target_proxy_name": "http-lb-proxy-2",
                    "url_map_name": "web-map-http-2",
                    "zone": "global",
                },
                "type": "http_load_balancer",
            },
            "severity": "INFO",
            "spanid": "d75cc31c93528953",
            "timestamp": "2023-03-09 23:19:25.712",
            "trace": "projects/gcp-project1/traces/dd43c6eb7046da54fa3724d2753262e6",
        },
    ),
    PantherRuleTest(
        Name="Redirected by IAP",
        ExpectedResult=False,
        Log={
            "httprequest": {
                "latency": "0.048180s",
                "remoteIp": "1.2.3.4",
                "requestMethod": "GET",
                "requestSize": 77,
                "requestUrl": "http://6.7.8.9/",
                "responseSize": 211,
                "status": 302,
                "userAgent": "curl/7.85.0",
            },
            "insertid": "u94qwjf25yzns",
            "jsonpayload": {
                "at_sign_type": "type.googleapis.com/google.cloud.loadbalancing.type.LoadBalancerLogEntry",
                "remoteIp": "1.2.3.4",
                "statusDetails": "handled_by_identity_aware_proxy",
            },
            "logname": "projects/gcp-project1/logs/requests",
            "p_any_ip_addresses": ["6.7.8.9", "1.2.3.4"],
            "p_any_trace_ids": ["projects/gcp-project1/traces/dd43c6eb7046da54fa3724d2753262e6"],
            "p_event_time": "2023-03-09 23:19:25.712",
            "p_log_type": "GCP.HTTPLoadBalancer",
            "p_parse_time": "2023-03-09 23:21:14.47",
            "p_row_id": "be93fccee09dd2f1b0b2d9ee16d5d704",
            "p_schema_version": 0,
            "p_source_id": "964c7894-9a0d-4ddf-864f-0193438221d6",
            "p_source_label": "panther-gcp-logsource",
            "receivetimestamp": "2023-03-09 23:19:26.392",
            "resource": {
                "labels": {
                    "backend_service_name": "web-backend-service",
                    "forwarding_rule_name": "http-content-rule",
                    "project_id": "gcp-project1",
                    "target_proxy_name": "http-lb-proxy-2",
                    "url_map_name": "web-map-http-2",
                    "zone": "global",
                },
                "type": "http_load_balancer",
            },
            "severity": "INFO",
            "spanid": "d75cc31c93528953",
            "timestamp": "2023-03-09 23:19:25.712",
            "trace": "projects/gcp-project1/traces/dd43c6eb7046da54fa3724d2753262e6",
        },
    ),
]


class GCPAccessAttemptsViolatingIAPAccessControls(PantherRule):
    Description = "GCP Access Attempts Violating IAP Access Controls"
    DisplayName = "GCP Access Attempts Violating IAP Access Controls"
    Reference = "https://cloud.google.com/iap/docs/concepts-overview"
    Severity = PantherSeverity.Medium
    LogTypes = [LogType.GCP_HTTPLoadBalancer]
    RuleID = "GCP.Access.Attempts.Violating.IAP.Access.Controls-prototype"
    Tests = gcp_access_attempts_violating_iap_access_controls_tests

    def rule(self, event):
        return all(
            [
                deep_get(event, "resource", "type", default="") == "http_load_balancer",
                deep_get(event, "jsonPayload", "statusDetails", default="")
                == "handled_by_identity_aware_proxy",
                not any(
                    [
                        str(deep_get(event, "httprequest", "status", default=0)).startswith("2"),
                        str(deep_get(event, "httprequest", "status", default=0)).startswith("3"),
                    ]
                ),
            ]
        )

    def title(self, event):
        source = deep_get(event, "jsonPayload", "remoteIp", default="<SRC_IP_NOT_FOUND>")
        request_url = deep_get(
            event, "httprequest", "requestUrl", default="<REQUEST_URL_NOT_FOUND>"
        )
        return f"GCP: Request Violating IAP controls from [{source}] to [{request_url}]"

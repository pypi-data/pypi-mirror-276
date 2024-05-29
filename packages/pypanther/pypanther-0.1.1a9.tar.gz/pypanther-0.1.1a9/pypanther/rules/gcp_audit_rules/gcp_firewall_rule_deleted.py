import re
from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.gcp_base_helpers import gcp_alert_context
from pypanther.helpers.panther_base_helpers import deep_get
from pypanther.log_types import LogType

gcp_firewall_rule_deleted_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="compute.firewalls-delete-should-alert",
        ExpectedResult=True,
        Log={
            "insertid": "-xxxxxxxx",
            "logname": "projects/test-project-123456/logs/cloudaudit.googleapis.com%2Factivity",
            "operation": {
                "id": "operation-1684869594486-5fc6145ac17b3-6f92b265-43256266",
                "last": True,
                "producer": "compute.googleapis.com",
            },
            "protoPayload": {
                "at_sign_type": "type.googleapis.com/google.cloud.audit.AuditLog",
                "authenticationInfo": {"principalEmail": "user@domain.com"},
                "methodName": "v1.compute.firewalls.delete",
                "request": {"@type": "type.googleapis.com/compute.firewalls.delete"},
                "requestMetadata": {
                    "callerIP": "12.12.12.12",
                    "callerSuppliedUserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36,gzip(gfe),gzip(gfe)",
                },
                "resourceName": "projects/test-project-123456/global/firewalls/firewall-create",
                "serviceName": "compute.googleapis.com",
            },
            "receivetimestamp": "2023-05-23 19:20:00.728",
            "resource": {
                "labels": {
                    "firewall_rule_id": "6563507997690081088",
                    "project_id": "test-project-123456",
                },
                "type": "gce_firewall_rule",
            },
            "severity": "NOTICE",
            "timestamp": "2023-05-23 19:20:00.396",
        },
    ),
    PantherRuleTest(
        Name="appengine.firewall.delete-should-alert",
        ExpectedResult=True,
        Log={
            "insertid": "-xxxxxxxx",
            "logname": "projects/test-project-123456/logs/cloudaudit.googleapis.com%2Factivity",
            "protoPayload": {
                "at_sign_type": "type.googleapis.com/google.cloud.audit.AuditLog",
                "authenticationInfo": {"principalEmail": "user@domain.com"},
                "authorizationInfo": [
                    {
                        "granted": True,
                        "permission": "appengine.applications.update",
                        "resource": "apps/test-project-123456/firewall/ingressRules/1000",
                        "resourceAttributes": {},
                    }
                ],
                "methodName": "google.appengine.v1.Firewall.DeleteIngressRule",
                "requestMetadata": {
                    "callerIP": "12.12.12.12",
                    "destinationAttributes": {},
                    "requestAttributes": {"auth": {}, "time": "2023-05-23T19:28:48.805823Z"},
                },
                "resourceName": "apps/test-project-123456/firewall/ingressRules/1000",
                "serviceData": {"@type": "type.googleapis.com/google.appengine.v1beta4.AuditData"},
                "serviceName": "appengine.googleapis.com",
                "status": {},
            },
            "receivetimestamp": "2023-05-23 19:28:49.474",
            "resource": {
                "labels": {
                    "module_id": "",
                    "project_id": "test-project-123456",
                    "version_id": "",
                    "zone": "",
                },
                "type": "gae_app",
            },
            "severity": "NOTICE",
            "timestamp": "2023-05-23 19:28:48.707",
        },
    ),
    PantherRuleTest(
        Name="compute.non-delete.firewall.method-should-not-alert",
        ExpectedResult=False,
        Log={"methodName": "v1.compute.firewalls.insert"},
    ),
    PantherRuleTest(
        Name="appengine.non-delete.firewall.method-should-not-alert",
        ExpectedResult=False,
        Log={"methodName": "appengine.compute.v1.Firewall.PatchIngressRule"},
    ),
    PantherRuleTest(
        Name="randomservice.firewall-delete.method-should-alert",
        ExpectedResult=True,
        Log={
            "protoPayload": {
                "authenticationInfo": {"principalEmail": "user@domain.com"},
                "methodName": "randomservice.compute.v1.Firewall.DeleteIngressRule",
                "resourceName": "randomservice/test-project-123456/firewall/ingressRules/1000",
                "requestMetadata": {
                    "callerIP": "12.12.12.12",
                    "destinationAttributes": {},
                    "requestAttributes": {"auth": {}, "time": "2023-05-23T19:28:44.663413Z"},
                },
            },
            "resource": {
                "labels": {
                    "firewall_rule_id": "6563507997690081088",
                    "project_id": "test-project-123456",
                },
                "type": "gce_firewall_rule",
            },
        },
    ),
]


class GCPFirewallRuleDeleted(PantherRule):
    DisplayName = "GCP Firewall Rule Deleted"
    RuleID = "GCP.Firewall.Rule.Deleted-prototype"
    Severity = PantherSeverity.Low
    LogTypes = [LogType.GCP_AuditLog]
    Tags = ["GCP", "Firewall", "Networking", "Infrastructure"]
    Description = "This rule detects deletions of GCP firewall rules.\n"
    Runbook = "Ensure that the rule deletion was expected. Firewall rule deletions can cause service interruptions or outages.\n"
    Reference = "https://cloud.google.com/firewall/docs/about-firewalls"
    Tests = gcp_firewall_rule_deleted_tests

    def rule(self, event):
        method_pattern = "(?:\\w+\\.)*v\\d\\.(?:Firewall\\.Delete)|(compute\\.firewalls\\.delete)"
        match = re.search(method_pattern, deep_get(event, "protoPayload", "methodName", default=""))
        return match is not None

    def title(self, event):
        actor = deep_get(
            event,
            "protoPayload",
            "authenticationInfo",
            "principalEmail",
            default="<ACTOR_NOT_FOUND>",
        )
        resource = deep_get(event, "protoPayload", "resourceName", default="<RESOURCE_NOT_FOUND>")
        resource_id = deep_get(
            event, "resource", "labels", "firewall_rule_id", default="<RESOURCE_ID_NOT_FOUND>"
        )
        if resource_id != "<RESOURCE_ID_NOT_FOUND>":
            return f"[GCP]: [{actor}] deleted firewall rule with resource ID [{resource_id}]"
        return f"[GCP]: [{actor}] deleted firewall rule for resource [{resource}]"

    def alert_context(self, event):
        return gcp_alert_context(event)

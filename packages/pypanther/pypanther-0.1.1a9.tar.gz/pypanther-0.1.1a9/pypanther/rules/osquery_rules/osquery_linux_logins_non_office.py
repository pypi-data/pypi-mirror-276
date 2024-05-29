import ipaddress
from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import deep_get
from pypanther.log_types import LogType

osquery_linux_login_from_non_office_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Non-office network login (logged_in_users)",
        ExpectedResult=True,
        Log={
            "name": "pack/incident_response/logged_in_users",
            "action": "added",
            "columns": {"host": "10.0.3.1", "type": "user", "user": "ubuntu"},
        },
    ),
    PantherRuleTest(
        Name="Non-office network login (last)",
        ExpectedResult=True,
        Log={
            "name": "pack-incident_response-last",
            "action": "added",
            "columns": {
                "host": "10.0.3.1",
                "type": "8",
                "username": "ubuntu",
                "tty": "ttys008",
                "pid": "648",
                "time": "1587502574",
            },
        },
    ),
    PantherRuleTest(
        Name="Office network login",
        ExpectedResult=False,
        Log={
            "name": "pack-logged_in_users",
            "action": "added",
            "columns": {"host": "192.168.1.200", "user": "ubuntu"},
        },
    ),
]


class OsqueryLinuxLoginFromNonOffice(PantherRule):
    RuleID = "Osquery.Linux.LoginFromNonOffice-prototype"
    DisplayName = "A Login from Outside the Corporate Office"
    Enabled = False
    LogTypes = [LogType.Osquery_Differential]
    Tags = ["Configuration Required", "Osquery", "Linux", "Initial Access:Valid Accounts"]
    Reports = {"MITRE ATT&CK": ["TA0001:T1078"]}
    Severity = PantherSeverity.High
    Description = "A system has been logged into from a non approved IP space."
    Runbook = "Analyze the host IP, and if possible, update allowlist or fix ACL."
    Reference = "https://attack.mitre.org/techniques/T1078/"
    SummaryAttributes = ["name", "action", "p_any_ip_addresses", "p_any_domain_names"]
    Tests = osquery_linux_login_from_non_office_tests
    # This is only an example network, but you can set it to whatever you'd like
    OFFICE_NETWORKS = [
        ipaddress.ip_network("192.168.1.100/32"),
        ipaddress.ip_network("192.168.1.200/32"),
    ]

    def _login_from_non_office_network(self, host):
        host_ipaddr = ipaddress.IPv4Address(host)
        non_office_logins = []
        for office_network in self.OFFICE_NETWORKS:
            non_office_logins.append(host_ipaddr in office_network)
        return not any(non_office_logins)

    def rule(self, event):
        if event.get("action") != "added":
            return False
        if "logged_in_users" in event.get("name"):
            # Only pay attention to users and not system-level accounts
            if deep_get(event, "columns", "type") != "user":
                return False
        elif "last" in event.get("name"):
            pass
        else:
            # A query we don't care about
            return False
        host_ip = deep_get(event, "columns", "host")
        return self._login_from_non_office_network(host_ip)

    def title(self, event):
        user = deep_get(event, "columns", "user", default=deep_get(event, "columns", "username"))
        return f"User [{(user if user else '<UNKNOWN_USER>')} has logged into production from a non-office network"

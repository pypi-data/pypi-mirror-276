from datetime import timedelta
from typing import List

from panther_detection_helpers.caching import add_to_string_set, get_string_set, put_string_set

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import is_ip_in_network
from pypanther.log_types import LogType

one_login_active_login_activity_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Normal Login Event",
        ExpectedResult=False,
        Log={
            "event_type_id": "6",
            "actor_user_id": 123456,
            "actor_user_name": "Bob Cat",
            "user_id": 123456,
            "user_name": "Bob Cat",
        },
    ),
    PantherRuleTest(
        Name="Shared IP Login Event",
        ExpectedResult=False,
        Log={
            "event_type_id": "5",
            "actor_user_id": 123456,
            "actor_user_name": "Bob Cat",
            "user_id": 123456,
            "user_name": "Bob Cat",
            "ipaddr": "192.168.1.1",
        },
    ),
]


class OneLoginActiveLoginActivity(PantherRule):
    RuleID = "OneLogin.ActiveLoginActivity-prototype"
    DisplayName = "OneLogin Active Login Activity"
    LogTypes = [LogType.OneLogin_Events]
    Tags = ["OneLogin", "Lateral Movement:Use Alternate Authentication Material"]
    Severity = PantherSeverity.Medium
    Reports = {"MITRE ATT&CK": ["TA0008:T1550"]}
    Description = "Multiple user accounts logged in from the same ip address."
    Reference = "https://support.onelogin.com/kb/4271392/user-policies"
    Runbook = "Investigate whether multiple user's logging in from the same ip address is expected. Determine if this ip address should be added to the SHARED_IP_SPACE array."
    SummaryAttributes = ["account_id", "user_name", "user_id"]
    Tests = one_login_active_login_activity_tests
    THRESH = 2
    THRESH_TTL = timedelta(hours=12).total_seconds()
    # Safelist for IP Subnets to ignore in this ruleset
    # Each entry in the list should be in CIDR notation
    # This should include any source ip addresses
    # that are shared among users such as:
    # proxy servers, the public corporate ip space,
    # scanner ips etc
    SHARED_IP_SPACE = ["192.168.0.0/16"]

    def rule(self, event):
        # Pre-filter: event_type_id = 5 is login events.
        if (
            str(event.get("event_type_id")) != "5"
            or not event.get("ipaddr")
            or (not event.get("user_id"))
        ):
            return False
        # We expect to see multiple user logins from these shared, common ip addresses
        if is_ip_in_network(event.get("ipaddr"), self.SHARED_IP_SPACE):
            return False
        # This tracks multiple successful logins for different accounts from the same ip address
        # First, keep a list of unique user ids that have logged in from this ip address
        event_key = self.get_key(event)
        user_ids = get_string_set(event_key)
        # the user id of the user that has just logged in
        user_id = str(event.get("user_id"))
        if not user_ids:
            # store this as the first user login from this ip address
            put_string_set(
                event_key, [user_id], epoch_seconds=event.event_time_epoch() + self.THRESH_TTL
            )
            return False
        # add a new username if this is a unique user from this ip address
        if user_id not in user_ids:
            user_ids = add_to_string_set(
                event_key, user_id, epoch_seconds=event.event_time_epoch() + self.THRESH_TTL
            )
        return len(user_ids) > self.THRESH

    def get_key(self, event):
        return __name__ + ":" + event.get("ipaddr", "<UNKNOWN_IP>")

    def title(self, event):
        return f"Unusual logins in OneLogin for multiple users from ip [{event.get('ipaddr', '<UNKNOWN_IP>')}]"

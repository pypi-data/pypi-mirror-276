from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.log_types import LogType

teleport_scheduled_jobs_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Crontab no args",
        ExpectedResult=True,
        Log={
            "argv": [],
            "cgroup_id": 4294967717,
            "code": "T4000I",
            "ei": 39,
            "event": "session.command",
            "login": "root",
            "namespace": "default",
            "path": "/bin/crontab",
            "pid": 18415,
            "ppid": 18413,
            "program": "crontab",
            "return_code": 0,
            "server_id": "e073ecab-6091-45da-83e4-80196e7bc659",
            "sid": "29a3d18c-2c05-453d-979a-2ed888a14788",
            "time": "2020-08-18T00:05:12.465Z",
            "uid": "83e88438-efbc-41a2-8135-b0157e0d14c0",
            "user": "panther",
        },
    ),
    PantherRuleTest(
        Name="Crontab Edit",
        ExpectedResult=True,
        Log={
            "argv": ["-e"],
            "cgroup_id": 4294967582,
            "code": "T4000I",
            "ei": 50,
            "event": "session.command",
            "login": "root",
            "namespace": "default",
            "path": "/bin/crontab",
            "pid": 9451,
            "ppid": 9217,
            "program": "crontab",
            "return_code": 0,
            "server_id": "e75992b4-9e27-456f-b1c9-7a32da83c661",
            "sid": "af24d0b8-9767-4bd8-99ce-7a4449ee3eba",
            "time": "2020-08-17T18:54:32.273Z",
            "uid": "ad4a31d0-d739-4409-8f1c-cf573ed97a89",
            "user": "panther",
        },
    ),
    PantherRuleTest(
        Name="Crontab List",
        ExpectedResult=False,
        Log={
            "argv": ["-l"],
            "cgroup_id": 4294967582,
            "code": "T4000I",
            "ei": 37,
            "event": "session.command",
            "login": "root",
            "namespace": "default",
            "path": "/bin/crontab",
            "pid": 9330,
            "ppid": 9315,
            "program": "crontab",
            "return_code": 0,
            "server_id": "e75992b4-9e27-456f-b1c9-7a32da83c661",
            "sid": "af24d0b8-9767-4bd8-99ce-7a4449ee3eba",
            "time": "2020-08-17T18:50:39.1Z",
            "uid": "6b463839-c641-43d3-ab97-3137ff9b09f8",
            "user": "panther",
        },
    ),
    PantherRuleTest(
        Name="Echo command",
        ExpectedResult=False,
        Log={
            "argv": [],
            "cgroup_id": 4294967537,
            "code": "T4000I",
            "ei": 15,
            "event": "session.command",
            "login": "root",
            "namespace": "default",
            "path": "/bin/echo",
            "pid": 7143,
            "ppid": 7115,
            "program": "echo",
            "return_code": 0,
            "server_id": "e75992b4-9e27-456f-b1c9-7a32da83c661",
            "sid": "8a3fc038-785b-43f3-8737-827b3e25fe5b",
            "time": "2020-08-17T17:40:37.491Z",
            "uid": "8eaf8f39-09d4-4a42-a22a-65163d2af702",
            "user": "panther",
        },
    ),
]


class TeleportScheduledJobs(PantherRule):
    RuleID = "Teleport.ScheduledJobs-prototype"
    DisplayName = "Teleport Scheduled Jobs"
    LogTypes = [LogType.Gravitational_TeleportAudit]
    Tags = ["SSH", "Execution:Scheduled Task/Job"]
    Severity = PantherSeverity.Medium
    Reports = {"MITRE ATT&CK": ["TA0002:T1053"]}
    Description = "A user has manually edited the Linux crontab"
    Threshold = 10
    DedupPeriodMinutes = 15
    Reference = "https://goteleport.com/docs/management/admin/"
    Runbook = "Validate the user behavior and rotate the host if necessary."
    SummaryAttributes = [
        "event",
        "code",
        "user",
        "program",
        "path",
        "return_code",
        "login",
        "server_id",
        "sid",
    ]
    Tests = teleport_scheduled_jobs_tests

    def rule(self, event):
        # Filter the events
        if event.get("event") != "session.command":
            return False
        # Ignore list/read events
        if "-l" in event.get("argv", []):
            return False
        return event.get("program") == "crontab"

    def title(self, event):
        return f"User [{event.get('user', '<UNKNOWN_USER>')}] has modified scheduled jobson [{event.get('cluster_name', '<UNKNOWN_CLUSTER>')}]"

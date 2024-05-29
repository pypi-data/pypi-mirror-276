from enum import Enum


class LogType(str, Enum):
    AWS_ALB = "AWS.ALB"
    AWS_AuroraMySQLAudit = "AWS.AuroraMySQLAudit"
    AWS_CloudTrail = "AWS.CloudTrail"
    AWS_CloudTrailDigest = "AWS.CloudTrailDigest"
    AWS_CloudTrailInsight = "AWS.CloudTrailInsight"
    AWS_CloudWatchEvents = "AWS.CloudWatchEvents"
    AWS_Config = "AWS.Config"
    AWS_GuardDuty = "AWS.GuardDuty"
    AWS_S3ServerAccess = "AWS.S3ServerAccess"
    AWS_SecurityFindingFormat = "AWS.SecurityFindingFormat"
    AWS_TransitGatewayFlow = "AWS.TransitGatewayFlow"
    AWS_VPCDns = "AWS.VPCDns"
    AWS_VPCFlow = "AWS.VPCFlow"
    AWS_WAFWebACL = "AWS.WAFWebACL"
    AlphaSOC_Alert = "AlphaSOC.Alert"
    Amazon_EKS_Audit = "Amazon.EKS.Audit"
    Amazon_EKS_Authenticator = "Amazon.EKS.Authenticator"
    Anomali_Indicator = "Anomali.Indicator"
    Apache_AccessCombined = "Apache.AccessCombined"
    Apache_AccessCommon = "Apache.AccessCommon"
    AppOmni_Alerts = "AppOmni.Alerts"
    AppOmni_Events = "AppOmni.Events"
    AppOmni_Policy = "AppOmni.Policy"
    Asana_Audit = "Asana.Audit"
    Atlassian_Audit = "Atlassian.Audit"
    Auth0_Events = "Auth0.Events"
    Azure_Audit = "Azure.Audit"
    Azure_DefenderAlerts = "Azure.DefenderAlerts"
    Azure_MonitorActivity = "Azure.MonitorActivity"
    Bitwarden_Events = "Bitwarden.Events"
    Box_Event = "Box.Event"
    CarbonBlack_AlertV2 = "CarbonBlack.AlertV2"
    CarbonBlack_Audit = "CarbonBlack.Audit"
    CarbonBlack_EndpointEvent = "CarbonBlack.EndpointEvent"
    CarbonBlack_WatchlistHit = "CarbonBlack.WatchlistHit"
    CiscoUmbrella_CloudFirewall = "CiscoUmbrella.CloudFirewall"
    CiscoUmbrella_DNS = "CiscoUmbrella.DNS"
    CiscoUmbrella_IP = "CiscoUmbrella.IP"
    CiscoUmbrella_Proxy = "CiscoUmbrella.Proxy"
    Cloudflare_Audit = "Cloudflare.Audit"
    Cloudflare_Firewall = "Cloudflare.Firewall"
    Cloudflare_HttpRequest = "Cloudflare.HttpRequest"
    Cloudflare_Spectrum = "Cloudflare.Spectrum"
    Cloudflare_ZeroTrust_RData = "Cloudflare.ZeroTrust.RData"
    Crowdstrike_AIDMaster = "Crowdstrike.AIDMaster"
    Crowdstrike_ActivityAudit = "Crowdstrike.ActivityAudit"
    Crowdstrike_AppInfo = "Crowdstrike.AppInfo"
    Crowdstrike_CriticalFile = "Crowdstrike.CriticalFile"
    Crowdstrike_DNSRequest = "Crowdstrike.DNSRequest"
    Crowdstrike_DetectionSummary = "Crowdstrike.DetectionSummary"
    Crowdstrike_FDREvent = "Crowdstrike.FDREvent"
    Crowdstrike_GroupIdentity = "Crowdstrike.GroupIdentity"
    Crowdstrike_ManagedAssets = "Crowdstrike.ManagedAssets"
    Crowdstrike_NetworkConnect = "Crowdstrike.NetworkConnect"
    Crowdstrike_NetworkListen = "Crowdstrike.NetworkListen"
    Crowdstrike_NotManagedAssets = "Crowdstrike.NotManagedAssets"
    Crowdstrike_ProcessRollup2 = "Crowdstrike.ProcessRollup2"
    Crowdstrike_ProcessRollup2Stats = "Crowdstrike.ProcessRollup2Stats"
    Crowdstrike_SyntheticProcessRollup2 = "Crowdstrike.SyntheticProcessRollup2"
    Crowdstrike_Unknown = "Crowdstrike.Unknown"
    Crowdstrike_UserIdentity = "Crowdstrike.UserIdentity"
    Crowdstrike_UserInfo = "Crowdstrike.UserInfo"
    Crowdstrike_UserLogonLogoff = "Crowdstrike.UserLogonLogoff"
    Docker_Events = "Docker.Events"
    Dropbox_TeamEvent = "Dropbox.TeamEvent"
    Duo_Administrator = "Duo.Administrator"
    Duo_Authentication = "Duo.Authentication"
    Duo_OfflineEnrollment = "Duo.OfflineEnrollment"
    Duo_Telephony = "Duo.Telephony"
    Envoy_Access = "Envoy.Access"
    Fastly_Access = "Fastly.Access"
    Fluentd_Syslog3164 = "Fluentd.Syslog3164"
    Fluentd_Syslog5424 = "Fluentd.Syslog5424"
    GCP_AuditLog = "GCP.AuditLog"
    GCP_HTTPLoadBalancer = "GCP.HTTPLoadBalancer"
    GSuite_ActivityEvent = "GSuite.ActivityEvent"
    GSuite_DirectoryUsers = "GSuite.DirectoryUsers"
    GSuite_Reports = "GSuite.Reports"
    GitHub_Audit = "GitHub.Audit"
    GitHub_Webhook = "GitHub.Webhook"
    GitLab_API = "GitLab.API"
    GitLab_Audit = "GitLab.Audit"
    GitLab_Exceptions = "GitLab.Exceptions"
    GitLab_Git = "GitLab.Git"
    GitLab_Integrations = "GitLab.Integrations"
    GitLab_Production = "GitLab.Production"
    Gravitational_TeleportAudit = "Gravitational.TeleportAudit"
    GreyNoise_Noise = "GreyNoise.Noise"
    GreyNoise_RIOT = "GreyNoise.RIOT"
    Heroku_Runtime = "Heroku.Runtime"
    IPInfo_ASNCIDR = "IPInfo.ASNCIDR"
    IPInfo_ASNRanges = "IPInfo.ASNRanges"
    IPInfo_LocationCIDR = "IPInfo.LocationCIDR"
    IPInfo_LocationRanges = "IPInfo.LocationRanges"
    IPInfo_PrivacyCIDR = "IPInfo.PrivacyCIDR"
    IPInfo_PrivacyRanges = "IPInfo.PrivacyRanges"
    Jamfpro_ComplianceReporter = "Jamfpro.ComplianceReporter"
    Jamfpro_Login = "Jamfpro.Login"
    Juniper_Access = "Juniper.Access"
    Juniper_Audit = "Juniper.Audit"
    Juniper_Firewall = "Juniper.Firewall"
    Juniper_MWS = "Juniper.MWS"
    Juniper_Postgres = "Juniper.Postgres"
    Juniper_Security = "Juniper.Security"
    Lacework_AgentManagement = "Lacework.AgentManagement"
    Lacework_AlertDetails = "Lacework.AlertDetails"
    Lacework_AllFiles = "Lacework.AllFiles"
    Lacework_Applications = "Lacework.Applications"
    Lacework_ChangeFiles = "Lacework.ChangeFiles"
    Lacework_CloudCompliance = "Lacework.CloudCompliance"
    Lacework_CloudConfiguration = "Lacework.CloudConfiguration"
    Lacework_Cmdline = "Lacework.Cmdline"
    Lacework_Connections = "Lacework.Connections"
    Lacework_ContainerSummary = "Lacework.ContainerSummary"
    Lacework_ContainerVulnDetails = "Lacework.ContainerVulnDetails"
    Lacework_DNSQuery = "Lacework.DNSQuery"
    Lacework_Events = "Lacework.Events"
    Lacework_HostVulnDetails = "Lacework.HostVulnDetails"
    Lacework_Image = "Lacework.Image"
    Lacework_Interfaces = "Lacework.Interfaces"
    Lacework_InternalIPA = "Lacework.InternalIPA"
    Lacework_MachineDetails = "Lacework.MachineDetails"
    Lacework_MachineSummary = "Lacework.MachineSummary"
    Lacework_NewHashes = "Lacework.NewHashes"
    Lacework_Package = "Lacework.Package"
    Lacework_PodSummary = "Lacework.PodSummary"
    Lacework_ProcessSummary = "Lacework.ProcessSummary"
    Lacework_UserDetails = "Lacework.UserDetails"
    Lacework_UserLogin = "Lacework.UserLogin"
    Linux_Auditd = "Linux.Auditd"
    Microsoft365_Audit_AzureActiveDirectory = "Microsoft365.Audit.AzureActiveDirectory"
    Microsoft365_Audit_Exchange = "Microsoft365.Audit.Exchange"
    Microsoft365_Audit_General = "Microsoft365.Audit.General"
    Microsoft365_Audit_SharePoint = "Microsoft365.Audit.SharePoint"
    Microsoft365_DLP_All = "Microsoft365.DLP.All"
    MicrosoftGraph_SecurityAlert = "MicrosoftGraph.SecurityAlert"
    MongoDB_OrganizationEvent = "MongoDB.OrganizationEvent"
    MongoDB_ProjectEvent = "MongoDB.ProjectEvent"
    Netskope_Audit = "Netskope.Audit"
    Nginx_Access = "Nginx.Access"
    Nginx_Error = "Nginx.Error"
    Notion_AuditLogs = "Notion.AuditLogs"
    OCSF_AccountChange = "OCSF.AccountChange"
    OCSF_ApiActivity = "OCSF.ApiActivity"
    OCSF_ApplicationLifecycle = "OCSF.ApplicationLifecycle"
    OCSF_Authentication = "OCSF.Authentication"
    OCSF_AuthorizeSession = "OCSF.AuthorizeSession"
    OCSF_BaseEvent = "OCSF.BaseEvent"
    OCSF_ComplianceFinding = "OCSF.ComplianceFinding"
    OCSF_ConfigState = "OCSF.ConfigState"
    OCSF_DatastoreActivity = "OCSF.DatastoreActivity"
    OCSF_DetectionFinding = "OCSF.DetectionFinding"
    OCSF_DeviceConfigStateChange = "OCSF.DeviceConfigStateChange"
    OCSF_DhcpActivity = "OCSF.DhcpActivity"
    OCSF_DnsActivity = "OCSF.DnsActivity"
    OCSF_EmailActivity = "OCSF.EmailActivity"
    OCSF_EmailFileActivity = "OCSF.EmailFileActivity"
    OCSF_EmailUrlActivity = "OCSF.EmailUrlActivity"
    OCSF_EntityManagement = "OCSF.EntityManagement"
    OCSF_FileActivity = "OCSF.FileActivity"
    OCSF_FileHosting = "OCSF.FileHosting"
    OCSF_FtpActivity = "OCSF.FtpActivity"
    OCSF_GroupManagement = "OCSF.GroupManagement"
    OCSF_HttpActivity = "OCSF.HttpActivity"
    OCSF_IncidentFinding = "OCSF.IncidentFinding"
    OCSF_InventoryInfo = "OCSF.InventoryInfo"
    OCSF_KernelActivity = "OCSF.KernelActivity"
    OCSF_KernelExtension = "OCSF.KernelExtension"
    OCSF_MemoryActivity = "OCSF.MemoryActivity"
    OCSF_ModuleActivity = "OCSF.ModuleActivity"
    OCSF_NetworkActivity = "OCSF.NetworkActivity"
    OCSF_NetworkFileActivity = "OCSF.NetworkFileActivity"
    OCSF_NtpActivity = "OCSF.NtpActivity"
    OCSF_PatchState = "OCSF.PatchState"
    OCSF_ProcessActivity = "OCSF.ProcessActivity"
    OCSF_RdpActivity = "OCSF.RdpActivity"
    OCSF_ScanActivity = "OCSF.ScanActivity"
    OCSF_ScheduledJobActivity = "OCSF.ScheduledJobActivity"
    OCSF_SecurityFinding = "OCSF.SecurityFinding"
    OCSF_SmbActivity = "OCSF.SmbActivity"
    OCSF_SshActivity = "OCSF.SshActivity"
    OCSF_UserAccess = "OCSF.UserAccess"
    OCSF_UserInventory = "OCSF.UserInventory"
    OCSF_VulnerabilityFinding = "OCSF.VulnerabilityFinding"
    OCSF_WebResourceAccessActivity = "OCSF.WebResourceAccessActivity"
    OCSF_WebResourcesActivity = "OCSF.WebResourcesActivity"
    OCSF_WinPrefetchInfo = "OCSF.WinPrefetchInfo"
    OCSF_WinRegistryKeyActivity = "OCSF.WinRegistryKeyActivity"
    OCSF_WinRegistryKeyInfo = "OCSF.WinRegistryKeyInfo"
    OCSF_WinRegistryValueActivity = "OCSF.WinRegistryValueActivity"
    OCSF_WinRegistryValueInfo = "OCSF.WinRegistryValueInfo"
    OCSF_WinResourceActivity = "OCSF.WinResourceActivity"
    OCSF_WinprefetchInfo = "OCSF.WinprefetchInfo"
    OCSF_WinregistryKeyActivity = "OCSF.WinregistryKeyActivity"
    OCSF_WinregistryKeyInfo = "OCSF.WinregistryKeyInfo"
    OCSF_WinregistryValueActivity = "OCSF.WinregistryValueActivity"
    OCSF_WinregistryValueInfo = "OCSF.WinregistryValueInfo"
    OCSF_WinresourceActivity = "OCSF.WinresourceActivity"
    OSSEC_EventInfo = "OSSEC.EventInfo"
    Okta_Devices = "Okta.Devices"
    Okta_SystemLog = "Okta.SystemLog"
    Okta_Users = "Okta.Users"
    OneLogin_Events = "OneLogin.Events"
    OnePassword_AuditEvent = "OnePassword.AuditEvent"
    OnePassword_ItemUsage = "OnePassword.ItemUsage"
    OnePassword_SignInAttempt = "OnePassword.SignInAttempt"
    Osquery_Batch = "Osquery.Batch"
    Osquery_Differential = "Osquery.Differential"
    Osquery_Snapshot = "Osquery.Snapshot"
    Osquery_Status = "Osquery.Status"
    Panther_Audit = "Panther.Audit"
    Proofpoint_Event = "Proofpoint.Event"
    PushSecurity_Activity = "PushSecurity.Activity"
    PushSecurity_AttackDetection = "PushSecurity.AttackDetection"
    PushSecurity_Entities = "PushSecurity.Entities"
    Salesforce_Login = "Salesforce.Login"
    Salesforce_LoginAs = "Salesforce.LoginAs"
    Salesforce_Logout = "Salesforce.Logout"
    Salesforce_URI = "Salesforce.URI"
    SentinelOne_Activity = "SentinelOne.Activity"
    SentinelOne_DeepVisibility = "SentinelOne.DeepVisibility"
    SentinelOne_DeepVisibilityV2 = "SentinelOne.DeepVisibilityV2"
    Slack_AccessLogs = "Slack.AccessLogs"
    Slack_AuditLogs = "Slack.AuditLogs"
    Slack_IntegrationLogs = "Slack.IntegrationLogs"
    Snyk_GroupAudit = "Snyk.GroupAudit"
    Snyk_OrgAudit = "Snyk.OrgAudit"
    Sophos_Central = "Sophos.Central"
    Suricata_Alert = "Suricata.Alert"
    Suricata_Anomaly = "Suricata.Anomaly"
    Suricata_DHCP = "Suricata.DHCP"
    Suricata_DNS = "Suricata.DNS"
    Suricata_FileInfo = "Suricata.FileInfo"
    Suricata_Flow = "Suricata.Flow"
    Suricata_HTTP = "Suricata.HTTP"
    Suricata_SSH = "Suricata.SSH"
    Suricata_TLS = "Suricata.TLS"
    Sysdig_Audit = "Sysdig.Audit"
    Syslog_RFC3164 = "Syslog.RFC3164"
    Syslog_RFC5424 = "Syslog.RFC5424"
    Tailscale_Audit = "Tailscale.Audit"
    Tailscale_Network = "Tailscale.Network"
    Tenable_Vulnerability = "Tenable.Vulnerability"
    Tines_Audit = "Tines.Audit"
    Tor_ExitNode = "Tor.ExitNode"
    TrailDiscover_CloudTrail = "TrailDiscover.CloudTrail"
    Windows_EventLogs = "Windows.EventLogs"
    Workday_Activity = "Workday.Activity"
    Workday_SignOnAttempt = "Workday.SignOnAttempt"
    Zeek_CaptureLoss = "Zeek.CaptureLoss"
    Zeek_Conn = "Zeek.Conn"
    Zeek_DHCP = "Zeek.DHCP"
    Zeek_DNS = "Zeek.DNS"
    Zeek_DPD = "Zeek.DPD"
    Zeek_Files = "Zeek.Files"
    Zeek_HTTP = "Zeek.HTTP"
    Zeek_NTP = "Zeek.NTP"
    Zeek_Notice = "Zeek.Notice"
    Zeek_OCSP = "Zeek.OCSP"
    Zeek_Reporter = "Zeek.Reporter"
    Zeek_SIP = "Zeek.SIP"
    Zeek_Software = "Zeek.Software"
    Zeek_Ssh = "Zeek.Ssh"
    Zeek_Ssl = "Zeek.Ssl"
    Zeek_Stats = "Zeek.Stats"
    Zeek_Tunnel = "Zeek.Tunnel"
    Zeek_Weird = "Zeek.Weird"
    Zeek_X509 = "Zeek.X509"
    Zendesk_Audit = "Zendesk.Audit"
    Zoom_Activity = "Zoom.Activity"
    Zoom_Operation = "Zoom.Operation"

    def __str__(self) -> str:
        """Returns a string representation of the class' value."""
        return self.value

    @staticmethod
    def get_attribute_name(value: str) -> str:
        """Returns the attribute name of the class' value."""
        for name, member in LogType.__members__.items():
            if member.value == value:
                return name
        raise AttributeError(f"LogType has no attribute with value {value}")

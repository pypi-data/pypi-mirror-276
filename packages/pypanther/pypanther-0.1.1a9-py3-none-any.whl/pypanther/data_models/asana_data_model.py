from typing import List

import pypanther.helpers.panther_event_type_helpers as event_type
from pypanther.base import PantherDataModel, PantherDataModelMapping
from pypanther.log_types import LogType

audit_log_type_map = {
    "user_login_succeeded": event_type.SUCCESSFUL_LOGIN,
    "user_login_failed": event_type.FAILED_LOGIN,
    "user_invited": event_type.USER_ACCOUNT_CREATED,
    "user_reprovisioned": event_type.USER_ACCOUNT_CREATED,
    "user_deprovisioned": event_type.USER_ACCOUNT_DELETED,
    "user_workspace_admin_role_changed": event_type.ADMIN_ROLE_ASSIGNED,
}


def get_event_type(event):
    logged_event_type = event.get("event_type", {})
    # Since this is a safe dict get if the event type is not mapped
    # there is an implicit return of None
    return audit_log_type_map.get(logged_event_type)


class StandardAsanaAudit(PantherDataModel):
    DataModelID: str = "Standard.Asana.Audit"
    DisplayName: str = "Asana Audit Logs"
    Enabled: bool = True
    LogTypes: List[str] = [LogType.Asana_Audit]
    Mappings: List[PantherDataModelMapping] = [
        PantherDataModelMapping(Name="actor_user", Path="$.actor.name"),
        PantherDataModelMapping(Name="event_type", Method=get_event_type),
        PantherDataModelMapping(Name="source_ip", Path="$.context.client_ip_address"),
        PantherDataModelMapping(Name="user", Path="$.resource.name"),
    ]

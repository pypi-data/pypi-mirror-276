import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.list_jobs_response_200_item_type_0_job_kind import ListJobsResponse200ItemType0JobKind
from ..models.list_jobs_response_200_item_type_0_language import ListJobsResponse200ItemType0Language
from ..models.list_jobs_response_200_item_type_0_type import ListJobsResponse200ItemType0Type
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_jobs_response_200_item_type_0_args import ListJobsResponse200ItemType0Args
    from ..models.list_jobs_response_200_item_type_0_flow_status import ListJobsResponse200ItemType0FlowStatus
    from ..models.list_jobs_response_200_item_type_0_raw_flow import ListJobsResponse200ItemType0RawFlow


T = TypeVar("T", bound="ListJobsResponse200ItemType0")


@_attrs_define
class ListJobsResponse200ItemType0:
    """
    Attributes:
        id (str):
        created_by (str):
        created_at (datetime.datetime):
        started_at (datetime.datetime):
        duration_ms (int):
        success (bool):
        canceled (bool):
        job_kind (ListJobsResponse200ItemType0JobKind):
        permissioned_as (str): The user (u/userfoo) or group (g/groupfoo) whom
            the execution of this script will be permissioned_as and by extension its DT_TOKEN.
        is_flow_step (bool):
        is_skipped (bool):
        email (str):
        visible_to_owner (bool):
        tag (str):
        workspace_id (Union[Unset, str]):
        parent_job (Union[Unset, str]):
        script_path (Union[Unset, str]):
        script_hash (Union[Unset, str]):
        args (Union[Unset, ListJobsResponse200ItemType0Args]):
        result (Union[Unset, Any]):
        logs (Union[Unset, str]):
        deleted (Union[Unset, bool]):
        raw_code (Union[Unset, str]):
        canceled_by (Union[Unset, str]):
        canceled_reason (Union[Unset, str]):
        schedule_path (Union[Unset, str]):
        flow_status (Union[Unset, ListJobsResponse200ItemType0FlowStatus]):
        raw_flow (Union[Unset, ListJobsResponse200ItemType0RawFlow]):
        language (Union[Unset, ListJobsResponse200ItemType0Language]):
        mem_peak (Union[Unset, int]):
        priority (Union[Unset, int]):
        labels (Union[Unset, List[str]]):
        type (Union[Unset, ListJobsResponse200ItemType0Type]):
    """

    id: str
    created_by: str
    created_at: datetime.datetime
    started_at: datetime.datetime
    duration_ms: int
    success: bool
    canceled: bool
    job_kind: ListJobsResponse200ItemType0JobKind
    permissioned_as: str
    is_flow_step: bool
    is_skipped: bool
    email: str
    visible_to_owner: bool
    tag: str
    workspace_id: Union[Unset, str] = UNSET
    parent_job: Union[Unset, str] = UNSET
    script_path: Union[Unset, str] = UNSET
    script_hash: Union[Unset, str] = UNSET
    args: Union[Unset, "ListJobsResponse200ItemType0Args"] = UNSET
    result: Union[Unset, Any] = UNSET
    logs: Union[Unset, str] = UNSET
    deleted: Union[Unset, bool] = UNSET
    raw_code: Union[Unset, str] = UNSET
    canceled_by: Union[Unset, str] = UNSET
    canceled_reason: Union[Unset, str] = UNSET
    schedule_path: Union[Unset, str] = UNSET
    flow_status: Union[Unset, "ListJobsResponse200ItemType0FlowStatus"] = UNSET
    raw_flow: Union[Unset, "ListJobsResponse200ItemType0RawFlow"] = UNSET
    language: Union[Unset, ListJobsResponse200ItemType0Language] = UNSET
    mem_peak: Union[Unset, int] = UNSET
    priority: Union[Unset, int] = UNSET
    labels: Union[Unset, List[str]] = UNSET
    type: Union[Unset, ListJobsResponse200ItemType0Type] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        created_by = self.created_by
        created_at = self.created_at.isoformat()

        started_at = self.started_at.isoformat()

        duration_ms = self.duration_ms
        success = self.success
        canceled = self.canceled
        job_kind = self.job_kind.value

        permissioned_as = self.permissioned_as
        is_flow_step = self.is_flow_step
        is_skipped = self.is_skipped
        email = self.email
        visible_to_owner = self.visible_to_owner
        tag = self.tag
        workspace_id = self.workspace_id
        parent_job = self.parent_job
        script_path = self.script_path
        script_hash = self.script_hash
        args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.args, Unset):
            args = self.args.to_dict()

        result = self.result
        logs = self.logs
        deleted = self.deleted
        raw_code = self.raw_code
        canceled_by = self.canceled_by
        canceled_reason = self.canceled_reason
        schedule_path = self.schedule_path
        flow_status: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.flow_status, Unset):
            flow_status = self.flow_status.to_dict()

        raw_flow: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.raw_flow, Unset):
            raw_flow = self.raw_flow.to_dict()

        language: Union[Unset, str] = UNSET
        if not isinstance(self.language, Unset):
            language = self.language.value

        mem_peak = self.mem_peak
        priority = self.priority
        labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_by": created_by,
                "created_at": created_at,
                "started_at": started_at,
                "duration_ms": duration_ms,
                "success": success,
                "canceled": canceled,
                "job_kind": job_kind,
                "permissioned_as": permissioned_as,
                "is_flow_step": is_flow_step,
                "is_skipped": is_skipped,
                "email": email,
                "visible_to_owner": visible_to_owner,
                "tag": tag,
            }
        )
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if parent_job is not UNSET:
            field_dict["parent_job"] = parent_job
        if script_path is not UNSET:
            field_dict["script_path"] = script_path
        if script_hash is not UNSET:
            field_dict["script_hash"] = script_hash
        if args is not UNSET:
            field_dict["args"] = args
        if result is not UNSET:
            field_dict["result"] = result
        if logs is not UNSET:
            field_dict["logs"] = logs
        if deleted is not UNSET:
            field_dict["deleted"] = deleted
        if raw_code is not UNSET:
            field_dict["raw_code"] = raw_code
        if canceled_by is not UNSET:
            field_dict["canceled_by"] = canceled_by
        if canceled_reason is not UNSET:
            field_dict["canceled_reason"] = canceled_reason
        if schedule_path is not UNSET:
            field_dict["schedule_path"] = schedule_path
        if flow_status is not UNSET:
            field_dict["flow_status"] = flow_status
        if raw_flow is not UNSET:
            field_dict["raw_flow"] = raw_flow
        if language is not UNSET:
            field_dict["language"] = language
        if mem_peak is not UNSET:
            field_dict["mem_peak"] = mem_peak
        if priority is not UNSET:
            field_dict["priority"] = priority
        if labels is not UNSET:
            field_dict["labels"] = labels
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_jobs_response_200_item_type_0_args import ListJobsResponse200ItemType0Args
        from ..models.list_jobs_response_200_item_type_0_flow_status import ListJobsResponse200ItemType0FlowStatus
        from ..models.list_jobs_response_200_item_type_0_raw_flow import ListJobsResponse200ItemType0RawFlow

        d = src_dict.copy()
        id = d.pop("id")

        created_by = d.pop("created_by")

        created_at = isoparse(d.pop("created_at"))

        started_at = isoparse(d.pop("started_at"))

        duration_ms = d.pop("duration_ms")

        success = d.pop("success")

        canceled = d.pop("canceled")

        job_kind = ListJobsResponse200ItemType0JobKind(d.pop("job_kind"))

        permissioned_as = d.pop("permissioned_as")

        is_flow_step = d.pop("is_flow_step")

        is_skipped = d.pop("is_skipped")

        email = d.pop("email")

        visible_to_owner = d.pop("visible_to_owner")

        tag = d.pop("tag")

        workspace_id = d.pop("workspace_id", UNSET)

        parent_job = d.pop("parent_job", UNSET)

        script_path = d.pop("script_path", UNSET)

        script_hash = d.pop("script_hash", UNSET)

        _args = d.pop("args", UNSET)
        args: Union[Unset, ListJobsResponse200ItemType0Args]
        if isinstance(_args, Unset):
            args = UNSET
        else:
            args = ListJobsResponse200ItemType0Args.from_dict(_args)

        result = d.pop("result", UNSET)

        logs = d.pop("logs", UNSET)

        deleted = d.pop("deleted", UNSET)

        raw_code = d.pop("raw_code", UNSET)

        canceled_by = d.pop("canceled_by", UNSET)

        canceled_reason = d.pop("canceled_reason", UNSET)

        schedule_path = d.pop("schedule_path", UNSET)

        _flow_status = d.pop("flow_status", UNSET)
        flow_status: Union[Unset, ListJobsResponse200ItemType0FlowStatus]
        if isinstance(_flow_status, Unset):
            flow_status = UNSET
        else:
            flow_status = ListJobsResponse200ItemType0FlowStatus.from_dict(_flow_status)

        _raw_flow = d.pop("raw_flow", UNSET)
        raw_flow: Union[Unset, ListJobsResponse200ItemType0RawFlow]
        if isinstance(_raw_flow, Unset):
            raw_flow = UNSET
        else:
            raw_flow = ListJobsResponse200ItemType0RawFlow.from_dict(_raw_flow)

        _language = d.pop("language", UNSET)
        language: Union[Unset, ListJobsResponse200ItemType0Language]
        if isinstance(_language, Unset):
            language = UNSET
        else:
            language = ListJobsResponse200ItemType0Language(_language)

        mem_peak = d.pop("mem_peak", UNSET)

        priority = d.pop("priority", UNSET)

        labels = cast(List[str], d.pop("labels", UNSET))

        _type = d.pop("type", UNSET)
        type: Union[Unset, ListJobsResponse200ItemType0Type]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = ListJobsResponse200ItemType0Type(_type)

        list_jobs_response_200_item_type_0 = cls(
            id=id,
            created_by=created_by,
            created_at=created_at,
            started_at=started_at,
            duration_ms=duration_ms,
            success=success,
            canceled=canceled,
            job_kind=job_kind,
            permissioned_as=permissioned_as,
            is_flow_step=is_flow_step,
            is_skipped=is_skipped,
            email=email,
            visible_to_owner=visible_to_owner,
            tag=tag,
            workspace_id=workspace_id,
            parent_job=parent_job,
            script_path=script_path,
            script_hash=script_hash,
            args=args,
            result=result,
            logs=logs,
            deleted=deleted,
            raw_code=raw_code,
            canceled_by=canceled_by,
            canceled_reason=canceled_reason,
            schedule_path=schedule_path,
            flow_status=flow_status,
            raw_flow=raw_flow,
            language=language,
            mem_peak=mem_peak,
            priority=priority,
            labels=labels,
            type=type,
        )

        list_jobs_response_200_item_type_0.additional_properties = d
        return list_jobs_response_200_item_type_0

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.run_steps_object import RunStepsObject
from ..models.run_steps_status import RunStepsStatus
from ..models.run_steps_type import RunStepsType

if TYPE_CHECKING:
    from ..models.message_creation import MessageCreation
    from ..models.run_step_completion_usage_type_0 import RunStepCompletionUsageType0
    from ..models.run_steps_last_error_type_0 import RunStepsLastErrorType0
    from ..models.run_steps_metadata_type_0 import RunStepsMetadataType0
    from ..models.tool_calls import ToolCalls


T = TypeVar("T", bound="RunSteps")


@_attrs_define
class RunSteps:
    """Represents a step in execution of a run.

    Attributes:
        id (str): The identifier of the run step, which can be referenced in API endpoints.
        object_ (RunStepsObject): The object type, which is always `thread.run.step`.
        created_at (int): The Unix timestamp (in seconds) for when the run step was created.
        assistant_id (str): The ID of the [assistant](/docs/api-reference/assistants) associated with the run step.
        thread_id (str): The ID of the [thread](/docs/api-reference/threads) that was run.
        run_id (str): The ID of the [run](/docs/api-reference/runs) that this run step is a part of.
        type (RunStepsType): The type of run step, which can be either `message_creation` or `tool_calls`.
        status (RunStepsStatus): The status of the run step, which can be either `in_progress`, `cancelled`, `failed`,
            `completed`, or `expired`.
        step_details (Union['MessageCreation', 'ToolCalls']): The details of the run step.
        last_error (Union['RunStepsLastErrorType0', None]): The last error associated with this run step. Will be `null`
            if there are no errors.
        expired_at (Union[None, int]): The Unix timestamp (in seconds) for when the run step expired. A step is
            considered expired if the parent run is expired.
        cancelled_at (Union[None, int]): The Unix timestamp (in seconds) for when the run step was cancelled.
        failed_at (Union[None, int]): The Unix timestamp (in seconds) for when the run step failed.
        completed_at (Union[None, int]): The Unix timestamp (in seconds) for when the run step completed.
        metadata (Union['RunStepsMetadataType0', None]): Set of 16 key-value pairs that can be attached to an object.
            This can be useful for storing additional information about the object in a structured format. Keys can be a
            maximum of 64 characters long and values can be a maxium of 512 characters long.
        usage (Union['RunStepCompletionUsageType0', None]): Usage statistics related to the run step. This value will be
            `null` while the run step's status is `in_progress`.
    """

    id: str
    object_: RunStepsObject
    created_at: int
    assistant_id: str
    thread_id: str
    run_id: str
    type: RunStepsType
    status: RunStepsStatus
    step_details: Union["MessageCreation", "ToolCalls"]
    last_error: Union["RunStepsLastErrorType0", None]
    expired_at: Union[None, int]
    cancelled_at: Union[None, int]
    failed_at: Union[None, int]
    completed_at: Union[None, int]
    metadata: Union["RunStepsMetadataType0", None]
    usage: Union["RunStepCompletionUsageType0", None]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.message_creation import MessageCreation
        from ..models.run_step_completion_usage_type_0 import RunStepCompletionUsageType0
        from ..models.run_steps_last_error_type_0 import RunStepsLastErrorType0
        from ..models.run_steps_metadata_type_0 import RunStepsMetadataType0

        id = self.id

        object_ = self.object_.value

        created_at = self.created_at

        assistant_id = self.assistant_id

        thread_id = self.thread_id

        run_id = self.run_id

        type = self.type.value

        status = self.status.value

        step_details: Dict[str, Any]
        if isinstance(self.step_details, MessageCreation):
            step_details = self.step_details.to_dict()
        else:
            step_details = self.step_details.to_dict()

        last_error: Union[Dict[str, Any], None]
        if isinstance(self.last_error, RunStepsLastErrorType0):
            last_error = self.last_error.to_dict()
        else:
            last_error = self.last_error

        expired_at: Union[None, int]
        expired_at = self.expired_at

        cancelled_at: Union[None, int]
        cancelled_at = self.cancelled_at

        failed_at: Union[None, int]
        failed_at = self.failed_at

        completed_at: Union[None, int]
        completed_at = self.completed_at

        metadata: Union[Dict[str, Any], None]
        if isinstance(self.metadata, RunStepsMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        usage: Union[Dict[str, Any], None]
        if isinstance(self.usage, RunStepCompletionUsageType0):
            usage = self.usage.to_dict()
        else:
            usage = self.usage

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "object": object_,
                "created_at": created_at,
                "assistant_id": assistant_id,
                "thread_id": thread_id,
                "run_id": run_id,
                "type": type,
                "status": status,
                "step_details": step_details,
                "last_error": last_error,
                "expired_at": expired_at,
                "cancelled_at": cancelled_at,
                "failed_at": failed_at,
                "completed_at": completed_at,
                "metadata": metadata,
                "usage": usage,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.message_creation import MessageCreation
        from ..models.run_step_completion_usage_type_0 import RunStepCompletionUsageType0
        from ..models.run_steps_last_error_type_0 import RunStepsLastErrorType0
        from ..models.run_steps_metadata_type_0 import RunStepsMetadataType0
        from ..models.tool_calls import ToolCalls

        d = src_dict.copy()
        id = d.pop("id")

        object_ = RunStepsObject(d.pop("object"))

        created_at = d.pop("created_at")

        assistant_id = d.pop("assistant_id")

        thread_id = d.pop("thread_id")

        run_id = d.pop("run_id")

        type = RunStepsType(d.pop("type"))

        status = RunStepsStatus(d.pop("status"))

        def _parse_step_details(data: object) -> Union["MessageCreation", "ToolCalls"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                step_details_type_0 = MessageCreation.from_dict(data)

                return step_details_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            step_details_type_1 = ToolCalls.from_dict(data)

            return step_details_type_1

        step_details = _parse_step_details(d.pop("step_details"))

        def _parse_last_error(data: object) -> Union["RunStepsLastErrorType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                last_error_type_0 = RunStepsLastErrorType0.from_dict(data)

                return last_error_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RunStepsLastErrorType0", None], data)

        last_error = _parse_last_error(d.pop("last_error"))

        def _parse_expired_at(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        expired_at = _parse_expired_at(d.pop("expired_at"))

        def _parse_cancelled_at(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        cancelled_at = _parse_cancelled_at(d.pop("cancelled_at"))

        def _parse_failed_at(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        failed_at = _parse_failed_at(d.pop("failed_at"))

        def _parse_completed_at(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        completed_at = _parse_completed_at(d.pop("completed_at"))

        def _parse_metadata(data: object) -> Union["RunStepsMetadataType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = RunStepsMetadataType0.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RunStepsMetadataType0", None], data)

        metadata = _parse_metadata(d.pop("metadata"))

        def _parse_usage(data: object) -> Union["RunStepCompletionUsageType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_run_step_completion_usage_type_0 = RunStepCompletionUsageType0.from_dict(data)

                return componentsschemas_run_step_completion_usage_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RunStepCompletionUsageType0", None], data)

        usage = _parse_usage(d.pop("usage"))

        run_steps = cls(
            id=id,
            object_=object_,
            created_at=created_at,
            assistant_id=assistant_id,
            thread_id=thread_id,
            run_id=run_id,
            type=type,
            status=status,
            step_details=step_details,
            last_error=last_error,
            expired_at=expired_at,
            cancelled_at=cancelled_at,
            failed_at=failed_at,
            completed_at=completed_at,
            metadata=metadata,
            usage=usage,
        )

        run_steps.additional_properties = d
        return run_steps

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

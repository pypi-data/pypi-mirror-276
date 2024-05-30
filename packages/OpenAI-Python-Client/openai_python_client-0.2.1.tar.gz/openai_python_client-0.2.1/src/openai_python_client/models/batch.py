from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.batch_object import BatchObject
from ..models.batch_status import BatchStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.batch_errors import BatchErrors
    from ..models.batch_metadata_type_0 import BatchMetadataType0
    from ..models.batch_request_counts import BatchRequestCounts


T = TypeVar("T", bound="Batch")


@_attrs_define
class Batch:
    """
    Attributes:
        id (str):
        object_ (BatchObject): The object type, which is always `batch`.
        endpoint (str): The OpenAI API endpoint used by the batch.
        input_file_id (str): The ID of the input file for the batch.
        completion_window (str): The time frame within which the batch should be processed.
        status (BatchStatus): The current status of the batch.
        created_at (int): The Unix timestamp (in seconds) for when the batch was created.
        errors (Union[Unset, BatchErrors]):
        output_file_id (Union[Unset, str]): The ID of the file containing the outputs of successfully executed requests.
        error_file_id (Union[Unset, str]): The ID of the file containing the outputs of requests with errors.
        in_progress_at (Union[Unset, int]): The Unix timestamp (in seconds) for when the batch started processing.
        expires_at (Union[Unset, int]): The Unix timestamp (in seconds) for when the batch will expire.
        finalizing_at (Union[Unset, int]): The Unix timestamp (in seconds) for when the batch started finalizing.
        completed_at (Union[Unset, int]): The Unix timestamp (in seconds) for when the batch was completed.
        failed_at (Union[Unset, int]): The Unix timestamp (in seconds) for when the batch failed.
        expired_at (Union[Unset, int]): The Unix timestamp (in seconds) for when the batch expired.
        cancelling_at (Union[Unset, int]): The Unix timestamp (in seconds) for when the batch started cancelling.
        cancelled_at (Union[Unset, int]): The Unix timestamp (in seconds) for when the batch was cancelled.
        request_counts (Union[Unset, BatchRequestCounts]): The request counts for different statuses within the batch.
        metadata (Union['BatchMetadataType0', None, Unset]): Set of 16 key-value pairs that can be attached to an
            object. This can be useful for storing additional information about the object in a structured format. Keys can
            be a maximum of 64 characters long and values can be a maxium of 512 characters long.
    """

    id: str
    object_: BatchObject
    endpoint: str
    input_file_id: str
    completion_window: str
    status: BatchStatus
    created_at: int
    errors: Union[Unset, "BatchErrors"] = UNSET
    output_file_id: Union[Unset, str] = UNSET
    error_file_id: Union[Unset, str] = UNSET
    in_progress_at: Union[Unset, int] = UNSET
    expires_at: Union[Unset, int] = UNSET
    finalizing_at: Union[Unset, int] = UNSET
    completed_at: Union[Unset, int] = UNSET
    failed_at: Union[Unset, int] = UNSET
    expired_at: Union[Unset, int] = UNSET
    cancelling_at: Union[Unset, int] = UNSET
    cancelled_at: Union[Unset, int] = UNSET
    request_counts: Union[Unset, "BatchRequestCounts"] = UNSET
    metadata: Union["BatchMetadataType0", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.batch_metadata_type_0 import BatchMetadataType0

        id = self.id

        object_ = self.object_.value

        endpoint = self.endpoint

        input_file_id = self.input_file_id

        completion_window = self.completion_window

        status = self.status.value

        created_at = self.created_at

        errors: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = self.errors.to_dict()

        output_file_id = self.output_file_id

        error_file_id = self.error_file_id

        in_progress_at = self.in_progress_at

        expires_at = self.expires_at

        finalizing_at = self.finalizing_at

        completed_at = self.completed_at

        failed_at = self.failed_at

        expired_at = self.expired_at

        cancelling_at = self.cancelling_at

        cancelled_at = self.cancelled_at

        request_counts: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.request_counts, Unset):
            request_counts = self.request_counts.to_dict()

        metadata: Union[Dict[str, Any], None, Unset]
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, BatchMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "object": object_,
                "endpoint": endpoint,
                "input_file_id": input_file_id,
                "completion_window": completion_window,
                "status": status,
                "created_at": created_at,
            }
        )
        if errors is not UNSET:
            field_dict["errors"] = errors
        if output_file_id is not UNSET:
            field_dict["output_file_id"] = output_file_id
        if error_file_id is not UNSET:
            field_dict["error_file_id"] = error_file_id
        if in_progress_at is not UNSET:
            field_dict["in_progress_at"] = in_progress_at
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if finalizing_at is not UNSET:
            field_dict["finalizing_at"] = finalizing_at
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if failed_at is not UNSET:
            field_dict["failed_at"] = failed_at
        if expired_at is not UNSET:
            field_dict["expired_at"] = expired_at
        if cancelling_at is not UNSET:
            field_dict["cancelling_at"] = cancelling_at
        if cancelled_at is not UNSET:
            field_dict["cancelled_at"] = cancelled_at
        if request_counts is not UNSET:
            field_dict["request_counts"] = request_counts
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.batch_errors import BatchErrors
        from ..models.batch_metadata_type_0 import BatchMetadataType0
        from ..models.batch_request_counts import BatchRequestCounts

        d = src_dict.copy()
        id = d.pop("id")

        object_ = BatchObject(d.pop("object"))

        endpoint = d.pop("endpoint")

        input_file_id = d.pop("input_file_id")

        completion_window = d.pop("completion_window")

        status = BatchStatus(d.pop("status"))

        created_at = d.pop("created_at")

        _errors = d.pop("errors", UNSET)
        errors: Union[Unset, BatchErrors]
        if isinstance(_errors, Unset):
            errors = UNSET
        else:
            errors = BatchErrors.from_dict(_errors)

        output_file_id = d.pop("output_file_id", UNSET)

        error_file_id = d.pop("error_file_id", UNSET)

        in_progress_at = d.pop("in_progress_at", UNSET)

        expires_at = d.pop("expires_at", UNSET)

        finalizing_at = d.pop("finalizing_at", UNSET)

        completed_at = d.pop("completed_at", UNSET)

        failed_at = d.pop("failed_at", UNSET)

        expired_at = d.pop("expired_at", UNSET)

        cancelling_at = d.pop("cancelling_at", UNSET)

        cancelled_at = d.pop("cancelled_at", UNSET)

        _request_counts = d.pop("request_counts", UNSET)
        request_counts: Union[Unset, BatchRequestCounts]
        if isinstance(_request_counts, Unset):
            request_counts = UNSET
        else:
            request_counts = BatchRequestCounts.from_dict(_request_counts)

        def _parse_metadata(data: object) -> Union["BatchMetadataType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = BatchMetadataType0.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BatchMetadataType0", None, Unset], data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        batch = cls(
            id=id,
            object_=object_,
            endpoint=endpoint,
            input_file_id=input_file_id,
            completion_window=completion_window,
            status=status,
            created_at=created_at,
            errors=errors,
            output_file_id=output_file_id,
            error_file_id=error_file_id,
            in_progress_at=in_progress_at,
            expires_at=expires_at,
            finalizing_at=finalizing_at,
            completed_at=completed_at,
            failed_at=failed_at,
            expired_at=expired_at,
            cancelling_at=cancelling_at,
            cancelled_at=cancelled_at,
            request_counts=request_counts,
            metadata=metadata,
        )

        batch.additional_properties = d
        return batch

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

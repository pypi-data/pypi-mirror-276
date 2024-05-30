from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_batch_body_completion_window import CreateBatchBodyCompletionWindow
from ..models.create_batch_body_endpoint import CreateBatchBodyEndpoint
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_batch_body_metadata_type_0 import CreateBatchBodyMetadataType0


T = TypeVar("T", bound="CreateBatchBody")


@_attrs_define
class CreateBatchBody:
    """
    Attributes:
        input_file_id (str): The ID of an uploaded file that contains requests for the new batch.

            See [upload file](/docs/api-reference/files/create) for how to upload a file.

            Your input file must be formatted as a [JSONL file](/docs/api-reference/batch/requestInput), and must be
            uploaded with the purpose `batch`.
        endpoint (CreateBatchBodyEndpoint): The endpoint to be used for all requests in the batch. Currently
            `/v1/chat/completions` and `/v1/embeddings` are supported.
        completion_window (CreateBatchBodyCompletionWindow): The time frame within which the batch should be processed.
            Currently only `24h` is supported.
        metadata (Union['CreateBatchBodyMetadataType0', None, Unset]): Optional custom metadata for the batch.
    """

    input_file_id: str
    endpoint: CreateBatchBodyEndpoint
    completion_window: CreateBatchBodyCompletionWindow
    metadata: Union["CreateBatchBodyMetadataType0", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.create_batch_body_metadata_type_0 import CreateBatchBodyMetadataType0

        input_file_id = self.input_file_id

        endpoint = self.endpoint.value

        completion_window = self.completion_window.value

        metadata: Union[Dict[str, Any], None, Unset]
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, CreateBatchBodyMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "input_file_id": input_file_id,
                "endpoint": endpoint,
                "completion_window": completion_window,
            }
        )
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_batch_body_metadata_type_0 import CreateBatchBodyMetadataType0

        d = src_dict.copy()
        input_file_id = d.pop("input_file_id")

        endpoint = CreateBatchBodyEndpoint(d.pop("endpoint"))

        completion_window = CreateBatchBodyCompletionWindow(d.pop("completion_window"))

        def _parse_metadata(data: object) -> Union["CreateBatchBodyMetadataType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = CreateBatchBodyMetadataType0.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CreateBatchBodyMetadataType0", None, Unset], data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        create_batch_body = cls(
            input_file_id=input_file_id,
            endpoint=endpoint,
            completion_window=completion_window,
            metadata=metadata,
        )

        create_batch_body.additional_properties = d
        return create_batch_body

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

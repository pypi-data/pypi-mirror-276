from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.batch_request_input_method import BatchRequestInputMethod
from ..types import UNSET, Unset

T = TypeVar("T", bound="BatchRequestInput")


@_attrs_define
class BatchRequestInput:
    """The per-line object of the batch input file

    Attributes:
        custom_id (Union[Unset, str]): A developer-provided per-request id that will be used to match outputs to inputs.
            Must be unique for each request in a batch.
        method (Union[Unset, BatchRequestInputMethod]): The HTTP method to be used for the request. Currently only
            `POST` is supported.
        url (Union[Unset, str]): The OpenAI API relative URL to be used for the request. Currently
            `/v1/chat/completions` and `/v1/embeddings` are supported.
    """

    custom_id: Union[Unset, str] = UNSET
    method: Union[Unset, BatchRequestInputMethod] = UNSET
    url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        custom_id = self.custom_id

        method: Union[Unset, str] = UNSET
        if not isinstance(self.method, Unset):
            method = self.method.value

        url = self.url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if custom_id is not UNSET:
            field_dict["custom_id"] = custom_id
        if method is not UNSET:
            field_dict["method"] = method
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        custom_id = d.pop("custom_id", UNSET)

        _method = d.pop("method", UNSET)
        method: Union[Unset, BatchRequestInputMethod]
        if isinstance(_method, Unset):
            method = UNSET
        else:
            method = BatchRequestInputMethod(_method)

        url = d.pop("url", UNSET)

        batch_request_input = cls(
            custom_id=custom_id,
            method=method,
            url=url,
        )

        batch_request_input.additional_properties = d
        return batch_request_input

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

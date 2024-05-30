from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.batch_request_output_response_type_0_body import BatchRequestOutputResponseType0Body


T = TypeVar("T", bound="BatchRequestOutputResponseType0")


@_attrs_define
class BatchRequestOutputResponseType0:
    """
    Attributes:
        status_code (Union[Unset, int]): The HTTP status code of the response
        request_id (Union[Unset, str]): An unique identifier for the OpenAI API request. Please include this request ID
            when contacting support.
        body (Union[Unset, BatchRequestOutputResponseType0Body]): The JSON body of the response
    """

    status_code: Union[Unset, int] = UNSET
    request_id: Union[Unset, str] = UNSET
    body: Union[Unset, "BatchRequestOutputResponseType0Body"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status_code = self.status_code

        request_id = self.request_id

        body: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.body, Unset):
            body = self.body.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if request_id is not UNSET:
            field_dict["request_id"] = request_id
        if body is not UNSET:
            field_dict["body"] = body

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.batch_request_output_response_type_0_body import BatchRequestOutputResponseType0Body

        d = src_dict.copy()
        status_code = d.pop("status_code", UNSET)

        request_id = d.pop("request_id", UNSET)

        _body = d.pop("body", UNSET)
        body: Union[Unset, BatchRequestOutputResponseType0Body]
        if isinstance(_body, Unset):
            body = UNSET
        else:
            body = BatchRequestOutputResponseType0Body.from_dict(_body)

        batch_request_output_response_type_0 = cls(
            status_code=status_code,
            request_id=request_id,
            body=body,
        )

        batch_request_output_response_type_0.additional_properties = d
        return batch_request_output_response_type_0

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

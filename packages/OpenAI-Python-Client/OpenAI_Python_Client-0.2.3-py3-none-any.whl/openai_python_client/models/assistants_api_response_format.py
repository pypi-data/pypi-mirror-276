from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.assistants_api_response_format_type import AssistantsApiResponseFormatType
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssistantsApiResponseFormat")


@_attrs_define
class AssistantsApiResponseFormat:
    """An object describing the expected output of the model. If `json_object` only `function` type `tools` are allowed to
    be passed to the Run. If `text` the model can return text or any value needed.

        Attributes:
            type (Union[Unset, AssistantsApiResponseFormatType]): Must be one of `text` or `json_object`. Default:
                AssistantsApiResponseFormatType.TEXT. Example: json_object.
    """

    type: Union[Unset, AssistantsApiResponseFormatType] = AssistantsApiResponseFormatType.TEXT
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _type = d.pop("type", UNSET)
        type: Union[Unset, AssistantsApiResponseFormatType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = AssistantsApiResponseFormatType(_type)

        assistants_api_response_format = cls(
            type=type,
        )

        assistants_api_response_format.additional_properties = d
        return assistants_api_response_format

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

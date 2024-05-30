from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BatchErrorsDataItem")


@_attrs_define
class BatchErrorsDataItem:
    """
    Attributes:
        code (Union[Unset, str]): An error code identifying the error type.
        message (Union[Unset, str]): A human-readable message providing more details about the error.
        param (Union[None, Unset, str]): The name of the parameter that caused the error, if applicable.
        line (Union[None, Unset, int]): The line number of the input file where the error occurred, if applicable.
    """

    code: Union[Unset, str] = UNSET
    message: Union[Unset, str] = UNSET
    param: Union[None, Unset, str] = UNSET
    line: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code = self.code

        message = self.message

        param: Union[None, Unset, str]
        if isinstance(self.param, Unset):
            param = UNSET
        else:
            param = self.param

        line: Union[None, Unset, int]
        if isinstance(self.line, Unset):
            line = UNSET
        else:
            line = self.line

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if code is not UNSET:
            field_dict["code"] = code
        if message is not UNSET:
            field_dict["message"] = message
        if param is not UNSET:
            field_dict["param"] = param
        if line is not UNSET:
            field_dict["line"] = line

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        code = d.pop("code", UNSET)

        message = d.pop("message", UNSET)

        def _parse_param(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        param = _parse_param(d.pop("param", UNSET))

        def _parse_line(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        line = _parse_line(d.pop("line", UNSET))

        batch_errors_data_item = cls(
            code=code,
            message=message,
            param=param,
            line=line,
        )

        batch_errors_data_item.additional_properties = d
        return batch_errors_data_item

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

from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.a_run_on_a_thread_last_error_type_0_code import ARunOnAThreadLastErrorType0Code

T = TypeVar("T", bound="ARunOnAThreadLastErrorType0")


@_attrs_define
class ARunOnAThreadLastErrorType0:
    """The last error associated with this run. Will be `null` if there are no errors.

    Attributes:
        code (ARunOnAThreadLastErrorType0Code): One of `server_error`, `rate_limit_exceeded`, or `invalid_prompt`.
        message (str): A human-readable description of the error.
    """

    code: ARunOnAThreadLastErrorType0Code
    message: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code = self.code.value

        message = self.message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        code = ARunOnAThreadLastErrorType0Code(d.pop("code"))

        message = d.pop("message")

        a_run_on_a_thread_last_error_type_0 = cls(
            code=code,
            message=message,
        )

        a_run_on_a_thread_last_error_type_0.additional_properties = d
        return a_run_on_a_thread_last_error_type_0

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

from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FineTuningJobErrorType0")


@_attrs_define
class FineTuningJobErrorType0:
    """For fine-tuning jobs that have `failed`, this will contain more information on the cause of the failure.

    Attributes:
        code (str): A machine-readable error code.
        message (str): A human-readable error message.
        param (Union[None, str]): The parameter that was invalid, usually `training_file` or `validation_file`. This
            field will be null if the failure was not parameter-specific.
    """

    code: str
    message: str
    param: Union[None, str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code = self.code

        message = self.message

        param: Union[None, str]
        param = self.param

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
                "param": param,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        code = d.pop("code")

        message = d.pop("message")

        def _parse_param(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        param = _parse_param(d.pop("param"))

        fine_tuning_job_error_type_0 = cls(
            code=code,
            message=message,
            param=param,
        )

        fine_tuning_job_error_type_0.additional_properties = d
        return fine_tuning_job_error_type_0

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

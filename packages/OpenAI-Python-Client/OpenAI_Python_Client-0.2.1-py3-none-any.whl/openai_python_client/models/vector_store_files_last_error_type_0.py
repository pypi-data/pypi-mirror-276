from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.vector_store_files_last_error_type_0_code import VectorStoreFilesLastErrorType0Code

T = TypeVar("T", bound="VectorStoreFilesLastErrorType0")


@_attrs_define
class VectorStoreFilesLastErrorType0:
    """The last error associated with this vector store file. Will be `null` if there are no errors.

    Attributes:
        code (VectorStoreFilesLastErrorType0Code): One of `server_error` or `rate_limit_exceeded`.
        message (str): A human-readable description of the error.
    """

    code: VectorStoreFilesLastErrorType0Code
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
        code = VectorStoreFilesLastErrorType0Code(d.pop("code"))

        message = d.pop("message")

        vector_store_files_last_error_type_0 = cls(
            code=code,
            message=message,
        )

        vector_store_files_last_error_type_0.additional_properties = d
        return vector_store_files_last_error_type_0

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

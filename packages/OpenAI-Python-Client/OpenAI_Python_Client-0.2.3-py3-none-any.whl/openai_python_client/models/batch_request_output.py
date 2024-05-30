from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.batch_request_output_error_type_0 import BatchRequestOutputErrorType0
    from ..models.batch_request_output_response_type_0 import BatchRequestOutputResponseType0


T = TypeVar("T", bound="BatchRequestOutput")


@_attrs_define
class BatchRequestOutput:
    """The per-line object of the batch output and error files

    Attributes:
        id (Union[Unset, str]):
        custom_id (Union[Unset, str]): A developer-provided per-request id that will be used to match outputs to inputs.
        response (Union['BatchRequestOutputResponseType0', None, Unset]):
        error (Union['BatchRequestOutputErrorType0', None, Unset]): For requests that failed with a non-HTTP error, this
            will contain more information on the cause of the failure.
    """

    id: Union[Unset, str] = UNSET
    custom_id: Union[Unset, str] = UNSET
    response: Union["BatchRequestOutputResponseType0", None, Unset] = UNSET
    error: Union["BatchRequestOutputErrorType0", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.batch_request_output_error_type_0 import BatchRequestOutputErrorType0
        from ..models.batch_request_output_response_type_0 import BatchRequestOutputResponseType0

        id = self.id

        custom_id = self.custom_id

        response: Union[Dict[str, Any], None, Unset]
        if isinstance(self.response, Unset):
            response = UNSET
        elif isinstance(self.response, BatchRequestOutputResponseType0):
            response = self.response.to_dict()
        else:
            response = self.response

        error: Union[Dict[str, Any], None, Unset]
        if isinstance(self.error, Unset):
            error = UNSET
        elif isinstance(self.error, BatchRequestOutputErrorType0):
            error = self.error.to_dict()
        else:
            error = self.error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if custom_id is not UNSET:
            field_dict["custom_id"] = custom_id
        if response is not UNSET:
            field_dict["response"] = response
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.batch_request_output_error_type_0 import BatchRequestOutputErrorType0
        from ..models.batch_request_output_response_type_0 import BatchRequestOutputResponseType0

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        custom_id = d.pop("custom_id", UNSET)

        def _parse_response(data: object) -> Union["BatchRequestOutputResponseType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_type_0 = BatchRequestOutputResponseType0.from_dict(data)

                return response_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BatchRequestOutputResponseType0", None, Unset], data)

        response = _parse_response(d.pop("response", UNSET))

        def _parse_error(data: object) -> Union["BatchRequestOutputErrorType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                error_type_0 = BatchRequestOutputErrorType0.from_dict(data)

                return error_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BatchRequestOutputErrorType0", None, Unset], data)

        error = _parse_error(d.pop("error", UNSET))

        batch_request_output = cls(
            id=id,
            custom_id=custom_id,
            response=response,
            error=error,
        )

        batch_request_output.additional_properties = d
        return batch_request_output

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

from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_moderation_request_model_type_1 import CreateModerationRequestModelType1
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateModerationRequest")


@_attrs_define
class CreateModerationRequest:
    """
    Attributes:
        input_ (Union[List[str], str]): The input text to classify
        model (Union[CreateModerationRequestModelType1, Unset, str]): Two content moderations models are available:
            `text-moderation-stable` and `text-moderation-latest`.

            The default is `text-moderation-latest` which will be automatically upgraded over time. This ensures you are
            always using our most accurate model. If you use `text-moderation-stable`, we will provide advanced notice
            before updating the model. Accuracy of `text-moderation-stable` may be slightly lower than for `text-moderation-
            latest`.
             Default: 'text-moderation-latest'. Example: text-moderation-stable.
    """

    input_: Union[List[str], str]
    model: Union[CreateModerationRequestModelType1, Unset, str] = "text-moderation-latest"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        input_: Union[List[str], str]
        if isinstance(self.input_, list):
            input_ = self.input_

        else:
            input_ = self.input_

        model: Union[Unset, str]
        if isinstance(self.model, Unset):
            model = UNSET
        elif isinstance(self.model, CreateModerationRequestModelType1):
            model = self.model.value
        else:
            model = self.model

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "input": input_,
            }
        )
        if model is not UNSET:
            field_dict["model"] = model

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_input_(data: object) -> Union[List[str], str]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                input_type_1 = cast(List[str], data)

                return input_type_1
            except:  # noqa: E722
                pass
            return cast(Union[List[str], str], data)

        input_ = _parse_input_(d.pop("input"))

        def _parse_model(data: object) -> Union[CreateModerationRequestModelType1, Unset, str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                model_type_1 = CreateModerationRequestModelType1(data)

                return model_type_1
            except:  # noqa: E722
                pass
            return cast(Union[CreateModerationRequestModelType1, Unset, str], data)

        model = _parse_model(d.pop("model", UNSET))

        create_moderation_request = cls(
            input_=input_,
            model=model,
        )

        create_moderation_request.additional_properties = d
        return create_moderation_request

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

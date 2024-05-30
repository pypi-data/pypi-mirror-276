from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_completion_response_object import CreateCompletionResponseObject
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.completion_usage import CompletionUsage
    from ..models.create_completion_response_choices_item import CreateCompletionResponseChoicesItem


T = TypeVar("T", bound="CreateCompletionResponse")


@_attrs_define
class CreateCompletionResponse:
    """Represents a completion response from the API. Note: both the streamed and non-streamed response objects share the
    same shape (unlike the chat endpoint).

        Attributes:
            id (str): A unique identifier for the completion.
            choices (List['CreateCompletionResponseChoicesItem']): The list of completion choices the model generated for
                the input prompt.
            created (int): The Unix timestamp (in seconds) of when the completion was created.
            model (str): The model used for completion.
            object_ (CreateCompletionResponseObject): The object type, which is always "text_completion"
            system_fingerprint (Union[Unset, str]): This fingerprint represents the backend configuration that the model
                runs with.

                Can be used in conjunction with the `seed` request parameter to understand when backend changes have been made
                that might impact determinism.
            usage (Union[Unset, CompletionUsage]): Usage statistics for the completion request.
    """

    id: str
    choices: List["CreateCompletionResponseChoicesItem"]
    created: int
    model: str
    object_: CreateCompletionResponseObject
    system_fingerprint: Union[Unset, str] = UNSET
    usage: Union[Unset, "CompletionUsage"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        choices = []
        for choices_item_data in self.choices:
            choices_item = choices_item_data.to_dict()
            choices.append(choices_item)

        created = self.created

        model = self.model

        object_ = self.object_.value

        system_fingerprint = self.system_fingerprint

        usage: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.usage, Unset):
            usage = self.usage.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "choices": choices,
                "created": created,
                "model": model,
                "object": object_,
            }
        )
        if system_fingerprint is not UNSET:
            field_dict["system_fingerprint"] = system_fingerprint
        if usage is not UNSET:
            field_dict["usage"] = usage

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.completion_usage import CompletionUsage
        from ..models.create_completion_response_choices_item import CreateCompletionResponseChoicesItem

        d = src_dict.copy()
        id = d.pop("id")

        choices = []
        _choices = d.pop("choices")
        for choices_item_data in _choices:
            choices_item = CreateCompletionResponseChoicesItem.from_dict(choices_item_data)

            choices.append(choices_item)

        created = d.pop("created")

        model = d.pop("model")

        object_ = CreateCompletionResponseObject(d.pop("object"))

        system_fingerprint = d.pop("system_fingerprint", UNSET)

        _usage = d.pop("usage", UNSET)
        usage: Union[Unset, CompletionUsage]
        if isinstance(_usage, Unset):
            usage = UNSET
        else:
            usage = CompletionUsage.from_dict(_usage)

        create_completion_response = cls(
            id=id,
            choices=choices,
            created=created,
            model=model,
            object_=object_,
            system_fingerprint=system_fingerprint,
            usage=usage,
        )

        create_completion_response.additional_properties = d
        return create_completion_response

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

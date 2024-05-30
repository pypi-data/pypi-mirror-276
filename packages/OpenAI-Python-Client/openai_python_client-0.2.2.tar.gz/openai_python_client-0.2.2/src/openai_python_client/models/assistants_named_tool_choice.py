from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.assistants_named_tool_choice_type import AssistantsNamedToolChoiceType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.assistants_named_tool_choice_function import AssistantsNamedToolChoiceFunction


T = TypeVar("T", bound="AssistantsNamedToolChoice")


@_attrs_define
class AssistantsNamedToolChoice:
    """Specifies a tool the model should use. Use to force the model to call a specific tool.

    Attributes:
        type (AssistantsNamedToolChoiceType): The type of the tool. If type is `function`, the function name must be set
        function (Union[Unset, AssistantsNamedToolChoiceFunction]):
    """

    type: AssistantsNamedToolChoiceType
    function: Union[Unset, "AssistantsNamedToolChoiceFunction"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        function: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.function, Unset):
            function = self.function.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )
        if function is not UNSET:
            field_dict["function"] = function

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.assistants_named_tool_choice_function import AssistantsNamedToolChoiceFunction

        d = src_dict.copy()
        type = AssistantsNamedToolChoiceType(d.pop("type"))

        _function = d.pop("function", UNSET)
        function: Union[Unset, AssistantsNamedToolChoiceFunction]
        if isinstance(_function, Unset):
            function = UNSET
        else:
            function = AssistantsNamedToolChoiceFunction.from_dict(_function)

        assistants_named_tool_choice = cls(
            type=type,
            function=function,
        )

        assistants_named_tool_choice.additional_properties = d
        return assistants_named_tool_choice

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

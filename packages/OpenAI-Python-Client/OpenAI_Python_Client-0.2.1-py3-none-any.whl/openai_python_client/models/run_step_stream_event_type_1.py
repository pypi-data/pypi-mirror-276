from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.run_step_stream_event_type_1_event import RunStepStreamEventType1Event

if TYPE_CHECKING:
    from ..models.run_steps import RunSteps


T = TypeVar("T", bound="RunStepStreamEventType1")


@_attrs_define
class RunStepStreamEventType1:
    """Occurs when a [run step](/docs/api-reference/runs/step-object) moves to an `in_progress` state.

    Attributes:
        event (RunStepStreamEventType1Event):
        data (RunSteps): Represents a step in execution of a run.
    """

    event: RunStepStreamEventType1Event
    data: "RunSteps"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        event = self.event.value

        data = self.data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "event": event,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.run_steps import RunSteps

        d = src_dict.copy()
        event = RunStepStreamEventType1Event(d.pop("event"))

        data = RunSteps.from_dict(d.pop("data"))

        run_step_stream_event_type_1 = cls(
            event=event,
            data=data,
        )

        run_step_stream_event_type_1.additional_properties = d
        return run_step_stream_event_type_1

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

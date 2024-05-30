from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.run_step_stream_event_type_5_event import RunStepStreamEventType5Event

if TYPE_CHECKING:
    from ..models.run_steps import RunSteps


T = TypeVar("T", bound="RunStepStreamEventType5")


@_attrs_define
class RunStepStreamEventType5:
    """Occurs when a [run step](/docs/api-reference/runs/step-object) is cancelled.

    Attributes:
        event (RunStepStreamEventType5Event):
        data (RunSteps): Represents a step in execution of a run.
    """

    event: RunStepStreamEventType5Event
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
        event = RunStepStreamEventType5Event(d.pop("event"))

        data = RunSteps.from_dict(d.pop("data"))

        run_step_stream_event_type_5 = cls(
            event=event,
            data=data,
        )

        run_step_stream_event_type_5.additional_properties = d
        return run_step_stream_event_type_5

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

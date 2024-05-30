from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.fine_tuning_job_event_level import FineTuningJobEventLevel
from ..models.fine_tuning_job_event_object import FineTuningJobEventObject

T = TypeVar("T", bound="FineTuningJobEvent")


@_attrs_define
class FineTuningJobEvent:
    """Fine-tuning job event object

    Attributes:
        id (str):
        created_at (int):
        level (FineTuningJobEventLevel):
        message (str):
        object_ (FineTuningJobEventObject):
    """

    id: str
    created_at: int
    level: FineTuningJobEventLevel
    message: str
    object_: FineTuningJobEventObject
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        created_at = self.created_at

        level = self.level.value

        message = self.message

        object_ = self.object_.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "level": level,
                "message": message,
                "object": object_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        created_at = d.pop("created_at")

        level = FineTuningJobEventLevel(d.pop("level"))

        message = d.pop("message")

        object_ = FineTuningJobEventObject(d.pop("object"))

        fine_tuning_job_event = cls(
            id=id,
            created_at=created_at,
            level=level,
            message=message,
            object_=object_,
        )

        fine_tuning_job_event.additional_properties = d
        return fine_tuning_job_event

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

from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.fine_tuning_job_checkpoint_object import FineTuningJobCheckpointObject

if TYPE_CHECKING:
    from ..models.fine_tuning_job_checkpoint_metrics import FineTuningJobCheckpointMetrics


T = TypeVar("T", bound="FineTuningJobCheckpoint")


@_attrs_define
class FineTuningJobCheckpoint:
    """The `fine_tuning.job.checkpoint` object represents a model checkpoint for a fine-tuning job that is ready to use.

    Attributes:
        id (str): The checkpoint identifier, which can be referenced in the API endpoints.
        created_at (int): The Unix timestamp (in seconds) for when the checkpoint was created.
        fine_tuned_model_checkpoint (str): The name of the fine-tuned checkpoint model that is created.
        step_number (int): The step number that the checkpoint was created at.
        metrics (FineTuningJobCheckpointMetrics): Metrics at the step number during the fine-tuning job.
        fine_tuning_job_id (str): The name of the fine-tuning job that this checkpoint was created from.
        object_ (FineTuningJobCheckpointObject): The object type, which is always "fine_tuning.job.checkpoint".
    """

    id: str
    created_at: int
    fine_tuned_model_checkpoint: str
    step_number: int
    metrics: "FineTuningJobCheckpointMetrics"
    fine_tuning_job_id: str
    object_: FineTuningJobCheckpointObject
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        created_at = self.created_at

        fine_tuned_model_checkpoint = self.fine_tuned_model_checkpoint

        step_number = self.step_number

        metrics = self.metrics.to_dict()

        fine_tuning_job_id = self.fine_tuning_job_id

        object_ = self.object_.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "fine_tuned_model_checkpoint": fine_tuned_model_checkpoint,
                "step_number": step_number,
                "metrics": metrics,
                "fine_tuning_job_id": fine_tuning_job_id,
                "object": object_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.fine_tuning_job_checkpoint_metrics import FineTuningJobCheckpointMetrics

        d = src_dict.copy()
        id = d.pop("id")

        created_at = d.pop("created_at")

        fine_tuned_model_checkpoint = d.pop("fine_tuned_model_checkpoint")

        step_number = d.pop("step_number")

        metrics = FineTuningJobCheckpointMetrics.from_dict(d.pop("metrics"))

        fine_tuning_job_id = d.pop("fine_tuning_job_id")

        object_ = FineTuningJobCheckpointObject(d.pop("object"))

        fine_tuning_job_checkpoint = cls(
            id=id,
            created_at=created_at,
            fine_tuned_model_checkpoint=fine_tuned_model_checkpoint,
            step_number=step_number,
            metrics=metrics,
            fine_tuning_job_id=fine_tuning_job_id,
            object_=object_,
        )

        fine_tuning_job_checkpoint.additional_properties = d
        return fine_tuning_job_checkpoint

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

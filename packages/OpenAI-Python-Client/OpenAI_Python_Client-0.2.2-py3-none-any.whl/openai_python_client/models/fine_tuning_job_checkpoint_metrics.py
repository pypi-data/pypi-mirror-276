from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="FineTuningJobCheckpointMetrics")


@_attrs_define
class FineTuningJobCheckpointMetrics:
    """Metrics at the step number during the fine-tuning job.

    Attributes:
        step (Union[Unset, float]):
        train_loss (Union[Unset, float]):
        train_mean_token_accuracy (Union[Unset, float]):
        valid_loss (Union[Unset, float]):
        valid_mean_token_accuracy (Union[Unset, float]):
        full_valid_loss (Union[Unset, float]):
        full_valid_mean_token_accuracy (Union[Unset, float]):
    """

    step: Union[Unset, float] = UNSET
    train_loss: Union[Unset, float] = UNSET
    train_mean_token_accuracy: Union[Unset, float] = UNSET
    valid_loss: Union[Unset, float] = UNSET
    valid_mean_token_accuracy: Union[Unset, float] = UNSET
    full_valid_loss: Union[Unset, float] = UNSET
    full_valid_mean_token_accuracy: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        step = self.step

        train_loss = self.train_loss

        train_mean_token_accuracy = self.train_mean_token_accuracy

        valid_loss = self.valid_loss

        valid_mean_token_accuracy = self.valid_mean_token_accuracy

        full_valid_loss = self.full_valid_loss

        full_valid_mean_token_accuracy = self.full_valid_mean_token_accuracy

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if step is not UNSET:
            field_dict["step"] = step
        if train_loss is not UNSET:
            field_dict["train_loss"] = train_loss
        if train_mean_token_accuracy is not UNSET:
            field_dict["train_mean_token_accuracy"] = train_mean_token_accuracy
        if valid_loss is not UNSET:
            field_dict["valid_loss"] = valid_loss
        if valid_mean_token_accuracy is not UNSET:
            field_dict["valid_mean_token_accuracy"] = valid_mean_token_accuracy
        if full_valid_loss is not UNSET:
            field_dict["full_valid_loss"] = full_valid_loss
        if full_valid_mean_token_accuracy is not UNSET:
            field_dict["full_valid_mean_token_accuracy"] = full_valid_mean_token_accuracy

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        step = d.pop("step", UNSET)

        train_loss = d.pop("train_loss", UNSET)

        train_mean_token_accuracy = d.pop("train_mean_token_accuracy", UNSET)

        valid_loss = d.pop("valid_loss", UNSET)

        valid_mean_token_accuracy = d.pop("valid_mean_token_accuracy", UNSET)

        full_valid_loss = d.pop("full_valid_loss", UNSET)

        full_valid_mean_token_accuracy = d.pop("full_valid_mean_token_accuracy", UNSET)

        fine_tuning_job_checkpoint_metrics = cls(
            step=step,
            train_loss=train_loss,
            train_mean_token_accuracy=train_mean_token_accuracy,
            valid_loss=valid_loss,
            valid_mean_token_accuracy=valid_mean_token_accuracy,
            full_valid_loss=full_valid_loss,
            full_valid_mean_token_accuracy=full_valid_mean_token_accuracy,
        )

        fine_tuning_job_checkpoint_metrics.additional_properties = d
        return fine_tuning_job_checkpoint_metrics

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

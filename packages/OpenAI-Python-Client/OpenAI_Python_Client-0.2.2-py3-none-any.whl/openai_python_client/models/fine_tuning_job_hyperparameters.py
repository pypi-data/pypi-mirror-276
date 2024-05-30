from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.fine_tuning_job_hyperparameters_n_epochs_type_0 import FineTuningJobHyperparametersNEpochsType0

T = TypeVar("T", bound="FineTuningJobHyperparameters")


@_attrs_define
class FineTuningJobHyperparameters:
    """The hyperparameters used for the fine-tuning job. See the [fine-tuning guide](/docs/guides/fine-tuning) for more
    details.

        Attributes:
            n_epochs (Union[FineTuningJobHyperparametersNEpochsType0, int]): The number of epochs to train the model for. An
                epoch refers to one full cycle through the training dataset.
                "auto" decides the optimal number of epochs based on the size of the dataset. If setting the number manually, we
                support any number between 1 and 50 epochs. Default: FineTuningJobHyperparametersNEpochsType0.AUTO.
    """

    n_epochs: Union[FineTuningJobHyperparametersNEpochsType0, int] = FineTuningJobHyperparametersNEpochsType0.AUTO
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        n_epochs: Union[int, str]
        if isinstance(self.n_epochs, FineTuningJobHyperparametersNEpochsType0):
            n_epochs = self.n_epochs.value
        else:
            n_epochs = self.n_epochs

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "n_epochs": n_epochs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_n_epochs(data: object) -> Union[FineTuningJobHyperparametersNEpochsType0, int]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                n_epochs_type_0 = FineTuningJobHyperparametersNEpochsType0(data)

                return n_epochs_type_0
            except:  # noqa: E722
                pass
            return cast(Union[FineTuningJobHyperparametersNEpochsType0, int], data)

        n_epochs = _parse_n_epochs(d.pop("n_epochs"))

        fine_tuning_job_hyperparameters = cls(
            n_epochs=n_epochs,
        )

        fine_tuning_job_hyperparameters.additional_properties = d
        return fine_tuning_job_hyperparameters

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

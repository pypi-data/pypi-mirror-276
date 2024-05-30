from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_fine_tuning_job_request_hyperparameters_batch_size_type_0 import (
    CreateFineTuningJobRequestHyperparametersBatchSizeType0,
)
from ..models.create_fine_tuning_job_request_hyperparameters_learning_rate_multiplier_type_0 import (
    CreateFineTuningJobRequestHyperparametersLearningRateMultiplierType0,
)
from ..models.create_fine_tuning_job_request_hyperparameters_n_epochs_type_0 import (
    CreateFineTuningJobRequestHyperparametersNEpochsType0,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateFineTuningJobRequestHyperparameters")


@_attrs_define
class CreateFineTuningJobRequestHyperparameters:
    """The hyperparameters used for the fine-tuning job.

    Attributes:
        batch_size (Union[CreateFineTuningJobRequestHyperparametersBatchSizeType0, Unset, int]): Number of examples in
            each batch. A larger batch size means that model parameters
            are updated less frequently, but with lower variance.
             Default: CreateFineTuningJobRequestHyperparametersBatchSizeType0.AUTO.
        learning_rate_multiplier (Union[CreateFineTuningJobRequestHyperparametersLearningRateMultiplierType0, Unset,
            float]): Scaling factor for the learning rate. A smaller learning rate may be useful to avoid
            overfitting.
             Default: CreateFineTuningJobRequestHyperparametersLearningRateMultiplierType0.AUTO.
        n_epochs (Union[CreateFineTuningJobRequestHyperparametersNEpochsType0, Unset, int]): The number of epochs to
            train the model for. An epoch refers to one full cycle
            through the training dataset.
             Default: CreateFineTuningJobRequestHyperparametersNEpochsType0.AUTO.
    """

    batch_size: Union[CreateFineTuningJobRequestHyperparametersBatchSizeType0, Unset, int] = (
        CreateFineTuningJobRequestHyperparametersBatchSizeType0.AUTO
    )
    learning_rate_multiplier: Union[
        CreateFineTuningJobRequestHyperparametersLearningRateMultiplierType0, Unset, float
    ] = CreateFineTuningJobRequestHyperparametersLearningRateMultiplierType0.AUTO
    n_epochs: Union[CreateFineTuningJobRequestHyperparametersNEpochsType0, Unset, int] = (
        CreateFineTuningJobRequestHyperparametersNEpochsType0.AUTO
    )
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        batch_size: Union[Unset, int, str]
        if isinstance(self.batch_size, Unset):
            batch_size = UNSET
        elif isinstance(self.batch_size, CreateFineTuningJobRequestHyperparametersBatchSizeType0):
            batch_size = self.batch_size.value
        else:
            batch_size = self.batch_size

        learning_rate_multiplier: Union[Unset, float, str]
        if isinstance(self.learning_rate_multiplier, Unset):
            learning_rate_multiplier = UNSET
        elif isinstance(
            self.learning_rate_multiplier, CreateFineTuningJobRequestHyperparametersLearningRateMultiplierType0
        ):
            learning_rate_multiplier = self.learning_rate_multiplier.value
        else:
            learning_rate_multiplier = self.learning_rate_multiplier

        n_epochs: Union[Unset, int, str]
        if isinstance(self.n_epochs, Unset):
            n_epochs = UNSET
        elif isinstance(self.n_epochs, CreateFineTuningJobRequestHyperparametersNEpochsType0):
            n_epochs = self.n_epochs.value
        else:
            n_epochs = self.n_epochs

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if batch_size is not UNSET:
            field_dict["batch_size"] = batch_size
        if learning_rate_multiplier is not UNSET:
            field_dict["learning_rate_multiplier"] = learning_rate_multiplier
        if n_epochs is not UNSET:
            field_dict["n_epochs"] = n_epochs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_batch_size(
            data: object,
        ) -> Union[CreateFineTuningJobRequestHyperparametersBatchSizeType0, Unset, int]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                batch_size_type_0 = CreateFineTuningJobRequestHyperparametersBatchSizeType0(data)

                return batch_size_type_0
            except:  # noqa: E722
                pass
            return cast(Union[CreateFineTuningJobRequestHyperparametersBatchSizeType0, Unset, int], data)

        batch_size = _parse_batch_size(d.pop("batch_size", UNSET))

        def _parse_learning_rate_multiplier(
            data: object,
        ) -> Union[CreateFineTuningJobRequestHyperparametersLearningRateMultiplierType0, Unset, float]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                learning_rate_multiplier_type_0 = CreateFineTuningJobRequestHyperparametersLearningRateMultiplierType0(
                    data
                )

                return learning_rate_multiplier_type_0
            except:  # noqa: E722
                pass
            return cast(Union[CreateFineTuningJobRequestHyperparametersLearningRateMultiplierType0, Unset, float], data)

        learning_rate_multiplier = _parse_learning_rate_multiplier(d.pop("learning_rate_multiplier", UNSET))

        def _parse_n_epochs(data: object) -> Union[CreateFineTuningJobRequestHyperparametersNEpochsType0, Unset, int]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                n_epochs_type_0 = CreateFineTuningJobRequestHyperparametersNEpochsType0(data)

                return n_epochs_type_0
            except:  # noqa: E722
                pass
            return cast(Union[CreateFineTuningJobRequestHyperparametersNEpochsType0, Unset, int], data)

        n_epochs = _parse_n_epochs(d.pop("n_epochs", UNSET))

        create_fine_tuning_job_request_hyperparameters = cls(
            batch_size=batch_size,
            learning_rate_multiplier=learning_rate_multiplier,
            n_epochs=n_epochs,
        )

        create_fine_tuning_job_request_hyperparameters.additional_properties = d
        return create_fine_tuning_job_request_hyperparameters

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

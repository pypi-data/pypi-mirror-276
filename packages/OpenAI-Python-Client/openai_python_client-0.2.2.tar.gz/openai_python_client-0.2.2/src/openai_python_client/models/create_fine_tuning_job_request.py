from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_fine_tuning_job_request_model_type_1 import CreateFineTuningJobRequestModelType1
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_fine_tuning_job_request_hyperparameters import CreateFineTuningJobRequestHyperparameters
    from ..models.create_fine_tuning_job_request_integrations_type_0_item import (
        CreateFineTuningJobRequestIntegrationsType0Item,
    )


T = TypeVar("T", bound="CreateFineTuningJobRequest")


@_attrs_define
class CreateFineTuningJobRequest:
    """
    Attributes:
        model (Union[CreateFineTuningJobRequestModelType1, str]): The name of the model to fine-tune. You can select one
            of the
            [supported models](/docs/guides/fine-tuning/what-models-can-be-fine-tuned).
             Example: gpt-3.5-turbo.
        training_file (str): The ID of an uploaded file that contains training data.

            See [upload file](/docs/api-reference/files/create) for how to upload a file.

            Your dataset must be formatted as a JSONL file. Additionally, you must upload your file with the purpose `fine-
            tune`.

            See the [fine-tuning guide](/docs/guides/fine-tuning) for more details.
             Example: file-abc123.
        hyperparameters (Union[Unset, CreateFineTuningJobRequestHyperparameters]): The hyperparameters used for the
            fine-tuning job.
        suffix (Union[None, Unset, str]): A string of up to 18 characters that will be added to your fine-tuned model
            name.

            For example, a `suffix` of "custom-model-name" would produce a model name like `ft:gpt-3.5-turbo:openai:custom-
            model-name:7p4lURel`.
        validation_file (Union[None, Unset, str]): The ID of an uploaded file that contains validation data.

            If you provide this file, the data is used to generate validation
            metrics periodically during fine-tuning. These metrics can be viewed in
            the fine-tuning results file.
            The same data should not be present in both train and validation files.

            Your dataset must be formatted as a JSONL file. You must upload your file with the purpose `fine-tune`.

            See the [fine-tuning guide](/docs/guides/fine-tuning) for more details.
             Example: file-abc123.
        integrations (Union[List['CreateFineTuningJobRequestIntegrationsType0Item'], None, Unset]): A list of
            integrations to enable for your fine-tuning job.
        seed (Union[None, Unset, int]): The seed controls the reproducibility of the job. Passing in the same seed and
            job parameters should produce the same results, but may differ in rare cases.
            If a seed is not specified, one will be generated for you.
             Example: 42.
    """

    model: Union[CreateFineTuningJobRequestModelType1, str]
    training_file: str
    hyperparameters: Union[Unset, "CreateFineTuningJobRequestHyperparameters"] = UNSET
    suffix: Union[None, Unset, str] = UNSET
    validation_file: Union[None, Unset, str] = UNSET
    integrations: Union[List["CreateFineTuningJobRequestIntegrationsType0Item"], None, Unset] = UNSET
    seed: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        model: str
        if isinstance(self.model, CreateFineTuningJobRequestModelType1):
            model = self.model.value
        else:
            model = self.model

        training_file = self.training_file

        hyperparameters: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.hyperparameters, Unset):
            hyperparameters = self.hyperparameters.to_dict()

        suffix: Union[None, Unset, str]
        if isinstance(self.suffix, Unset):
            suffix = UNSET
        else:
            suffix = self.suffix

        validation_file: Union[None, Unset, str]
        if isinstance(self.validation_file, Unset):
            validation_file = UNSET
        else:
            validation_file = self.validation_file

        integrations: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.integrations, Unset):
            integrations = UNSET
        elif isinstance(self.integrations, list):
            integrations = []
            for integrations_type_0_item_data in self.integrations:
                integrations_type_0_item = integrations_type_0_item_data.to_dict()
                integrations.append(integrations_type_0_item)

        else:
            integrations = self.integrations

        seed: Union[None, Unset, int]
        if isinstance(self.seed, Unset):
            seed = UNSET
        else:
            seed = self.seed

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "model": model,
                "training_file": training_file,
            }
        )
        if hyperparameters is not UNSET:
            field_dict["hyperparameters"] = hyperparameters
        if suffix is not UNSET:
            field_dict["suffix"] = suffix
        if validation_file is not UNSET:
            field_dict["validation_file"] = validation_file
        if integrations is not UNSET:
            field_dict["integrations"] = integrations
        if seed is not UNSET:
            field_dict["seed"] = seed

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_fine_tuning_job_request_hyperparameters import CreateFineTuningJobRequestHyperparameters
        from ..models.create_fine_tuning_job_request_integrations_type_0_item import (
            CreateFineTuningJobRequestIntegrationsType0Item,
        )

        d = src_dict.copy()

        def _parse_model(data: object) -> Union[CreateFineTuningJobRequestModelType1, str]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                model_type_1 = CreateFineTuningJobRequestModelType1(data)

                return model_type_1
            except:  # noqa: E722
                pass
            return cast(Union[CreateFineTuningJobRequestModelType1, str], data)

        model = _parse_model(d.pop("model"))

        training_file = d.pop("training_file")

        _hyperparameters = d.pop("hyperparameters", UNSET)
        hyperparameters: Union[Unset, CreateFineTuningJobRequestHyperparameters]
        if isinstance(_hyperparameters, Unset):
            hyperparameters = UNSET
        else:
            hyperparameters = CreateFineTuningJobRequestHyperparameters.from_dict(_hyperparameters)

        def _parse_suffix(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        suffix = _parse_suffix(d.pop("suffix", UNSET))

        def _parse_validation_file(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        validation_file = _parse_validation_file(d.pop("validation_file", UNSET))

        def _parse_integrations(
            data: object,
        ) -> Union[List["CreateFineTuningJobRequestIntegrationsType0Item"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                integrations_type_0 = []
                _integrations_type_0 = data
                for integrations_type_0_item_data in _integrations_type_0:
                    integrations_type_0_item = CreateFineTuningJobRequestIntegrationsType0Item.from_dict(
                        integrations_type_0_item_data
                    )

                    integrations_type_0.append(integrations_type_0_item)

                return integrations_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["CreateFineTuningJobRequestIntegrationsType0Item"], None, Unset], data)

        integrations = _parse_integrations(d.pop("integrations", UNSET))

        def _parse_seed(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        seed = _parse_seed(d.pop("seed", UNSET))

        create_fine_tuning_job_request = cls(
            model=model,
            training_file=training_file,
            hyperparameters=hyperparameters,
            suffix=suffix,
            validation_file=validation_file,
            integrations=integrations,
            seed=seed,
        )

        create_fine_tuning_job_request.additional_properties = d
        return create_fine_tuning_job_request

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

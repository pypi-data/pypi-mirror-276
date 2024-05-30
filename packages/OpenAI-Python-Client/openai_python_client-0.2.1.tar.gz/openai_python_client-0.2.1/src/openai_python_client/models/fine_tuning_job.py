from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.fine_tuning_job_object import FineTuningJobObject
from ..models.fine_tuning_job_status import FineTuningJobStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fine_tuning_job_error_type_0 import FineTuningJobErrorType0
    from ..models.fine_tuning_job_hyperparameters import FineTuningJobHyperparameters
    from ..models.fine_tuning_job_integration import FineTuningJobIntegration


T = TypeVar("T", bound="FineTuningJob")


@_attrs_define
class FineTuningJob:
    """The `fine_tuning.job` object represents a fine-tuning job that has been created through the API.

    Attributes:
        id (str): The object identifier, which can be referenced in the API endpoints.
        created_at (int): The Unix timestamp (in seconds) for when the fine-tuning job was created.
        error (Union['FineTuningJobErrorType0', None]): For fine-tuning jobs that have `failed`, this will contain more
            information on the cause of the failure.
        fine_tuned_model (Union[None, str]): The name of the fine-tuned model that is being created. The value will be
            null if the fine-tuning job is still running.
        finished_at (Union[None, int]): The Unix timestamp (in seconds) for when the fine-tuning job was finished. The
            value will be null if the fine-tuning job is still running.
        hyperparameters (FineTuningJobHyperparameters): The hyperparameters used for the fine-tuning job. See the [fine-
            tuning guide](/docs/guides/fine-tuning) for more details.
        model (str): The base model that is being fine-tuned.
        object_ (FineTuningJobObject): The object type, which is always "fine_tuning.job".
        organization_id (str): The organization that owns the fine-tuning job.
        result_files (List[str]): The compiled results file ID(s) for the fine-tuning job. You can retrieve the results
            with the [Files API](/docs/api-reference/files/retrieve-contents).
        status (FineTuningJobStatus): The current status of the fine-tuning job, which can be either `validating_files`,
            `queued`, `running`, `succeeded`, `failed`, or `cancelled`.
        trained_tokens (Union[None, int]): The total number of billable tokens processed by this fine-tuning job. The
            value will be null if the fine-tuning job is still running.
        training_file (str): The file ID used for training. You can retrieve the training data with the [Files
            API](/docs/api-reference/files/retrieve-contents).
        validation_file (Union[None, str]): The file ID used for validation. You can retrieve the validation results
            with the [Files API](/docs/api-reference/files/retrieve-contents).
        seed (int): The seed used for the fine-tuning job.
        integrations (Union[List['FineTuningJobIntegration'], None, Unset]): A list of integrations to enable for this
            fine-tuning job.
        estimated_finish (Union[None, Unset, int]): The Unix timestamp (in seconds) for when the fine-tuning job is
            estimated to finish. The value will be null if the fine-tuning job is not running.
    """

    id: str
    created_at: int
    error: Union["FineTuningJobErrorType0", None]
    fine_tuned_model: Union[None, str]
    finished_at: Union[None, int]
    hyperparameters: "FineTuningJobHyperparameters"
    model: str
    object_: FineTuningJobObject
    organization_id: str
    result_files: List[str]
    status: FineTuningJobStatus
    trained_tokens: Union[None, int]
    training_file: str
    validation_file: Union[None, str]
    seed: int
    integrations: Union[List["FineTuningJobIntegration"], None, Unset] = UNSET
    estimated_finish: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.fine_tuning_job_error_type_0 import FineTuningJobErrorType0

        id = self.id

        created_at = self.created_at

        error: Union[Dict[str, Any], None]
        if isinstance(self.error, FineTuningJobErrorType0):
            error = self.error.to_dict()
        else:
            error = self.error

        fine_tuned_model: Union[None, str]
        fine_tuned_model = self.fine_tuned_model

        finished_at: Union[None, int]
        finished_at = self.finished_at

        hyperparameters = self.hyperparameters.to_dict()

        model = self.model

        object_ = self.object_.value

        organization_id = self.organization_id

        result_files = self.result_files

        status = self.status.value

        trained_tokens: Union[None, int]
        trained_tokens = self.trained_tokens

        training_file = self.training_file

        validation_file: Union[None, str]
        validation_file = self.validation_file

        seed = self.seed

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

        estimated_finish: Union[None, Unset, int]
        if isinstance(self.estimated_finish, Unset):
            estimated_finish = UNSET
        else:
            estimated_finish = self.estimated_finish

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "error": error,
                "fine_tuned_model": fine_tuned_model,
                "finished_at": finished_at,
                "hyperparameters": hyperparameters,
                "model": model,
                "object": object_,
                "organization_id": organization_id,
                "result_files": result_files,
                "status": status,
                "trained_tokens": trained_tokens,
                "training_file": training_file,
                "validation_file": validation_file,
                "seed": seed,
            }
        )
        if integrations is not UNSET:
            field_dict["integrations"] = integrations
        if estimated_finish is not UNSET:
            field_dict["estimated_finish"] = estimated_finish

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.fine_tuning_job_error_type_0 import FineTuningJobErrorType0
        from ..models.fine_tuning_job_hyperparameters import FineTuningJobHyperparameters
        from ..models.fine_tuning_job_integration import FineTuningJobIntegration

        d = src_dict.copy()
        id = d.pop("id")

        created_at = d.pop("created_at")

        def _parse_error(data: object) -> Union["FineTuningJobErrorType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                error_type_0 = FineTuningJobErrorType0.from_dict(data)

                return error_type_0
            except:  # noqa: E722
                pass
            return cast(Union["FineTuningJobErrorType0", None], data)

        error = _parse_error(d.pop("error"))

        def _parse_fine_tuned_model(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        fine_tuned_model = _parse_fine_tuned_model(d.pop("fine_tuned_model"))

        def _parse_finished_at(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        finished_at = _parse_finished_at(d.pop("finished_at"))

        hyperparameters = FineTuningJobHyperparameters.from_dict(d.pop("hyperparameters"))

        model = d.pop("model")

        object_ = FineTuningJobObject(d.pop("object"))

        organization_id = d.pop("organization_id")

        result_files = cast(List[str], d.pop("result_files"))

        status = FineTuningJobStatus(d.pop("status"))

        def _parse_trained_tokens(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        trained_tokens = _parse_trained_tokens(d.pop("trained_tokens"))

        training_file = d.pop("training_file")

        def _parse_validation_file(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        validation_file = _parse_validation_file(d.pop("validation_file"))

        seed = d.pop("seed")

        def _parse_integrations(data: object) -> Union[List["FineTuningJobIntegration"], None, Unset]:
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
                    integrations_type_0_item = FineTuningJobIntegration.from_dict(integrations_type_0_item_data)

                    integrations_type_0.append(integrations_type_0_item)

                return integrations_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["FineTuningJobIntegration"], None, Unset], data)

        integrations = _parse_integrations(d.pop("integrations", UNSET))

        def _parse_estimated_finish(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        estimated_finish = _parse_estimated_finish(d.pop("estimated_finish", UNSET))

        fine_tuning_job = cls(
            id=id,
            created_at=created_at,
            error=error,
            fine_tuned_model=fine_tuned_model,
            finished_at=finished_at,
            hyperparameters=hyperparameters,
            model=model,
            object_=object_,
            organization_id=organization_id,
            result_files=result_files,
            status=status,
            trained_tokens=trained_tokens,
            training_file=training_file,
            validation_file=validation_file,
            seed=seed,
            integrations=integrations,
            estimated_finish=estimated_finish,
        )

        fine_tuning_job.additional_properties = d
        return fine_tuning_job

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

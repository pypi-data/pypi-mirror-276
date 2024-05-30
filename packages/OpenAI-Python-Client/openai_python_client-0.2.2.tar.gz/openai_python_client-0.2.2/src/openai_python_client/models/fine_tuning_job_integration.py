from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.fine_tuning_job_integration_type import FineTuningJobIntegrationType

if TYPE_CHECKING:
    from ..models.fine_tuning_job_integration_wandb import FineTuningJobIntegrationWandb


T = TypeVar("T", bound="FineTuningJobIntegration")


@_attrs_define
class FineTuningJobIntegration:
    """
    Attributes:
        type (FineTuningJobIntegrationType): The type of the integration being enabled for the fine-tuning job
        wandb (FineTuningJobIntegrationWandb): The settings for your integration with Weights and Biases. This payload
            specifies the project that
            metrics will be sent to. Optionally, you can set an explicit display name for your run, add tags
            to your run, and set a default entity (team, username, etc) to be associated with your run.
    """

    type: FineTuningJobIntegrationType
    wandb: "FineTuningJobIntegrationWandb"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        wandb = self.wandb.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "wandb": wandb,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.fine_tuning_job_integration_wandb import FineTuningJobIntegrationWandb

        d = src_dict.copy()
        type = FineTuningJobIntegrationType(d.pop("type"))

        wandb = FineTuningJobIntegrationWandb.from_dict(d.pop("wandb"))

        fine_tuning_job_integration = cls(
            type=type,
            wandb=wandb,
        )

        fine_tuning_job_integration.additional_properties = d
        return fine_tuning_job_integration

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

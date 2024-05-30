from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_fine_tuning_job_request_integrations_type_0_item_type_type_0 import (
    CreateFineTuningJobRequestIntegrationsType0ItemTypeType0,
)

if TYPE_CHECKING:
    from ..models.create_fine_tuning_job_request_integrations_type_0_item_wandb import (
        CreateFineTuningJobRequestIntegrationsType0ItemWandb,
    )


T = TypeVar("T", bound="CreateFineTuningJobRequestIntegrationsType0Item")


@_attrs_define
class CreateFineTuningJobRequestIntegrationsType0Item:
    """
    Attributes:
        type (CreateFineTuningJobRequestIntegrationsType0ItemTypeType0): The type of integration to enable. Currently,
            only "wandb" (Weights and Biases) is supported.
        wandb (CreateFineTuningJobRequestIntegrationsType0ItemWandb): The settings for your integration with Weights and
            Biases. This payload specifies the project that
            metrics will be sent to. Optionally, you can set an explicit display name for your run, add tags
            to your run, and set a default entity (team, username, etc) to be associated with your run.
    """

    type: CreateFineTuningJobRequestIntegrationsType0ItemTypeType0
    wandb: "CreateFineTuningJobRequestIntegrationsType0ItemWandb"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type: str
        if isinstance(self.type, CreateFineTuningJobRequestIntegrationsType0ItemTypeType0):
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
        from ..models.create_fine_tuning_job_request_integrations_type_0_item_wandb import (
            CreateFineTuningJobRequestIntegrationsType0ItemWandb,
        )

        d = src_dict.copy()

        def _parse_type(data: object) -> CreateFineTuningJobRequestIntegrationsType0ItemTypeType0:
            if not isinstance(data, str):
                raise TypeError()
            type_type_0 = CreateFineTuningJobRequestIntegrationsType0ItemTypeType0(data)

            return type_type_0

        type = _parse_type(d.pop("type"))

        wandb = CreateFineTuningJobRequestIntegrationsType0ItemWandb.from_dict(d.pop("wandb"))

        create_fine_tuning_job_request_integrations_type_0_item = cls(
            type=type,
            wandb=wandb,
        )

        create_fine_tuning_job_request_integrations_type_0_item.additional_properties = d
        return create_fine_tuning_job_request_integrations_type_0_item

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

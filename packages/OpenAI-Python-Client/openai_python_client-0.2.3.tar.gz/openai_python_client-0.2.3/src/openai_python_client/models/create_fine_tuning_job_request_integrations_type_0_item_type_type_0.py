from enum import Enum


class CreateFineTuningJobRequestIntegrationsType0ItemTypeType0(str, Enum):
    WANDB = "wandb"

    def __str__(self) -> str:
        return str(self.value)

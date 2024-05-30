from enum import Enum


class FineTuningJobIntegrationType(str, Enum):
    WANDB = "wandb"

    def __str__(self) -> str:
        return str(self.value)

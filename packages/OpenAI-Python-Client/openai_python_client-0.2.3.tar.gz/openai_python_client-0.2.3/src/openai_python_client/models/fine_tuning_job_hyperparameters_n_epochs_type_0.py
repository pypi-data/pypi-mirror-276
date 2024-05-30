from enum import Enum


class FineTuningJobHyperparametersNEpochsType0(str, Enum):
    AUTO = "auto"

    def __str__(self) -> str:
        return str(self.value)

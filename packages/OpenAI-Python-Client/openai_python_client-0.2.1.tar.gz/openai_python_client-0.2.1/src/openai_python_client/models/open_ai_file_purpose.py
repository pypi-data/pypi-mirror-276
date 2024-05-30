from enum import Enum


class OpenAIFilePurpose(str, Enum):
    ASSISTANTS = "assistants"
    ASSISTANTS_OUTPUT = "assistants_output"
    BATCH = "batch"
    BATCH_OUTPUT = "batch_output"
    FINE_TUNE = "fine-tune"
    FINE_TUNE_RESULTS = "fine-tune-results"

    def __str__(self) -> str:
        return str(self.value)

"""Contains all the data models used in inputs/outputs"""

from .a_run_on_a_thread import ARunOnAThread
from .a_run_on_a_thread_incomplete_details_type_0 import ARunOnAThreadIncompleteDetailsType0
from .a_run_on_a_thread_incomplete_details_type_0_reason import ARunOnAThreadIncompleteDetailsType0Reason
from .a_run_on_a_thread_last_error_type_0 import ARunOnAThreadLastErrorType0
from .a_run_on_a_thread_last_error_type_0_code import ARunOnAThreadLastErrorType0Code
from .a_run_on_a_thread_metadata_type_0 import ARunOnAThreadMetadataType0
from .a_run_on_a_thread_object import ARunOnAThreadObject
from .a_run_on_a_thread_required_action_type_0 import ARunOnAThreadRequiredActionType0
from .a_run_on_a_thread_required_action_type_0_submit_tool_outputs import (
    ARunOnAThreadRequiredActionType0SubmitToolOutputs,
)
from .a_run_on_a_thread_required_action_type_0_type import ARunOnAThreadRequiredActionType0Type
from .a_run_on_a_thread_status import ARunOnAThreadStatus
from .assistant import Assistant
from .assistant_message import AssistantMessage
from .assistant_message_function_call import AssistantMessageFunctionCall
from .assistant_message_role import AssistantMessageRole
from .assistant_metadata_type_0 import AssistantMetadataType0
from .assistant_object import AssistantObject
from .assistant_tool_resources_type_0 import AssistantToolResourcesType0
from .assistant_tool_resources_type_0_code_interpreter import AssistantToolResourcesType0CodeInterpreter
from .assistant_tool_resources_type_0_file_search import AssistantToolResourcesType0FileSearch
from .assistants_api_response_format import AssistantsApiResponseFormat
from .assistants_api_response_format_option_type_0 import AssistantsApiResponseFormatOptionType0
from .assistants_api_response_format_type import AssistantsApiResponseFormatType
from .assistants_api_tool_choice_option_type_0 import AssistantsApiToolChoiceOptionType0
from .assistants_named_tool_choice import AssistantsNamedToolChoice
from .assistants_named_tool_choice_function import AssistantsNamedToolChoiceFunction
from .assistants_named_tool_choice_type import AssistantsNamedToolChoiceType
from .batch import Batch
from .batch_errors import BatchErrors
from .batch_errors_data_item import BatchErrorsDataItem
from .batch_metadata_type_0 import BatchMetadataType0
from .batch_object import BatchObject
from .batch_request_counts import BatchRequestCounts
from .batch_request_input import BatchRequestInput
from .batch_request_input_method import BatchRequestInputMethod
from .batch_request_output import BatchRequestOutput
from .batch_request_output_error_type_0 import BatchRequestOutputErrorType0
from .batch_request_output_response_type_0 import BatchRequestOutputResponseType0
from .batch_request_output_response_type_0_body import BatchRequestOutputResponseType0Body
from .batch_status import BatchStatus
from .chat_completion_function_call_option import ChatCompletionFunctionCallOption
from .chat_completion_functions import ChatCompletionFunctions
from .chat_completion_message_tool_call import ChatCompletionMessageToolCall
from .chat_completion_message_tool_call_chunk import ChatCompletionMessageToolCallChunk
from .chat_completion_message_tool_call_chunk_function import ChatCompletionMessageToolCallChunkFunction
from .chat_completion_message_tool_call_chunk_type import ChatCompletionMessageToolCallChunkType
from .chat_completion_message_tool_call_function import ChatCompletionMessageToolCallFunction
from .chat_completion_message_tool_call_type import ChatCompletionMessageToolCallType
from .chat_completion_named_tool_choice import ChatCompletionNamedToolChoice
from .chat_completion_named_tool_choice_function import ChatCompletionNamedToolChoiceFunction
from .chat_completion_named_tool_choice_type import ChatCompletionNamedToolChoiceType
from .chat_completion_response_message import ChatCompletionResponseMessage
from .chat_completion_response_message_function_call import ChatCompletionResponseMessageFunctionCall
from .chat_completion_response_message_role import ChatCompletionResponseMessageRole
from .chat_completion_role import ChatCompletionRole
from .chat_completion_stream_options_type_0 import ChatCompletionStreamOptionsType0
from .chat_completion_stream_response_delta import ChatCompletionStreamResponseDelta
from .chat_completion_stream_response_delta_function_call import ChatCompletionStreamResponseDeltaFunctionCall
from .chat_completion_stream_response_delta_role import ChatCompletionStreamResponseDeltaRole
from .chat_completion_token_logprob import ChatCompletionTokenLogprob
from .chat_completion_token_logprob_top_logprobs_item import ChatCompletionTokenLogprobTopLogprobsItem
from .chat_completion_tool import ChatCompletionTool
from .chat_completion_tool_choice_option_type_0 import ChatCompletionToolChoiceOptionType0
from .chat_completion_tool_type import ChatCompletionToolType
from .code_interpreter_image_output import CodeInterpreterImageOutput
from .code_interpreter_image_output_image import CodeInterpreterImageOutputImage
from .code_interpreter_image_output_type import CodeInterpreterImageOutputType
from .code_interpreter_log_output import CodeInterpreterLogOutput
from .code_interpreter_log_output_type import CodeInterpreterLogOutputType
from .code_interpreter_tool import CodeInterpreterTool
from .code_interpreter_tool_call import CodeInterpreterToolCall
from .code_interpreter_tool_call_code_interpreter import CodeInterpreterToolCallCodeInterpreter
from .code_interpreter_tool_call_type import CodeInterpreterToolCallType
from .code_interpreter_tool_type import CodeInterpreterToolType
from .completion_usage import CompletionUsage
from .create_assistant_request import CreateAssistantRequest
from .create_assistant_request_metadata_type_0 import CreateAssistantRequestMetadataType0
from .create_assistant_request_model_type_1 import CreateAssistantRequestModelType1
from .create_assistant_request_tool_resources_type_0 import CreateAssistantRequestToolResourcesType0
from .create_assistant_request_tool_resources_type_0_code_interpreter import (
    CreateAssistantRequestToolResourcesType0CodeInterpreter,
)
from .create_batch_body import CreateBatchBody
from .create_batch_body_completion_window import CreateBatchBodyCompletionWindow
from .create_batch_body_endpoint import CreateBatchBodyEndpoint
from .create_batch_body_metadata_type_0 import CreateBatchBodyMetadataType0
from .create_chat_completion_function_response import CreateChatCompletionFunctionResponse
from .create_chat_completion_function_response_choices_item import CreateChatCompletionFunctionResponseChoicesItem
from .create_chat_completion_function_response_choices_item_finish_reason import (
    CreateChatCompletionFunctionResponseChoicesItemFinishReason,
)
from .create_chat_completion_function_response_object import CreateChatCompletionFunctionResponseObject
from .create_chat_completion_image_response import CreateChatCompletionImageResponse
from .create_chat_completion_request import CreateChatCompletionRequest
from .create_chat_completion_request_function_call_type_0 import CreateChatCompletionRequestFunctionCallType0
from .create_chat_completion_request_logit_bias_type_0 import CreateChatCompletionRequestLogitBiasType0
from .create_chat_completion_request_model_type_1 import CreateChatCompletionRequestModelType1
from .create_chat_completion_request_response_format import CreateChatCompletionRequestResponseFormat
from .create_chat_completion_request_response_format_type import CreateChatCompletionRequestResponseFormatType
from .create_chat_completion_response import CreateChatCompletionResponse
from .create_chat_completion_response_choices_item import CreateChatCompletionResponseChoicesItem
from .create_chat_completion_response_choices_item_finish_reason import (
    CreateChatCompletionResponseChoicesItemFinishReason,
)
from .create_chat_completion_response_choices_item_logprobs_type_0 import (
    CreateChatCompletionResponseChoicesItemLogprobsType0,
)
from .create_chat_completion_response_object import CreateChatCompletionResponseObject
from .create_chat_completion_stream_response import CreateChatCompletionStreamResponse
from .create_chat_completion_stream_response_choices_item import CreateChatCompletionStreamResponseChoicesItem
from .create_chat_completion_stream_response_choices_item_finish_reason import (
    CreateChatCompletionStreamResponseChoicesItemFinishReason,
)
from .create_chat_completion_stream_response_choices_item_logprobs_type_0 import (
    CreateChatCompletionStreamResponseChoicesItemLogprobsType0,
)
from .create_chat_completion_stream_response_object import CreateChatCompletionStreamResponseObject
from .create_chat_completion_stream_response_usage import CreateChatCompletionStreamResponseUsage
from .create_completion_request import CreateCompletionRequest
from .create_completion_request_logit_bias_type_0 import CreateCompletionRequestLogitBiasType0
from .create_completion_request_model_type_1 import CreateCompletionRequestModelType1
from .create_completion_response import CreateCompletionResponse
from .create_completion_response_choices_item import CreateCompletionResponseChoicesItem
from .create_completion_response_choices_item_finish_reason import CreateCompletionResponseChoicesItemFinishReason
from .create_completion_response_choices_item_logprobs_type_0 import CreateCompletionResponseChoicesItemLogprobsType0
from .create_completion_response_choices_item_logprobs_type_0_top_logprobs_item import (
    CreateCompletionResponseChoicesItemLogprobsType0TopLogprobsItem,
)
from .create_completion_response_object import CreateCompletionResponseObject
from .create_embedding_request import CreateEmbeddingRequest
from .create_embedding_request_encoding_format import CreateEmbeddingRequestEncodingFormat
from .create_embedding_request_model_type_1 import CreateEmbeddingRequestModelType1
from .create_embedding_response import CreateEmbeddingResponse
from .create_embedding_response_object import CreateEmbeddingResponseObject
from .create_embedding_response_usage import CreateEmbeddingResponseUsage
from .create_file_request import CreateFileRequest
from .create_file_request_purpose import CreateFileRequestPurpose
from .create_fine_tuning_job_request import CreateFineTuningJobRequest
from .create_fine_tuning_job_request_hyperparameters import CreateFineTuningJobRequestHyperparameters
from .create_fine_tuning_job_request_hyperparameters_batch_size_type_0 import (
    CreateFineTuningJobRequestHyperparametersBatchSizeType0,
)
from .create_fine_tuning_job_request_hyperparameters_learning_rate_multiplier_type_0 import (
    CreateFineTuningJobRequestHyperparametersLearningRateMultiplierType0,
)
from .create_fine_tuning_job_request_hyperparameters_n_epochs_type_0 import (
    CreateFineTuningJobRequestHyperparametersNEpochsType0,
)
from .create_fine_tuning_job_request_integrations_type_0_item import CreateFineTuningJobRequestIntegrationsType0Item
from .create_fine_tuning_job_request_integrations_type_0_item_type_type_0 import (
    CreateFineTuningJobRequestIntegrationsType0ItemTypeType0,
)
from .create_fine_tuning_job_request_integrations_type_0_item_wandb import (
    CreateFineTuningJobRequestIntegrationsType0ItemWandb,
)
from .create_fine_tuning_job_request_model_type_1 import CreateFineTuningJobRequestModelType1
from .create_image_edit_request import CreateImageEditRequest
from .create_image_edit_request_model_type_1 import CreateImageEditRequestModelType1
from .create_image_edit_request_response_format import CreateImageEditRequestResponseFormat
from .create_image_edit_request_size import CreateImageEditRequestSize
from .create_image_request import CreateImageRequest
from .create_image_request_model_type_1 import CreateImageRequestModelType1
from .create_image_request_quality import CreateImageRequestQuality
from .create_image_request_response_format import CreateImageRequestResponseFormat
from .create_image_request_size import CreateImageRequestSize
from .create_image_request_style import CreateImageRequestStyle
from .create_image_variation_request import CreateImageVariationRequest
from .create_image_variation_request_model_type_1 import CreateImageVariationRequestModelType1
from .create_image_variation_request_response_format import CreateImageVariationRequestResponseFormat
from .create_image_variation_request_size import CreateImageVariationRequestSize
from .create_message_request import CreateMessageRequest
from .create_message_request_attachments_type_0_item import CreateMessageRequestAttachmentsType0Item
from .create_message_request_metadata_type_0 import CreateMessageRequestMetadataType0
from .create_message_request_role import CreateMessageRequestRole
from .create_moderation_request import CreateModerationRequest
from .create_moderation_request_model_type_1 import CreateModerationRequestModelType1
from .create_moderation_response import CreateModerationResponse
from .create_moderation_response_results_item import CreateModerationResponseResultsItem
from .create_moderation_response_results_item_categories import CreateModerationResponseResultsItemCategories
from .create_moderation_response_results_item_category_scores import CreateModerationResponseResultsItemCategoryScores
from .create_run_request import CreateRunRequest
from .create_run_request_metadata_type_0 import CreateRunRequestMetadataType0
from .create_run_request_model_type_1 import CreateRunRequestModelType1
from .create_speech_request import CreateSpeechRequest
from .create_speech_request_model_type_1 import CreateSpeechRequestModelType1
from .create_speech_request_response_format import CreateSpeechRequestResponseFormat
from .create_speech_request_voice import CreateSpeechRequestVoice
from .create_thread_and_run_request import CreateThreadAndRunRequest
from .create_thread_and_run_request_metadata_type_0 import CreateThreadAndRunRequestMetadataType0
from .create_thread_and_run_request_model_type_1 import CreateThreadAndRunRequestModelType1
from .create_thread_and_run_request_tool_resources_type_0 import CreateThreadAndRunRequestToolResourcesType0
from .create_thread_and_run_request_tool_resources_type_0_code_interpreter import (
    CreateThreadAndRunRequestToolResourcesType0CodeInterpreter,
)
from .create_thread_and_run_request_tool_resources_type_0_file_search import (
    CreateThreadAndRunRequestToolResourcesType0FileSearch,
)
from .create_thread_request import CreateThreadRequest
from .create_thread_request_metadata_type_0 import CreateThreadRequestMetadataType0
from .create_thread_request_tool_resources_type_0 import CreateThreadRequestToolResourcesType0
from .create_thread_request_tool_resources_type_0_code_interpreter import (
    CreateThreadRequestToolResourcesType0CodeInterpreter,
)
from .create_transcription_request import CreateTranscriptionRequest
from .create_transcription_request_model_type_1 import CreateTranscriptionRequestModelType1
from .create_transcription_request_response_format import CreateTranscriptionRequestResponseFormat
from .create_transcription_request_timestamp_granularities_item import (
    CreateTranscriptionRequestTimestampGranularitiesItem,
)
from .create_transcription_response_json import CreateTranscriptionResponseJson
from .create_transcription_response_verbose_json import CreateTranscriptionResponseVerboseJson
from .create_translation_request import CreateTranslationRequest
from .create_translation_request_model_type_1 import CreateTranslationRequestModelType1
from .create_translation_response_json import CreateTranslationResponseJson
from .create_translation_response_verbose_json import CreateTranslationResponseVerboseJson
from .create_vector_store_file_batch_request import CreateVectorStoreFileBatchRequest
from .create_vector_store_file_request import CreateVectorStoreFileRequest
from .create_vector_store_request import CreateVectorStoreRequest
from .create_vector_store_request_metadata_type_0 import CreateVectorStoreRequestMetadataType0
from .delete_assistant_response import DeleteAssistantResponse
from .delete_assistant_response_object import DeleteAssistantResponseObject
from .delete_file_response import DeleteFileResponse
from .delete_file_response_object import DeleteFileResponseObject
from .delete_message_response import DeleteMessageResponse
from .delete_message_response_object import DeleteMessageResponseObject
from .delete_model_response import DeleteModelResponse
from .delete_thread_response import DeleteThreadResponse
from .delete_thread_response_object import DeleteThreadResponseObject
from .delete_vector_store_file_response import DeleteVectorStoreFileResponse
from .delete_vector_store_file_response_object import DeleteVectorStoreFileResponseObject
from .delete_vector_store_response import DeleteVectorStoreResponse
from .delete_vector_store_response_object import DeleteVectorStoreResponseObject
from .done_event import DoneEvent
from .done_event_data import DoneEventData
from .done_event_event import DoneEventEvent
from .embedding import Embedding
from .embedding_object import EmbeddingObject
from .error import Error
from .error_event import ErrorEvent
from .error_event_event import ErrorEventEvent
from .error_response import ErrorResponse
from .file_citation import FileCitation
from .file_citation_file_citation import FileCitationFileCitation
from .file_citation_type import FileCitationType
from .file_path import FilePath
from .file_path_file_path import FilePathFilePath
from .file_path_type import FilePathType
from .file_search_tool import FileSearchTool
from .file_search_tool_call import FileSearchToolCall
from .file_search_tool_call_file_search import FileSearchToolCallFileSearch
from .file_search_tool_call_type import FileSearchToolCallType
from .file_search_tool_type import FileSearchToolType
from .fine_tuning_job import FineTuningJob
from .fine_tuning_job_checkpoint import FineTuningJobCheckpoint
from .fine_tuning_job_checkpoint_metrics import FineTuningJobCheckpointMetrics
from .fine_tuning_job_checkpoint_object import FineTuningJobCheckpointObject
from .fine_tuning_job_error_type_0 import FineTuningJobErrorType0
from .fine_tuning_job_event import FineTuningJobEvent
from .fine_tuning_job_event_level import FineTuningJobEventLevel
from .fine_tuning_job_event_object import FineTuningJobEventObject
from .fine_tuning_job_hyperparameters import FineTuningJobHyperparameters
from .fine_tuning_job_hyperparameters_n_epochs_type_0 import FineTuningJobHyperparametersNEpochsType0
from .fine_tuning_job_integration import FineTuningJobIntegration
from .fine_tuning_job_integration_type import FineTuningJobIntegrationType
from .fine_tuning_job_integration_wandb import FineTuningJobIntegrationWandb
from .fine_tuning_job_object import FineTuningJobObject
from .fine_tuning_job_status import FineTuningJobStatus
from .function_message import FunctionMessage
from .function_message_role import FunctionMessageRole
from .function_object import FunctionObject
from .function_parameters import FunctionParameters
from .function_tool import FunctionTool
from .function_tool_call import FunctionToolCall
from .function_tool_call_function import FunctionToolCallFunction
from .function_tool_call_type import FunctionToolCallType
from .function_tool_type import FunctionToolType
from .image import Image
from .image_content_part import ImageContentPart
from .image_content_part_image_url import ImageContentPartImageUrl
from .image_content_part_image_url_detail import ImageContentPartImageUrlDetail
from .image_content_part_type import ImageContentPartType
from .image_file import ImageFile
from .image_file_image_file import ImageFileImageFile
from .image_file_type import ImageFileType
from .images_response import ImagesResponse
from .list_assistants_order import ListAssistantsOrder
from .list_assistants_response import ListAssistantsResponse
from .list_batches_response import ListBatchesResponse
from .list_batches_response_object import ListBatchesResponseObject
from .list_files_in_vector_store_batch_filter import ListFilesInVectorStoreBatchFilter
from .list_files_in_vector_store_batch_order import ListFilesInVectorStoreBatchOrder
from .list_files_response import ListFilesResponse
from .list_files_response_object import ListFilesResponseObject
from .list_fine_tuning_job_checkpoints_response import ListFineTuningJobCheckpointsResponse
from .list_fine_tuning_job_checkpoints_response_object import ListFineTuningJobCheckpointsResponseObject
from .list_fine_tuning_job_events_response import ListFineTuningJobEventsResponse
from .list_fine_tuning_job_events_response_object import ListFineTuningJobEventsResponseObject
from .list_messages_order import ListMessagesOrder
from .list_messages_response import ListMessagesResponse
from .list_models_response import ListModelsResponse
from .list_models_response_object import ListModelsResponseObject
from .list_paginated_fine_tuning_jobs_response import ListPaginatedFineTuningJobsResponse
from .list_paginated_fine_tuning_jobs_response_object import ListPaginatedFineTuningJobsResponseObject
from .list_run_steps_order import ListRunStepsOrder
from .list_run_steps_response import ListRunStepsResponse
from .list_runs_order import ListRunsOrder
from .list_runs_response import ListRunsResponse
from .list_threads_response import ListThreadsResponse
from .list_vector_store_files_filter import ListVectorStoreFilesFilter
from .list_vector_store_files_order import ListVectorStoreFilesOrder
from .list_vector_store_files_response import ListVectorStoreFilesResponse
from .list_vector_stores_order import ListVectorStoresOrder
from .list_vector_stores_response import ListVectorStoresResponse
from .message_creation import MessageCreation
from .message_creation_message_creation import MessageCreationMessageCreation
from .message_creation_type import MessageCreationType
from .message_stream_event_type_0 import MessageStreamEventType0
from .message_stream_event_type_0_event import MessageStreamEventType0Event
from .message_stream_event_type_1 import MessageStreamEventType1
from .message_stream_event_type_1_event import MessageStreamEventType1Event
from .message_stream_event_type_2_event import MessageStreamEventType2Event
from .message_stream_event_type_3 import MessageStreamEventType3
from .message_stream_event_type_3_event import MessageStreamEventType3Event
from .message_stream_event_type_4 import MessageStreamEventType4
from .message_stream_event_type_4_event import MessageStreamEventType4Event
from .model import Model
from .model_object import ModelObject
from .modify_assistant_request import ModifyAssistantRequest
from .modify_assistant_request_metadata_type_0 import ModifyAssistantRequestMetadataType0
from .modify_assistant_request_tool_resources_type_0 import ModifyAssistantRequestToolResourcesType0
from .modify_assistant_request_tool_resources_type_0_code_interpreter import (
    ModifyAssistantRequestToolResourcesType0CodeInterpreter,
)
from .modify_assistant_request_tool_resources_type_0_file_search import (
    ModifyAssistantRequestToolResourcesType0FileSearch,
)
from .modify_message_request import ModifyMessageRequest
from .modify_message_request_metadata_type_0 import ModifyMessageRequestMetadataType0
from .modify_run_request import ModifyRunRequest
from .modify_run_request_metadata_type_0 import ModifyRunRequestMetadataType0
from .modify_thread_request import ModifyThreadRequest
from .modify_thread_request_metadata_type_0 import ModifyThreadRequestMetadataType0
from .modify_thread_request_tool_resources_type_0 import ModifyThreadRequestToolResourcesType0
from .modify_thread_request_tool_resources_type_0_code_interpreter import (
    ModifyThreadRequestToolResourcesType0CodeInterpreter,
)
from .modify_thread_request_tool_resources_type_0_file_search import ModifyThreadRequestToolResourcesType0FileSearch
from .open_ai_file import OpenAIFile
from .open_ai_file_object import OpenAIFileObject
from .open_ai_file_purpose import OpenAIFilePurpose
from .open_ai_file_status import OpenAIFileStatus
from .run_completion_usage_type_0 import RunCompletionUsageType0
from .run_step_completion_usage_type_0 import RunStepCompletionUsageType0
from .run_step_stream_event_type_0 import RunStepStreamEventType0
from .run_step_stream_event_type_0_event import RunStepStreamEventType0Event
from .run_step_stream_event_type_1 import RunStepStreamEventType1
from .run_step_stream_event_type_1_event import RunStepStreamEventType1Event
from .run_step_stream_event_type_2_event import RunStepStreamEventType2Event
from .run_step_stream_event_type_3 import RunStepStreamEventType3
from .run_step_stream_event_type_3_event import RunStepStreamEventType3Event
from .run_step_stream_event_type_4 import RunStepStreamEventType4
from .run_step_stream_event_type_4_event import RunStepStreamEventType4Event
from .run_step_stream_event_type_5 import RunStepStreamEventType5
from .run_step_stream_event_type_5_event import RunStepStreamEventType5Event
from .run_step_stream_event_type_6 import RunStepStreamEventType6
from .run_step_stream_event_type_6_event import RunStepStreamEventType6Event
from .run_steps import RunSteps
from .run_steps_last_error_type_0 import RunStepsLastErrorType0
from .run_steps_last_error_type_0_code import RunStepsLastErrorType0Code
from .run_steps_metadata_type_0 import RunStepsMetadataType0
from .run_steps_object import RunStepsObject
from .run_steps_status import RunStepsStatus
from .run_steps_type import RunStepsType
from .run_stream_event_type_0 import RunStreamEventType0
from .run_stream_event_type_0_event import RunStreamEventType0Event
from .run_stream_event_type_1 import RunStreamEventType1
from .run_stream_event_type_1_event import RunStreamEventType1Event
from .run_stream_event_type_2 import RunStreamEventType2
from .run_stream_event_type_2_event import RunStreamEventType2Event
from .run_stream_event_type_3 import RunStreamEventType3
from .run_stream_event_type_3_event import RunStreamEventType3Event
from .run_stream_event_type_4 import RunStreamEventType4
from .run_stream_event_type_4_event import RunStreamEventType4Event
from .run_stream_event_type_5 import RunStreamEventType5
from .run_stream_event_type_5_event import RunStreamEventType5Event
from .run_stream_event_type_6 import RunStreamEventType6
from .run_stream_event_type_6_event import RunStreamEventType6Event
from .run_stream_event_type_7 import RunStreamEventType7
from .run_stream_event_type_7_event import RunStreamEventType7Event
from .run_stream_event_type_8 import RunStreamEventType8
from .run_stream_event_type_8_event import RunStreamEventType8Event
from .run_tool_call_object import RunToolCallObject
from .run_tool_call_object_function import RunToolCallObjectFunction
from .run_tool_call_object_type import RunToolCallObjectType
from .submit_tool_outputs_run_request import SubmitToolOutputsRunRequest
from .submit_tool_outputs_run_request_tool_outputs_item import SubmitToolOutputsRunRequestToolOutputsItem
from .system_message import SystemMessage
from .system_message_role import SystemMessageRole
from .text import Text
from .text_content_part import TextContentPart
from .text_content_part_type import TextContentPartType
from .text_text import TextText
from .text_type import TextType
from .the_message_object import TheMessageObject
from .the_message_object_attachments_type_0_item import TheMessageObjectAttachmentsType0Item
from .the_message_object_incomplete_details_type_0 import TheMessageObjectIncompleteDetailsType0
from .the_message_object_incomplete_details_type_0_reason import TheMessageObjectIncompleteDetailsType0Reason
from .the_message_object_metadata_type_0 import TheMessageObjectMetadataType0
from .the_message_object_object import TheMessageObjectObject
from .the_message_object_role import TheMessageObjectRole
from .the_message_object_status import TheMessageObjectStatus
from .thread import Thread
from .thread_metadata_type_0 import ThreadMetadataType0
from .thread_object import ThreadObject
from .thread_stream_event_type_0 import ThreadStreamEventType0
from .thread_stream_event_type_0_event import ThreadStreamEventType0Event
from .thread_tool_resources_type_0 import ThreadToolResourcesType0
from .thread_tool_resources_type_0_code_interpreter import ThreadToolResourcesType0CodeInterpreter
from .thread_tool_resources_type_0_file_search import ThreadToolResourcesType0FileSearch
from .thread_truncation_controls import ThreadTruncationControls
from .thread_truncation_controls_type import ThreadTruncationControlsType
from .tool_calls import ToolCalls
from .tool_calls_type import ToolCallsType
from .tool_message import ToolMessage
from .tool_message_role import ToolMessageRole
from .transcription_segment import TranscriptionSegment
from .transcription_word import TranscriptionWord
from .update_vector_store_request import UpdateVectorStoreRequest
from .update_vector_store_request_metadata_type_0 import UpdateVectorStoreRequestMetadataType0
from .user_message import UserMessage
from .user_message_role import UserMessageRole
from .vector_store import VectorStore
from .vector_store_expiration_policy import VectorStoreExpirationPolicy
from .vector_store_expiration_policy_anchor import VectorStoreExpirationPolicyAnchor
from .vector_store_file_batch import VectorStoreFileBatch
from .vector_store_file_batch_file_counts import VectorStoreFileBatchFileCounts
from .vector_store_file_batch_object import VectorStoreFileBatchObject
from .vector_store_file_batch_status import VectorStoreFileBatchStatus
from .vector_store_file_counts import VectorStoreFileCounts
from .vector_store_files import VectorStoreFiles
from .vector_store_files_last_error_type_0 import VectorStoreFilesLastErrorType0
from .vector_store_files_last_error_type_0_code import VectorStoreFilesLastErrorType0Code
from .vector_store_files_object import VectorStoreFilesObject
from .vector_store_files_status import VectorStoreFilesStatus
from .vector_store_metadata_type_0 import VectorStoreMetadataType0
from .vector_store_object import VectorStoreObject
from .vector_store_status import VectorStoreStatus

__all__ = (
    "ARunOnAThread",
    "ARunOnAThreadIncompleteDetailsType0",
    "ARunOnAThreadIncompleteDetailsType0Reason",
    "ARunOnAThreadLastErrorType0",
    "ARunOnAThreadLastErrorType0Code",
    "ARunOnAThreadMetadataType0",
    "ARunOnAThreadObject",
    "ARunOnAThreadRequiredActionType0",
    "ARunOnAThreadRequiredActionType0SubmitToolOutputs",
    "ARunOnAThreadRequiredActionType0Type",
    "ARunOnAThreadStatus",
    "Assistant",
    "AssistantMessage",
    "AssistantMessageFunctionCall",
    "AssistantMessageRole",
    "AssistantMetadataType0",
    "AssistantObject",
    "AssistantsApiResponseFormat",
    "AssistantsApiResponseFormatOptionType0",
    "AssistantsApiResponseFormatType",
    "AssistantsApiToolChoiceOptionType0",
    "AssistantsNamedToolChoice",
    "AssistantsNamedToolChoiceFunction",
    "AssistantsNamedToolChoiceType",
    "AssistantToolResourcesType0",
    "AssistantToolResourcesType0CodeInterpreter",
    "AssistantToolResourcesType0FileSearch",
    "Batch",
    "BatchErrors",
    "BatchErrorsDataItem",
    "BatchMetadataType0",
    "BatchObject",
    "BatchRequestCounts",
    "BatchRequestInput",
    "BatchRequestInputMethod",
    "BatchRequestOutput",
    "BatchRequestOutputErrorType0",
    "BatchRequestOutputResponseType0",
    "BatchRequestOutputResponseType0Body",
    "BatchStatus",
    "ChatCompletionFunctionCallOption",
    "ChatCompletionFunctions",
    "ChatCompletionMessageToolCall",
    "ChatCompletionMessageToolCallChunk",
    "ChatCompletionMessageToolCallChunkFunction",
    "ChatCompletionMessageToolCallChunkType",
    "ChatCompletionMessageToolCallFunction",
    "ChatCompletionMessageToolCallType",
    "ChatCompletionNamedToolChoice",
    "ChatCompletionNamedToolChoiceFunction",
    "ChatCompletionNamedToolChoiceType",
    "ChatCompletionResponseMessage",
    "ChatCompletionResponseMessageFunctionCall",
    "ChatCompletionResponseMessageRole",
    "ChatCompletionRole",
    "ChatCompletionStreamOptionsType0",
    "ChatCompletionStreamResponseDelta",
    "ChatCompletionStreamResponseDeltaFunctionCall",
    "ChatCompletionStreamResponseDeltaRole",
    "ChatCompletionTokenLogprob",
    "ChatCompletionTokenLogprobTopLogprobsItem",
    "ChatCompletionTool",
    "ChatCompletionToolChoiceOptionType0",
    "ChatCompletionToolType",
    "CodeInterpreterImageOutput",
    "CodeInterpreterImageOutputImage",
    "CodeInterpreterImageOutputType",
    "CodeInterpreterLogOutput",
    "CodeInterpreterLogOutputType",
    "CodeInterpreterTool",
    "CodeInterpreterToolCall",
    "CodeInterpreterToolCallCodeInterpreter",
    "CodeInterpreterToolCallType",
    "CodeInterpreterToolType",
    "CompletionUsage",
    "CreateAssistantRequest",
    "CreateAssistantRequestMetadataType0",
    "CreateAssistantRequestModelType1",
    "CreateAssistantRequestToolResourcesType0",
    "CreateAssistantRequestToolResourcesType0CodeInterpreter",
    "CreateBatchBody",
    "CreateBatchBodyCompletionWindow",
    "CreateBatchBodyEndpoint",
    "CreateBatchBodyMetadataType0",
    "CreateChatCompletionFunctionResponse",
    "CreateChatCompletionFunctionResponseChoicesItem",
    "CreateChatCompletionFunctionResponseChoicesItemFinishReason",
    "CreateChatCompletionFunctionResponseObject",
    "CreateChatCompletionImageResponse",
    "CreateChatCompletionRequest",
    "CreateChatCompletionRequestFunctionCallType0",
    "CreateChatCompletionRequestLogitBiasType0",
    "CreateChatCompletionRequestModelType1",
    "CreateChatCompletionRequestResponseFormat",
    "CreateChatCompletionRequestResponseFormatType",
    "CreateChatCompletionResponse",
    "CreateChatCompletionResponseChoicesItem",
    "CreateChatCompletionResponseChoicesItemFinishReason",
    "CreateChatCompletionResponseChoicesItemLogprobsType0",
    "CreateChatCompletionResponseObject",
    "CreateChatCompletionStreamResponse",
    "CreateChatCompletionStreamResponseChoicesItem",
    "CreateChatCompletionStreamResponseChoicesItemFinishReason",
    "CreateChatCompletionStreamResponseChoicesItemLogprobsType0",
    "CreateChatCompletionStreamResponseObject",
    "CreateChatCompletionStreamResponseUsage",
    "CreateCompletionRequest",
    "CreateCompletionRequestLogitBiasType0",
    "CreateCompletionRequestModelType1",
    "CreateCompletionResponse",
    "CreateCompletionResponseChoicesItem",
    "CreateCompletionResponseChoicesItemFinishReason",
    "CreateCompletionResponseChoicesItemLogprobsType0",
    "CreateCompletionResponseChoicesItemLogprobsType0TopLogprobsItem",
    "CreateCompletionResponseObject",
    "CreateEmbeddingRequest",
    "CreateEmbeddingRequestEncodingFormat",
    "CreateEmbeddingRequestModelType1",
    "CreateEmbeddingResponse",
    "CreateEmbeddingResponseObject",
    "CreateEmbeddingResponseUsage",
    "CreateFileRequest",
    "CreateFileRequestPurpose",
    "CreateFineTuningJobRequest",
    "CreateFineTuningJobRequestHyperparameters",
    "CreateFineTuningJobRequestHyperparametersBatchSizeType0",
    "CreateFineTuningJobRequestHyperparametersLearningRateMultiplierType0",
    "CreateFineTuningJobRequestHyperparametersNEpochsType0",
    "CreateFineTuningJobRequestIntegrationsType0Item",
    "CreateFineTuningJobRequestIntegrationsType0ItemTypeType0",
    "CreateFineTuningJobRequestIntegrationsType0ItemWandb",
    "CreateFineTuningJobRequestModelType1",
    "CreateImageEditRequest",
    "CreateImageEditRequestModelType1",
    "CreateImageEditRequestResponseFormat",
    "CreateImageEditRequestSize",
    "CreateImageRequest",
    "CreateImageRequestModelType1",
    "CreateImageRequestQuality",
    "CreateImageRequestResponseFormat",
    "CreateImageRequestSize",
    "CreateImageRequestStyle",
    "CreateImageVariationRequest",
    "CreateImageVariationRequestModelType1",
    "CreateImageVariationRequestResponseFormat",
    "CreateImageVariationRequestSize",
    "CreateMessageRequest",
    "CreateMessageRequestAttachmentsType0Item",
    "CreateMessageRequestMetadataType0",
    "CreateMessageRequestRole",
    "CreateModerationRequest",
    "CreateModerationRequestModelType1",
    "CreateModerationResponse",
    "CreateModerationResponseResultsItem",
    "CreateModerationResponseResultsItemCategories",
    "CreateModerationResponseResultsItemCategoryScores",
    "CreateRunRequest",
    "CreateRunRequestMetadataType0",
    "CreateRunRequestModelType1",
    "CreateSpeechRequest",
    "CreateSpeechRequestModelType1",
    "CreateSpeechRequestResponseFormat",
    "CreateSpeechRequestVoice",
    "CreateThreadAndRunRequest",
    "CreateThreadAndRunRequestMetadataType0",
    "CreateThreadAndRunRequestModelType1",
    "CreateThreadAndRunRequestToolResourcesType0",
    "CreateThreadAndRunRequestToolResourcesType0CodeInterpreter",
    "CreateThreadAndRunRequestToolResourcesType0FileSearch",
    "CreateThreadRequest",
    "CreateThreadRequestMetadataType0",
    "CreateThreadRequestToolResourcesType0",
    "CreateThreadRequestToolResourcesType0CodeInterpreter",
    "CreateTranscriptionRequest",
    "CreateTranscriptionRequestModelType1",
    "CreateTranscriptionRequestResponseFormat",
    "CreateTranscriptionRequestTimestampGranularitiesItem",
    "CreateTranscriptionResponseJson",
    "CreateTranscriptionResponseVerboseJson",
    "CreateTranslationRequest",
    "CreateTranslationRequestModelType1",
    "CreateTranslationResponseJson",
    "CreateTranslationResponseVerboseJson",
    "CreateVectorStoreFileBatchRequest",
    "CreateVectorStoreFileRequest",
    "CreateVectorStoreRequest",
    "CreateVectorStoreRequestMetadataType0",
    "DeleteAssistantResponse",
    "DeleteAssistantResponseObject",
    "DeleteFileResponse",
    "DeleteFileResponseObject",
    "DeleteMessageResponse",
    "DeleteMessageResponseObject",
    "DeleteModelResponse",
    "DeleteThreadResponse",
    "DeleteThreadResponseObject",
    "DeleteVectorStoreFileResponse",
    "DeleteVectorStoreFileResponseObject",
    "DeleteVectorStoreResponse",
    "DeleteVectorStoreResponseObject",
    "DoneEvent",
    "DoneEventData",
    "DoneEventEvent",
    "Embedding",
    "EmbeddingObject",
    "Error",
    "ErrorEvent",
    "ErrorEventEvent",
    "ErrorResponse",
    "FileCitation",
    "FileCitationFileCitation",
    "FileCitationType",
    "FilePath",
    "FilePathFilePath",
    "FilePathType",
    "FileSearchTool",
    "FileSearchToolCall",
    "FileSearchToolCallFileSearch",
    "FileSearchToolCallType",
    "FileSearchToolType",
    "FineTuningJob",
    "FineTuningJobCheckpoint",
    "FineTuningJobCheckpointMetrics",
    "FineTuningJobCheckpointObject",
    "FineTuningJobErrorType0",
    "FineTuningJobEvent",
    "FineTuningJobEventLevel",
    "FineTuningJobEventObject",
    "FineTuningJobHyperparameters",
    "FineTuningJobHyperparametersNEpochsType0",
    "FineTuningJobIntegration",
    "FineTuningJobIntegrationType",
    "FineTuningJobIntegrationWandb",
    "FineTuningJobObject",
    "FineTuningJobStatus",
    "FunctionMessage",
    "FunctionMessageRole",
    "FunctionObject",
    "FunctionParameters",
    "FunctionTool",
    "FunctionToolCall",
    "FunctionToolCallFunction",
    "FunctionToolCallType",
    "FunctionToolType",
    "Image",
    "ImageContentPart",
    "ImageContentPartImageUrl",
    "ImageContentPartImageUrlDetail",
    "ImageContentPartType",
    "ImageFile",
    "ImageFileImageFile",
    "ImageFileType",
    "ImagesResponse",
    "ListAssistantsOrder",
    "ListAssistantsResponse",
    "ListBatchesResponse",
    "ListBatchesResponseObject",
    "ListFilesInVectorStoreBatchFilter",
    "ListFilesInVectorStoreBatchOrder",
    "ListFilesResponse",
    "ListFilesResponseObject",
    "ListFineTuningJobCheckpointsResponse",
    "ListFineTuningJobCheckpointsResponseObject",
    "ListFineTuningJobEventsResponse",
    "ListFineTuningJobEventsResponseObject",
    "ListMessagesOrder",
    "ListMessagesResponse",
    "ListModelsResponse",
    "ListModelsResponseObject",
    "ListPaginatedFineTuningJobsResponse",
    "ListPaginatedFineTuningJobsResponseObject",
    "ListRunsOrder",
    "ListRunsResponse",
    "ListRunStepsOrder",
    "ListRunStepsResponse",
    "ListThreadsResponse",
    "ListVectorStoreFilesFilter",
    "ListVectorStoreFilesOrder",
    "ListVectorStoreFilesResponse",
    "ListVectorStoresOrder",
    "ListVectorStoresResponse",
    "MessageCreation",
    "MessageCreationMessageCreation",
    "MessageCreationType",
    "MessageStreamEventType0",
    "MessageStreamEventType0Event",
    "MessageStreamEventType1",
    "MessageStreamEventType1Event",
    "MessageStreamEventType2Event",
    "MessageStreamEventType3",
    "MessageStreamEventType3Event",
    "MessageStreamEventType4",
    "MessageStreamEventType4Event",
    "Model",
    "ModelObject",
    "ModifyAssistantRequest",
    "ModifyAssistantRequestMetadataType0",
    "ModifyAssistantRequestToolResourcesType0",
    "ModifyAssistantRequestToolResourcesType0CodeInterpreter",
    "ModifyAssistantRequestToolResourcesType0FileSearch",
    "ModifyMessageRequest",
    "ModifyMessageRequestMetadataType0",
    "ModifyRunRequest",
    "ModifyRunRequestMetadataType0",
    "ModifyThreadRequest",
    "ModifyThreadRequestMetadataType0",
    "ModifyThreadRequestToolResourcesType0",
    "ModifyThreadRequestToolResourcesType0CodeInterpreter",
    "ModifyThreadRequestToolResourcesType0FileSearch",
    "OpenAIFile",
    "OpenAIFileObject",
    "OpenAIFilePurpose",
    "OpenAIFileStatus",
    "RunCompletionUsageType0",
    "RunStepCompletionUsageType0",
    "RunSteps",
    "RunStepsLastErrorType0",
    "RunStepsLastErrorType0Code",
    "RunStepsMetadataType0",
    "RunStepsObject",
    "RunStepsStatus",
    "RunStepStreamEventType0",
    "RunStepStreamEventType0Event",
    "RunStepStreamEventType1",
    "RunStepStreamEventType1Event",
    "RunStepStreamEventType2Event",
    "RunStepStreamEventType3",
    "RunStepStreamEventType3Event",
    "RunStepStreamEventType4",
    "RunStepStreamEventType4Event",
    "RunStepStreamEventType5",
    "RunStepStreamEventType5Event",
    "RunStepStreamEventType6",
    "RunStepStreamEventType6Event",
    "RunStepsType",
    "RunStreamEventType0",
    "RunStreamEventType0Event",
    "RunStreamEventType1",
    "RunStreamEventType1Event",
    "RunStreamEventType2",
    "RunStreamEventType2Event",
    "RunStreamEventType3",
    "RunStreamEventType3Event",
    "RunStreamEventType4",
    "RunStreamEventType4Event",
    "RunStreamEventType5",
    "RunStreamEventType5Event",
    "RunStreamEventType6",
    "RunStreamEventType6Event",
    "RunStreamEventType7",
    "RunStreamEventType7Event",
    "RunStreamEventType8",
    "RunStreamEventType8Event",
    "RunToolCallObject",
    "RunToolCallObjectFunction",
    "RunToolCallObjectType",
    "SubmitToolOutputsRunRequest",
    "SubmitToolOutputsRunRequestToolOutputsItem",
    "SystemMessage",
    "SystemMessageRole",
    "Text",
    "TextContentPart",
    "TextContentPartType",
    "TextText",
    "TextType",
    "TheMessageObject",
    "TheMessageObjectAttachmentsType0Item",
    "TheMessageObjectIncompleteDetailsType0",
    "TheMessageObjectIncompleteDetailsType0Reason",
    "TheMessageObjectMetadataType0",
    "TheMessageObjectObject",
    "TheMessageObjectRole",
    "TheMessageObjectStatus",
    "Thread",
    "ThreadMetadataType0",
    "ThreadObject",
    "ThreadStreamEventType0",
    "ThreadStreamEventType0Event",
    "ThreadToolResourcesType0",
    "ThreadToolResourcesType0CodeInterpreter",
    "ThreadToolResourcesType0FileSearch",
    "ThreadTruncationControls",
    "ThreadTruncationControlsType",
    "ToolCalls",
    "ToolCallsType",
    "ToolMessage",
    "ToolMessageRole",
    "TranscriptionSegment",
    "TranscriptionWord",
    "UpdateVectorStoreRequest",
    "UpdateVectorStoreRequestMetadataType0",
    "UserMessage",
    "UserMessageRole",
    "VectorStore",
    "VectorStoreExpirationPolicy",
    "VectorStoreExpirationPolicyAnchor",
    "VectorStoreFileBatch",
    "VectorStoreFileBatchFileCounts",
    "VectorStoreFileBatchObject",
    "VectorStoreFileBatchStatus",
    "VectorStoreFileCounts",
    "VectorStoreFiles",
    "VectorStoreFilesLastErrorType0",
    "VectorStoreFilesLastErrorType0Code",
    "VectorStoreFilesObject",
    "VectorStoreFilesStatus",
    "VectorStoreMetadataType0",
    "VectorStoreObject",
    "VectorStoreStatus",
)

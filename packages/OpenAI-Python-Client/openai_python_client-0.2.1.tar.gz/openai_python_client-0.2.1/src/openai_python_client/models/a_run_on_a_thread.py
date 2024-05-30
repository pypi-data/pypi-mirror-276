from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.a_run_on_a_thread_object import ARunOnAThreadObject
from ..models.a_run_on_a_thread_status import ARunOnAThreadStatus
from ..models.assistants_api_response_format_option_type_0 import AssistantsApiResponseFormatOptionType0
from ..models.assistants_api_tool_choice_option_type_0 import AssistantsApiToolChoiceOptionType0
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.a_run_on_a_thread_incomplete_details_type_0 import ARunOnAThreadIncompleteDetailsType0
    from ..models.a_run_on_a_thread_last_error_type_0 import ARunOnAThreadLastErrorType0
    from ..models.a_run_on_a_thread_metadata_type_0 import ARunOnAThreadMetadataType0
    from ..models.a_run_on_a_thread_required_action_type_0 import ARunOnAThreadRequiredActionType0
    from ..models.assistants_api_response_format import AssistantsApiResponseFormat
    from ..models.assistants_named_tool_choice import AssistantsNamedToolChoice
    from ..models.code_interpreter_tool import CodeInterpreterTool
    from ..models.file_search_tool import FileSearchTool
    from ..models.function_tool import FunctionTool
    from ..models.run_completion_usage_type_0 import RunCompletionUsageType0
    from ..models.thread_truncation_controls import ThreadTruncationControls


T = TypeVar("T", bound="ARunOnAThread")


@_attrs_define
class ARunOnAThread:
    """Represents an execution run on a [thread](/docs/api-reference/threads).

    Attributes:
        id (str): The identifier, which can be referenced in API endpoints.
        object_ (ARunOnAThreadObject): The object type, which is always `thread.run`.
        created_at (int): The Unix timestamp (in seconds) for when the run was created.
        thread_id (str): The ID of the [thread](/docs/api-reference/threads) that was executed on as a part of this run.
        assistant_id (str): The ID of the [assistant](/docs/api-reference/assistants) used for execution of this run.
        status (ARunOnAThreadStatus): The status of the run, which can be either `queued`, `in_progress`,
            `requires_action`, `cancelling`, `cancelled`, `failed`, `completed`, or `expired`.
        required_action (Union['ARunOnAThreadRequiredActionType0', None]): Details on the action required to continue
            the run. Will be `null` if no action is required.
        last_error (Union['ARunOnAThreadLastErrorType0', None]): The last error associated with this run. Will be `null`
            if there are no errors.
        expires_at (Union[None, int]): The Unix timestamp (in seconds) for when the run will expire.
        started_at (Union[None, int]): The Unix timestamp (in seconds) for when the run was started.
        cancelled_at (Union[None, int]): The Unix timestamp (in seconds) for when the run was cancelled.
        failed_at (Union[None, int]): The Unix timestamp (in seconds) for when the run failed.
        completed_at (Union[None, int]): The Unix timestamp (in seconds) for when the run was completed.
        incomplete_details (Union['ARunOnAThreadIncompleteDetailsType0', None]): Details on why the run is incomplete.
            Will be `null` if the run is not incomplete.
        model (str): The model that the [assistant](/docs/api-reference/assistants) used for this run.
        instructions (str): The instructions that the [assistant](/docs/api-reference/assistants) used for this run.
        tools (List[Union['CodeInterpreterTool', 'FileSearchTool', 'FunctionTool']]): The list of tools that the
            [assistant](/docs/api-reference/assistants) used for this run.
        metadata (Union['ARunOnAThreadMetadataType0', None]): Set of 16 key-value pairs that can be attached to an
            object. This can be useful for storing additional information about the object in a structured format. Keys can
            be a maximum of 64 characters long and values can be a maxium of 512 characters long.
        usage (Union['RunCompletionUsageType0', None]): Usage statistics related to the run. This value will be `null`
            if the run is not in a terminal state (i.e. `in_progress`, `queued`, etc.).
        max_prompt_tokens (Union[None, int]): The maximum number of prompt tokens specified to have been used over the
            course of the run.
        max_completion_tokens (Union[None, int]): The maximum number of completion tokens specified to have been used
            over the course of the run.
        truncation_strategy (ThreadTruncationControls): Controls for how a thread will be truncated prior to the run.
            Use this to control the intial context window of the run.
        tool_choice (Union['AssistantsNamedToolChoice', AssistantsApiToolChoiceOptionType0]): Controls which (if any)
            tool is called by the model.
            `none` means the model will not call any tools and instead generates a message.
            `auto` is the default value and means the model can pick between generating a message or calling one or more
            tools.
            `required` means the model must call one or more tools before responding to the user.
            Specifying a particular tool like `{"type": "file_search"}` or `{"type": "function", "function": {"name":
            "my_function"}}` forces the model to call that tool.
        response_format (Union['AssistantsApiResponseFormat', AssistantsApiResponseFormatOptionType0]): Specifies the
            format that the model must output. Compatible with [GPT-4 Turbo](/docs/models/gpt-4-and-gpt-4-turbo) and all
            GPT-3.5 Turbo models since `gpt-3.5-turbo-1106`.

            Setting to `{ "type": "json_object" }` enables JSON mode, which guarantees the message the model generates is
            valid JSON.

            **Important:** when using JSON mode, you **must** also instruct the model to produce JSON yourself via a system
            or user message. Without this, the model may generate an unending stream of whitespace until the generation
            reaches the token limit, resulting in a long-running and seemingly "stuck" request. Also note that the message
            content may be partially cut off if `finish_reason="length"`, which indicates the generation exceeded
            `max_tokens` or the conversation exceeded the max context length.
        temperature (Union[None, Unset, float]): The sampling temperature used for this run. If not set, defaults to 1.
        top_p (Union[None, Unset, float]): The nucleus sampling value used for this run. If not set, defaults to 1.
    """

    id: str
    object_: ARunOnAThreadObject
    created_at: int
    thread_id: str
    assistant_id: str
    status: ARunOnAThreadStatus
    required_action: Union["ARunOnAThreadRequiredActionType0", None]
    last_error: Union["ARunOnAThreadLastErrorType0", None]
    expires_at: Union[None, int]
    started_at: Union[None, int]
    cancelled_at: Union[None, int]
    failed_at: Union[None, int]
    completed_at: Union[None, int]
    incomplete_details: Union["ARunOnAThreadIncompleteDetailsType0", None]
    model: str
    instructions: str
    tools: List[Union["CodeInterpreterTool", "FileSearchTool", "FunctionTool"]]
    metadata: Union["ARunOnAThreadMetadataType0", None]
    usage: Union["RunCompletionUsageType0", None]
    max_prompt_tokens: Union[None, int]
    max_completion_tokens: Union[None, int]
    truncation_strategy: "ThreadTruncationControls"
    tool_choice: Union["AssistantsNamedToolChoice", AssistantsApiToolChoiceOptionType0]
    response_format: Union["AssistantsApiResponseFormat", AssistantsApiResponseFormatOptionType0]
    temperature: Union[None, Unset, float] = UNSET
    top_p: Union[None, Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.a_run_on_a_thread_incomplete_details_type_0 import ARunOnAThreadIncompleteDetailsType0
        from ..models.a_run_on_a_thread_last_error_type_0 import ARunOnAThreadLastErrorType0
        from ..models.a_run_on_a_thread_metadata_type_0 import ARunOnAThreadMetadataType0
        from ..models.a_run_on_a_thread_required_action_type_0 import ARunOnAThreadRequiredActionType0
        from ..models.code_interpreter_tool import CodeInterpreterTool
        from ..models.file_search_tool import FileSearchTool
        from ..models.run_completion_usage_type_0 import RunCompletionUsageType0

        id = self.id

        object_ = self.object_.value

        created_at = self.created_at

        thread_id = self.thread_id

        assistant_id = self.assistant_id

        status = self.status.value

        required_action: Union[Dict[str, Any], None]
        if isinstance(self.required_action, ARunOnAThreadRequiredActionType0):
            required_action = self.required_action.to_dict()
        else:
            required_action = self.required_action

        last_error: Union[Dict[str, Any], None]
        if isinstance(self.last_error, ARunOnAThreadLastErrorType0):
            last_error = self.last_error.to_dict()
        else:
            last_error = self.last_error

        expires_at: Union[None, int]
        expires_at = self.expires_at

        started_at: Union[None, int]
        started_at = self.started_at

        cancelled_at: Union[None, int]
        cancelled_at = self.cancelled_at

        failed_at: Union[None, int]
        failed_at = self.failed_at

        completed_at: Union[None, int]
        completed_at = self.completed_at

        incomplete_details: Union[Dict[str, Any], None]
        if isinstance(self.incomplete_details, ARunOnAThreadIncompleteDetailsType0):
            incomplete_details = self.incomplete_details.to_dict()
        else:
            incomplete_details = self.incomplete_details

        model = self.model

        instructions = self.instructions

        tools = []
        for tools_item_data in self.tools:
            tools_item: Dict[str, Any]
            if isinstance(tools_item_data, CodeInterpreterTool):
                tools_item = tools_item_data.to_dict()
            elif isinstance(tools_item_data, FileSearchTool):
                tools_item = tools_item_data.to_dict()
            else:
                tools_item = tools_item_data.to_dict()

            tools.append(tools_item)

        metadata: Union[Dict[str, Any], None]
        if isinstance(self.metadata, ARunOnAThreadMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        usage: Union[Dict[str, Any], None]
        if isinstance(self.usage, RunCompletionUsageType0):
            usage = self.usage.to_dict()
        else:
            usage = self.usage

        max_prompt_tokens: Union[None, int]
        max_prompt_tokens = self.max_prompt_tokens

        max_completion_tokens: Union[None, int]
        max_completion_tokens = self.max_completion_tokens

        truncation_strategy = self.truncation_strategy.to_dict()

        tool_choice: Union[Dict[str, Any], str]
        if isinstance(self.tool_choice, AssistantsApiToolChoiceOptionType0):
            tool_choice = self.tool_choice.value
        else:
            tool_choice = self.tool_choice.to_dict()

        response_format: Union[Dict[str, Any], str]
        if isinstance(self.response_format, AssistantsApiResponseFormatOptionType0):
            response_format = self.response_format.value
        else:
            response_format = self.response_format.to_dict()

        temperature: Union[None, Unset, float]
        if isinstance(self.temperature, Unset):
            temperature = UNSET
        else:
            temperature = self.temperature

        top_p: Union[None, Unset, float]
        if isinstance(self.top_p, Unset):
            top_p = UNSET
        else:
            top_p = self.top_p

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "object": object_,
                "created_at": created_at,
                "thread_id": thread_id,
                "assistant_id": assistant_id,
                "status": status,
                "required_action": required_action,
                "last_error": last_error,
                "expires_at": expires_at,
                "started_at": started_at,
                "cancelled_at": cancelled_at,
                "failed_at": failed_at,
                "completed_at": completed_at,
                "incomplete_details": incomplete_details,
                "model": model,
                "instructions": instructions,
                "tools": tools,
                "metadata": metadata,
                "usage": usage,
                "max_prompt_tokens": max_prompt_tokens,
                "max_completion_tokens": max_completion_tokens,
                "truncation_strategy": truncation_strategy,
                "tool_choice": tool_choice,
                "response_format": response_format,
            }
        )
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if top_p is not UNSET:
            field_dict["top_p"] = top_p

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.a_run_on_a_thread_incomplete_details_type_0 import ARunOnAThreadIncompleteDetailsType0
        from ..models.a_run_on_a_thread_last_error_type_0 import ARunOnAThreadLastErrorType0
        from ..models.a_run_on_a_thread_metadata_type_0 import ARunOnAThreadMetadataType0
        from ..models.a_run_on_a_thread_required_action_type_0 import ARunOnAThreadRequiredActionType0
        from ..models.assistants_api_response_format import AssistantsApiResponseFormat
        from ..models.assistants_named_tool_choice import AssistantsNamedToolChoice
        from ..models.code_interpreter_tool import CodeInterpreterTool
        from ..models.file_search_tool import FileSearchTool
        from ..models.function_tool import FunctionTool
        from ..models.run_completion_usage_type_0 import RunCompletionUsageType0
        from ..models.thread_truncation_controls import ThreadTruncationControls

        d = src_dict.copy()
        id = d.pop("id")

        object_ = ARunOnAThreadObject(d.pop("object"))

        created_at = d.pop("created_at")

        thread_id = d.pop("thread_id")

        assistant_id = d.pop("assistant_id")

        status = ARunOnAThreadStatus(d.pop("status"))

        def _parse_required_action(data: object) -> Union["ARunOnAThreadRequiredActionType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                required_action_type_0 = ARunOnAThreadRequiredActionType0.from_dict(data)

                return required_action_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ARunOnAThreadRequiredActionType0", None], data)

        required_action = _parse_required_action(d.pop("required_action"))

        def _parse_last_error(data: object) -> Union["ARunOnAThreadLastErrorType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                last_error_type_0 = ARunOnAThreadLastErrorType0.from_dict(data)

                return last_error_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ARunOnAThreadLastErrorType0", None], data)

        last_error = _parse_last_error(d.pop("last_error"))

        def _parse_expires_at(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        expires_at = _parse_expires_at(d.pop("expires_at"))

        def _parse_started_at(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        started_at = _parse_started_at(d.pop("started_at"))

        def _parse_cancelled_at(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        cancelled_at = _parse_cancelled_at(d.pop("cancelled_at"))

        def _parse_failed_at(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        failed_at = _parse_failed_at(d.pop("failed_at"))

        def _parse_completed_at(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        completed_at = _parse_completed_at(d.pop("completed_at"))

        def _parse_incomplete_details(data: object) -> Union["ARunOnAThreadIncompleteDetailsType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                incomplete_details_type_0 = ARunOnAThreadIncompleteDetailsType0.from_dict(data)

                return incomplete_details_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ARunOnAThreadIncompleteDetailsType0", None], data)

        incomplete_details = _parse_incomplete_details(d.pop("incomplete_details"))

        model = d.pop("model")

        instructions = d.pop("instructions")

        tools = []
        _tools = d.pop("tools")
        for tools_item_data in _tools:

            def _parse_tools_item(data: object) -> Union["CodeInterpreterTool", "FileSearchTool", "FunctionTool"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    tools_item_type_0 = CodeInterpreterTool.from_dict(data)

                    return tools_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    tools_item_type_1 = FileSearchTool.from_dict(data)

                    return tools_item_type_1
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                tools_item_type_2 = FunctionTool.from_dict(data)

                return tools_item_type_2

            tools_item = _parse_tools_item(tools_item_data)

            tools.append(tools_item)

        def _parse_metadata(data: object) -> Union["ARunOnAThreadMetadataType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = ARunOnAThreadMetadataType0.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ARunOnAThreadMetadataType0", None], data)

        metadata = _parse_metadata(d.pop("metadata"))

        def _parse_usage(data: object) -> Union["RunCompletionUsageType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_run_completion_usage_type_0 = RunCompletionUsageType0.from_dict(data)

                return componentsschemas_run_completion_usage_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RunCompletionUsageType0", None], data)

        usage = _parse_usage(d.pop("usage"))

        def _parse_max_prompt_tokens(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        max_prompt_tokens = _parse_max_prompt_tokens(d.pop("max_prompt_tokens"))

        def _parse_max_completion_tokens(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        max_completion_tokens = _parse_max_completion_tokens(d.pop("max_completion_tokens"))

        truncation_strategy = ThreadTruncationControls.from_dict(d.pop("truncation_strategy"))

        def _parse_tool_choice(data: object) -> Union["AssistantsNamedToolChoice", AssistantsApiToolChoiceOptionType0]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                componentsschemas_assistants_api_tool_choice_option_type_0 = AssistantsApiToolChoiceOptionType0(data)

                return componentsschemas_assistants_api_tool_choice_option_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_assistants_api_tool_choice_option_type_1 = AssistantsNamedToolChoice.from_dict(data)

            return componentsschemas_assistants_api_tool_choice_option_type_1

        tool_choice = _parse_tool_choice(d.pop("tool_choice"))

        def _parse_response_format(
            data: object,
        ) -> Union["AssistantsApiResponseFormat", AssistantsApiResponseFormatOptionType0]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                componentsschemas_assistants_api_response_format_option_type_0 = AssistantsApiResponseFormatOptionType0(
                    data
                )

                return componentsschemas_assistants_api_response_format_option_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_assistants_api_response_format_option_type_1 = AssistantsApiResponseFormat.from_dict(data)

            return componentsschemas_assistants_api_response_format_option_type_1

        response_format = _parse_response_format(d.pop("response_format"))

        def _parse_temperature(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        temperature = _parse_temperature(d.pop("temperature", UNSET))

        def _parse_top_p(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        top_p = _parse_top_p(d.pop("top_p", UNSET))

        a_run_on_a_thread = cls(
            id=id,
            object_=object_,
            created_at=created_at,
            thread_id=thread_id,
            assistant_id=assistant_id,
            status=status,
            required_action=required_action,
            last_error=last_error,
            expires_at=expires_at,
            started_at=started_at,
            cancelled_at=cancelled_at,
            failed_at=failed_at,
            completed_at=completed_at,
            incomplete_details=incomplete_details,
            model=model,
            instructions=instructions,
            tools=tools,
            metadata=metadata,
            usage=usage,
            max_prompt_tokens=max_prompt_tokens,
            max_completion_tokens=max_completion_tokens,
            truncation_strategy=truncation_strategy,
            tool_choice=tool_choice,
            response_format=response_format,
            temperature=temperature,
            top_p=top_p,
        )

        a_run_on_a_thread.additional_properties = d
        return a_run_on_a_thread

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

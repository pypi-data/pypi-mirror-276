from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.assistants_api_response_format_option_type_0 import AssistantsApiResponseFormatOptionType0
from ..models.assistants_api_tool_choice_option_type_0 import AssistantsApiToolChoiceOptionType0
from ..models.create_run_request_model_type_1 import CreateRunRequestModelType1
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.assistants_api_response_format import AssistantsApiResponseFormat
    from ..models.assistants_named_tool_choice import AssistantsNamedToolChoice
    from ..models.code_interpreter_tool import CodeInterpreterTool
    from ..models.create_message_request import CreateMessageRequest
    from ..models.create_run_request_metadata_type_0 import CreateRunRequestMetadataType0
    from ..models.file_search_tool import FileSearchTool
    from ..models.function_tool import FunctionTool
    from ..models.thread_truncation_controls import ThreadTruncationControls


T = TypeVar("T", bound="CreateRunRequest")


@_attrs_define
class CreateRunRequest:
    """
    Attributes:
        assistant_id (str): The ID of the [assistant](/docs/api-reference/assistants) to use to execute this run.
        model (Union[CreateRunRequestModelType1, None, Unset, str]): The ID of the [Model](/docs/api-reference/models)
            to be used to execute this run. If a value is provided here, it will override the model associated with the
            assistant. If not, the model associated with the assistant will be used. Example: gpt-4-turbo.
        instructions (Union[None, Unset, str]): Overrides the [instructions](/docs/api-
            reference/assistants/createAssistant) of the assistant. This is useful for modifying the behavior on a per-run
            basis.
        additional_instructions (Union[None, Unset, str]): Appends additional instructions at the end of the
            instructions for the run. This is useful for modifying the behavior on a per-run basis without overriding other
            instructions.
        additional_messages (Union[List['CreateMessageRequest'], None, Unset]): Adds additional messages to the thread
            before creating the run.
        tools (Union[List[Union['CodeInterpreterTool', 'FileSearchTool', 'FunctionTool']], None, Unset]): Override the
            tools the assistant can use for this run. This is useful for modifying the behavior on a per-run basis.
        metadata (Union['CreateRunRequestMetadataType0', None, Unset]): Set of 16 key-value pairs that can be attached
            to an object. This can be useful for storing additional information about the object in a structured format.
            Keys can be a maximum of 64 characters long and values can be a maxium of 512 characters long.
        temperature (Union[None, Unset, float]): What sampling temperature to use, between 0 and 2. Higher values like
            0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.
             Default: 1.0. Example: 1.
        top_p (Union[None, Unset, float]): An alternative to sampling with temperature, called nucleus sampling, where
            the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens
            comprising the top 10% probability mass are considered.

            We generally recommend altering this or temperature but not both.
             Default: 1.0. Example: 1.
        stream (Union[None, Unset, bool]): If `true`, returns a stream of events that happen during the Run as server-
            sent events, terminating when the Run enters a terminal state with a `data: [DONE]` message.
        max_prompt_tokens (Union[None, Unset, int]): The maximum number of prompt tokens that may be used over the
            course of the run. The run will make a best effort to use only the number of prompt tokens specified, across
            multiple turns of the run. If the run exceeds the number of prompt tokens specified, the run will end with
            status `incomplete`. See `incomplete_details` for more info.
        max_completion_tokens (Union[None, Unset, int]): The maximum number of completion tokens that may be used over
            the course of the run. The run will make a best effort to use only the number of completion tokens specified,
            across multiple turns of the run. If the run exceeds the number of completion tokens specified, the run will end
            with status `incomplete`. See `incomplete_details` for more info.
        truncation_strategy (Union[Unset, ThreadTruncationControls]): Controls for how a thread will be truncated prior
            to the run. Use this to control the intial context window of the run.
        tool_choice (Union['AssistantsNamedToolChoice', AssistantsApiToolChoiceOptionType0, Unset]): Controls which (if
            any) tool is called by the model.
            `none` means the model will not call any tools and instead generates a message.
            `auto` is the default value and means the model can pick between generating a message or calling one or more
            tools.
            `required` means the model must call one or more tools before responding to the user.
            Specifying a particular tool like `{"type": "file_search"}` or `{"type": "function", "function": {"name":
            "my_function"}}` forces the model to call that tool.
        response_format (Union['AssistantsApiResponseFormat', AssistantsApiResponseFormatOptionType0, Unset]): Specifies
            the format that the model must output. Compatible with [GPT-4 Turbo](/docs/models/gpt-4-and-gpt-4-turbo) and all
            GPT-3.5 Turbo models since `gpt-3.5-turbo-1106`.

            Setting to `{ "type": "json_object" }` enables JSON mode, which guarantees the message the model generates is
            valid JSON.

            **Important:** when using JSON mode, you **must** also instruct the model to produce JSON yourself via a system
            or user message. Without this, the model may generate an unending stream of whitespace until the generation
            reaches the token limit, resulting in a long-running and seemingly "stuck" request. Also note that the message
            content may be partially cut off if `finish_reason="length"`, which indicates the generation exceeded
            `max_tokens` or the conversation exceeded the max context length.
    """

    assistant_id: str
    model: Union[CreateRunRequestModelType1, None, Unset, str] = UNSET
    instructions: Union[None, Unset, str] = UNSET
    additional_instructions: Union[None, Unset, str] = UNSET
    additional_messages: Union[List["CreateMessageRequest"], None, Unset] = UNSET
    tools: Union[List[Union["CodeInterpreterTool", "FileSearchTool", "FunctionTool"]], None, Unset] = UNSET
    metadata: Union["CreateRunRequestMetadataType0", None, Unset] = UNSET
    temperature: Union[None, Unset, float] = 1.0
    top_p: Union[None, Unset, float] = 1.0
    stream: Union[None, Unset, bool] = UNSET
    max_prompt_tokens: Union[None, Unset, int] = UNSET
    max_completion_tokens: Union[None, Unset, int] = UNSET
    truncation_strategy: Union[Unset, "ThreadTruncationControls"] = UNSET
    tool_choice: Union["AssistantsNamedToolChoice", AssistantsApiToolChoiceOptionType0, Unset] = UNSET
    response_format: Union["AssistantsApiResponseFormat", AssistantsApiResponseFormatOptionType0, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        from ..models.code_interpreter_tool import CodeInterpreterTool
        from ..models.create_run_request_metadata_type_0 import CreateRunRequestMetadataType0
        from ..models.file_search_tool import FileSearchTool

        assistant_id = self.assistant_id

        model: Union[None, Unset, str]
        if isinstance(self.model, Unset):
            model = UNSET
        elif isinstance(self.model, CreateRunRequestModelType1):
            model = self.model.value
        else:
            model = self.model

        instructions: Union[None, Unset, str]
        if isinstance(self.instructions, Unset):
            instructions = UNSET
        else:
            instructions = self.instructions

        additional_instructions: Union[None, Unset, str]
        if isinstance(self.additional_instructions, Unset):
            additional_instructions = UNSET
        else:
            additional_instructions = self.additional_instructions

        additional_messages: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.additional_messages, Unset):
            additional_messages = UNSET
        elif isinstance(self.additional_messages, list):
            additional_messages = []
            for additional_messages_type_0_item_data in self.additional_messages:
                additional_messages_type_0_item = additional_messages_type_0_item_data.to_dict()
                additional_messages.append(additional_messages_type_0_item)

        else:
            additional_messages = self.additional_messages

        tools: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.tools, Unset):
            tools = UNSET
        elif isinstance(self.tools, list):
            tools = []
            for tools_type_0_item_data in self.tools:
                tools_type_0_item: Dict[str, Any]
                if isinstance(tools_type_0_item_data, CodeInterpreterTool):
                    tools_type_0_item = tools_type_0_item_data.to_dict()
                elif isinstance(tools_type_0_item_data, FileSearchTool):
                    tools_type_0_item = tools_type_0_item_data.to_dict()
                else:
                    tools_type_0_item = tools_type_0_item_data.to_dict()

                tools.append(tools_type_0_item)

        else:
            tools = self.tools

        metadata: Union[Dict[str, Any], None, Unset]
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, CreateRunRequestMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

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

        stream: Union[None, Unset, bool]
        if isinstance(self.stream, Unset):
            stream = UNSET
        else:
            stream = self.stream

        max_prompt_tokens: Union[None, Unset, int]
        if isinstance(self.max_prompt_tokens, Unset):
            max_prompt_tokens = UNSET
        else:
            max_prompt_tokens = self.max_prompt_tokens

        max_completion_tokens: Union[None, Unset, int]
        if isinstance(self.max_completion_tokens, Unset):
            max_completion_tokens = UNSET
        else:
            max_completion_tokens = self.max_completion_tokens

        truncation_strategy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.truncation_strategy, Unset):
            truncation_strategy = self.truncation_strategy.to_dict()

        tool_choice: Union[Dict[str, Any], Unset, str]
        if isinstance(self.tool_choice, Unset):
            tool_choice = UNSET
        elif isinstance(self.tool_choice, AssistantsApiToolChoiceOptionType0):
            tool_choice = self.tool_choice.value
        else:
            tool_choice = self.tool_choice.to_dict()

        response_format: Union[Dict[str, Any], Unset, str]
        if isinstance(self.response_format, Unset):
            response_format = UNSET
        elif isinstance(self.response_format, AssistantsApiResponseFormatOptionType0):
            response_format = self.response_format.value
        else:
            response_format = self.response_format.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "assistant_id": assistant_id,
            }
        )
        if model is not UNSET:
            field_dict["model"] = model
        if instructions is not UNSET:
            field_dict["instructions"] = instructions
        if additional_instructions is not UNSET:
            field_dict["additional_instructions"] = additional_instructions
        if additional_messages is not UNSET:
            field_dict["additional_messages"] = additional_messages
        if tools is not UNSET:
            field_dict["tools"] = tools
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if top_p is not UNSET:
            field_dict["top_p"] = top_p
        if stream is not UNSET:
            field_dict["stream"] = stream
        if max_prompt_tokens is not UNSET:
            field_dict["max_prompt_tokens"] = max_prompt_tokens
        if max_completion_tokens is not UNSET:
            field_dict["max_completion_tokens"] = max_completion_tokens
        if truncation_strategy is not UNSET:
            field_dict["truncation_strategy"] = truncation_strategy
        if tool_choice is not UNSET:
            field_dict["tool_choice"] = tool_choice
        if response_format is not UNSET:
            field_dict["response_format"] = response_format

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.assistants_api_response_format import AssistantsApiResponseFormat
        from ..models.assistants_named_tool_choice import AssistantsNamedToolChoice
        from ..models.code_interpreter_tool import CodeInterpreterTool
        from ..models.create_message_request import CreateMessageRequest
        from ..models.create_run_request_metadata_type_0 import CreateRunRequestMetadataType0
        from ..models.file_search_tool import FileSearchTool
        from ..models.function_tool import FunctionTool
        from ..models.thread_truncation_controls import ThreadTruncationControls

        d = src_dict.copy()
        assistant_id = d.pop("assistant_id")

        def _parse_model(data: object) -> Union[CreateRunRequestModelType1, None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                model_type_1 = CreateRunRequestModelType1(data)

                return model_type_1
            except:  # noqa: E722
                pass
            return cast(Union[CreateRunRequestModelType1, None, Unset, str], data)

        model = _parse_model(d.pop("model", UNSET))

        def _parse_instructions(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        instructions = _parse_instructions(d.pop("instructions", UNSET))

        def _parse_additional_instructions(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        additional_instructions = _parse_additional_instructions(d.pop("additional_instructions", UNSET))

        def _parse_additional_messages(data: object) -> Union[List["CreateMessageRequest"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                additional_messages_type_0 = []
                _additional_messages_type_0 = data
                for additional_messages_type_0_item_data in _additional_messages_type_0:
                    additional_messages_type_0_item = CreateMessageRequest.from_dict(
                        additional_messages_type_0_item_data
                    )

                    additional_messages_type_0.append(additional_messages_type_0_item)

                return additional_messages_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["CreateMessageRequest"], None, Unset], data)

        additional_messages = _parse_additional_messages(d.pop("additional_messages", UNSET))

        def _parse_tools(
            data: object,
        ) -> Union[List[Union["CodeInterpreterTool", "FileSearchTool", "FunctionTool"]], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tools_type_0 = []
                _tools_type_0 = data
                for tools_type_0_item_data in _tools_type_0:

                    def _parse_tools_type_0_item(
                        data: object,
                    ) -> Union["CodeInterpreterTool", "FileSearchTool", "FunctionTool"]:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            tools_type_0_item_type_0 = CodeInterpreterTool.from_dict(data)

                            return tools_type_0_item_type_0
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            tools_type_0_item_type_1 = FileSearchTool.from_dict(data)

                            return tools_type_0_item_type_1
                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        tools_type_0_item_type_2 = FunctionTool.from_dict(data)

                        return tools_type_0_item_type_2

                    tools_type_0_item = _parse_tools_type_0_item(tools_type_0_item_data)

                    tools_type_0.append(tools_type_0_item)

                return tools_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[Union["CodeInterpreterTool", "FileSearchTool", "FunctionTool"]], None, Unset], data)

        tools = _parse_tools(d.pop("tools", UNSET))

        def _parse_metadata(data: object) -> Union["CreateRunRequestMetadataType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = CreateRunRequestMetadataType0.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CreateRunRequestMetadataType0", None, Unset], data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

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

        def _parse_stream(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        stream = _parse_stream(d.pop("stream", UNSET))

        def _parse_max_prompt_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_prompt_tokens = _parse_max_prompt_tokens(d.pop("max_prompt_tokens", UNSET))

        def _parse_max_completion_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_completion_tokens = _parse_max_completion_tokens(d.pop("max_completion_tokens", UNSET))

        _truncation_strategy = d.pop("truncation_strategy", UNSET)
        truncation_strategy: Union[Unset, ThreadTruncationControls]
        if isinstance(_truncation_strategy, Unset):
            truncation_strategy = UNSET
        else:
            truncation_strategy = ThreadTruncationControls.from_dict(_truncation_strategy)

        def _parse_tool_choice(
            data: object,
        ) -> Union["AssistantsNamedToolChoice", AssistantsApiToolChoiceOptionType0, Unset]:
            if isinstance(data, Unset):
                return data
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

        tool_choice = _parse_tool_choice(d.pop("tool_choice", UNSET))

        def _parse_response_format(
            data: object,
        ) -> Union["AssistantsApiResponseFormat", AssistantsApiResponseFormatOptionType0, Unset]:
            if isinstance(data, Unset):
                return data
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

        response_format = _parse_response_format(d.pop("response_format", UNSET))

        create_run_request = cls(
            assistant_id=assistant_id,
            model=model,
            instructions=instructions,
            additional_instructions=additional_instructions,
            additional_messages=additional_messages,
            tools=tools,
            metadata=metadata,
            temperature=temperature,
            top_p=top_p,
            stream=stream,
            max_prompt_tokens=max_prompt_tokens,
            max_completion_tokens=max_completion_tokens,
            truncation_strategy=truncation_strategy,
            tool_choice=tool_choice,
            response_format=response_format,
        )

        return create_run_request

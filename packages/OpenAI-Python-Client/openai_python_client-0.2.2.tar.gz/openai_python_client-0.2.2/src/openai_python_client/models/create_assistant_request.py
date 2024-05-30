from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.assistants_api_response_format_option_type_0 import AssistantsApiResponseFormatOptionType0
from ..models.create_assistant_request_model_type_1 import CreateAssistantRequestModelType1
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.assistants_api_response_format import AssistantsApiResponseFormat
    from ..models.code_interpreter_tool import CodeInterpreterTool
    from ..models.create_assistant_request_metadata_type_0 import CreateAssistantRequestMetadataType0
    from ..models.create_assistant_request_tool_resources_type_0 import CreateAssistantRequestToolResourcesType0
    from ..models.file_search_tool import FileSearchTool
    from ..models.function_tool import FunctionTool


T = TypeVar("T", bound="CreateAssistantRequest")


@_attrs_define
class CreateAssistantRequest:
    """
    Attributes:
        model (Union[CreateAssistantRequestModelType1, str]): ID of the model to use. You can use the [List
            models](/docs/api-reference/models/list) API to see all of your available models, or see our [Model
            overview](/docs/models/overview) for descriptions of them.
             Example: gpt-4-turbo.
        name (Union[None, Unset, str]): The name of the assistant. The maximum length is 256 characters.
        description (Union[None, Unset, str]): The description of the assistant. The maximum length is 512 characters.
        instructions (Union[None, Unset, str]): The system instructions that the assistant uses. The maximum length is
            256,000 characters.
        tools (Union[Unset, List[Union['CodeInterpreterTool', 'FileSearchTool', 'FunctionTool']]]): A list of tool
            enabled on the assistant. There can be a maximum of 128 tools per assistant. Tools can be of types
            `code_interpreter`, `file_search`, or `function`.
        tool_resources (Union['CreateAssistantRequestToolResourcesType0', None, Unset]): A set of resources that are
            used by the assistant's tools. The resources are specific to the type of tool. For example, the
            `code_interpreter` tool requires a list of file IDs, while the `file_search` tool requires a list of vector
            store IDs.
        metadata (Union['CreateAssistantRequestMetadataType0', None, Unset]): Set of 16 key-value pairs that can be
            attached to an object. This can be useful for storing additional information about the object in a structured
            format. Keys can be a maximum of 64 characters long and values can be a maxium of 512 characters long.
        temperature (Union[None, Unset, float]): What sampling temperature to use, between 0 and 2. Higher values like
            0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.
             Default: 1.0. Example: 1.
        top_p (Union[None, Unset, float]): An alternative to sampling with temperature, called nucleus sampling, where
            the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens
            comprising the top 10% probability mass are considered.

            We generally recommend altering this or temperature but not both.
             Default: 1.0. Example: 1.
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

    model: Union[CreateAssistantRequestModelType1, str]
    name: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    instructions: Union[None, Unset, str] = UNSET
    tools: Union[Unset, List[Union["CodeInterpreterTool", "FileSearchTool", "FunctionTool"]]] = UNSET
    tool_resources: Union["CreateAssistantRequestToolResourcesType0", None, Unset] = UNSET
    metadata: Union["CreateAssistantRequestMetadataType0", None, Unset] = UNSET
    temperature: Union[None, Unset, float] = 1.0
    top_p: Union[None, Unset, float] = 1.0
    response_format: Union["AssistantsApiResponseFormat", AssistantsApiResponseFormatOptionType0, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        from ..models.code_interpreter_tool import CodeInterpreterTool
        from ..models.create_assistant_request_metadata_type_0 import CreateAssistantRequestMetadataType0
        from ..models.create_assistant_request_tool_resources_type_0 import CreateAssistantRequestToolResourcesType0
        from ..models.file_search_tool import FileSearchTool

        model: str
        if isinstance(self.model, CreateAssistantRequestModelType1):
            model = self.model.value
        else:
            model = self.model

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        instructions: Union[None, Unset, str]
        if isinstance(self.instructions, Unset):
            instructions = UNSET
        else:
            instructions = self.instructions

        tools: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.tools, Unset):
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

        tool_resources: Union[Dict[str, Any], None, Unset]
        if isinstance(self.tool_resources, Unset):
            tool_resources = UNSET
        elif isinstance(self.tool_resources, CreateAssistantRequestToolResourcesType0):
            tool_resources = self.tool_resources.to_dict()
        else:
            tool_resources = self.tool_resources

        metadata: Union[Dict[str, Any], None, Unset]
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, CreateAssistantRequestMetadataType0):
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
                "model": model,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if instructions is not UNSET:
            field_dict["instructions"] = instructions
        if tools is not UNSET:
            field_dict["tools"] = tools
        if tool_resources is not UNSET:
            field_dict["tool_resources"] = tool_resources
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if top_p is not UNSET:
            field_dict["top_p"] = top_p
        if response_format is not UNSET:
            field_dict["response_format"] = response_format

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.assistants_api_response_format import AssistantsApiResponseFormat
        from ..models.code_interpreter_tool import CodeInterpreterTool
        from ..models.create_assistant_request_metadata_type_0 import CreateAssistantRequestMetadataType0
        from ..models.create_assistant_request_tool_resources_type_0 import CreateAssistantRequestToolResourcesType0
        from ..models.file_search_tool import FileSearchTool
        from ..models.function_tool import FunctionTool

        d = src_dict.copy()

        def _parse_model(data: object) -> Union[CreateAssistantRequestModelType1, str]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                model_type_1 = CreateAssistantRequestModelType1(data)

                return model_type_1
            except:  # noqa: E722
                pass
            return cast(Union[CreateAssistantRequestModelType1, str], data)

        model = _parse_model(d.pop("model"))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_instructions(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        instructions = _parse_instructions(d.pop("instructions", UNSET))

        tools = []
        _tools = d.pop("tools", UNSET)
        for tools_item_data in _tools or []:

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

        def _parse_tool_resources(data: object) -> Union["CreateAssistantRequestToolResourcesType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                tool_resources_type_0 = CreateAssistantRequestToolResourcesType0.from_dict(data)

                return tool_resources_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CreateAssistantRequestToolResourcesType0", None, Unset], data)

        tool_resources = _parse_tool_resources(d.pop("tool_resources", UNSET))

        def _parse_metadata(data: object) -> Union["CreateAssistantRequestMetadataType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = CreateAssistantRequestMetadataType0.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CreateAssistantRequestMetadataType0", None, Unset], data)

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

        create_assistant_request = cls(
            model=model,
            name=name,
            description=description,
            instructions=instructions,
            tools=tools,
            tool_resources=tool_resources,
            metadata=metadata,
            temperature=temperature,
            top_p=top_p,
            response_format=response_format,
        )

        return create_assistant_request

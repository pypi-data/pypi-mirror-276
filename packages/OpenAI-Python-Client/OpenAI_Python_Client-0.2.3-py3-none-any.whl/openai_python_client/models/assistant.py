from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.assistant_object import AssistantObject
from ..models.assistants_api_response_format_option_type_0 import AssistantsApiResponseFormatOptionType0
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.assistant_metadata_type_0 import AssistantMetadataType0
    from ..models.assistant_tool_resources_type_0 import AssistantToolResourcesType0
    from ..models.assistants_api_response_format import AssistantsApiResponseFormat
    from ..models.code_interpreter_tool import CodeInterpreterTool
    from ..models.file_search_tool import FileSearchTool
    from ..models.function_tool import FunctionTool


T = TypeVar("T", bound="Assistant")


@_attrs_define
class Assistant:
    """Represents an `assistant` that can call the model and use tools.

    Attributes:
        id (str): The identifier, which can be referenced in API endpoints.
        object_ (AssistantObject): The object type, which is always `assistant`.
        created_at (int): The Unix timestamp (in seconds) for when the assistant was created.
        name (Union[None, str]): The name of the assistant. The maximum length is 256 characters.
        description (Union[None, str]): The description of the assistant. The maximum length is 512 characters.
        model (str): ID of the model to use. You can use the [List models](/docs/api-reference/models/list) API to see
            all of your available models, or see our [Model overview](/docs/models/overview) for descriptions of them.
        instructions (Union[None, str]): The system instructions that the assistant uses. The maximum length is 256,000
            characters.
        tools (List[Union['CodeInterpreterTool', 'FileSearchTool', 'FunctionTool']]): A list of tool enabled on the
            assistant. There can be a maximum of 128 tools per assistant. Tools can be of types `code_interpreter`,
            `file_search`, or `function`.
        metadata (Union['AssistantMetadataType0', None]): Set of 16 key-value pairs that can be attached to an object.
            This can be useful for storing additional information about the object in a structured format. Keys can be a
            maximum of 64 characters long and values can be a maxium of 512 characters long.
        tool_resources (Union['AssistantToolResourcesType0', None, Unset]): A set of resources that are used by the
            assistant's tools. The resources are specific to the type of tool. For example, the `code_interpreter` tool
            requires a list of file IDs, while the `file_search` tool requires a list of vector store IDs.
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

    id: str
    object_: AssistantObject
    created_at: int
    name: Union[None, str]
    description: Union[None, str]
    model: str
    instructions: Union[None, str]
    tools: List[Union["CodeInterpreterTool", "FileSearchTool", "FunctionTool"]]
    metadata: Union["AssistantMetadataType0", None]
    tool_resources: Union["AssistantToolResourcesType0", None, Unset] = UNSET
    temperature: Union[None, Unset, float] = 1.0
    top_p: Union[None, Unset, float] = 1.0
    response_format: Union["AssistantsApiResponseFormat", AssistantsApiResponseFormatOptionType0, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.assistant_metadata_type_0 import AssistantMetadataType0
        from ..models.assistant_tool_resources_type_0 import AssistantToolResourcesType0
        from ..models.code_interpreter_tool import CodeInterpreterTool
        from ..models.file_search_tool import FileSearchTool

        id = self.id

        object_ = self.object_.value

        created_at = self.created_at

        name: Union[None, str]
        name = self.name

        description: Union[None, str]
        description = self.description

        model = self.model

        instructions: Union[None, str]
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
        if isinstance(self.metadata, AssistantMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        tool_resources: Union[Dict[str, Any], None, Unset]
        if isinstance(self.tool_resources, Unset):
            tool_resources = UNSET
        elif isinstance(self.tool_resources, AssistantToolResourcesType0):
            tool_resources = self.tool_resources.to_dict()
        else:
            tool_resources = self.tool_resources

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
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "object": object_,
                "created_at": created_at,
                "name": name,
                "description": description,
                "model": model,
                "instructions": instructions,
                "tools": tools,
                "metadata": metadata,
            }
        )
        if tool_resources is not UNSET:
            field_dict["tool_resources"] = tool_resources
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if top_p is not UNSET:
            field_dict["top_p"] = top_p
        if response_format is not UNSET:
            field_dict["response_format"] = response_format

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.assistant_metadata_type_0 import AssistantMetadataType0
        from ..models.assistant_tool_resources_type_0 import AssistantToolResourcesType0
        from ..models.assistants_api_response_format import AssistantsApiResponseFormat
        from ..models.code_interpreter_tool import CodeInterpreterTool
        from ..models.file_search_tool import FileSearchTool
        from ..models.function_tool import FunctionTool

        d = src_dict.copy()
        id = d.pop("id")

        object_ = AssistantObject(d.pop("object"))

        created_at = d.pop("created_at")

        def _parse_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        name = _parse_name(d.pop("name"))

        def _parse_description(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        description = _parse_description(d.pop("description"))

        model = d.pop("model")

        def _parse_instructions(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        instructions = _parse_instructions(d.pop("instructions"))

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

        def _parse_metadata(data: object) -> Union["AssistantMetadataType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = AssistantMetadataType0.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["AssistantMetadataType0", None], data)

        metadata = _parse_metadata(d.pop("metadata"))

        def _parse_tool_resources(data: object) -> Union["AssistantToolResourcesType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                tool_resources_type_0 = AssistantToolResourcesType0.from_dict(data)

                return tool_resources_type_0
            except:  # noqa: E722
                pass
            return cast(Union["AssistantToolResourcesType0", None, Unset], data)

        tool_resources = _parse_tool_resources(d.pop("tool_resources", UNSET))

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

        assistant = cls(
            id=id,
            object_=object_,
            created_at=created_at,
            name=name,
            description=description,
            model=model,
            instructions=instructions,
            tools=tools,
            metadata=metadata,
            tool_resources=tool_resources,
            temperature=temperature,
            top_p=top_p,
            response_format=response_format,
        )

        assistant.additional_properties = d
        return assistant

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

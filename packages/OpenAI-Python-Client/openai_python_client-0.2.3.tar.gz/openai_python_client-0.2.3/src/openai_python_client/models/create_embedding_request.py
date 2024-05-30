from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.create_embedding_request_encoding_format import CreateEmbeddingRequestEncodingFormat
from ..models.create_embedding_request_model_type_1 import CreateEmbeddingRequestModelType1
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateEmbeddingRequest")


@_attrs_define
class CreateEmbeddingRequest:
    """
    Attributes:
        input_ (Union[List[List[int]], List[int], List[str], str]): Input text to embed, encoded as a string or array of
            tokens. To embed multiple inputs in a single request, pass an array of strings or array of token arrays. The
            input must not exceed the max input tokens for the model (8192 tokens for `text-embedding-ada-002`), cannot be
            an empty string, and any array must be 2048 dimensions or less. [Example Python
            code](https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken) for counting tokens.
             Example: The quick brown fox jumped over the lazy dog.
        model (Union[CreateEmbeddingRequestModelType1, str]): ID of the model to use. You can use the [List
            models](/docs/api-reference/models/list) API to see all of your available models, or see our [Model
            overview](/docs/models/overview) for descriptions of them.
             Example: text-embedding-3-small.
        encoding_format (Union[Unset, CreateEmbeddingRequestEncodingFormat]): The format to return the embeddings in.
            Can be either `float` or [`base64`](https://pypi.org/project/pybase64/). Default:
            CreateEmbeddingRequestEncodingFormat.FLOAT. Example: float.
        dimensions (Union[Unset, int]): The number of dimensions the resulting output embeddings should have. Only
            supported in `text-embedding-3` and later models.
        user (Union[Unset, str]): A unique identifier representing your end-user, which can help OpenAI to monitor and
            detect abuse. [Learn more](/docs/guides/safety-best-practices/end-user-ids).
             Example: user-1234.
    """

    input_: Union[List[List[int]], List[int], List[str], str]
    model: Union[CreateEmbeddingRequestModelType1, str]
    encoding_format: Union[Unset, CreateEmbeddingRequestEncodingFormat] = CreateEmbeddingRequestEncodingFormat.FLOAT
    dimensions: Union[Unset, int] = UNSET
    user: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        input_: Union[List[List[int]], List[int], List[str], str]
        if isinstance(self.input_, list):
            input_ = self.input_

        elif isinstance(self.input_, list):
            input_ = self.input_

        elif isinstance(self.input_, list):
            input_ = []
            for input_type_3_item_data in self.input_:
                input_type_3_item = input_type_3_item_data

                input_.append(input_type_3_item)

        else:
            input_ = self.input_

        model: str
        if isinstance(self.model, CreateEmbeddingRequestModelType1):
            model = self.model.value
        else:
            model = self.model

        encoding_format: Union[Unset, str] = UNSET
        if not isinstance(self.encoding_format, Unset):
            encoding_format = self.encoding_format.value

        dimensions = self.dimensions

        user = self.user

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "input": input_,
                "model": model,
            }
        )
        if encoding_format is not UNSET:
            field_dict["encoding_format"] = encoding_format
        if dimensions is not UNSET:
            field_dict["dimensions"] = dimensions
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_input_(data: object) -> Union[List[List[int]], List[int], List[str], str]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                input_type_1 = cast(List[str], data)

                return input_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                input_type_2 = cast(List[int], data)

                return input_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                input_type_3 = []
                _input_type_3 = data
                for input_type_3_item_data in _input_type_3:
                    input_type_3_item = cast(List[int], input_type_3_item_data)

                    input_type_3.append(input_type_3_item)

                return input_type_3
            except:  # noqa: E722
                pass
            return cast(Union[List[List[int]], List[int], List[str], str], data)

        input_ = _parse_input_(d.pop("input"))

        def _parse_model(data: object) -> Union[CreateEmbeddingRequestModelType1, str]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                model_type_1 = CreateEmbeddingRequestModelType1(data)

                return model_type_1
            except:  # noqa: E722
                pass
            return cast(Union[CreateEmbeddingRequestModelType1, str], data)

        model = _parse_model(d.pop("model"))

        _encoding_format = d.pop("encoding_format", UNSET)
        encoding_format: Union[Unset, CreateEmbeddingRequestEncodingFormat]
        if isinstance(_encoding_format, Unset):
            encoding_format = UNSET
        else:
            encoding_format = CreateEmbeddingRequestEncodingFormat(_encoding_format)

        dimensions = d.pop("dimensions", UNSET)

        user = d.pop("user", UNSET)

        create_embedding_request = cls(
            input_=input_,
            model=model,
            encoding_format=encoding_format,
            dimensions=dimensions,
            user=user,
        )

        return create_embedding_request

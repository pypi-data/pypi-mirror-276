from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.embedding_object import EmbeddingObject

T = TypeVar("T", bound="Embedding")


@_attrs_define
class Embedding:
    """Represents an embedding vector returned by embedding endpoint.

    Attributes:
        index (int): The index of the embedding in the list of embeddings.
        embedding (List[float]): The embedding vector, which is a list of floats. The length of vector depends on the
            model as listed in the [embedding guide](/docs/guides/embeddings).
        object_ (EmbeddingObject): The object type, which is always "embedding".
    """

    index: int
    embedding: List[float]
    object_: EmbeddingObject
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        index = self.index

        embedding = self.embedding

        object_ = self.object_.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "index": index,
                "embedding": embedding,
                "object": object_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        index = d.pop("index")

        embedding = cast(List[float], d.pop("embedding"))

        object_ = EmbeddingObject(d.pop("object"))

        embedding = cls(
            index=index,
            embedding=embedding,
            object_=object_,
        )

        embedding.additional_properties = d
        return embedding

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

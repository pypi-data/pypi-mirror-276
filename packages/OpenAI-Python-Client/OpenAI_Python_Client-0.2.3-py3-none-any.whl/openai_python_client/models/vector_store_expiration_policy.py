from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.vector_store_expiration_policy_anchor import VectorStoreExpirationPolicyAnchor

T = TypeVar("T", bound="VectorStoreExpirationPolicy")


@_attrs_define
class VectorStoreExpirationPolicy:
    """The expiration policy for a vector store.

    Attributes:
        anchor (VectorStoreExpirationPolicyAnchor): Anchor timestamp after which the expiration policy applies.
            Supported anchors: `last_active_at`.
        days (int): The number of days after the anchor time that the vector store will expire.
    """

    anchor: VectorStoreExpirationPolicyAnchor
    days: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        anchor = self.anchor.value

        days = self.days

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "anchor": anchor,
                "days": days,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        anchor = VectorStoreExpirationPolicyAnchor(d.pop("anchor"))

        days = d.pop("days")

        vector_store_expiration_policy = cls(
            anchor=anchor,
            days=days,
        )

        vector_store_expiration_policy.additional_properties = d
        return vector_store_expiration_policy

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

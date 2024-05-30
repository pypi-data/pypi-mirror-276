from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreateModerationResponseResultsItemCategoryScores")


@_attrs_define
class CreateModerationResponseResultsItemCategoryScores:
    """A list of the categories along with their scores as predicted by model.

    Attributes:
        hate (float): The score for the category 'hate'.
        hatethreatening (float): The score for the category 'hate/threatening'.
        harassment (float): The score for the category 'harassment'.
        harassmentthreatening (float): The score for the category 'harassment/threatening'.
        self_harm (float): The score for the category 'self-harm'.
        self_harmintent (float): The score for the category 'self-harm/intent'.
        self_harminstructions (float): The score for the category 'self-harm/instructions'.
        sexual (float): The score for the category 'sexual'.
        sexualminors (float): The score for the category 'sexual/minors'.
        violence (float): The score for the category 'violence'.
        violencegraphic (float): The score for the category 'violence/graphic'.
    """

    hate: float
    hatethreatening: float
    harassment: float
    harassmentthreatening: float
    self_harm: float
    self_harmintent: float
    self_harminstructions: float
    sexual: float
    sexualminors: float
    violence: float
    violencegraphic: float
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        hate = self.hate

        hatethreatening = self.hatethreatening

        harassment = self.harassment

        harassmentthreatening = self.harassmentthreatening

        self_harm = self.self_harm

        self_harmintent = self.self_harmintent

        self_harminstructions = self.self_harminstructions

        sexual = self.sexual

        sexualminors = self.sexualminors

        violence = self.violence

        violencegraphic = self.violencegraphic

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "hate": hate,
                "hate/threatening": hatethreatening,
                "harassment": harassment,
                "harassment/threatening": harassmentthreatening,
                "self-harm": self_harm,
                "self-harm/intent": self_harmintent,
                "self-harm/instructions": self_harminstructions,
                "sexual": sexual,
                "sexual/minors": sexualminors,
                "violence": violence,
                "violence/graphic": violencegraphic,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        hate = d.pop("hate")

        hatethreatening = d.pop("hate/threatening")

        harassment = d.pop("harassment")

        harassmentthreatening = d.pop("harassment/threatening")

        self_harm = d.pop("self-harm")

        self_harmintent = d.pop("self-harm/intent")

        self_harminstructions = d.pop("self-harm/instructions")

        sexual = d.pop("sexual")

        sexualminors = d.pop("sexual/minors")

        violence = d.pop("violence")

        violencegraphic = d.pop("violence/graphic")

        create_moderation_response_results_item_category_scores = cls(
            hate=hate,
            hatethreatening=hatethreatening,
            harassment=harassment,
            harassmentthreatening=harassmentthreatening,
            self_harm=self_harm,
            self_harmintent=self_harmintent,
            self_harminstructions=self_harminstructions,
            sexual=sexual,
            sexualminors=sexualminors,
            violence=violence,
            violencegraphic=violencegraphic,
        )

        create_moderation_response_results_item_category_scores.additional_properties = d
        return create_moderation_response_results_item_category_scores

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

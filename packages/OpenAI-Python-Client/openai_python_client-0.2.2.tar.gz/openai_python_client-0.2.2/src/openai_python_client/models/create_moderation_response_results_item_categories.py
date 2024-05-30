from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreateModerationResponseResultsItemCategories")


@_attrs_define
class CreateModerationResponseResultsItemCategories:
    """A list of the categories, and whether they are flagged or not.

    Attributes:
        hate (bool): Content that expresses, incites, or promotes hate based on race, gender, ethnicity, religion,
            nationality, sexual orientation, disability status, or caste. Hateful content aimed at non-protected groups
            (e.g., chess players) is harassment.
        hatethreatening (bool): Hateful content that also includes violence or serious harm towards the targeted group
            based on race, gender, ethnicity, religion, nationality, sexual orientation, disability status, or caste.
        harassment (bool): Content that expresses, incites, or promotes harassing language towards any target.
        harassmentthreatening (bool): Harassment content that also includes violence or serious harm towards any target.
        self_harm (bool): Content that promotes, encourages, or depicts acts of self-harm, such as suicide, cutting, and
            eating disorders.
        self_harmintent (bool): Content where the speaker expresses that they are engaging or intend to engage in acts
            of self-harm, such as suicide, cutting, and eating disorders.
        self_harminstructions (bool): Content that encourages performing acts of self-harm, such as suicide, cutting,
            and eating disorders, or that gives instructions or advice on how to commit such acts.
        sexual (bool): Content meant to arouse sexual excitement, such as the description of sexual activity, or that
            promotes sexual services (excluding sex education and wellness).
        sexualminors (bool): Sexual content that includes an individual who is under 18 years old.
        violence (bool): Content that depicts death, violence, or physical injury.
        violencegraphic (bool): Content that depicts death, violence, or physical injury in graphic detail.
    """

    hate: bool
    hatethreatening: bool
    harassment: bool
    harassmentthreatening: bool
    self_harm: bool
    self_harmintent: bool
    self_harminstructions: bool
    sexual: bool
    sexualminors: bool
    violence: bool
    violencegraphic: bool
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

        create_moderation_response_results_item_categories = cls(
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

        create_moderation_response_results_item_categories.additional_properties = d
        return create_moderation_response_results_item_categories

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

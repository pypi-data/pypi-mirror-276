from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.submit_tool_outputs_run_request_tool_outputs_item import SubmitToolOutputsRunRequestToolOutputsItem


T = TypeVar("T", bound="SubmitToolOutputsRunRequest")


@_attrs_define
class SubmitToolOutputsRunRequest:
    """
    Attributes:
        tool_outputs (List['SubmitToolOutputsRunRequestToolOutputsItem']): A list of tools for which the outputs are
            being submitted.
        stream (Union[None, Unset, bool]): If `true`, returns a stream of events that happen during the Run as server-
            sent events, terminating when the Run enters a terminal state with a `data: [DONE]` message.
    """

    tool_outputs: List["SubmitToolOutputsRunRequestToolOutputsItem"]
    stream: Union[None, Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        tool_outputs = []
        for tool_outputs_item_data in self.tool_outputs:
            tool_outputs_item = tool_outputs_item_data.to_dict()
            tool_outputs.append(tool_outputs_item)

        stream: Union[None, Unset, bool]
        if isinstance(self.stream, Unset):
            stream = UNSET
        else:
            stream = self.stream

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "tool_outputs": tool_outputs,
            }
        )
        if stream is not UNSET:
            field_dict["stream"] = stream

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.submit_tool_outputs_run_request_tool_outputs_item import (
            SubmitToolOutputsRunRequestToolOutputsItem,
        )

        d = src_dict.copy()
        tool_outputs = []
        _tool_outputs = d.pop("tool_outputs")
        for tool_outputs_item_data in _tool_outputs:
            tool_outputs_item = SubmitToolOutputsRunRequestToolOutputsItem.from_dict(tool_outputs_item_data)

            tool_outputs.append(tool_outputs_item)

        def _parse_stream(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        stream = _parse_stream(d.pop("stream", UNSET))

        submit_tool_outputs_run_request = cls(
            tool_outputs=tool_outputs,
            stream=stream,
        )

        return submit_tool_outputs_run_request

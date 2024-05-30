from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_assistants_order import ListAssistantsOrder
from ...models.list_assistants_response import ListAssistantsResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: Union[Unset, int] = 20,
    order: Union[Unset, ListAssistantsOrder] = ListAssistantsOrder.DESC,
    after: Union[Unset, str] = UNSET,
    before: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["limit"] = limit

    json_order: Union[Unset, str] = UNSET
    if not isinstance(order, Unset):
        json_order = order.value

    params["order"] = json_order

    params["after"] = after

    params["before"] = before

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/assistants",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ListAssistantsResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListAssistantsResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ListAssistantsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 20,
    order: Union[Unset, ListAssistantsOrder] = ListAssistantsOrder.DESC,
    after: Union[Unset, str] = UNSET,
    before: Union[Unset, str] = UNSET,
) -> Response[ListAssistantsResponse]:
    """Returns a list of assistants.

    Args:
        limit (Union[Unset, int]):  Default: 20.
        order (Union[Unset, ListAssistantsOrder]):  Default: ListAssistantsOrder.DESC.
        after (Union[Unset, str]):
        before (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListAssistantsResponse]
    """

    kwargs = _get_kwargs(
        limit=limit,
        order=order,
        after=after,
        before=before,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 20,
    order: Union[Unset, ListAssistantsOrder] = ListAssistantsOrder.DESC,
    after: Union[Unset, str] = UNSET,
    before: Union[Unset, str] = UNSET,
) -> Optional[ListAssistantsResponse]:
    """Returns a list of assistants.

    Args:
        limit (Union[Unset, int]):  Default: 20.
        order (Union[Unset, ListAssistantsOrder]):  Default: ListAssistantsOrder.DESC.
        after (Union[Unset, str]):
        before (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListAssistantsResponse
    """

    return sync_detailed(
        client=client,
        limit=limit,
        order=order,
        after=after,
        before=before,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 20,
    order: Union[Unset, ListAssistantsOrder] = ListAssistantsOrder.DESC,
    after: Union[Unset, str] = UNSET,
    before: Union[Unset, str] = UNSET,
) -> Response[ListAssistantsResponse]:
    """Returns a list of assistants.

    Args:
        limit (Union[Unset, int]):  Default: 20.
        order (Union[Unset, ListAssistantsOrder]):  Default: ListAssistantsOrder.DESC.
        after (Union[Unset, str]):
        before (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListAssistantsResponse]
    """

    kwargs = _get_kwargs(
        limit=limit,
        order=order,
        after=after,
        before=before,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 20,
    order: Union[Unset, ListAssistantsOrder] = ListAssistantsOrder.DESC,
    after: Union[Unset, str] = UNSET,
    before: Union[Unset, str] = UNSET,
) -> Optional[ListAssistantsResponse]:
    """Returns a list of assistants.

    Args:
        limit (Union[Unset, int]):  Default: 20.
        order (Union[Unset, ListAssistantsOrder]):  Default: ListAssistantsOrder.DESC.
        after (Union[Unset, str]):
        before (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListAssistantsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            order=order,
            after=after,
            before=before,
        )
    ).parsed

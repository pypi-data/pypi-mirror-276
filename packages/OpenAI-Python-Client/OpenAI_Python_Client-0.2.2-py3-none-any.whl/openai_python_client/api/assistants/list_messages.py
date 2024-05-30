from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_messages_order import ListMessagesOrder
from ...models.list_messages_response import ListMessagesResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    thread_id: str,
    *,
    limit: Union[Unset, int] = 20,
    order: Union[Unset, ListMessagesOrder] = ListMessagesOrder.DESC,
    after: Union[Unset, str] = UNSET,
    before: Union[Unset, str] = UNSET,
    run_id: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["limit"] = limit

    json_order: Union[Unset, str] = UNSET
    if not isinstance(order, Unset):
        json_order = order.value

    params["order"] = json_order

    params["after"] = after

    params["before"] = before

    params["run_id"] = run_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/threads/{thread_id}/messages",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ListMessagesResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListMessagesResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ListMessagesResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    thread_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 20,
    order: Union[Unset, ListMessagesOrder] = ListMessagesOrder.DESC,
    after: Union[Unset, str] = UNSET,
    before: Union[Unset, str] = UNSET,
    run_id: Union[Unset, str] = UNSET,
) -> Response[ListMessagesResponse]:
    """Returns a list of messages for a given thread.

    Args:
        thread_id (str):
        limit (Union[Unset, int]):  Default: 20.
        order (Union[Unset, ListMessagesOrder]):  Default: ListMessagesOrder.DESC.
        after (Union[Unset, str]):
        before (Union[Unset, str]):
        run_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListMessagesResponse]
    """

    kwargs = _get_kwargs(
        thread_id=thread_id,
        limit=limit,
        order=order,
        after=after,
        before=before,
        run_id=run_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    thread_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 20,
    order: Union[Unset, ListMessagesOrder] = ListMessagesOrder.DESC,
    after: Union[Unset, str] = UNSET,
    before: Union[Unset, str] = UNSET,
    run_id: Union[Unset, str] = UNSET,
) -> Optional[ListMessagesResponse]:
    """Returns a list of messages for a given thread.

    Args:
        thread_id (str):
        limit (Union[Unset, int]):  Default: 20.
        order (Union[Unset, ListMessagesOrder]):  Default: ListMessagesOrder.DESC.
        after (Union[Unset, str]):
        before (Union[Unset, str]):
        run_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListMessagesResponse
    """

    return sync_detailed(
        thread_id=thread_id,
        client=client,
        limit=limit,
        order=order,
        after=after,
        before=before,
        run_id=run_id,
    ).parsed


async def asyncio_detailed(
    thread_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 20,
    order: Union[Unset, ListMessagesOrder] = ListMessagesOrder.DESC,
    after: Union[Unset, str] = UNSET,
    before: Union[Unset, str] = UNSET,
    run_id: Union[Unset, str] = UNSET,
) -> Response[ListMessagesResponse]:
    """Returns a list of messages for a given thread.

    Args:
        thread_id (str):
        limit (Union[Unset, int]):  Default: 20.
        order (Union[Unset, ListMessagesOrder]):  Default: ListMessagesOrder.DESC.
        after (Union[Unset, str]):
        before (Union[Unset, str]):
        run_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListMessagesResponse]
    """

    kwargs = _get_kwargs(
        thread_id=thread_id,
        limit=limit,
        order=order,
        after=after,
        before=before,
        run_id=run_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    thread_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 20,
    order: Union[Unset, ListMessagesOrder] = ListMessagesOrder.DESC,
    after: Union[Unset, str] = UNSET,
    before: Union[Unset, str] = UNSET,
    run_id: Union[Unset, str] = UNSET,
) -> Optional[ListMessagesResponse]:
    """Returns a list of messages for a given thread.

    Args:
        thread_id (str):
        limit (Union[Unset, int]):  Default: 20.
        order (Union[Unset, ListMessagesOrder]):  Default: ListMessagesOrder.DESC.
        after (Union[Unset, str]):
        before (Union[Unset, str]):
        run_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListMessagesResponse
    """

    return (
        await asyncio_detailed(
            thread_id=thread_id,
            client=client,
            limit=limit,
            order=order,
            after=after,
            before=before,
            run_id=run_id,
        )
    ).parsed

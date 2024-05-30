from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_vector_stores_order import ListVectorStoresOrder
from ...models.list_vector_stores_response import ListVectorStoresResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: Union[Unset, int] = 20,
    order: Union[Unset, ListVectorStoresOrder] = ListVectorStoresOrder.DESC,
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
        "url": "/vector_stores",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ListVectorStoresResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListVectorStoresResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ListVectorStoresResponse]:
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
    order: Union[Unset, ListVectorStoresOrder] = ListVectorStoresOrder.DESC,
    after: Union[Unset, str] = UNSET,
    before: Union[Unset, str] = UNSET,
) -> Response[ListVectorStoresResponse]:
    """Returns a list of vector stores.

    Args:
        limit (Union[Unset, int]):  Default: 20.
        order (Union[Unset, ListVectorStoresOrder]):  Default: ListVectorStoresOrder.DESC.
        after (Union[Unset, str]):
        before (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListVectorStoresResponse]
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
    order: Union[Unset, ListVectorStoresOrder] = ListVectorStoresOrder.DESC,
    after: Union[Unset, str] = UNSET,
    before: Union[Unset, str] = UNSET,
) -> Optional[ListVectorStoresResponse]:
    """Returns a list of vector stores.

    Args:
        limit (Union[Unset, int]):  Default: 20.
        order (Union[Unset, ListVectorStoresOrder]):  Default: ListVectorStoresOrder.DESC.
        after (Union[Unset, str]):
        before (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListVectorStoresResponse
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
    order: Union[Unset, ListVectorStoresOrder] = ListVectorStoresOrder.DESC,
    after: Union[Unset, str] = UNSET,
    before: Union[Unset, str] = UNSET,
) -> Response[ListVectorStoresResponse]:
    """Returns a list of vector stores.

    Args:
        limit (Union[Unset, int]):  Default: 20.
        order (Union[Unset, ListVectorStoresOrder]):  Default: ListVectorStoresOrder.DESC.
        after (Union[Unset, str]):
        before (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListVectorStoresResponse]
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
    order: Union[Unset, ListVectorStoresOrder] = ListVectorStoresOrder.DESC,
    after: Union[Unset, str] = UNSET,
    before: Union[Unset, str] = UNSET,
) -> Optional[ListVectorStoresResponse]:
    """Returns a list of vector stores.

    Args:
        limit (Union[Unset, int]):  Default: 20.
        order (Union[Unset, ListVectorStoresOrder]):  Default: ListVectorStoresOrder.DESC.
        after (Union[Unset, str]):
        before (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListVectorStoresResponse
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

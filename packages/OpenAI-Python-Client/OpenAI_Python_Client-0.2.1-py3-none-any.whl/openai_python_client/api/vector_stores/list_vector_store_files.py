from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_vector_store_files_filter import ListVectorStoreFilesFilter
from ...models.list_vector_store_files_order import ListVectorStoreFilesOrder
from ...models.list_vector_store_files_response import ListVectorStoreFilesResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    vector_store_id: str,
    *,
    limit: Union[Unset, int] = 20,
    order: Union[Unset, ListVectorStoreFilesOrder] = ListVectorStoreFilesOrder.DESC,
    after: Union[Unset, str] = UNSET,
    before: Union[Unset, str] = UNSET,
    filter_: Union[Unset, ListVectorStoreFilesFilter] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["limit"] = limit

    json_order: Union[Unset, str] = UNSET
    if not isinstance(order, Unset):
        json_order = order.value

    params["order"] = json_order

    params["after"] = after

    params["before"] = before

    json_filter_: Union[Unset, str] = UNSET
    if not isinstance(filter_, Unset):
        json_filter_ = filter_.value

    params["filter"] = json_filter_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/vector_stores/{vector_store_id}/files",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ListVectorStoreFilesResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListVectorStoreFilesResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ListVectorStoreFilesResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    vector_store_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 20,
    order: Union[Unset, ListVectorStoreFilesOrder] = ListVectorStoreFilesOrder.DESC,
    after: Union[Unset, str] = UNSET,
    before: Union[Unset, str] = UNSET,
    filter_: Union[Unset, ListVectorStoreFilesFilter] = UNSET,
) -> Response[ListVectorStoreFilesResponse]:
    """Returns a list of vector store files.

    Args:
        vector_store_id (str):
        limit (Union[Unset, int]):  Default: 20.
        order (Union[Unset, ListVectorStoreFilesOrder]):  Default: ListVectorStoreFilesOrder.DESC.
        after (Union[Unset, str]):
        before (Union[Unset, str]):
        filter_ (Union[Unset, ListVectorStoreFilesFilter]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListVectorStoreFilesResponse]
    """

    kwargs = _get_kwargs(
        vector_store_id=vector_store_id,
        limit=limit,
        order=order,
        after=after,
        before=before,
        filter_=filter_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    vector_store_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 20,
    order: Union[Unset, ListVectorStoreFilesOrder] = ListVectorStoreFilesOrder.DESC,
    after: Union[Unset, str] = UNSET,
    before: Union[Unset, str] = UNSET,
    filter_: Union[Unset, ListVectorStoreFilesFilter] = UNSET,
) -> Optional[ListVectorStoreFilesResponse]:
    """Returns a list of vector store files.

    Args:
        vector_store_id (str):
        limit (Union[Unset, int]):  Default: 20.
        order (Union[Unset, ListVectorStoreFilesOrder]):  Default: ListVectorStoreFilesOrder.DESC.
        after (Union[Unset, str]):
        before (Union[Unset, str]):
        filter_ (Union[Unset, ListVectorStoreFilesFilter]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListVectorStoreFilesResponse
    """

    return sync_detailed(
        vector_store_id=vector_store_id,
        client=client,
        limit=limit,
        order=order,
        after=after,
        before=before,
        filter_=filter_,
    ).parsed


async def asyncio_detailed(
    vector_store_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 20,
    order: Union[Unset, ListVectorStoreFilesOrder] = ListVectorStoreFilesOrder.DESC,
    after: Union[Unset, str] = UNSET,
    before: Union[Unset, str] = UNSET,
    filter_: Union[Unset, ListVectorStoreFilesFilter] = UNSET,
) -> Response[ListVectorStoreFilesResponse]:
    """Returns a list of vector store files.

    Args:
        vector_store_id (str):
        limit (Union[Unset, int]):  Default: 20.
        order (Union[Unset, ListVectorStoreFilesOrder]):  Default: ListVectorStoreFilesOrder.DESC.
        after (Union[Unset, str]):
        before (Union[Unset, str]):
        filter_ (Union[Unset, ListVectorStoreFilesFilter]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListVectorStoreFilesResponse]
    """

    kwargs = _get_kwargs(
        vector_store_id=vector_store_id,
        limit=limit,
        order=order,
        after=after,
        before=before,
        filter_=filter_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    vector_store_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 20,
    order: Union[Unset, ListVectorStoreFilesOrder] = ListVectorStoreFilesOrder.DESC,
    after: Union[Unset, str] = UNSET,
    before: Union[Unset, str] = UNSET,
    filter_: Union[Unset, ListVectorStoreFilesFilter] = UNSET,
) -> Optional[ListVectorStoreFilesResponse]:
    """Returns a list of vector store files.

    Args:
        vector_store_id (str):
        limit (Union[Unset, int]):  Default: 20.
        order (Union[Unset, ListVectorStoreFilesOrder]):  Default: ListVectorStoreFilesOrder.DESC.
        after (Union[Unset, str]):
        before (Union[Unset, str]):
        filter_ (Union[Unset, ListVectorStoreFilesFilter]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListVectorStoreFilesResponse
    """

    return (
        await asyncio_detailed(
            vector_store_id=vector_store_id,
            client=client,
            limit=limit,
            order=order,
            after=after,
            before=before,
            filter_=filter_,
        )
    ).parsed

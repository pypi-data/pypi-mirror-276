from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_vector_store_file_batch_request import CreateVectorStoreFileBatchRequest
from ...models.vector_store_file_batch import VectorStoreFileBatch
from ...types import Response


def _get_kwargs(
    vector_store_id: str,
    *,
    body: CreateVectorStoreFileBatchRequest,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/vector_stores/{vector_store_id}/file_batches",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[VectorStoreFileBatch]:
    if response.status_code == HTTPStatus.OK:
        response_200 = VectorStoreFileBatch.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[VectorStoreFileBatch]:
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
    body: CreateVectorStoreFileBatchRequest,
) -> Response[VectorStoreFileBatch]:
    """Create a vector store file batch.

    Args:
        vector_store_id (str):  Example: vs_abc123.
        body (CreateVectorStoreFileBatchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VectorStoreFileBatch]
    """

    kwargs = _get_kwargs(
        vector_store_id=vector_store_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    vector_store_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateVectorStoreFileBatchRequest,
) -> Optional[VectorStoreFileBatch]:
    """Create a vector store file batch.

    Args:
        vector_store_id (str):  Example: vs_abc123.
        body (CreateVectorStoreFileBatchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VectorStoreFileBatch
    """

    return sync_detailed(
        vector_store_id=vector_store_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    vector_store_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateVectorStoreFileBatchRequest,
) -> Response[VectorStoreFileBatch]:
    """Create a vector store file batch.

    Args:
        vector_store_id (str):  Example: vs_abc123.
        body (CreateVectorStoreFileBatchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VectorStoreFileBatch]
    """

    kwargs = _get_kwargs(
        vector_store_id=vector_store_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    vector_store_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateVectorStoreFileBatchRequest,
) -> Optional[VectorStoreFileBatch]:
    """Create a vector store file batch.

    Args:
        vector_store_id (str):  Example: vs_abc123.
        body (CreateVectorStoreFileBatchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VectorStoreFileBatch
    """

    return (
        await asyncio_detailed(
            vector_store_id=vector_store_id,
            client=client,
            body=body,
        )
    ).parsed

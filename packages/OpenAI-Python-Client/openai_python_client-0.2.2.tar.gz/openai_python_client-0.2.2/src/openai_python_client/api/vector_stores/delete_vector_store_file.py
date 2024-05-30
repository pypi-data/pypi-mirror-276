from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_vector_store_file_response import DeleteVectorStoreFileResponse
from ...types import Response


def _get_kwargs(
    vector_store_id: str,
    file_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "delete",
        "url": f"/vector_stores/{vector_store_id}/files/{file_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[DeleteVectorStoreFileResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = DeleteVectorStoreFileResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[DeleteVectorStoreFileResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    vector_store_id: str,
    file_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[DeleteVectorStoreFileResponse]:
    """Delete a vector store file. This will remove the file from the vector store but the file itself will
    not be deleted. To delete the file, use the [delete file](/docs/api-reference/files/delete)
    endpoint.

    Args:
        vector_store_id (str):
        file_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteVectorStoreFileResponse]
    """

    kwargs = _get_kwargs(
        vector_store_id=vector_store_id,
        file_id=file_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    vector_store_id: str,
    file_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[DeleteVectorStoreFileResponse]:
    """Delete a vector store file. This will remove the file from the vector store but the file itself will
    not be deleted. To delete the file, use the [delete file](/docs/api-reference/files/delete)
    endpoint.

    Args:
        vector_store_id (str):
        file_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteVectorStoreFileResponse
    """

    return sync_detailed(
        vector_store_id=vector_store_id,
        file_id=file_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    vector_store_id: str,
    file_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[DeleteVectorStoreFileResponse]:
    """Delete a vector store file. This will remove the file from the vector store but the file itself will
    not be deleted. To delete the file, use the [delete file](/docs/api-reference/files/delete)
    endpoint.

    Args:
        vector_store_id (str):
        file_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteVectorStoreFileResponse]
    """

    kwargs = _get_kwargs(
        vector_store_id=vector_store_id,
        file_id=file_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    vector_store_id: str,
    file_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[DeleteVectorStoreFileResponse]:
    """Delete a vector store file. This will remove the file from the vector store but the file itself will
    not be deleted. To delete the file, use the [delete file](/docs/api-reference/files/delete)
    endpoint.

    Args:
        vector_store_id (str):
        file_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteVectorStoreFileResponse
    """

    return (
        await asyncio_detailed(
            vector_store_id=vector_store_id,
            file_id=file_id,
            client=client,
        )
    ).parsed

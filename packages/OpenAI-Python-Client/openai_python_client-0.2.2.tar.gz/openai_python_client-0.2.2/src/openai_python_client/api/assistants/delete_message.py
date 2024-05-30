from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_message_response import DeleteMessageResponse
from ...types import Response


def _get_kwargs(
    thread_id: str,
    message_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "delete",
        "url": f"/threads/{thread_id}/messages/{message_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[DeleteMessageResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = DeleteMessageResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[DeleteMessageResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    thread_id: str,
    message_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[DeleteMessageResponse]:
    """Deletes a message.

    Args:
        thread_id (str):
        message_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteMessageResponse]
    """

    kwargs = _get_kwargs(
        thread_id=thread_id,
        message_id=message_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    thread_id: str,
    message_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[DeleteMessageResponse]:
    """Deletes a message.

    Args:
        thread_id (str):
        message_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteMessageResponse
    """

    return sync_detailed(
        thread_id=thread_id,
        message_id=message_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    thread_id: str,
    message_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[DeleteMessageResponse]:
    """Deletes a message.

    Args:
        thread_id (str):
        message_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteMessageResponse]
    """

    kwargs = _get_kwargs(
        thread_id=thread_id,
        message_id=message_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    thread_id: str,
    message_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[DeleteMessageResponse]:
    """Deletes a message.

    Args:
        thread_id (str):
        message_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteMessageResponse
    """

    return (
        await asyncio_detailed(
            thread_id=thread_id,
            message_id=message_id,
            client=client,
        )
    ).parsed

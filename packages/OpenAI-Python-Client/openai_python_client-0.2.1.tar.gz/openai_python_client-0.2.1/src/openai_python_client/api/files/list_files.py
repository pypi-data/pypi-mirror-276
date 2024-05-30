from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_files_response import ListFilesResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    purpose: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["purpose"] = purpose

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/files",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ListFilesResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListFilesResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ListFilesResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    purpose: Union[Unset, str] = UNSET,
) -> Response[ListFilesResponse]:
    """Returns a list of files that belong to the user's organization.

    Args:
        purpose (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListFilesResponse]
    """

    kwargs = _get_kwargs(
        purpose=purpose,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    purpose: Union[Unset, str] = UNSET,
) -> Optional[ListFilesResponse]:
    """Returns a list of files that belong to the user's organization.

    Args:
        purpose (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListFilesResponse
    """

    return sync_detailed(
        client=client,
        purpose=purpose,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    purpose: Union[Unset, str] = UNSET,
) -> Response[ListFilesResponse]:
    """Returns a list of files that belong to the user's organization.

    Args:
        purpose (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListFilesResponse]
    """

    kwargs = _get_kwargs(
        purpose=purpose,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    purpose: Union[Unset, str] = UNSET,
) -> Optional[ListFilesResponse]:
    """Returns a list of files that belong to the user's organization.

    Args:
        purpose (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListFilesResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            purpose=purpose,
        )
    ).parsed

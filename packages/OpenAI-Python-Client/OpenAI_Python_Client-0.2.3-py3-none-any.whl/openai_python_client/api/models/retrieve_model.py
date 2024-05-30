from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.model import Model
from ...types import Response


def _get_kwargs(
    model: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/models/{model}",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Model]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Model.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Model]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    model: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Model]:
    """Retrieves a model instance, providing basic information about the model such as the owner and
    permissioning.

    Args:
        model (str):  Example: gpt-3.5-turbo.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Model]
    """

    kwargs = _get_kwargs(
        model=model,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    model: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Model]:
    """Retrieves a model instance, providing basic information about the model such as the owner and
    permissioning.

    Args:
        model (str):  Example: gpt-3.5-turbo.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Model
    """

    return sync_detailed(
        model=model,
        client=client,
    ).parsed


async def asyncio_detailed(
    model: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Model]:
    """Retrieves a model instance, providing basic information about the model such as the owner and
    permissioning.

    Args:
        model (str):  Example: gpt-3.5-turbo.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Model]
    """

    kwargs = _get_kwargs(
        model=model,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    model: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Model]:
    """Retrieves a model instance, providing basic information about the model such as the owner and
    permissioning.

    Args:
        model (str):  Example: gpt-3.5-turbo.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Model
    """

    return (
        await asyncio_detailed(
            model=model,
            client=client,
        )
    ).parsed

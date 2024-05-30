from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.a_run_on_a_thread import ARunOnAThread
from ...types import Response


def _get_kwargs(
    thread_id: str,
    run_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/threads/{thread_id}/runs/{run_id}/cancel",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ARunOnAThread]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ARunOnAThread.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ARunOnAThread]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    thread_id: str,
    run_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ARunOnAThread]:
    """Cancels a run that is `in_progress`.

    Args:
        thread_id (str):
        run_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ARunOnAThread]
    """

    kwargs = _get_kwargs(
        thread_id=thread_id,
        run_id=run_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    thread_id: str,
    run_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ARunOnAThread]:
    """Cancels a run that is `in_progress`.

    Args:
        thread_id (str):
        run_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ARunOnAThread
    """

    return sync_detailed(
        thread_id=thread_id,
        run_id=run_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    thread_id: str,
    run_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ARunOnAThread]:
    """Cancels a run that is `in_progress`.

    Args:
        thread_id (str):
        run_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ARunOnAThread]
    """

    kwargs = _get_kwargs(
        thread_id=thread_id,
        run_id=run_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    thread_id: str,
    run_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ARunOnAThread]:
    """Cancels a run that is `in_progress`.

    Args:
        thread_id (str):
        run_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ARunOnAThread
    """

    return (
        await asyncio_detailed(
            thread_id=thread_id,
            run_id=run_id,
            client=client,
        )
    ).parsed

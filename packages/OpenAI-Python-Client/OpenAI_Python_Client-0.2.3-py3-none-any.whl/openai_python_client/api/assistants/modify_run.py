from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.a_run_on_a_thread import ARunOnAThread
from ...models.modify_run_request import ModifyRunRequest
from ...types import Response


def _get_kwargs(
    thread_id: str,
    run_id: str,
    *,
    body: ModifyRunRequest,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/threads/{thread_id}/runs/{run_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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
    body: ModifyRunRequest,
) -> Response[ARunOnAThread]:
    """Modifies a run.

    Args:
        thread_id (str):
        run_id (str):
        body (ModifyRunRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ARunOnAThread]
    """

    kwargs = _get_kwargs(
        thread_id=thread_id,
        run_id=run_id,
        body=body,
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
    body: ModifyRunRequest,
) -> Optional[ARunOnAThread]:
    """Modifies a run.

    Args:
        thread_id (str):
        run_id (str):
        body (ModifyRunRequest):

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
        body=body,
    ).parsed


async def asyncio_detailed(
    thread_id: str,
    run_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ModifyRunRequest,
) -> Response[ARunOnAThread]:
    """Modifies a run.

    Args:
        thread_id (str):
        run_id (str):
        body (ModifyRunRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ARunOnAThread]
    """

    kwargs = _get_kwargs(
        thread_id=thread_id,
        run_id=run_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    thread_id: str,
    run_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: ModifyRunRequest,
) -> Optional[ARunOnAThread]:
    """Modifies a run.

    Args:
        thread_id (str):
        run_id (str):
        body (ModifyRunRequest):

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
            body=body,
        )
    ).parsed

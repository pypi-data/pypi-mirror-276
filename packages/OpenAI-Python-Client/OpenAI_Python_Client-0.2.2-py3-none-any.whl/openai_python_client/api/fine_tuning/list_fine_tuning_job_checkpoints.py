from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_fine_tuning_job_checkpoints_response import ListFineTuningJobCheckpointsResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    fine_tuning_job_id: str,
    *,
    after: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 10,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["after"] = after

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/fine_tuning/jobs/{fine_tuning_job_id}/checkpoints",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ListFineTuningJobCheckpointsResponse]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListFineTuningJobCheckpointsResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ListFineTuningJobCheckpointsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    fine_tuning_job_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    after: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 10,
) -> Response[ListFineTuningJobCheckpointsResponse]:
    """List checkpoints for a fine-tuning job.

    Args:
        fine_tuning_job_id (str):  Example: ft-AF1WoRqd3aJAHsqc9NY7iL8F.
        after (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListFineTuningJobCheckpointsResponse]
    """

    kwargs = _get_kwargs(
        fine_tuning_job_id=fine_tuning_job_id,
        after=after,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    fine_tuning_job_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    after: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 10,
) -> Optional[ListFineTuningJobCheckpointsResponse]:
    """List checkpoints for a fine-tuning job.

    Args:
        fine_tuning_job_id (str):  Example: ft-AF1WoRqd3aJAHsqc9NY7iL8F.
        after (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListFineTuningJobCheckpointsResponse
    """

    return sync_detailed(
        fine_tuning_job_id=fine_tuning_job_id,
        client=client,
        after=after,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    fine_tuning_job_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    after: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 10,
) -> Response[ListFineTuningJobCheckpointsResponse]:
    """List checkpoints for a fine-tuning job.

    Args:
        fine_tuning_job_id (str):  Example: ft-AF1WoRqd3aJAHsqc9NY7iL8F.
        after (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListFineTuningJobCheckpointsResponse]
    """

    kwargs = _get_kwargs(
        fine_tuning_job_id=fine_tuning_job_id,
        after=after,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    fine_tuning_job_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    after: Union[Unset, str] = UNSET,
    limit: Union[Unset, int] = 10,
) -> Optional[ListFineTuningJobCheckpointsResponse]:
    """List checkpoints for a fine-tuning job.

    Args:
        fine_tuning_job_id (str):  Example: ft-AF1WoRqd3aJAHsqc9NY7iL8F.
        after (Union[Unset, str]):
        limit (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListFineTuningJobCheckpointsResponse
    """

    return (
        await asyncio_detailed(
            fine_tuning_job_id=fine_tuning_job_id,
            client=client,
            after=after,
            limit=limit,
        )
    ).parsed

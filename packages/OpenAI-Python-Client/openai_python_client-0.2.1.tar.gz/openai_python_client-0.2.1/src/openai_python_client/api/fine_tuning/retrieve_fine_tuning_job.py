from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.fine_tuning_job import FineTuningJob
from ...types import Response


def _get_kwargs(
    fine_tuning_job_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/fine_tuning/jobs/{fine_tuning_job_id}",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[FineTuningJob]:
    if response.status_code == HTTPStatus.OK:
        response_200 = FineTuningJob.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[FineTuningJob]:
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
) -> Response[FineTuningJob]:
    """Get info about a fine-tuning job.

    [Learn more about fine-tuning](/docs/guides/fine-tuning)

    Args:
        fine_tuning_job_id (str):  Example: ft-AF1WoRqd3aJAHsqc9NY7iL8F.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FineTuningJob]
    """

    kwargs = _get_kwargs(
        fine_tuning_job_id=fine_tuning_job_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    fine_tuning_job_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[FineTuningJob]:
    """Get info about a fine-tuning job.

    [Learn more about fine-tuning](/docs/guides/fine-tuning)

    Args:
        fine_tuning_job_id (str):  Example: ft-AF1WoRqd3aJAHsqc9NY7iL8F.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FineTuningJob
    """

    return sync_detailed(
        fine_tuning_job_id=fine_tuning_job_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    fine_tuning_job_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[FineTuningJob]:
    """Get info about a fine-tuning job.

    [Learn more about fine-tuning](/docs/guides/fine-tuning)

    Args:
        fine_tuning_job_id (str):  Example: ft-AF1WoRqd3aJAHsqc9NY7iL8F.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FineTuningJob]
    """

    kwargs = _get_kwargs(
        fine_tuning_job_id=fine_tuning_job_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    fine_tuning_job_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[FineTuningJob]:
    """Get info about a fine-tuning job.

    [Learn more about fine-tuning](/docs/guides/fine-tuning)

    Args:
        fine_tuning_job_id (str):  Example: ft-AF1WoRqd3aJAHsqc9NY7iL8F.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FineTuningJob
    """

    return (
        await asyncio_detailed(
            fine_tuning_job_id=fine_tuning_job_id,
            client=client,
        )
    ).parsed

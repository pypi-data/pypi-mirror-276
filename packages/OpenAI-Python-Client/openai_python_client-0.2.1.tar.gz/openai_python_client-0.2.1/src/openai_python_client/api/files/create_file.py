from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_file_request import CreateFileRequest
from ...models.open_ai_file import OpenAIFile
from ...types import Response


def _get_kwargs(
    *,
    body: CreateFileRequest,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/files",
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[OpenAIFile]:
    if response.status_code == HTTPStatus.OK:
        response_200 = OpenAIFile.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[OpenAIFile]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateFileRequest,
) -> Response[OpenAIFile]:
    """Upload a file that can be used across various endpoints. The size of all the files uploaded by one
    organization can be up to 100 GB.

    The size of individual files can be a maximum of 512 MB or 2 million tokens for Assistants. See the
    [Assistants Tools guide](/docs/assistants/tools) to learn more about the types of files supported.
    The Fine-tuning API only supports `.jsonl` files.

    Please [contact us](https://help.openai.com/) if you need to increase these storage limits.

    Args:
        body (CreateFileRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OpenAIFile]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateFileRequest,
) -> Optional[OpenAIFile]:
    """Upload a file that can be used across various endpoints. The size of all the files uploaded by one
    organization can be up to 100 GB.

    The size of individual files can be a maximum of 512 MB or 2 million tokens for Assistants. See the
    [Assistants Tools guide](/docs/assistants/tools) to learn more about the types of files supported.
    The Fine-tuning API only supports `.jsonl` files.

    Please [contact us](https://help.openai.com/) if you need to increase these storage limits.

    Args:
        body (CreateFileRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OpenAIFile
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateFileRequest,
) -> Response[OpenAIFile]:
    """Upload a file that can be used across various endpoints. The size of all the files uploaded by one
    organization can be up to 100 GB.

    The size of individual files can be a maximum of 512 MB or 2 million tokens for Assistants. See the
    [Assistants Tools guide](/docs/assistants/tools) to learn more about the types of files supported.
    The Fine-tuning API only supports `.jsonl` files.

    Please [contact us](https://help.openai.com/) if you need to increase these storage limits.

    Args:
        body (CreateFileRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OpenAIFile]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateFileRequest,
) -> Optional[OpenAIFile]:
    """Upload a file that can be used across various endpoints. The size of all the files uploaded by one
    organization can be up to 100 GB.

    The size of individual files can be a maximum of 512 MB or 2 million tokens for Assistants. See the
    [Assistants Tools guide](/docs/assistants/tools) to learn more about the types of files supported.
    The Fine-tuning API only supports `.jsonl` files.

    Please [contact us](https://help.openai.com/) if you need to increase these storage limits.

    Args:
        body (CreateFileRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OpenAIFile
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed

from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_transcription_request import CreateTranscriptionRequest
from ...models.create_transcription_response_json import CreateTranscriptionResponseJson
from ...models.create_transcription_response_verbose_json import CreateTranscriptionResponseVerboseJson
from ...types import Response


def _get_kwargs(
    *,
    body: CreateTranscriptionRequest,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/audio/transcriptions",
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union["CreateTranscriptionResponseJson", "CreateTranscriptionResponseVerboseJson"]]:
    if response.status_code == HTTPStatus.OK:

        def _parse_response_200(
            data: object,
        ) -> Union["CreateTranscriptionResponseJson", "CreateTranscriptionResponseVerboseJson"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = CreateTranscriptionResponseJson.from_dict(data)

                return response_200_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_1 = CreateTranscriptionResponseVerboseJson.from_dict(data)

            return response_200_type_1

        response_200 = _parse_response_200(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union["CreateTranscriptionResponseJson", "CreateTranscriptionResponseVerboseJson"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateTranscriptionRequest,
) -> Response[Union["CreateTranscriptionResponseJson", "CreateTranscriptionResponseVerboseJson"]]:
    """Transcribes audio into the input language.

    Args:
        body (CreateTranscriptionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union['CreateTranscriptionResponseJson', 'CreateTranscriptionResponseVerboseJson']]
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
    body: CreateTranscriptionRequest,
) -> Optional[Union["CreateTranscriptionResponseJson", "CreateTranscriptionResponseVerboseJson"]]:
    """Transcribes audio into the input language.

    Args:
        body (CreateTranscriptionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union['CreateTranscriptionResponseJson', 'CreateTranscriptionResponseVerboseJson']
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateTranscriptionRequest,
) -> Response[Union["CreateTranscriptionResponseJson", "CreateTranscriptionResponseVerboseJson"]]:
    """Transcribes audio into the input language.

    Args:
        body (CreateTranscriptionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union['CreateTranscriptionResponseJson', 'CreateTranscriptionResponseVerboseJson']]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateTranscriptionRequest,
) -> Optional[Union["CreateTranscriptionResponseJson", "CreateTranscriptionResponseVerboseJson"]]:
    """Transcribes audio into the input language.

    Args:
        body (CreateTranscriptionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union['CreateTranscriptionResponseJson', 'CreateTranscriptionResponseVerboseJson']
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed

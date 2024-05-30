from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_translation_request import CreateTranslationRequest
from ...models.create_translation_response_json import CreateTranslationResponseJson
from ...models.create_translation_response_verbose_json import CreateTranslationResponseVerboseJson
from ...types import Response


def _get_kwargs(
    *,
    body: CreateTranslationRequest,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/audio/translations",
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union["CreateTranslationResponseJson", "CreateTranslationResponseVerboseJson"]]:
    if response.status_code == HTTPStatus.OK:

        def _parse_response_200(
            data: object,
        ) -> Union["CreateTranslationResponseJson", "CreateTranslationResponseVerboseJson"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = CreateTranslationResponseJson.from_dict(data)

                return response_200_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_1 = CreateTranslationResponseVerboseJson.from_dict(data)

            return response_200_type_1

        response_200 = _parse_response_200(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union["CreateTranslationResponseJson", "CreateTranslationResponseVerboseJson"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateTranslationRequest,
) -> Response[Union["CreateTranslationResponseJson", "CreateTranslationResponseVerboseJson"]]:
    """Translates audio into English.

    Args:
        body (CreateTranslationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union['CreateTranslationResponseJson', 'CreateTranslationResponseVerboseJson']]
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
    body: CreateTranslationRequest,
) -> Optional[Union["CreateTranslationResponseJson", "CreateTranslationResponseVerboseJson"]]:
    """Translates audio into English.

    Args:
        body (CreateTranslationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union['CreateTranslationResponseJson', 'CreateTranslationResponseVerboseJson']
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateTranslationRequest,
) -> Response[Union["CreateTranslationResponseJson", "CreateTranslationResponseVerboseJson"]]:
    """Translates audio into English.

    Args:
        body (CreateTranslationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union['CreateTranslationResponseJson', 'CreateTranslationResponseVerboseJson']]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateTranslationRequest,
) -> Optional[Union["CreateTranslationResponseJson", "CreateTranslationResponseVerboseJson"]]:
    """Translates audio into English.

    Args:
        body (CreateTranslationRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union['CreateTranslationResponseJson', 'CreateTranslationResponseVerboseJson']
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed

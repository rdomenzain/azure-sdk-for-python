# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
from unittest import mock

from azure.identity._constants import EnvironmentVariables
from azure.identity.aio._credentials.managed_identity import MsiCredential
import pytest

from helpers_async import AsyncMockTransport


@pytest.mark.asyncio
async def test_no_scopes():
    """The credential should raise ValueError when get_token is called with no scopes"""

    with mock.patch("os.environ", {EnvironmentVariables.MSI_ENDPOINT: "https://url"}):
        credential = MsiCredential()

    with pytest.raises(ValueError):
        await credential.get_token()


@pytest.mark.asyncio
async def test_multiple_scopes():
    """The credential should raise ValueError when get_token is called with more than one scope"""

    with mock.patch("os.environ", {EnvironmentVariables.MSI_ENDPOINT: "https://url"}):
        credential = MsiCredential()

    with pytest.raises(ValueError):
        await credential.get_token("one scope", "and another")


@pytest.mark.asyncio
async def test_close():
    transport = AsyncMockTransport()

    with mock.patch("os.environ", {EnvironmentVariables.MSI_ENDPOINT: "https://url"}):
        credential = MsiCredential(transport=transport)

    await credential.close()

    assert transport.__aexit__.call_count == 1


@pytest.mark.asyncio
async def test_context_manager():
    transport = AsyncMockTransport()

    with mock.patch("os.environ", {EnvironmentVariables.MSI_ENDPOINT: "https://url"}):
        credential = MsiCredential(transport=transport)

    async with credential:
        assert transport.__aenter__.call_count == 1

    assert transport.__aenter__.call_count == 1
    assert transport.__aexit__.call_count == 1

from typing import Any, Dict

import pytest
from app.core.exceptions import ExternalAPIClientError
from app.external.base_client import BaseAPIClient
from pytest import MonkeyPatch


class MockResponse:
    def json(self) -> Dict[str, Any]:
        return {}

    def raise_for_status(self) -> None:
        pass


@pytest.mark.asyncio
async def test_request_success(monkeypatch: MonkeyPatch) -> None:
    """Test successful request"""
    mock_response = {"data": "test"}

    class MockResponse:
        def raise_for_status(self) -> None:
            pass

        def json(self) -> Dict[str, Any]:
            return mock_response

    async def mock_request(*args: Any, **kwargs: Any) -> MockResponse:
        return MockResponse()

    async with BaseAPIClient() as client:
        monkeypatch.setattr(client.client, "request", mock_request)
        response = await client.request("GET", "/test")
        assert response == mock_response


@pytest.mark.asyncio
async def test_request_retry_and_failure(monkeypatch: MonkeyPatch) -> None:
    async def mock_failing_request(*args: Any, **kwargs: Any) -> None:
        raise Exception("Request failed")

    with pytest.raises(Exception):
        async with BaseAPIClient() as client:
            monkeypatch.setattr(client.client, "request", mock_failing_request)
            with pytest.raises(ExternalAPIClientError):
                await client.request("GET", "/test")


@pytest.mark.asyncio
async def test_client_not_initialized() -> None:
    client = BaseAPIClient()
    with pytest.raises(RuntimeError, match="Client not initialized"):
        await client.request("GET", "/test")


@pytest.mark.asyncio
async def test_headers_setup(monkeypatch: MonkeyPatch) -> None:
    """Test headers are properly set in request"""
    headers_sent: Dict[str, str] = {}

    class MockResponse:
        def raise_for_status(self) -> None:
            pass

        def json(self) -> Dict[str, Any]:
            return {}

    async def mock_request(*args: Any, **kwargs: Any) -> MockResponse:
        nonlocal headers_sent
        headers_sent = kwargs.get("headers", {})
        return MockResponse()

    async with BaseAPIClient() as client:
        monkeypatch.setattr(client.client, "request", mock_request)
        await client.request("GET", "/test")
        assert "User-Agent" in headers_sent

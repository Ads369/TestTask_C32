from typing import Any, Dict, TypedDict

import pytest
from app.core.exceptions import ExternalAPIClientError
from app.external.CBRF_client import CBRFClient
from pytest import MonkeyPatch


class CBRFApiResponse(TypedDict):
    """Type definition for CBRF API response"""

    Date: str
    Valute: Dict[str, Dict[str, float]]


@pytest.fixture
def mock_cbrf_response() -> CBRFApiResponse:
    return {"Date": "2024-02-20", "Valute": {"USD": {"Value": 92.5}}}


@pytest.mark.asyncio
async def test_get_daily_rates_success(
    monkeypatch: MonkeyPatch, mock_cbrf_response: CBRFApiResponse
) -> None:
    """Test successful currency rates retrieval"""

    async def mock_request(*args: Any, **kwargs: Any) -> CBRFApiResponse:
        return mock_cbrf_response

    async with CBRFClient() as client:
        monkeypatch.setattr(client, "request", mock_request)
        result = await client.get_daily_rates()

        assert result["Date"] == "2024-02-20"
        assert result["Valute"] == 92.5


@pytest.mark.asyncio
async def test_get_daily_rates_error(monkeypatch: MonkeyPatch) -> None:
    """Test error handling in currency rates retrieval"""

    async def mock_request(*args: Any, **kwargs: Any) -> None:
        raise ExternalAPIClientError("API Error")

    async with CBRFClient() as client:
        monkeypatch.setattr(client, "request", mock_request)
        with pytest.raises(ExternalAPIClientError):
            await client.get_daily_rates()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_real_cbrf_api_connection() -> None:
    """Integration test: Test real connection to CBRF API"""
    async with CBRFClient() as client:
        response: CBRFApiResponse = await client.get_daily_rates()

        # Verify response structure
        assert "Date" in response
        assert "Valute" in response

        # Verify data types
        assert isinstance(response["Date"], str)
        assert isinstance(response["Valute"], float)

from typing import Any, AsyncGenerator, TypedDict

from app.core.config import settings

from .base_client import BaseAPIClient


class CBRFResponse(TypedDict):
    Date: str
    Valute: float


class CBRFClient(BaseAPIClient):
    def __init__(self):
        super().__init__()
        self.base_url = str(settings.CBR_API_URL)

    async def get_daily_rates(self) -> CBRFResponse:
        """GET currency rates data of USD

        Returns:
            CBRFResponse: Dictionary containing currency rates data
        """
        response = await self.request("GET", "daily_json.js")
        usd_rate = response["Valute"]["USD"]["Value"]
        return CBRFResponse(Date=response["Date"], Valute=usd_rate)


async def get_cbrf_client() -> AsyncGenerator[CBRFClient, Any]:
    async with CBRFClient() as client:
        yield client

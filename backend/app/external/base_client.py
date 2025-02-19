"""Client for making HTTP requests with retry functionality.

This module provides a base client for making HTTP requests with automatic retries
and error handling. It uses httpx for async HTTP operations.

Classes:
    RequestKwargs: TypedDict for request keyword arguments
    BaseAPIClient: Base class for implementing API clients with retry logic

Example:
    async with BaseAPIClient() as client:
        response = await client._request('GET', '/endpoint')
"""

from types import TracebackType
from typing import Any, Dict, Optional, TypedDict

import httpx
from httpx import AsyncClient

from app.core.config import settings
from app.core.exceptions import ExternalAPIClientError
from app.core.logger import logger


class RequestKwargs(TypedDict, total=False):
    """TypedDict defining valid keyword arguments for HTTP requests.

    Fields:
        headers: Dict of HTTP headers
        params: Dict of URL parameters
        json: Request body for JSON requests
        timeout: Request timeout in seconds
        follow_redirects: Whether to follow redirects
        files: Files to upload
        auth: Authentication credentials
        cookies: Dict of cookies

    Example:
        kwargs: RequestKwargs = {
            'headers': {'Authorization': 'Bearer token'},
            'params': {'key': 'value'},
            'json': {'data': 'value'}
        }
    """

    headers: Dict[str, str]
    params: Dict[str, Any]
    json: Any
    timeout: float
    follow_redirects: bool
    files: Any
    auth: Any
    cookies: Dict[str, str]


class BaseAPIClient:
    """Base client for making HTTP requests with retry functionality.

    This class provides functionality for making HTTP requests with automatic
    retries and error handling. It implements the async context manager protocol
    for proper resource management.

    Attributes:
        client: AsyncClient instance for making requests
        base_url: Base URL for all requests
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts on failure

    Example:
        async with BaseAPIClient() as client:
            try:
                response = await client._request('GET', '/api/data')
            except Exception as e:
                logger.error(f"Request failed: {e}")
    """

    def __init__(self) -> None:
        self.client: Optional[AsyncClient] = None
        self.base_url: str = ""
        self.timeout: int = settings.EXTERNAL_API_TIMEOUT
        self.max_retries: int = settings.EXTERNAL_API_MAX_RETRIES

    async def __aenter__(self) -> "BaseAPIClient":
        self.client = AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            limits=httpx.Limits(max_connections=100),
        )
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        if self.client is not None:
            await self.client.aclose()

    async def request(
        self, method: str, endpoint: str, **kwargs: Any
    ) -> Dict[str, Any]:
        """Make an HTTP request with retry functionality.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: URL endpoint to request
            **kwargs: Additional request parameters

        Returns:
            Dict containing the JSON response

        Raises:
            RuntimeError: If client is not initialized
            ExternalAPIClientError: If max retries are exceeded
            Exception: For other request failures
        """
        if self.client is None:
            raise RuntimeError("Client not initialized")

        headers = kwargs.pop("headers", {})
        headers.update(
            {"User-Agent": settings.USER_AGENT, "Content-Type": "application/json"}
        )

        for attempt in range(self.max_retries + 1):
            try:
                response = await self.client.request(
                    method=method, url=endpoint, headers=headers, **kwargs
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(
                    "API request failed",
                    extra={"attempt": attempt, "error": str(e), "endpoint": endpoint},
                )
                if attempt == self.max_retries:
                    raise

        raise ExternalAPIClientError("Max retries exceeded")

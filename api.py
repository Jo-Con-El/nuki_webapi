"""Nuki Web API client."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp

from .const import API_BASE_URL, API_TIMEOUT

_LOGGER = logging.getLogger(__name__)


class NukiWebApiClient:
    """Client to interact with Nuki Web API."""

    def __init__(self, api_token: str) -> None:
        """Initialize the API client."""
        self.api_token = api_token
        self.base_url = API_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any] | list[dict[str, Any]] | None:
        """Make a request to the Nuki API."""
        url = f"{self.base_url}{endpoint}"
        
        _LOGGER.debug("Making %s request to %s", method, url)
        
        try:
            timeout = aiohttp.ClientTimeout(total=API_TIMEOUT)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.request(
                    method,
                    url,
                    headers=self.headers,
                    json=data,
                ) as response:
                    if response.status == 204:
                        # No content response (successful action)
                        return None
                    
                    response.raise_for_status()
                    
                    if response.content_type == "application/json":
                        return await response.json()
                    
                    return None
                    
        except aiohttp.ClientError as err:
            _LOGGER.error("Error making request to %s: %s", url, err)
            raise
        except Exception as err:
            _LOGGER.error("Unexpected error making request to %s: %s", url, err)
            raise

    async def get_smartlocks(self) -> list[dict[str, Any]]:
        """Get all smartlocks from the account."""
        result = await self._request("GET", "/smartlock")
        if isinstance(result, list):
            return result
        return []

    async def get_smartlock(self, smartlock_id: int) -> dict[str, Any]:
        """Get a specific smartlock."""
        result = await self._request("GET", f"/smartlock/{smartlock_id}")
        if isinstance(result, dict):
            return result
        return {}

    async def lock(self, smartlock_id: int) -> None:
        """Lock the smartlock."""
        await self._request("POST", f"/smartlock/{smartlock_id}/action/lock")

    async def unlock(self, smartlock_id: int) -> None:
        """Unlock the smartlock."""
        await self._request("POST", f"/smartlock/{smartlock_id}/action/unlock")

    async def unlatch(self, smartlock_id: int) -> None:
        """Unlatch the smartlock (open door)."""
        await self._request("POST", f"/smartlock/{smartlock_id}/action/unlatch")

    async def lock_n_go(self, smartlock_id: int, unlatch: bool = False) -> None:
        """Execute lock'n'go action.

        Action codes:
        4 = lock'n'go
        5 = lock'n'go with unlatch
        """
        action_code = 5 if unlatch else 4
        await self._request("POST", f"/smartlock/{smartlock_id}/action", {"action": action_code})

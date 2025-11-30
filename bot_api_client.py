from __future__ import annotations

import logging
from typing import Dict, Any, Optional
import aiohttp

log = logging.getLogger("bot_api_client")

class BananaAPI:
    """
    API Client for Discord bot to communicate with Banana Hub API.
    """
    
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }
    
    async def whitelist_user(self, user_id: str) -> Dict[str, Any]:
        """Whitelist a user with auto-generated key."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/api/whitelist",
                    headers=self.headers,
                    json={"user_id": user_id}
                ) as resp:
                    return await resp.json()
        except Exception as e:
            log.error(f"Whitelist API error: {e}")
            return {"success": False, "error": str(e)}
    
    async def unwhitelist_user(self, user_id: str) -> Dict[str, Any]:
        """Remove user from whitelist."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/api/unwhitelist",
                    headers=self.headers,
                    json={"user_id": user_id}
                ) as resp:
                    return await resp.json()
        except Exception as e:
            log.error(f"Unwhitelist API error: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get user information."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_url}/api/user/{user_id}",
                    headers=self.headers
                ) as resp:
                    return await resp.json()
        except Exception as e:
            log.error(f"Get user API error: {e}")
            return {"success": False, "error": str(e)}
    
    async def reset_hwid(self, user_id: str) -> Dict[str, Any]:
        """Reset user's HWID."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/api/user/{user_id}/reset-hwid",
                    headers=self.headers
                ) as resp:
                    return await resp.json()
        except Exception as e:
            log.error(f"Reset HWID API error: {e}")
            return {"success": False, "error": str(e)}
    
    async def ban_user(self, user_id: str, reason: str = "No reason provided") -> Dict[str, Any]:
        """Ban or unban a user."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/api/blacklist",
                    headers=self.headers,
                    json={"user_id": user_id, "reason": reason}
                ) as resp:
                    return await resp.json()
        except Exception as e:
            log.error(f"Ban user API error: {e}")
            return {"success": False, "error": str(e)}
    
    async def generate_keys(self, count: int = 1) -> Dict[str, Any]:
        """Generate license keys."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/api/generate-key",
                    headers=self.headers,
                    json={"count": count}
                ) as resp:
                    return await resp.json()
        except Exception as e:
            log.error(f"Generate keys API error: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get system statistics."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_url}/api/stats",
                    headers=self.headers
                ) as resp:
                    return await resp.json()
        except Exception as e:
            log.error(f"Get stats API error: {e}")
            return {"success": False, "error": str(e)}
    
    async def check_key(self, key: str) -> Dict[str, Any]:
        """Check if a key is valid and available."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/api/check-key",
                    headers=self.headers,
                    json={"key": key}
                ) as resp:
                    return await resp.json()
        except Exception as e:
            log.error(f"Check key API error: {e}")
            return {"success": False, "error": str(e)}

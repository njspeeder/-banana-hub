from __future__ import annotations

import logging
from typing import Dict, Any, Optional
import aiohttp

log = logging.getLogger("bot_api_client")


class BananaAPI:
    """
    API Client for Discord bot to communicate with Banana Hub API.
    Handles all HTTP requests to the Flask API backend.
    """
    
    def __init__(self, api_url: str, api_key: str):
        """
        Initialize the API client.
        
        Args:
            api_url: Base URL of the API (e.g., https://banana-hub.onrender.com)
            api_key: Admin API key for authentication
        """
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "X-Admin-Key": api_key,
            "Content-Type": "application/json"
        }
        self.timeout = aiohttp.ClientTimeout(total=30)
        log.info(f"BananaAPI initialized with URL: {self.api_url}")
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        json_data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Internal method to make HTTP requests with error handling.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            json_data: JSON body data
            params: URL query parameters
            
        Returns:
            Response data as dictionary
        """
        url = f"{self.api_url}{endpoint}"
        
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    json=json_data,
                    params=params
                ) as resp:
                    log.debug(f"{method} {url} -> Status {resp.status}")
                    
                    try:
                        data = await resp.json()
                        return data
                    except aiohttp.ContentTypeError:
                        text = await resp.text()
                        log.error(f"Non-JSON response from {url}: {text[:200]}")
                        return {
                            'success': False,
                            'error': f'Server returned non-JSON response (Status {resp.status})'
                        }
                    
        except aiohttp.ClientConnectorError as e:
            log.error(f"Connection error to {url}: {e}")
            return {'success': False, 'error': 'Cannot connect to API server'}
        except asyncio.TimeoutError:
            log.error(f"Timeout requesting {url}")
            return {'success': False, 'error': 'Request timeout'}
        except Exception as e:
            log.error(f"Unexpected error requesting {url}: {e}", exc_info=True)
            return {'success': False, 'error': str(e)}
    
    async def get_stats(self) -> Dict[str, Any]:
        """
        Get system statistics.
        
        Returns:
            {
                'success': bool,
                'stats': {
                    'total_users': int,
                    'available_keys': int,
                    'total_keys': int,
                    'total_logins': int,
                    'total_blacklisted': int
                }
            }
        """
        log.info("Fetching system stats")
        return await self._make_request('GET', '/api/stats')
    
    async def whitelist_user(self, user_id: str) -> Dict[str, Any]:
        """
        Whitelist a user with auto-generated key.
        
        Args:
            user_id: Discord user ID
            
        Returns:
            {
                'success': bool,
                'user_id': str,
                'key': str  # Generated license key
            }
        """
        log.info(f"Whitelisting user: {user_id}")
        return await self._make_request(
            'POST',
            '/api/whitelist',
            json_data={'user_id': user_id}
        )
    
    async def unwhitelist_user(self, user_id: str) -> Dict[str, Any]:
        """
        Remove user from whitelist.
        
        Args:
            user_id: Discord user ID
            
        Returns:
            {
                'success': bool,
                'message': str
            }
        """
        log.info(f"Unwhitelisting user: {user_id}")
        return await self._make_request(
            'POST',
            '/api/unwhitelist',
            json_data={'user_id': user_id}
        )
    
    async def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        Get user information.
        
        Args:
            user_id: Discord user ID
            
        Returns:
            {
                'success': bool,
                'user': {
                    'discord_id': str,
                    'key': str,
                    'hwid': str,
                    'hwid_set': bool,
                    'joined_at': str,
                    'last_login': str,
                    'login_count': int,
                    'banned': bool
                }
            }
        """
        log.info(f"Fetching user info: {user_id}")
        return await self._make_request('GET', f'/api/user/{user_id}')
    
    async def reset_hwid(self, user_id: str) -> Dict[str, Any]:
        """
        Reset user's HWID.
        
        Args:
            user_id: Discord user ID
            
        Returns:
            {
                'success': bool,
                'message': str
            }
        """
        log.info(f"Resetting HWID for user: {user_id}")
        return await self._make_request(
            'POST',
            f'/api/user/{user_id}/reset-hwid'
        )
    
    async def ban_user(self, user_id: str, reason: str = "No reason provided") -> Dict[str, Any]:
        """
        Ban or unban a user (toggles blacklist status).
        
        Args:
            user_id: Discord user ID
            reason: Ban reason
            
        Returns:
            {
                'success': bool,
                'user_id': str,
                'banned': bool,  # Current ban status after toggle
                'action': str    # 'banned' or 'unbanned'
            }
        """
        log.info(f"Toggling ban for user: {user_id} - Reason: {reason}")
        return await self._make_request(
            'POST',
            '/api/blacklist',
            json_data={'user_id': user_id, 'reason': reason}
        )
    
    async def generate_keys(self, count: int = 1) -> Dict[str, Any]:
        """
        Generate license keys.
        
        Args:
            count: Number of keys to generate (1-25)
            
        Returns:
            {
                'success': bool,
                'keys': List[str],  # List of generated keys
                'count': int        # Number of keys generated
            }
        """
        if count < 1 or count > 25:
            log.warning(f"Invalid key count requested: {count}")
            return {
                'success': False,
                'error': 'Count must be between 1 and 25'
            }
        
        log.info(f"Generating {count} license keys")
        return await self._make_request(
            'POST',
            '/api/generate-key',
            json_data={'count': count}
        )
    
    async def check_key(self, key: str) -> Dict[str, Any]:
        """
        Check if a key is valid and available.
        
        Args:
            key: License key to check
            
        Returns:
            {
                'success': bool,
                'key': str,
                'available': bool
            }
        """
        log.info(f"Checking key: {key[:15]}...")
        return await self._make_request(
            'POST',
            '/api/check-key',
            json_data={'key': key}
        )
    
    async def authenticate(self, user_id: str, key: str, hwid: Optional[str] = None) -> Dict[str, Any]:
        """
        Authenticate user for script access.
        
        Args:
            user_id: Discord user ID
            key: License key
            hwid: Hardware ID (optional)
            
        Returns:
            {
                'success': bool,
                'authenticated': bool,
                'hwid_match': bool,
                'hwid_set': bool,
                'message': str
            }
        """
        log.info(f"Authenticating user: {user_id}")
        data = {'user_id': user_id, 'key': key}
        if hwid:
            data['hwid'] = hwid
        
        return await self._make_request('POST', '/api/auth', json_data=data)
    
    async def verify_license(self, user_id: str, key: str) -> Dict[str, Any]:
        """
        Quick license verification.
        
        Args:
            user_id: Discord user ID
            key: License key
            
        Returns:
            {
                'valid': bool,
                'reason': str,     # If invalid
                'user_id': str     # If valid
            }
        """
        log.info(f"Verifying license for user: {user_id}")
        return await self._make_request(
            'POST',
            '/api/verify',
            json_data={'user_id': user_id, 'key': key}
        )
    
    async def health_check(self) -> bool:
        """
        Check if API is online and responding.
        
        Returns:
            True if API is healthy, False otherwise
        """
        try:
            result = await self._make_request('GET', '/api/status')
            if result.get('success') and result.get('data', {}).get('status') == 'online':
                log.info("✅ API health check passed")
                return True
            log.warning("⚠️ API health check failed: unexpected response")
            return False
        except Exception as e:
            log.error(f"❌ API health check failed: {e}")
            return False


# Import asyncio for timeout handling
import asyncio


__all__ = ['BananaAPI']

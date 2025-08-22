"""Data for SEO API client implementation."""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import aiohttp
from pydantic import BaseModel

from ..config import get_settings

logger = logging.getLogger(__name__)


class DataForSEOError(Exception):
    """Base exception for Data for SEO API errors."""
    pass


class AuthenticationError(DataForSEOError):
    """Authentication failed."""
    pass


class RateLimitError(DataForSEOError):
    """Rate limit exceeded."""
    pass


class InsufficientCreditsError(DataForSEOError):
    """Insufficient API credits."""
    pass


class AsyncRateLimiter:
    """Async rate limiter for API requests."""
    
    def __init__(self, max_requests: int, time_window: int = 60):
        """Initialize rate limiter.
        
        Args:
            max_requests: Maximum requests allowed in time window
            time_window: Time window in seconds (default: 60)
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: List[datetime] = []
        self._lock = asyncio.Lock()
    
    async def acquire(self) -> None:
        """Acquire permission to make a request."""
        async with self._lock:
            now = datetime.utcnow()
            # Remove requests outside the time window
            self.requests = [
                req_time for req_time in self.requests
                if now - req_time < timedelta(seconds=self.time_window)
            ]
            
            # Check if we can make the request
            if len(self.requests) >= self.max_requests:
                # Calculate wait time
                oldest_request = min(self.requests)
                wait_time = self.time_window - (now - oldest_request).total_seconds()
                if wait_time > 0:
                    logger.info(f"Rate limit reached, waiting {wait_time:.2f} seconds")
                    await asyncio.sleep(wait_time)
                    return await self.acquire()
            
            # Record this request
            self.requests.append(now)


class DataForSEOClient:
    """Client for Data for SEO API."""
    
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        """Initialize Data for SEO client.
        
        Args:
            username: API username (defaults to settings)
            password: API password (defaults to settings)
        """
        self.settings = get_settings()
        self.username = username or self.settings.dataforseo_username
        self.password = password or self.settings.dataforseo_password
        
        if not self.username or not self.password:
            raise ValueError("Data for SEO credentials must be provided")
        
        self.auth = aiohttp.BasicAuth(self.username, self.password)
        self.base_url = str(self.settings.dataforseo_api_url)
        self.rate_limiter = AsyncRateLimiter(
            self.settings.dataforseo_rate_limit,
            60  # 1 minute window
        )
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.settings.request_timeout),
            headers={"User-Agent": self.settings.user_agent}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def _handle_response(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        """Handle API response with proper error checking."""
        if response.status == 401:
            raise AuthenticationError("Invalid Data for SEO credentials")
        elif response.status == 429:
            raise RateLimitError("Rate limit exceeded")
        elif response.status != 200:
            text = await response.text()
            raise DataForSEOError(f"API error {response.status}: {text}")
        
        try:
            data = await response.json()
        except Exception as e:
            raise DataForSEOError(f"Failed to parse response JSON: {e}")
        
        # Check API-specific status codes
        if isinstance(data, dict):
            status_code = data.get("status_code")
            if status_code == 40101:
                raise AuthenticationError("Authentication failed")
            elif status_code == 40102:
                raise InsufficientCreditsError("Insufficient credits")
            elif status_code == 40401:
                raise RateLimitError("Rate limit exceeded")
            elif status_code and status_code != 20000:
                status_message = data.get("status_message", "Unknown error")
                raise DataForSEOError(f"API error {status_code}: {status_message}")
        
        return data
    
    async def make_request(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        method: str = "POST",
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """Make authenticated request to Data for SEO API.
        
        Args:
            endpoint: API endpoint path
            data: Request payload
            method: HTTP method
            retry_count: Current retry attempt
            
        Returns:
            API response data
            
        Raises:
            DataForSEOError: For API errors
            AuthenticationError: For auth failures
            RateLimitError: For rate limit exceeded
            InsufficientCreditsError: For insufficient credits
        """
        if not self.session:
            raise RuntimeError("Client session not initialized. Use async context manager.")
        
        # Apply rate limiting
        await self.rate_limiter.acquire()
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            if method.upper() == "POST":
                async with self.session.post(
                    url,
                    json=data or {},
                    auth=self.auth
                ) as response:
                    return await self._handle_response(response)
            else:
                async with self.session.get(
                    url,
                    params=data or {},
                    auth=self.auth
                ) as response:
                    return await self._handle_response(response)
                    
        except RateLimitError:
            if retry_count < self.settings.max_retries:
                wait_time = 2 ** retry_count  # Exponential backoff
                logger.warning(f"Rate limit hit, retrying in {wait_time} seconds")
                await asyncio.sleep(wait_time)
                return await self.make_request(endpoint, data, method, retry_count + 1)
            raise
        except aiohttp.ClientError as e:
            if retry_count < self.settings.max_retries:
                wait_time = 2 ** retry_count
                logger.warning(f"Network error: {e}, retrying in {wait_time} seconds")
                await asyncio.sleep(wait_time)
                return await self.make_request(endpoint, data, method, retry_count + 1)
            raise DataForSEOError(f"Network error after {retry_count + 1} attempts: {e}")
    
    # Keyword research methods
    async def get_keyword_ideas(
        self,
        keywords: List[str],
        location: Optional[str] = None,
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get keyword ideas and suggestions.
        
        Args:
            keywords: Target keywords
            location: Geographic location
            language: Language code
            
        Returns:
            Keyword ideas data
        """
        payload = [
            {
                "keywords": keywords,
                "location_name": location or self.settings.default_location,
                "language_name": language or self.settings.default_language,
            }
        ]
        
        return await self.make_request("keywords_data/google/keyword_ideas/live", payload)
    
    async def get_keyword_metrics(
        self,
        keywords: List[str],
        location: Optional[str] = None,
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get keyword search volume and metrics.
        
        Args:
            keywords: Keywords to analyze
            location: Geographic location
            language: Language code
            
        Returns:
            Keyword metrics data
        """
        payload = [
            {
                "keywords": keywords,
                "location_name": location or self.settings.default_location,
                "language_name": language or self.settings.default_language,
            }
        ]
        
        return await self.make_request("keywords_data/google/search_volume/live", payload)
    
    # SERP analysis methods
    async def get_serp_data(
        self,
        keyword: str,
        location: Optional[str] = None,
        language: Optional[str] = None,
        device: str = "desktop"
    ) -> Dict[str, Any]:
        """Get SERP (Search Engine Results Page) data.
        
        Args:
            keyword: Search keyword
            location: Geographic location
            language: Language code
            device: Device type (desktop/mobile)
            
        Returns:
            SERP data
        """
        payload = [
            {
                "keyword": keyword,
                "location_name": location or self.settings.default_location,
                "language_name": language or self.settings.default_language,
                "device": device,
                "os": "windows" if device == "desktop" else "android",
            }
        ]
        
        return await self.make_request("serp/google/organic/live/regular", payload)
    
    # Ranking data methods
    async def get_ranking_data(
        self,
        keywords: List[str],
        target_url: str,
        location: Optional[str] = None,
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get ranking positions for keywords and URL.
        
        Args:
            keywords: Keywords to check rankings for
            target_url: URL to check rankings for
            location: Geographic location
            language: Language code
            
        Returns:
            Ranking data
        """
        payload = [
            {
                "keywords": keywords,
                "url": target_url,
                "location_name": location or self.settings.default_location,
                "language_name": language or self.settings.default_language,
            }
        ]
        
        return await self.make_request("serp/google/organic/live/regular", payload)
    
    # Competitor analysis methods
    async def get_competitor_keywords(
        self,
        target_url: str,
        location: Optional[str] = None,
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get competitor keyword analysis.
        
        Args:
            target_url: Competitor URL to analyze
            location: Geographic location
            language: Language code
            
        Returns:
            Competitor keyword data
        """
        payload = [
            {
                "target": target_url,
                "location_name": location or self.settings.default_location,
                "language_name": language or self.settings.default_language,
            }
        ]
        
        return await self.make_request("dataforseo_labs/google/competitors_domain/live", payload)
    
    async def get_domain_analytics(
        self,
        domain: str,
        location: Optional[str] = None,
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get domain analytics and metrics.
        
        Args:
            domain: Domain to analyze
            location: Geographic location
            language: Language code
            
        Returns:
            Domain analytics data
        """
        payload = [
            {
                "target": domain,
                "location_name": location or self.settings.default_location,
                "language_name": language or self.settings.default_language,
            }
        ]
        
        return await self.make_request("dataforseo_labs/google/domain_metrics/live", payload)
    
    # Backlink analysis methods
    async def get_backlinks(
        self,
        target_url: str,
        limit: int = 100
    ) -> Dict[str, Any]:
        """Get backlink data for a URL.
        
        Args:
            target_url: URL to analyze backlinks for
            limit: Maximum number of backlinks to return
            
        Returns:
            Backlink data
        """
        payload = [
            {
                "target": target_url,
                "limit": limit,
            }
        ]
        
        return await self.make_request("backlinks/backlinks/live", payload)
    
    # Technical SEO methods
    async def get_page_insights(
        self,
        url: str,
        device: str = "desktop"
    ) -> Dict[str, Any]:
        """Get technical page insights.
        
        Args:
            url: URL to analyze
            device: Device type (desktop/mobile)
            
        Returns:
            Page insights data
        """
        payload = [
            {
                "url": url,
                "device": device,
            }
        ]
        
        return await self.make_request("on_page/page_screenshot/live", payload)


# Convenience function for creating client instances
async def create_dataforseo_client(
    username: Optional[str] = None,
    password: Optional[str] = None
) -> DataForSEOClient:
    """Create and return a Data for SEO client instance.
    
    Args:
        username: API username (optional)
        password: API password (optional)
        
    Returns:
        Configured DataForSEOClient instance
    """
    return DataForSEOClient(username=username, password=password)
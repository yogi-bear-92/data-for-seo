"""Data for SEO API client with rate limiting and error handling."""

import asyncio
import json
import hashlib
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

import aiohttp
import redis.asyncio as redis
from pydantic import BaseModel, Field, ConfigDict

from .rate_limiter import AsyncRateLimiter


class DataForSEOError(Exception):
    """Base exception for Data for SEO API errors."""
    pass


class AuthenticationError(DataForSEOError):
    """Authentication failed."""
    pass


class InsufficientCreditsError(DataForSEOError):
    """Insufficient credits for the request."""
    pass


class RateLimitError(DataForSEOError):
    """Rate limit exceeded."""
    pass


class APICache:
    """Redis-based caching for API responses."""
    
    def __init__(self, redis_url: Optional[str] = None):
        """Initialize cache with optional Redis URL."""
        self.redis_url = redis_url
        self._redis: Optional[redis.Redis] = None
    
    async def _get_redis(self) -> Optional[redis.Redis]:
        """Get Redis connection, return None if not configured."""
        if not self.redis_url:
            return None
        
        if self._redis is None:
            try:
                self._redis = redis.from_url(self.redis_url)
                # Test connection
                await self._redis.ping()
            except Exception:
                # Redis not available, disable caching
                self._redis = None
                
        return self._redis
    
    async def get_cached_result(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get cached API result."""
        redis_client = await self._get_redis()
        if not redis_client:
            return None
            
        try:
            cached = await redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
        except Exception:
            # Cache error, continue without cache
            pass
        return None
    
    async def cache_result(self, cache_key: str, data: Dict[str, Any], ttl: int = 3600) -> None:
        """Cache API result with TTL."""
        redis_client = await self._get_redis()
        if not redis_client:
            return
            
        try:
            await redis_client.setex(
                cache_key,
                ttl,
                json.dumps(data, default=str)
            )
        except Exception:
            # Cache error, continue without cache
            pass
    
    def generate_cache_key(self, endpoint: str, params: Dict[str, Any]) -> str:
        """Generate consistent cache key."""
        key_data = f"{endpoint}:{json.dumps(params, sort_keys=True)}"
        return f"dataforseo:{hashlib.md5(key_data.encode()).hexdigest()}"
    
    async def close(self) -> None:
        """Close Redis connection."""
        if self._redis:
            await self._redis.close()


class DataForSEORequest(BaseModel):
    """Base request model for Data for SEO API."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
    )


class SERPRequest(DataForSEORequest):
    """Request model for SERP analysis."""
    
    keyword: str = Field(description="Target keyword")
    location_name: Optional[str] = Field(default="United States", description="Location name")
    language_name: Optional[str] = Field(default="English", description="Language name")
    device: Optional[str] = Field(default="desktop", description="Device type")
    os: Optional[str] = Field(default=None, description="Operating system")


class KeywordsForSiteRequest(DataForSEORequest):
    """Request model for keywords for site analysis."""
    
    target: str = Field(description="Target domain or URL")
    location_name: Optional[str] = Field(default="United States", description="Location name")
    language_name: Optional[str] = Field(default="English", description="Language name")
    limit: Optional[int] = Field(default=100, description="Maximum number of results")


class KeywordSuggestionsRequest(DataForSEORequest):
    """Request model for keyword suggestions."""
    
    keyword: str = Field(description="Target keyword")
    location_name: Optional[str] = Field(default="United States", description="Location name")
    language_name: Optional[str] = Field(default="English", description="Language name")
    limit: Optional[int] = Field(default=100, description="Maximum number of results")


class RankedKeywordsRequest(DataForSEORequest):
    """Request model for ranked keywords analysis."""
    
    target: str = Field(description="Target domain")
    location_name: Optional[str] = Field(default="United States", description="Location name")
    language_name: Optional[str] = Field(default="English", description="Language name")
    limit: Optional[int] = Field(default=100, description="Maximum number of results")


class DataForSEOResponse(BaseModel):
    """Base response model for Data for SEO API."""
    
    model_config = ConfigDict(extra="allow")
    
    version: Optional[str] = None
    status_code: int
    status_message: str
    time: Optional[str] = None
    cost: Optional[float] = None
    tasks_count: Optional[int] = None
    tasks_error: Optional[int] = None
    tasks: List[Dict[str, Any]] = Field(default_factory=list)


class DataForSEOClient:
    """Async Data for SEO API client with rate limiting and caching."""
    
    def __init__(
        self,
        username: str,
        password: str,
        rate_limit: int = 100,
        time_window: int = 60,
        redis_url: Optional[str] = None,
        base_url: str = "https://api.dataforseo.com/v3",
        max_retries: int = 3,
        backoff_factor: float = 1.0,
        timeout: int = 30,
    ):
        """Initialize DataForSEO client.
        
        Args:
            username: Data for SEO username
            password: Data for SEO password
            rate_limit: Maximum requests per time window
            time_window: Time window in seconds
            redis_url: Optional Redis URL for caching
            base_url: Base API URL
            max_retries: Maximum retry attempts
            backoff_factor: Exponential backoff factor
            timeout: Request timeout in seconds
        """
        self.auth = aiohttp.BasicAuth(username, password)
        self.base_url = base_url
        self.rate_limiter = AsyncRateLimiter(rate_limit, time_window)
        self.cache = APICache(redis_url)
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self._ensure_session()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    async def _ensure_session(self) -> aiohttp.ClientSession:
        """Ensure session is created."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                auth=self.auth,
                timeout=self.timeout,
                headers={"Content-Type": "application/json"}
            )
        return self._session
    
    async def close(self) -> None:
        """Close client connections."""
        if self._session and not self._session.closed:
            await self._session.close()
        await self.cache.close()
    
    async def _handle_api_response(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        """Handle API response and check for errors."""
        data = await response.json()
        
        # Validate response structure
        parsed_response = DataForSEOResponse(**data)
        
        # Check for API errors
        if parsed_response.status_code == 40101:
            raise AuthenticationError("Authentication failed")
        elif parsed_response.status_code == 40102:
            raise InsufficientCreditsError("Insufficient credits")
        elif parsed_response.status_code == 40401:
            raise RateLimitError("Rate limit exceeded")
        elif parsed_response.status_code != 20000:
            raise DataForSEOError(f"API error: {parsed_response.status_message}")
        
        return data
    
    async def _make_request_with_retry(
        self,
        endpoint: str,
        data: List[Dict[str, Any]],
        cache_ttl: int = 3600,
        use_cache: bool = True,
    ) -> Dict[str, Any]:
        """Make API request with retry logic and caching."""
        
        # Check cache first
        cache_key = None
        if use_cache:
            cache_key = self.cache.generate_cache_key(endpoint, {"data": data})
            cached_result = await self.cache.get_cached_result(cache_key)
            if cached_result:
                return cached_result
        
        # Rate limiting
        await self.rate_limiter.acquire()
        
        session = await self._ensure_session()
        url = f"{self.base_url}/{endpoint}"
        
        for attempt in range(self.max_retries + 1):
            try:
                async with session.post(url, json=data) as response:
                    result = await self._handle_api_response(response)
                    
                    # Cache successful result
                    if use_cache and cache_key:
                        await self.cache.cache_result(cache_key, result, cache_ttl)
                    
                    return result
                    
            except RateLimitError:
                if attempt == self.max_retries:
                    raise
                
                # Exponential backoff for rate limiting
                wait_time = self.backoff_factor * (2 ** attempt)
                await asyncio.sleep(wait_time)
                
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                if attempt == self.max_retries:
                    raise DataForSEOError(f"Request failed after {self.max_retries} retries: {e}")
                
                # Exponential backoff for network errors
                wait_time = self.backoff_factor * (2 ** attempt)
                await asyncio.sleep(wait_time)
    
    async def get_serp_data(
        self,
        keyword: str,
        location_name: str = "United States",
        language_name: str = "English",
        device: str = "desktop",
        cache_ttl: int = 3600,
    ) -> Dict[str, Any]:
        """Get SERP analysis data."""
        request_data = SERPRequest(
            keyword=keyword,
            location_name=location_name,
            language_name=language_name,
            device=device,
        )
        
        return await self._make_request_with_retry(
            "serp/google/organic/live/advanced",
            [request_data.model_dump()],
            cache_ttl=cache_ttl,
        )
    
    async def get_keywords_for_site(
        self,
        target: str,
        location_name: str = "United States",
        language_name: str = "English",
        limit: int = 100,
        cache_ttl: int = 3600,
    ) -> Dict[str, Any]:
        """Get keywords for site analysis."""
        request_data = KeywordsForSiteRequest(
            target=target,
            location_name=location_name,
            language_name=language_name,
            limit=limit,
        )
        
        return await self._make_request_with_retry(
            "dataforseo_labs/google/keywords_for_site/live",
            [request_data.model_dump()],
            cache_ttl=cache_ttl,
        )
    
    async def get_keyword_suggestions(
        self,
        keyword: str,
        location_name: str = "United States",
        language_name: str = "English",
        limit: int = 100,
        cache_ttl: int = 3600,
    ) -> Dict[str, Any]:
        """Get keyword suggestions."""
        request_data = KeywordSuggestionsRequest(
            keyword=keyword,
            location_name=location_name,
            language_name=language_name,
            limit=limit,
        )
        
        return await self._make_request_with_retry(
            "dataforseo_labs/google/keyword_suggestions/live",
            [request_data.model_dump()],
            cache_ttl=cache_ttl,
        )
    
    async def get_ranked_keywords(
        self,
        target: str,
        location_name: str = "United States",
        language_name: str = "English",
        limit: int = 100,
        cache_ttl: int = 3600,
    ) -> Dict[str, Any]:
        """Get ranked keywords analysis."""
        request_data = RankedKeywordsRequest(
            target=target,
            location_name=location_name,
            language_name=language_name,
            limit=limit,
        )
        
        return await self._make_request_with_retry(
            "dataforseo_labs/google/ranked_keywords/live",
            [request_data.model_dump()],
            cache_ttl=cache_ttl,
        )
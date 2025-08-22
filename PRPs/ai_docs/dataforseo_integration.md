# Data for SEO API Integration Guide

## Overview

Data for SEO provides comprehensive SEO and marketing data through RESTful APIs. This guide covers integration patterns, authentication, rate limiting, and best practices for the SEO automation framework.

## Authentication

### Basic Authentication
Data for SEO uses HTTP Basic Authentication with username and password.

```python
import aiohttp
from aiohttp import BasicAuth

# Create authentication object
auth = BasicAuth(username="your_username", password="your_password")

# Use in requests
async with aiohttp.ClientSession() as session:
    async with session.post(
        "https://api.dataforseo.com/v3/serp/google/organic/live/advanced",
        json=request_data,
        auth=auth
    ) as response:
        data = await response.json()
```

### Environment Configuration
Store credentials securely in environment variables:

```python
# settings.py
dataforseo_username: Optional[str] = Field(
    default=None, 
    description="Data for SEO API username"
)
dataforseo_password: Optional[str] = Field(
    default=None, 
    description="Data for SEO API password"
)

# .env file
DATAFORSEO_USERNAME=your_username
DATAFORSEO_PASSWORD=your_password
```

## Rate Limiting

### API Limits
- **Standard Plan**: 100 requests per minute
- **Professional Plan**: 200 requests per minute
- **Enterprise Plan**: Custom limits

### Implementation Pattern

```python
import asyncio
from asyncio import Semaphore
from datetime import datetime, timedelta

class AsyncRateLimiter:
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
        self.semaphore = Semaphore(max_requests)
    
    async def acquire(self):
        await self.semaphore.acquire()
        
        now = datetime.utcnow()
        # Remove old requests outside time window
        self.requests = [req_time for req_time in self.requests 
                        if now - req_time < timedelta(seconds=self.time_window)]
        
        if len(self.requests) >= self.max_requests:
            sleep_time = self.time_window - (now - self.requests[0]).total_seconds()
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
        
        self.requests.append(now)
        self.semaphore.release()

# Usage
rate_limiter = AsyncRateLimiter(100, 60)  # 100 requests per minute

async def make_api_call():
    await rate_limiter.acquire()
    # Make API call here
```

## Core API Endpoints

### 1. SERP Analysis

#### Google Organic Results
```python
# Endpoint: /v3/serp/google/organic/live/advanced
request_data = [{
    "keyword": "seo tools",
    "location_name": "United States",
    "language_name": "English",
    "device": "desktop",
    "os": "windows"
}]

async def get_serp_data(keyword: str, location: str = "United States"):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{base_url}/serp/google/organic/live/advanced",
            json=[{
                "keyword": keyword,
                "location_name": location,
                "language_name": "English"
            }],
            auth=auth
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data["tasks"][0]["result"]
            else:
                raise APIError(f"SERP request failed: {response.status}")
```

#### Response Structure
```python
{
    "version": "0.1.20240801",
    "status_code": 20000,
    "status_message": "Ok.",
    "time": "0.1234 sec.",
    "cost": 0.001,
    "tasks_count": 1,
    "tasks_error": 0,
    "tasks": [{
        "id": "12345678-1234-1234-1234-123456789012",
        "status_code": 20000,
        "status_message": "Ok.",
        "time": "0.1234 sec.",
        "cost": 0.001,
        "result_count": 1,
        "path": ["v3", "serp", "google", "organic", "live", "advanced"],
        "data": {
            "api": "serp",
            "function": "live",
            "se": "google",
            "se_type": "organic",
            "keyword": "seo tools",
            "location_code": 2840,
            "language_code": "en"
        },
        "result": [{
            "keyword": "seo tools",
            "type": "organic",
            "se_domain": "google.com",
            "location_code": 2840,
            "language_code": "en",
            "check_url": "https://www.google.com/search?q=seo+tools",
            "datetime": "2024-01-15 12:00:00 +00:00",
            "items_count": 100,
            "items": [
                {
                    "type": "organic",
                    "rank_group": 1,
                    "rank_absolute": 1,
                    "position": "left",
                    "xpath": "/html[1]/body[1]/div[6]/div[1]/div[9]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/span[1]/a[1]",
                    "domain": "example.com",
                    "title": "Best SEO Tools for 2024",
                    "url": "https://example.com/seo-tools",
                    "description": "Comprehensive list of the best SEO tools...",
                    "website_name": "Example SEO",
                    "is_featured_snippet": false,
                    "is_malicious": false,
                    "is_web_story": false,
                    "about_this_result": {
                        "type": "organic_about_this_result",
                        "url": "https://example.com/about",
                        "source": "Example.com",
                        "source_info": "Example is a leading SEO platform...",
                        "source_url": "https://example.com",
                        "language": "en",
                        "location": "US"
                    }
                }
            ]
        }]
    }]
}
```

### 2. Keyword Research

#### Keywords For Site
```python
# Endpoint: /v3/dataforseo_labs/google/keywords_for_site/live
async def get_keywords_for_site(target_url: str, limit: int = 100):
    request_data = [{
        "target": target_url,
        "location_name": "United States",
        "language_name": "English",
        "limit": limit,
        "filters": [
            ["keyword_data.keyword_info.search_volume", ">", 100]
        ],
        "order_by": ["keyword_data.keyword_info.search_volume,desc"]
    }]
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{base_url}/dataforseo_labs/google/keywords_for_site/live",
            json=request_data,
            auth=auth
        ) as response:
            data = await response.json()
            return data["tasks"][0]["result"]
```

#### Keyword Suggestions
```python
# Endpoint: /v3/dataforseo_labs/google/keyword_suggestions/live
async def get_keyword_suggestions(seed_keyword: str, limit: int = 100):
    request_data = [{
        "keyword": seed_keyword,
        "location_name": "United States",
        "language_name": "English",
        "limit": limit,
        "include_serp_info": True,
        "filters": [
            ["keyword_data.keyword_info.search_volume", ">", 50]
        ]
    }]
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{base_url}/dataforseo_labs/google/keyword_suggestions/live",
            json=request_data,
            auth=auth
        ) as response:
            data = await response.json()
            return data["tasks"][0]["result"]
```

### 3. Ranking Data

#### Ranked Keywords
```python
# Endpoint: /v3/dataforseo_labs/google/ranked_keywords/live
async def get_ranked_keywords(target_url: str):
    request_data = [{
        "target": target_url,
        "location_name": "United States",
        "language_name": "English",
        "limit": 1000,
        "filters": [
            ["ranked_serp_element.serp_item.rank_absolute", "<=", 100]
        ]
    }]
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{base_url}/dataforseo_labs/google/ranked_keywords/live",
            json=request_data,
            auth=auth
        ) as response:
            data = await response.json()
            return data["tasks"][0]["result"]
```

## Error Handling

### Common Error Codes
- **20000**: Success
- **40001**: General error
- **40101**: Authentication failed
- **40102**: Low balance
- **40401**: Rate limit exceeded
- **50000**: Internal server error

### Error Handling Pattern
```python
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

async def handle_api_response(response: aiohttp.ClientResponse) -> dict:
    """Handle API response with proper error checking."""
    if response.status == 401:
        raise AuthenticationError("Invalid credentials")
    elif response.status == 429:
        raise RateLimitError("Rate limit exceeded")
    elif response.status != 200:
        text = await response.text()
        raise DataForSEOError(f"API error {response.status}: {text}")
    
    data = await response.json()
    
    # Check API-specific status codes
    if data.get("status_code") == 40101:
        raise AuthenticationError("Authentication failed")
    elif data.get("status_code") == 40102:
        raise InsufficientCreditsError("Insufficient credits")
    elif data.get("status_code") == 40401:
        raise RateLimitError("Rate limit exceeded")
    elif data.get("status_code") != 20000:
        raise DataForSEOError(f"API error: {data.get('status_message')}")
    
    return data
```

### Retry Logic
```python
import asyncio
from typing import Optional

async def make_request_with_retry(
    session: aiohttp.ClientSession,
    url: str,
    data: dict,
    max_retries: int = 3,
    backoff_factor: float = 1.0
) -> dict:
    """Make API request with exponential backoff retry."""
    
    for attempt in range(max_retries + 1):
        try:
            async with session.post(url, json=data, auth=auth) as response:
                return await handle_api_response(response)
                
        except RateLimitError:
            if attempt == max_retries:
                raise
            
            # Exponential backoff for rate limiting
            wait_time = backoff_factor * (2 ** attempt)
            await asyncio.sleep(wait_time)
            
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            if attempt == max_retries:
                raise DataForSEOError(f"Request failed after {max_retries} retries: {e}")
            
            wait_time = backoff_factor * (2 ** attempt)
            await asyncio.sleep(wait_time)
```

## Data Models

### Pydantic Models for API Responses

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class KeywordInfo(BaseModel):
    """Keyword information from Data for SEO."""
    keyword: str
    location_code: int
    language_code: str
    search_volume: Optional[int] = None
    cpc: Optional[float] = None
    competition: Optional[float] = None
    competition_level: Optional[str] = None
    search_volume_trend: Optional[List[Dict[str, Any]]] = None

class SERPItem(BaseModel):
    """SERP result item."""
    type: str
    rank_group: int
    rank_absolute: int
    position: str
    xpath: str
    domain: str
    title: str
    url: str
    description: Optional[str] = None
    is_featured_snippet: bool = False
    is_malicious: bool = False
    
class SERPResult(BaseModel):
    """Complete SERP result."""
    keyword: str
    type: str
    se_domain: str
    location_code: int
    language_code: str
    check_url: str
    datetime: datetime
    items_count: int
    items: List[SERPItem]

class DataForSEOResponse(BaseModel):
    """Base Data for SEO API response."""
    version: str
    status_code: int
    status_message: str
    time: str
    cost: float
    tasks_count: int
    tasks_error: int
    tasks: List[Dict[str, Any]]
```

## Best Practices

### 1. Connection Management
```python
class DataForSEOClient:
    def __init__(self, username: str, password: str):
        self.auth = BasicAuth(username, password)
        self.base_url = "https://api.dataforseo.com/v3"
        self.session: Optional[aiohttp.ClientSession] = None
        self.rate_limiter = AsyncRateLimiter(100, 60)
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            connector=aiohttp.TCPConnector(limit=10)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
```

### 2. Batch Processing
```python
async def process_keywords_batch(keywords: List[str], batch_size: int = 10):
    """Process keywords in batches to respect rate limits."""
    results = []
    
    for i in range(0, len(keywords), batch_size):
        batch = keywords[i:i + batch_size]
        
        # Create batch request
        request_data = [
            {
                "keyword": keyword,
                "location_name": "United States",
                "language_name": "English"
            }
            for keyword in batch
        ]
        
        # Process batch
        batch_results = await make_api_request("keyword_data", request_data)
        results.extend(batch_results)
        
        # Rate limiting delay
        await asyncio.sleep(0.6)  # Ensure we don't exceed 100 requests/minute
    
    return results
```

### 3. Caching Strategy
```python
import redis.asyncio as redis
import json
from datetime import timedelta

class APICache:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
    
    async def get_cached_result(self, cache_key: str) -> Optional[dict]:
        """Get cached API result."""
        cached = await self.redis.get(cache_key)
        if cached:
            return json.loads(cached)
        return None
    
    async def cache_result(self, cache_key: str, data: dict, ttl: int = 3600):
        """Cache API result with TTL."""
        await self.redis.setex(
            cache_key,
            ttl,
            json.dumps(data, default=str)
        )
    
    def generate_cache_key(self, endpoint: str, params: dict) -> str:
        """Generate consistent cache key."""
        import hashlib
        key_data = f"{endpoint}:{json.dumps(params, sort_keys=True)}"
        return f"dataforseo:{hashlib.md5(key_data.encode()).hexdigest()}"

# Usage
cache = APICache("redis://localhost:6379/1")

async def get_serp_data_cached(keyword: str, location: str):
    cache_key = cache.generate_cache_key("serp", {"keyword": keyword, "location": location})
    
    # Try cache first
    cached_result = await cache.get_cached_result(cache_key)
    if cached_result:
        return cached_result
    
    # Make API call
    result = await get_serp_data(keyword, location)
    
    # Cache result for 1 hour
    await cache.cache_result(cache_key, result, 3600)
    
    return result
```

## Testing Patterns

### Mock API Responses
```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture
def mock_serp_response():
    return {
        "status_code": 20000,
        "status_message": "Ok.",
        "tasks": [{
            "result": [{
                "keyword": "test keyword",
                "items": [
                    {
                        "type": "organic",
                        "rank_absolute": 1,
                        "domain": "example.com",
                        "title": "Test Title",
                        "url": "https://example.com",
                        "description": "Test description"
                    }
                ]
            }]
        }]
    }

@pytest.mark.asyncio
async def test_get_serp_data(mock_serp_response):
    with patch('aiohttp.ClientSession.post') as mock_post:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = mock_serp_response
        mock_post.return_value.__aenter__.return_value = mock_response
        
        client = DataForSEOClient("test_user", "test_pass")
        result = await client.get_serp_data("test keyword")
        
        assert result[0]["keyword"] == "test keyword"
        assert len(result[0]["items"]) == 1
```

### Integration Testing
```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_dataforseo_integration():
    """Test actual Data for SEO API integration."""
    if not os.getenv("DATAFORSEO_USERNAME"):
        pytest.skip("Data for SEO credentials not available")
    
    client = DataForSEOClient(
        os.getenv("DATAFORSEO_USERNAME"),
        os.getenv("DATAFORSEO_PASSWORD")
    )
    
    async with client:
        # Test with a simple keyword
        result = await client.get_serp_data("test", "United States")
        
        assert result is not None
        assert len(result) > 0
        assert "keyword" in result[0]
```

This integration guide provides comprehensive patterns for working with the Data for SEO API in an async Python environment with proper error handling, rate limiting, and caching strategies.

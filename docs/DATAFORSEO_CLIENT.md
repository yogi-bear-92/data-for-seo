# Data for SEO API Client

This module provides a comprehensive, production-ready client for the Data for SEO API with advanced features including rate limiting, error handling, retry logic, and caching.

## Features

- **Authentication**: HTTP Basic Auth with username/password
- **Rate Limiting**: 100 requests per minute with exponential backoff (configurable)
- **Error Handling**: Comprehensive error handling for all API status codes
- **Retry Logic**: Automatic retry with exponential backoff for transient failures
- **Caching**: Redis-based caching for API responses with configurable TTL (optional)
- **Async/Await**: Full async implementation using aiohttp
- **Pydantic Models**: Request/response models with validation
- **Configuration**: Environment-based configuration support

## Quick Start

```python
import asyncio
from data_for_seo.tools import DataForSEOClient

async def main():
    # Initialize client
    client = DataForSEOClient(
        username="your_username",
        password="your_password",
        rate_limit=100,  # 100 requests per minute
        redis_url="redis://localhost:6379/1"  # Optional for caching
    )
    
    async with client:
        # Get SERP data
        serp_data = await client.get_serp_data(
            keyword="python programming",
            location_name="United States"
        )
        
        # Get keywords for a site
        keywords = await client.get_keywords_for_site(
            target="example.com",
            limit=100
        )
        
        # Get keyword suggestions
        suggestions = await client.get_keyword_suggestions(
            keyword="web development",
            limit=50
        )
        
        # Get ranked keywords
        ranked = await client.get_ranked_keywords(
            target="github.com",
            limit=100
        )

asyncio.run(main())
```

## API Endpoints

### SERP Analysis
```python
serp_data = await client.get_serp_data(
    keyword="your keyword",
    location_name="United States",
    language_name="English",
    device="desktop"
)
```

### Keywords for Site
```python
keywords_data = await client.get_keywords_for_site(
    target="example.com",
    location_name="United States",
    limit=100
)
```

### Keyword Suggestions
```python
suggestions_data = await client.get_keyword_suggestions(
    keyword="your keyword",
    location_name="United States",
    limit=100
)
```

### Ranked Keywords
```python
ranked_data = await client.get_ranked_keywords(
    target="domain.com",
    location_name="United States",
    limit=100
)
```

## Configuration

Set environment variables for production use:

```bash
export DATAFORSEO_USERNAME=your_username
export DATAFORSEO_PASSWORD=your_password
export REDIS_URL=redis://localhost:6379/1  # Optional for caching
```

## Error Handling

The client provides specific exception types for different error conditions:

```python
from data_for_seo.tools.dataforseo_client import (
    DataForSEOError,
    AuthenticationError,
    InsufficientCreditsError,
    RateLimitError
)

try:
    result = await client.get_serp_data("keyword")
except AuthenticationError:
    print("Invalid credentials")
except InsufficientCreditsError:
    print("Not enough credits")
except RateLimitError:
    print("Rate limit exceeded")
except DataForSEOError as e:
    print(f"API error: {e}")
```

## Rate Limiting

The client automatically handles rate limiting with a configurable limit:

```python
client = DataForSEOClient(
    username="user",
    password="pass",
    rate_limit=50,      # 50 requests per minute
    time_window=60,     # 60 seconds
    max_retries=5,      # Retry failed requests up to 5 times
    backoff_factor=2.0  # Exponential backoff multiplier
)

# Check current usage
usage = client.rate_limiter.get_current_usage()
time_until_next = client.rate_limiter.get_time_until_next_slot()
```

## Caching

Redis-based caching is optional and gracefully falls back if Redis is not available:

```python
# With Redis caching
client = DataForSEOClient(
    username="user",
    password="pass",
    redis_url="redis://localhost:6379/1"
)

# Cache results for 2 hours
result = await client.get_serp_data("keyword", cache_ttl=7200)

# Without caching
client = DataForSEOClient(username="user", password="pass")
```

## Testing

Run the included tests:

```bash
python tests/tools/test_rate_limiter.py
python tests/tools/test_dataforseo_client.py
```

## Examples

See `examples/dataforseo_example.py` for a complete usage demonstration.
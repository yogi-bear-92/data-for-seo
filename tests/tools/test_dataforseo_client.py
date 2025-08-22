"""Tests for DataForSEOClient."""

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

from data_for_seo.tools.dataforseo_client import (
    DataForSEOClient,
    DataForSEOError,
    AuthenticationError,
    InsufficientCreditsError,
    RateLimitError,
    SERPRequest,
    KeywordsForSiteRequest,
)


class TestDataForSEOClient:
    """Test cases for DataForSEOClient."""
    
    def test_request_models(self):
        """Test Pydantic request models."""
        # Test SERP request
        serp_request = SERPRequest(keyword="test keyword")
        assert serp_request.keyword == "test keyword"
        assert serp_request.location_name == "United States"
        assert serp_request.language_name == "English"
        
        # Test keywords for site request
        site_request = KeywordsForSiteRequest(target="example.com")
        assert site_request.target == "example.com"
        assert site_request.limit == 100
    
    def test_client_init(self):
        """Test client initialization."""
        client = DataForSEOClient("test_user", "test_pass")
        assert client.auth.login == "test_user"
        assert client.auth.password == "test_pass"
        assert client.base_url == "https://api.dataforseo.com/v3"
        assert client.rate_limiter.max_requests == 100
        assert client.max_retries == 3
    
    def test_custom_config(self):
        """Test client with custom configuration."""
        client = DataForSEOClient(
            "user", "pass",
            rate_limit=50,
            time_window=30,
            max_retries=5,
            backoff_factor=2.0,
        )
        assert client.rate_limiter.max_requests == 50
        assert client.rate_limiter.time_window == 30
        assert client.max_retries == 5
        assert client.backoff_factor == 2.0
    
    async def test_error_handling(self):
        """Test API error handling."""
        client = DataForSEOClient("test_user", "test_pass")
        
        # Mock session and response
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "status_code": 40101,
            "status_message": "Authentication failed",
            "tasks": []
        }
        
        mock_session = AsyncMock()
        mock_session.post.return_value.__aenter__.return_value = mock_response
        client._session = mock_session
        
        # Test authentication error
        try:
            await client._handle_api_response(mock_response)
            assert False, "Should have raised AuthenticationError"
        except AuthenticationError as e:
            assert "Authentication failed" in str(e)
        
        # Test insufficient credits error
        mock_response.json.return_value = {
            "status_code": 40102,
            "status_message": "Insufficient credits",
            "tasks": []
        }
        try:
            await client._handle_api_response(mock_response)
            assert False, "Should have raised InsufficientCreditsError"
        except InsufficientCreditsError:
            pass
        
        # Test rate limit error
        mock_response.json.return_value = {
            "status_code": 40401,
            "status_message": "Rate limit exceeded",
            "tasks": []
        }
        try:
            await client._handle_api_response(mock_response)
            assert False, "Should have raised RateLimitError"
        except RateLimitError:
            pass
        
        await client.close()
    
    async def test_successful_response(self):
        """Test successful API response handling."""
        client = DataForSEOClient("test_user", "test_pass")
        
        mock_response = AsyncMock()
        success_data = {
            "status_code": 20000,
            "status_message": "Ok.",
            "tasks": [{"result": [{"keyword": "test"}]}]
        }
        mock_response.json.return_value = success_data
        
        result = await client._handle_api_response(mock_response)
        assert result == success_data
        
        await client.close()
    
    async def test_cache_operations(self):
        """Test caching functionality."""
        client = DataForSEOClient("test_user", "test_pass")
        
        # Test cache key generation
        cache_key = client.cache.generate_cache_key("test/endpoint", {"param": "value"})
        assert cache_key.startswith("dataforseo:")
        assert len(cache_key) > 20  # Should be a hash
        
        # Test cache operations without Redis (should not fail)
        await client.cache.cache_result(cache_key, {"test": "data"})
        result = await client.cache.get_cached_result(cache_key)
        assert result is None  # No Redis, so no cache
        
        await client.close()


class TestIntegration:
    """Integration-style tests with mocked responses."""
    
    async def test_get_serp_data_mock(self):
        """Test SERP data retrieval with mocked response."""
        client = DataForSEOClient("test_user", "test_pass")
        
        # Mock successful response
        mock_response_data = {
            "status_code": 20000,
            "status_message": "Ok.",
            "tasks": [{
                "result": [{
                    "keyword": "test keyword",
                    "location_code": 2840,
                    "language_code": "en",
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
        
        with patch.object(client, '_make_request_with_retry') as mock_request:
            mock_request.return_value = mock_response_data
            
            result = await client.get_serp_data("test keyword")
            
            assert result == mock_response_data
            assert mock_request.called
            
            # Verify correct endpoint was called
            call_args = mock_request.call_args
            assert call_args[0][0] == "serp/google/organic/live/advanced"
            
            # Verify request data structure
            request_data = call_args[0][1][0]
            assert request_data["keyword"] == "test keyword"
            assert request_data["location_name"] == "United States"
        
        await client.close()
    
    async def test_get_keywords_for_site_mock(self):
        """Test keywords for site retrieval with mocked response."""
        client = DataForSEOClient("test_user", "test_pass")
        
        mock_response_data = {
            "status_code": 20000,
            "status_message": "Ok.",
            "tasks": [{
                "result": [{
                    "target": "example.com",
                    "total_count": 100,
                    "items": [
                        {
                            "keyword": "example keyword",
                            "search_volume": 1000,
                            "competition": 0.5
                        }
                    ]
                }]
            }]
        }
        
        with patch.object(client, '_make_request_with_retry') as mock_request:
            mock_request.return_value = mock_response_data
            
            result = await client.get_keywords_for_site("example.com")
            
            assert result == mock_response_data
            call_args = mock_request.call_args
            assert call_args[0][0] == "dataforseo_labs/google/keywords_for_site/live"
            
            request_data = call_args[0][1][0]
            assert request_data["target"] == "example.com"
        
        await client.close()


# Simple test runner if pytest not available
if __name__ == "__main__":
    async def run_tests():
        test_instance = TestDataForSEOClient()
        integration_test = TestIntegration()
        
        # Run synchronous tests
        test_instance.test_request_models()
        test_instance.test_client_init()
        test_instance.test_custom_config()
        print("✓ Synchronous tests passed")
        
        # Run async tests
        await test_instance.test_error_handling()
        print("✓ Error handling test passed")
        
        await test_instance.test_successful_response()
        print("✓ Successful response test passed")
        
        await test_instance.test_cache_operations()
        print("✓ Cache operations test passed")
        
        await integration_test.test_get_serp_data_mock()
        print("✓ SERP data mock test passed")
        
        await integration_test.test_get_keywords_for_site_mock()
        print("✓ Keywords for site mock test passed")
        
        print("All DataForSEO client tests passed!")
    
    asyncio.run(run_tests())
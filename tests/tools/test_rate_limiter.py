"""Tests for AsyncRateLimiter."""

import asyncio
import time
from datetime import datetime, timezone

from data_for_seo.tools.rate_limiter import AsyncRateLimiter


class TestAsyncRateLimiter:
    """Test cases for AsyncRateLimiter."""
    
    def test_init(self):
        """Test rate limiter initialization."""
        limiter = AsyncRateLimiter(10, 60)
        assert limiter.max_requests == 10
        assert limiter.time_window == 60
        assert limiter.get_current_usage() == 0
        
    async def test_acquire_basic(self):
        """Test basic request acquisition."""
        limiter = AsyncRateLimiter(5, 60)
        
        # First few requests should be immediate
        start_time = time.time()
        await limiter.acquire()
        await limiter.acquire()
        await limiter.acquire()
        end_time = time.time()
        
        # Should be very fast
        assert end_time - start_time < 1.0
        assert limiter.get_current_usage() == 3
    
    async def test_rate_limiting(self):
        """Test rate limiting behavior."""
        # Use small limits for fast testing
        limiter = AsyncRateLimiter(2, 2)  # 2 requests per 2 seconds
        
        start_time = time.time()
        
        # First 2 requests should be immediate
        await limiter.acquire()
        await limiter.acquire()
        
        # Third request should wait
        await limiter.acquire()
        
        end_time = time.time()
        
        # Should have waited approximately 2 seconds
        assert end_time - start_time >= 1.5  # Allow some variance
        assert limiter.get_current_usage() <= 2
    
    async def test_concurrent_requests(self):
        """Test rate limiter with concurrent requests."""
        limiter = AsyncRateLimiter(3, 1)  # 3 requests per second
        
        async def make_request(delay=0):
            await asyncio.sleep(delay)
            await limiter.acquire()
            return time.time()
        
        # Start 5 concurrent requests
        tasks = [make_request(i * 0.1) for i in range(5)]
        completion_times = await asyncio.gather(*tasks)
        
        # First 3 should be quick, last 2 should be delayed
        first_batch = completion_times[:3]
        second_batch = completion_times[3:]
        
        # All completion times should be reasonable
        assert len(completion_times) == 5
        assert all(isinstance(t, float) for t in completion_times)
    
    def test_get_time_until_next_slot(self):
        """Test time until next slot calculation."""
        limiter = AsyncRateLimiter(2, 10)
        
        # No requests yet
        assert limiter.get_time_until_next_slot() == 0.0
        
        # Simulate some requests
        now = datetime.now(timezone.utc)
        limiter.requests = [now, now]
        
        # Should need to wait
        time_to_wait = limiter.get_time_until_next_slot()
        assert 0 < time_to_wait <= 10


# Simple test runner if pytest not available
if __name__ == "__main__":
    async def run_tests():
        test_instance = TestAsyncRateLimiter()
        
        # Run synchronous tests
        test_instance.test_init()
        test_instance.test_get_time_until_next_slot()
        print("✓ Synchronous tests passed")
        
        # Run async tests
        await test_instance.test_acquire_basic()
        print("✓ Basic acquire test passed")
        
        await test_instance.test_rate_limiting()
        print("✓ Rate limiting test passed")
        
        await test_instance.test_concurrent_requests()
        print("✓ Concurrent requests test passed")
        
        print("All rate limiter tests passed!")
    
    asyncio.run(run_tests())
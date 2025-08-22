"""Rate limiting utilities for Data for SEO API."""

import asyncio
from asyncio import Semaphore
from datetime import datetime, timedelta, timezone
from typing import List


class AsyncRateLimiter:
    """Async rate limiter with time window tracking."""
    
    def __init__(self, max_requests: int, time_window: int):
        """Initialize rate limiter.
        
        Args:
            max_requests: Maximum number of requests allowed in time window
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: List[datetime] = []
        self.semaphore = Semaphore(max_requests)
        self._lock = asyncio.Lock()
    
    async def acquire(self) -> None:
        """Acquire permission to make a request."""
        await self.semaphore.acquire()
        
        async with self._lock:
            now = datetime.now(timezone.utc)
            
            # Remove old requests outside time window
            cutoff = now - timedelta(seconds=self.time_window)
            self.requests = [req_time for req_time in self.requests if req_time > cutoff]
            
            # If we're at the limit, wait until oldest request expires
            if len(self.requests) >= self.max_requests:
                oldest_request = self.requests[0]
                sleep_time = self.time_window - (now - oldest_request).total_seconds()
                if sleep_time > 0:
                    self.semaphore.release()  # Release before sleeping
                    await asyncio.sleep(sleep_time)
                    await self.semaphore.acquire()  # Re-acquire after sleeping
                    # Refresh the now time after sleeping
                    now = datetime.now(timezone.utc)
                    cutoff = now - timedelta(seconds=self.time_window)
                    self.requests = [req_time for req_time in self.requests if req_time > cutoff]
            
            # Record this request
            self.requests.append(now)
        
        # Always release the semaphore after recording the request
        self.semaphore.release()
    
    def get_current_usage(self) -> int:
        """Get current number of requests in the time window."""
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(seconds=self.time_window)
        valid_requests = [req_time for req_time in self.requests if req_time > cutoff]
        return len(valid_requests)
    
    def get_time_until_next_slot(self) -> float:
        """Get time in seconds until next request slot is available."""
        if len(self.requests) < self.max_requests:
            return 0.0
        
        now = datetime.now(timezone.utc)
        oldest_request = self.requests[0]
        time_since_oldest = (now - oldest_request).total_seconds()
        return max(0.0, self.time_window - time_since_oldest)
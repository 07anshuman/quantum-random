"""
Caching module for the Quantum Randomness Service.
Provides Redis-based caching for random numbers and statistics.
"""

import json
import logging
import time
from typing import Optional, Dict, Any, List
import redis.asyncio as redis  # type: ignore

from .config import settings

logger = logging.getLogger(__name__)


class CacheManager:
    """Manages caching operations for the QRNG service."""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self._in_memory_cache: Dict[str, Any] = {}
        self._cache_timestamps: Dict[str, float] = {}
        self._connect()
    
    def _connect(self):
        """Connect to Redis."""
        try:
            self.redis_client = redis.from_url(
                settings.redis_url,
                decode_responses=True
            )
            logger.info("Connected to Redis cache")
        except Exception as e:
            logger.warning(f"Failed to connect to Redis: {e}")
            self.redis_client = None
    
    def _get_in_memory(self, key: str) -> Optional[Any]:
        """Get value from in-memory cache."""
        if key in self._in_memory_cache:
            timestamp = self._cache_timestamps.get(key, 0)
            if time.time() - timestamp < settings.cache_ttl:
                return self._in_memory_cache[key]
            else:
                # Expired, remove it
                del self._in_memory_cache[key]
                if key in self._cache_timestamps:
                    del self._cache_timestamps[key]
        return None
    
    def _set_in_memory(self, key: str, value: Any):
        """Set value in in-memory cache."""
        self._in_memory_cache[key] = value
        self._cache_timestamps[key] = time.time()
    
    async def get_random_numbers(self, count: int) -> Optional[List[int]]:
        """Get cached random numbers."""
        key = f"random:batch:{count}"
        
        # Try Redis first
        if self.redis_client:
            try:
                data = await self.redis_client.get(key)
                if data:
                    return json.loads(data)
            except Exception as e:
                logger.error(f"Redis get error: {e}")
        
        # Fallback to in-memory cache
        return self._get_in_memory(key)
    
    async def set_random_numbers(self, count: int, numbers: List[int], ttl: Optional[int] = None):
        """Cache random numbers."""
        key = f"random:batch:{count}"
        
        # Try Redis first
        if self.redis_client:
            try:
                ttl = ttl or settings.cache_ttl
                await self.redis_client.setex(
                    key, 
                    ttl, 
                    json.dumps(numbers)
                )
            except Exception as e:
                logger.error(f"Redis set error: {e}")
        
        # Fallback to in-memory cache
        self._set_in_memory(key, numbers)
    
    async def get_single_random(self) -> Optional[int]:
        """Get a single cached random number."""
        key = "random:single"
        
        # Try Redis first
        if self.redis_client:
            try:
                data = await self.redis_client.get(key)
                if data:
                    return json.loads(data)
            except Exception as e:
                logger.error(f"Redis get error: {e}")
        
        # Fallback to in-memory cache
        return self._get_in_memory(key)
    
    async def set_single_random(self, number: int, ttl: Optional[int] = None):
        """Cache a single random number."""
        key = "random:single"
        
        # Try Redis first
        if self.redis_client:
            try:
                ttl = ttl or settings.cache_ttl
                await self.redis_client.setex(
                    key, 
                    ttl, 
                    json.dumps(number)
                )
            except Exception as e:
                logger.error(f"Redis set error: {e}")
        
        # Fallback to in-memory cache
        self._set_in_memory(key, number)
    
    async def get_stats(self) -> Optional[Dict[str, Any]]:
        """Get cached service statistics."""
        key = "stats:service"
        
        # Try Redis first
        if self.redis_client:
            try:
                data = await self.redis_client.get(key)
                if data:
                    return json.loads(data)
            except Exception as e:
                logger.error(f"Redis get error: {e}")
        
        # Fallback to in-memory cache
        return self._get_in_memory(key)
    
    async def set_stats(self, stats: Dict[str, Any], ttl: int = 60):
        """Cache service statistics."""
        key = "stats:service"
        
        # Try Redis first
        if self.redis_client:
            try:
                await self.redis_client.setex(
                    key, 
                    ttl, 
                    json.dumps(stats)
                )
            except Exception as e:
                logger.error(f"Redis set error: {e}")
        
        # Fallback to in-memory cache
        self._set_in_memory(key, stats)
    
    async def increment_counter(self, counter_name: str) -> int:
        """Increment a counter in cache."""
        key = f"counter:{counter_name}"
        
        # Try Redis first
        if self.redis_client:
            try:
                return await self.redis_client.incr(key)
            except Exception as e:
                logger.error(f"Redis increment error: {e}")
        
        # Fallback to in-memory counter
        current = self._get_in_memory(key) or 0
        new_value = current + 1
        self._set_in_memory(key, new_value)
        return new_value
    
    async def get_cache_hit_rate(self) -> float:
        """Calculate cache hit rate."""
        hits_key = "counter:hits"
        misses_key = "counter:misses"
        
        # Try Redis first
        if self.redis_client:
            try:
                hits = await self.redis_client.get(hits_key) or 0
                misses = await self.redis_client.get(misses_key) or 0
                
                total = int(hits) + int(misses)
                if total == 0:
                    return 0.0
                
                return (int(hits) / total) * 100
            except Exception as e:
                logger.error(f"Redis hit rate calculation error: {e}")
        
        # Fallback to in-memory calculation
        hits = self._get_in_memory(hits_key) or 0
        misses = self._get_in_memory(misses_key) or 0
        
        total = hits + misses
        if total == 0:
            return 0.0
        
        return (hits / total) * 100
    
    async def close(self):
        """Close Redis connection."""
        if self.redis_client:
            await self.redis_client.close()


# Global cache manager instance
cache_manager = CacheManager() 
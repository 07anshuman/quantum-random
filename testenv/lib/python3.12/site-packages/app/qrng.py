"""
Quantum Random Number Generator (QRNG) module.
Handles fetching true quantum random numbers from various sources.
"""

import asyncio
import aiohttp  # type: ignore
import time
import json
import logging
import secrets
from typing import List, Optional, Dict, Any
from datetime import datetime
import numpy as np  # type: ignore

from .config import settings

logger = logging.getLogger(__name__)


class QRNGSource:
    """Base class for QRNG sources."""
    
    def __init__(self, name: str, url: str, timeout: int = 10):
        self.name = name
        self.url = url
        self.timeout = timeout
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def get_random(self, count: int = 1) -> List[int]:
        """Get random numbers from this source."""
        raise NotImplementedError
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def close(self):
        """Close the session."""
        if self.session and not self.session.closed:
            await self.session.close()


class LocalFallbackQRNG(QRNGSource):
    """Local fallback QRNG using cryptographically secure random numbers."""
    
    def __init__(self):
        super().__init__(
            name="Local Fallback QRNG",
            url="local://fallback",
            timeout=1
        )
    
    async def get_random(self, count: int = 1) -> List[int]:
        """Generate cryptographically secure random numbers."""
        try:
            # Use secrets module for cryptographically secure random numbers
            numbers = [secrets.randbelow(256) for _ in range(count)]
            logger.info(f"Generated {count} local fallback random numbers")
            return numbers
        except Exception as e:
            logger.error(f"Error generating local random numbers: {e}")
            raise


class ANUQRNG(QRNGSource):
    """ANU Quantum Random Number Generator source."""
    
    def __init__(self):
        super().__init__(
            name="ANU QRNG",
            url=settings.anu_api_url,
            timeout=settings.anu_api_timeout
        )
        self.last_request_time = 0
        self.rate_limit_delay = 65  # seconds between requests
    
    async def get_random(self, count: int = 1) -> List[int]:
        """Get random numbers from ANU QRNG with rate limiting."""
        session = await self._get_session()
        
        # Check if we need to wait due to rate limiting
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.rate_limit_delay:
            wait_time = self.rate_limit_delay - time_since_last
            logger.info(f"Rate limit: waiting {wait_time:.1f}s before ANU request")
            await asyncio.sleep(wait_time)
        
        try:
            params = {
                "length": count,
                "type": "uint8"
            }
            
            async with session.get(
                self.url, 
                params=params, 
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as response:
                self.last_request_time = time.time()
                
                if response.status == 200:
                    data = await response.json()
                    if "data" in data:
                        logger.info(f"Successfully fetched {len(data['data'])} numbers from ANU QRNG")
                        return data["data"]
                    else:
                        raise ValueError(f"Invalid response format: {data}")
                elif response.status == 500:
                    # Check if it's a rate limit error
                    text = await response.text()
                    if "rate limit" in text.lower() or "requests per minute" in text.lower():
                        logger.warning("ANU QRNG rate limit hit, will retry after delay")
                        # Wait and retry once
                        await asyncio.sleep(self.rate_limit_delay)
                        return await self.get_random(count)
                    else:
                        raise Exception(f"ANU API error: {response.status} - {text}")
                else:
                    raise Exception(f"ANU API error: {response.status}")
                    
        except Exception as e:
            logger.error(f"Error fetching from ANU QRNG: {e}")
            raise


class CustomQRNG(QRNGSource):
    """Custom QRNG source."""
    
    def __init__(self, url: str):
        super().__init__(
            name="Custom QRNG",
            url=url,
            timeout=settings.custom_qrng_timeout
        )
    
    async def get_random(self, count: int = 1) -> List[int]:
        """Get random numbers from custom QRNG."""
        session = await self._get_session()
        
        try:
            params = {"count": count}
            
            async with session.get(
                self.url, 
                params=params, 
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    # Assume the custom API returns a list of numbers
                    if isinstance(data, list):
                        return data
                    elif "numbers" in data:
                        return data["numbers"]
                    else:
                        raise ValueError(f"Invalid custom QRNG response format: {data}")
                else:
                    raise Exception(f"Custom QRNG API error: {response.status}")
                    
        except Exception as e:
            logger.error(f"Error fetching from custom QRNG: {e}")
            raise


class QRNGManager:
    """Manages multiple QRNG sources with fallback logic."""
    
    def __init__(self):
        self.sources: List[QRNGSource] = []
        self.current_source_index = 0
        self._setup_sources()
    
    def _setup_sources(self):
        """Setup available QRNG sources."""
        # Add ANU as primary source
        self.sources.append(ANUQRNG())
        
        # Add local fallback as secondary source
        self.sources.append(LocalFallbackQRNG())
        
        # Add custom source if configured
        if settings.custom_qrng_url:
            self.sources.append(CustomQRNG(settings.custom_qrng_url))
    
    async def get_random(self, count: int = 1) -> Dict[str, Any]:
        """Get random numbers with fallback logic."""
        last_error = None
        
        for i in range(len(self.sources)):
            source_index = (self.current_source_index + i) % len(self.sources)
            source = self.sources[source_index]
            
            try:
                numbers = await source.get_random(count)
                
                # Update current source to the successful one
                self.current_source_index = source_index
                
                return {
                    "numbers": numbers,
                    "source": source.name,
                    "timestamp": datetime.utcnow().isoformat(),
                    "count": len(numbers)
                }
                
            except Exception as e:
                last_error = e
                logger.warning(f"Source {source.name} failed: {e}")
                continue
        
        # All sources failed
        raise Exception(f"All QRNG sources failed. Last error: {last_error}")
    
    async def get_random_single(self) -> Dict[str, Any]:
        """Get a single random number."""
        result = await self.get_random(1)
        result["random_number"] = result["numbers"][0]
        return result
    
    async def close(self):
        """Close all source sessions."""
        for source in self.sources:
            await source.close()


# Global QRNG manager instance
qrng_manager = QRNGManager() 
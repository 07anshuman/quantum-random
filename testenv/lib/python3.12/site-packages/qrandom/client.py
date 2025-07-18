"""
Quantum Randomness Service Python Client

A simple client library for accessing quantum random numbers.
"""

import asyncio
import aiohttp
import time
import logging
from typing import List, Dict, Any, Optional, Union
from datetime import datetime

logger = logging.getLogger(__name__)


class QuantumRandom:
    """
    Python client for the Quantum Randomness Service.
    
    Provides both synchronous and asynchronous methods for accessing
    quantum random numbers from the service.
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the Quantum Random client.
        
        Args:
            base_url: Base URL of the Quantum Randomness Service
        """
        self.base_url = base_url.rstrip('/')
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make a request to the service."""
        session = await self._get_session()
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Service error {response.status}: {error_text}")
        except Exception as e:
            logger.error(f"Request error: {e}")
            raise
    
    async def get_random(self) -> Dict[str, Any]:
        """
        Get a single quantum random number asynchronously.
        
        Returns:
            Dict containing random_number, source, timestamp, and entropy_score
        """
        return await self._make_request("/random")
    
    async def get_random_batch(self, count: int = 100) -> Dict[str, Any]:
        """
        Get multiple quantum random numbers asynchronously.
        
        Args:
            count: Number of random numbers to get (1-1000)
            
        Returns:
            Dict containing random_numbers, count, source, timestamp, and entropy_score
        """
        if count < 1 or count > 1000:
            raise ValueError("Count must be between 1 and 1000")
        
        return await self._make_request("/random/batch", {"count": count})
    
    async def get_stats(self) -> Dict[str, Any]:
        """
        Get service statistics asynchronously.
        
        Returns:
            Dict containing service statistics and metrics
        """
        return await self._make_request("/stats")
    
    def get_random_sync(self) -> Dict[str, Any]:
        """
        Get a single quantum random number synchronously.
        
        Returns:
            Dict containing random_number, source, timestamp, and entropy_score
        """
        return asyncio.run(self.get_random())
    
    def get_random_batch_sync(self, count: int = 100) -> Dict[str, Any]:
        """
        Get multiple quantum random numbers synchronously.
        
        Args:
            count: Number of random numbers to get (1-1000)
            
        Returns:
            Dict containing random_numbers, count, source, timestamp, and entropy_score
        """
        return asyncio.run(self.get_random_batch(count))
    
    def get_stats_sync(self) -> Dict[str, Any]:
        """
        Get service statistics synchronously.
        
        Returns:
            Dict containing service statistics and metrics
        """
        return asyncio.run(self.get_stats())
    
    def get_random_number(self) -> int:
        """
        Get a single random number as an integer.
        
        Returns:
            Random number (0-255)
        """
        result = self.get_random_sync()
        return result["random_number"]
    
    def get_random_numbers(self, count: int = 100) -> List[int]:
        """
        Get multiple random numbers as a list.
        
        Args:
            count: Number of random numbers to get (1-1000)
            
        Returns:
            List of random numbers (0-255)
        """
        result = self.get_random_batch_sync(count)
        return result["random_numbers"]
    
    async def close(self):
        """Close the client session."""
        if self.session and not self.session.closed:
            await self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        asyncio.run(self.close())


# Convenience functions for quick access
def get_random() -> int:
    """Get a single random number quickly."""
    client = QuantumRandom()
    return client.get_random_number()


def get_random_batch(count: int = 100) -> List[int]:
    """Get multiple random numbers quickly."""
    client = QuantumRandom()
    return client.get_random_numbers(count)


def get_service_stats() -> Dict[str, Any]:
    """Get service statistics quickly."""
    client = QuantumRandom()
    return client.get_stats_sync() 
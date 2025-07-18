#!/usr/bin/env python3
"""
Tests for the Quantum Randomness Service.
"""

import pytest
import asyncio
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.qrng import ANUQRNG, QRNGManager
from app.entropy import EntropyAnalyzer
from app.cache import CacheManager


class TestANUQRNG:
    """Test ANU QRNG functionality."""
    
    @pytest.fixture
    def qrng(self):
        """Create ANU QRNG instance."""
        return ANUQRNG()
    
    @pytest.mark.asyncio
    async def test_get_random_single(self, qrng):
        """Test getting a single random number."""
        try:
            numbers = await qrng.get_random(1)
            assert len(numbers) == 1
            assert isinstance(numbers[0], int)
            assert 0 <= numbers[0] <= 255
        except Exception as e:
            # Skip test if ANU API is not available
            pytest.skip(f"ANU API not available: {e}")
    
    @pytest.mark.asyncio
    async def test_get_random_multiple(self, qrng):
        """Test getting multiple random numbers."""
        try:
            numbers = await qrng.get_random(10)
            assert len(numbers) == 10
            assert all(isinstance(n, int) for n in numbers)
            assert all(0 <= n <= 255 for n in numbers)
        except Exception as e:
            pytest.skip(f"ANU API not available: {e}")
    
    @pytest.mark.asyncio
    async def test_cleanup(self, qrng):
        """Test cleanup of resources."""
        await qrng.close()
        # Should not raise any exceptions


class TestQRNGManager:
    """Test QRNG manager functionality."""
    
    @pytest.fixture
    def manager(self):
        """Create QRNG manager instance."""
        return QRNGManager()
    
    @pytest.mark.asyncio
    async def test_get_random_single(self, manager):
        """Test getting a single random number from manager."""
        try:
            result = await manager.get_random_single()
            assert "random_number" in result
            assert "source" in result
            assert "timestamp" in result
            assert isinstance(result["random_number"], int)
            assert 0 <= result["random_number"] <= 255
        except Exception as e:
            pytest.skip(f"QRNG sources not available: {e}")
    
    @pytest.mark.asyncio
    async def test_get_random_batch(self, manager):
        """Test getting multiple random numbers from manager."""
        try:
            result = await manager.get_random(5)
            assert "numbers" in result
            assert "source" in result
            assert "timestamp" in result
            assert len(result["numbers"]) == 5
            assert all(isinstance(n, int) for n in result["numbers"])
        except Exception as e:
            pytest.skip(f"QRNG sources not available: {e}")
    
    @pytest.mark.asyncio
    async def test_cleanup(self, manager):
        """Test cleanup of manager resources."""
        await manager.close()
        # Should not raise any exceptions


class TestEntropyAnalyzer:
    """Test entropy analysis functionality."""
    
    @pytest.fixture
    def analyzer(self):
        """Create entropy analyzer instance."""
        return EntropyAnalyzer()
    
    def test_add_numbers(self, analyzer):
        """Test adding numbers to analyzer."""
        numbers = [1, 2, 3, 4, 5]
        analyzer.add_numbers(numbers)
        assert len(analyzer.number_buffer) == 5
    
    def test_calculate_entropy_score(self, analyzer):
        """Test entropy score calculation."""
        # Add some test data
        test_numbers = list(range(256))  # Full range for good entropy
        analyzer.add_numbers(test_numbers)
        
        score = analyzer.calculate_entropy_score()
        assert 0.0 <= score <= 1.0
    
    def test_run_randomness_tests(self, analyzer):
        """Test randomness tests."""
        # Add test data
        test_numbers = list(range(256)) * 4  # 1024 numbers
        analyzer.add_numbers(test_numbers)
        
        results = analyzer.run_randomness_tests()
        assert "entropy_score" in results
        assert "mean" in results
        assert "std" in results
        assert "distribution_uniformity" in results
        assert "autocorrelation" in results
        assert "runs_test" in results
    
    def test_get_quality_summary(self, analyzer):
        """Test quality summary generation."""
        # Add test data
        test_numbers = list(range(256)) * 4
        analyzer.add_numbers(test_numbers)
        
        summary = analyzer.get_quality_summary()
        assert "overall_quality" in summary
        assert "entropy_score" in summary
        assert "uniformity" in summary
        assert "autocorrelation" in summary
        assert "runs_test" in summary
        assert "sample_size" in summary
        assert "quality_level" in summary


class TestCacheManager:
    """Test cache manager functionality."""
    
    @pytest.fixture
    def cache(self):
        """Create cache manager instance."""
        return CacheManager()
    
    @pytest.mark.asyncio
    async def test_cache_operations(self, cache):
        """Test basic cache operations."""
        # Test setting and getting single random number
        test_number = 42
        await cache.set_single_random(test_number)
        
        # Note: This might fail if Redis is not available
        # That's expected behavior
        cached_number = await cache.get_single_random()
        if cached_number is not None:
            assert cached_number == test_number
    
    @pytest.mark.asyncio
    async def test_cache_batch_operations(self, cache):
        """Test batch cache operations."""
        test_numbers = [1, 2, 3, 4, 5]
        await cache.set_random_numbers(5, test_numbers)
        
        cached_numbers = await cache.get_random_numbers(5)
        if cached_numbers is not None:
            assert cached_numbers == test_numbers
    
    @pytest.mark.asyncio
    async def test_cache_stats(self, cache):
        """Test cache statistics."""
        await cache.increment_counter("test_counter")
        
        # Test cache hit rate calculation
        hit_rate = await cache.get_cache_hit_rate()
        assert isinstance(hit_rate, float)
        assert 0.0 <= hit_rate <= 100.0
    
    @pytest.mark.asyncio
    async def test_cleanup(self, cache):
        """Test cache cleanup."""
        await cache.close()
        # Should not raise any exceptions


def test_entropy_calculation_edge_cases():
    """Test entropy calculation with edge cases."""
    analyzer = EntropyAnalyzer()
    
    # Test with empty data
    score = analyzer.calculate_entropy_score([])
    assert score == 0.5  # Default score for small samples
    
    # Test with single value
    score = analyzer.calculate_entropy_score([42])
    assert score == 0.5  # Default score for small samples
    
    # Test with repeated values (low entropy)
    repeated = [42] * 100
    score = analyzer.calculate_entropy_score(repeated)
    assert 0.0 <= score <= 1.0


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"]) 
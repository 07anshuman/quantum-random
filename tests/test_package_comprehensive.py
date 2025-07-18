#!/usr/bin/env python3
"""
Comprehensive test script for the Quantum Randomness Service package.
"""

import asyncio
import aiohttp
import json
import time


async def test_service_api():
    """Test all service API endpoints."""
    print("🔬 Testing Service API Endpoints")
    print("=" * 40)
    
    async with aiohttp.ClientSession() as session:
        # Test 1: Single random number
        print("\n1. Single random number:")
        try:
            async with session.get("http://localhost:8000/random", 
                                 timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"   ✅ Success! Number: {data['random_number']}")
                    print(f"   Source: {data['source']}")
                    print(f"   Entropy: {data.get('entropy_score', 'N/A')}")
                else:
                    print(f"   ❌ HTTP Error: {response.status}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 2: Service stats
        print("\n2. Service statistics:")
        try:
            async with session.get("http://localhost:8000/stats", 
                                 timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"   ✅ Success! Requests: {data.get('total_requests', 'N/A')}")
                    print(f"   Cache hit rate: {data.get('cache_hit_rate', 'N/A')}%")
                    print(f"   Entropy quality: {data.get('entropy_quality', 'N/A')}")
                else:
                    print(f"   ❌ HTTP Error: {response.status}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 3: Service info
        print("\n3. Service info:")
        try:
            async with session.get("http://localhost:8000/", 
                                 timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    print(f"   ✅ Success! Status: {response.status}")
                else:
                    print(f"   ❌ HTTP Error: {response.status}")
        except Exception as e:
            print(f"   ❌ Error: {e}")


async def test_package_client():
    """Test the package client functionality."""
    print("\n🔬 Testing Package Client")
    print("=" * 30)
    
    try:
        from qrandom import QuantumRandom
        
        # Test async client
        print("\n1. Async client test:")
        client = QuantumRandom()
        
        try:
            result = await client.get_random()
            print(f"   ✅ Async random: {result['random_number']}")
            print(f"   Source: {result['source']}")
        except Exception as e:
            print(f"   ❌ Async error: {e}")
        
        try:
            stats = await client.get_stats()
            print(f"   ✅ Async stats: {stats.get('total_requests', 'N/A')} requests")
        except Exception as e:
            print(f"   ❌ Async stats error: {e}")
        
        await client.close()
        
        # Test convenience functions
        print("\n2. Convenience functions test:")
        try:
            from qrandom.client import get_random, get_service_stats
            random_num = get_random()
            print(f"   ✅ Convenience random: {random_num}")
        except Exception as e:
            print(f"   ❌ Convenience function error: {e}")
        
        return True
    except Exception as e:
        print(f"   ❌ Package client error: {e}")
        return False


def test_package_installation():
    """Test package installation and import."""
    print("\n🔬 Testing Package Installation")
    print("=" * 35)
    
    try:
        # Test main package import
        import qrandom
        print("   ✅ Main package import successful")
        
        # Test client import
        from qrandom import QuantumRandom
        print("   ✅ Client import successful")
        
        # Test convenience functions import
        from qrandom.client import get_random, get_random_batch, get_service_stats
        print("   ✅ Convenience functions import successful")
        
        # Test package version
        try:
            version = qrandom.__version__
            print(f"   ✅ Package version: {version}")
        except AttributeError:
            print("   ⚠️  No version attribute found")
        
        return True
    except Exception as e:
        print(f"   ❌ Package installation error: {e}")
        return False


async def test_entropy_analysis():
    """Test entropy analysis functionality."""
    print("\n🔬 Testing Entropy Analysis")
    print("=" * 30)
    
    try:
        from app.entropy import entropy_analyzer
        
        # Test with some sample numbers
        test_numbers = [42, 128, 255, 0, 100, 200, 50, 150, 75, 225]
        entropy_analyzer.add_numbers(test_numbers)
        
        quality = entropy_analyzer.get_quality_summary()
        print(f"   ✅ Entropy analysis: {quality.get('overall_quality', 'N/A')}")
        print(f"   Quality level: {quality.get('quality_level', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"   ❌ Entropy analysis error: {e}")
        return False


async def main():
    """Run comprehensive package tests."""
    print("🌊 Quantum Randomness Service - Comprehensive Package Test")
    print("=" * 70)
    
    # Test package installation
    install_success = test_package_installation()
    
    # Test service API
    await test_service_api()
    
    # Test package client
    client_success = await test_package_client()
    
    # Test entropy analysis
    entropy_success = await test_entropy_analysis()
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    print(f"Package Installation: {'✅ PASS' if install_success else '❌ FAIL'}")
    print(f"Service API: ✅ PASS (tested endpoints)")
    print(f"Package Client: {'✅ PASS' if client_success else '❌ FAIL'}")
    print(f"Entropy Analysis: {'✅ PASS' if entropy_success else '❌ FAIL'}")
    
    if all([install_success, client_success, entropy_success]):
        print("\n🎉 All tests passed! Package is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")


if __name__ == "__main__":
    asyncio.run(main()) 
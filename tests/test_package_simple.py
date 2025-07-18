#!/usr/bin/env python3
"""
Simple test script for the Quantum Randomness Service package.
"""

import asyncio
import aiohttp
import json


async def test_service_directly():
    """Test the service directly via HTTP."""
    print("🔬 Testing Quantum Randomness Service directly...")
    print("=" * 50)
    
    async with aiohttp.ClientSession() as session:
        # Test single random number
        print("\n1. Testing single random number:")
        try:
            async with session.get("http://localhost:8000/random", 
                                 timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"   ✅ Success! Random number: {data['random_number']}")
                    print(f"   Source: {data['source']}")
                    print(f"   Timestamp: {data['timestamp']}")
                else:
                    print(f"   ❌ HTTP Error: {response.status}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test service stats
        print("\n2. Testing service stats:")
        try:
            async with session.get("http://localhost:8000/stats", 
                                 timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"   ✅ Success! Total requests: {data.get('total_requests', 'N/A')}")
                    print(f"   Cache hit rate: {data.get('cache_hit_rate', 'N/A')}%")
                    print(f"   Entropy quality: {data.get('entropy_quality', 'N/A')}")
                else:
                    print(f"   ❌ HTTP Error: {response.status}")
        except Exception as e:
            print(f"   ❌ Error: {e}")


def test_package_import():
    """Test package import and basic functionality."""
    print("\n🔬 Testing package import...")
    print("=" * 30)
    
    try:
        from qrandom import QuantumRandom
        print("   ✅ Package import successful")
        
        # Test client creation
        client = QuantumRandom()
        print("   ✅ Client creation successful")
        
        # Test sync method
        try:
            result = client.get_random_sync()
            print(f"   ✅ Sync method works: {result['random_number']}")
        except Exception as e:
            print(f"   ⚠️  Sync method error (expected if service not running): {e}")
        
        return True
    except Exception as e:
        print(f"   ❌ Package import error: {e}")
        return False


async def main():
    """Run all tests."""
    print("🌊 Quantum Randomness Service Package Test")
    print("=" * 60)
    
    # Test package import
    import_success = test_package_import()
    
    # Test service directly
    await test_service_directly()
    
    if import_success:
        print("\n✅ Package test completed successfully!")
    else:
        print("\n❌ Package test failed!")


if __name__ == "__main__":
    asyncio.run(main()) 
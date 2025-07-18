#!/usr/bin/env python3
"""
Test script to demonstrate ANU QRNG rate limiting.
"""

import asyncio
import aiohttp
import json
import time


async def test_anu_rate_limit():
    """Test ANU QRNG API rate limiting."""
    url = "https://qrng.anu.edu.au/API/jsonI.php"
    
    print("🔬 Testing ANU QRNG Rate Limiting...")
    print(f"URL: {url}")
    print("=" * 50)
    
    async with aiohttp.ClientSession() as session:
        # Test 1: First request (should succeed)
        print("\n📊 Test 1: First request (should succeed)")
        params = {"length": 1, "type": "uint8"}
        
        try:
            start_time = time.time()
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
                elapsed = time.time() - start_time
                print(f"Status: {response.status}")
                print(f"Response time: {elapsed:.2f}s")
                
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Success! Got random number: {data['data'][0]}")
                else:
                    text = await response.text()
                    print(f"❌ Error: {text}")
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        # Test 2: Immediate second request (should fail due to rate limit)
        print("\n📊 Test 2: Immediate second request (should fail)")
        params = {"length": 1, "type": "uint8"}
        
        try:
            start_time = time.time()
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
                elapsed = time.time() - start_time
                print(f"Status: {response.status}")
                print(f"Response time: {elapsed:.2f}s")
                
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Unexpected success! Got random number: {data['data'][0]}")
                else:
                    text = await response.text()
                    print(f"❌ Expected rate limit error: {text}")
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        # Test 3: Wait 65 seconds and try again
        print("\n📊 Test 3: Waiting 65 seconds for rate limit to reset...")
        for i in range(65, 0, -1):
            print(f"\r⏳ Waiting: {i}s remaining...", end="", flush=True)
            await asyncio.sleep(1)
        print("\n")
        
        print("📊 Test 3: Request after waiting (should succeed)")
        params = {"length": 1, "type": "uint8"}
        
        try:
            start_time = time.time()
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
                elapsed = time.time() - start_time
                print(f"Status: {response.status}")
                print(f"Response time: {elapsed:.2f}s")
                
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Success! Got random number: {data['data'][0]}")
                else:
                    text = await response.text()
                    print(f"❌ Error: {text}")
        except Exception as e:
            print(f"❌ Exception: {e}")


if __name__ == "__main__":
    asyncio.run(test_anu_rate_limit()) 
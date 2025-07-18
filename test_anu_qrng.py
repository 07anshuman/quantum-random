#!/usr/bin/env python3
"""
Test script to check if ANU QRNG API is working.
"""

import asyncio
import aiohttp
import json
import time


async def test_anu_qrng():
    """Test ANU QRNG API directly."""
    url = "https://qrng.anu.edu.au/API/jsonI.php"
    
    print("🔬 Testing ANU QRNG API...")
    print(f"URL: {url}")
    print("=" * 50)
    
    async with aiohttp.ClientSession() as session:
        # Test 1: Single number
        print("\n📊 Test 1: Single random number")
        params = {"length": 1, "type": "uint8"}
        
        try:
            start_time = time.time()
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
                elapsed = time.time() - start_time
                print(f"Status: {response.status}")
                print(f"Response time: {elapsed:.2f}s")
                
                if response.status == 200:
                    data = await response.json()
                    print(f"Response: {json.dumps(data, indent=2)}")
                    
                    if "data" in data:
                        print(f"✅ Success! Got {len(data['data'])} random number(s)")
                        print(f"Numbers: {data['data']}")
                    else:
                        print("❌ Invalid response format")
                else:
                    print(f"❌ HTTP Error: {response.status}")
                    text = await response.text()
                    print(f"Error response: {text}")
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        # Test 2: Multiple numbers
        print("\n📊 Test 2: Multiple random numbers")
        params = {"length": 5, "type": "uint8"}
        
        try:
            start_time = time.time()
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
                elapsed = time.time() - start_time
                print(f"Status: {response.status}")
                print(f"Response time: {elapsed:.2f}s")
                
                if response.status == 200:
                    data = await response.json()
                    print(f"Response: {json.dumps(data, indent=2)}")
                    
                    if "data" in data:
                        print(f"✅ Success! Got {len(data['data'])} random number(s)")
                        print(f"Numbers: {data['data']}")
                    else:
                        print("❌ Invalid response format")
                else:
                    print(f"❌ HTTP Error: {response.status}")
                    text = await response.text()
                    print(f"Error response: {text}")
        except Exception as e:
            print(f"❌ Exception: {e}")
        
        # Test 3: Different data type
        print("\n📊 Test 3: Different data type (hex16)")
        params = {"length": 3, "type": "hex16"}
        
        try:
            start_time = time.time()
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
                elapsed = time.time() - start_time
                print(f"Status: {response.status}")
                print(f"Response time: {elapsed:.2f}s")
                
                if response.status == 200:
                    data = await response.json()
                    print(f"Response: {json.dumps(data, indent=2)}")
                    
                    if "data" in data:
                        print(f"✅ Success! Got {len(data['data'])} random hex values")
                        print(f"Hex values: {data['data']}")
                    else:
                        print("❌ Invalid response format")
                else:
                    print(f"❌ HTTP Error: {response.status}")
                    text = await response.text()
                    print(f"Error response: {text}")
        except Exception as e:
            print(f"❌ Exception: {e}")


if __name__ == "__main__":
    asyncio.run(test_anu_qrng()) 
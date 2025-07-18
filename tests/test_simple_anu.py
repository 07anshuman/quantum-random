#!/usr/bin/env python3
"""
Simple test to check ANU QRNG status.
"""

import asyncio
import aiohttp
import json


async def test_simple():
    """Simple test of ANU QRNG."""
    url = "https://qrng.anu.edu.au/API/jsonI.php"
    
    print("🔬 Simple ANU QRNG Test")
    print("=" * 30)
    
    async with aiohttp.ClientSession() as session:
        params = {"length": 1, "type": "uint8"}
        
        try:
            print(f"Making request to: {url}")
            print(f"Parameters: {params}")
            
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
                print(f"Status: {response.status}")
                print(f"Headers: {dict(response.headers)}")
                
                text = await response.text()
                print(f"Response: {text}")
                
                if response.status == 200:
                    try:
                        data = json.loads(text)
                        print(f"✅ Success! JSON: {json.dumps(data, indent=2)}")
                    except json.JSONDecodeError:
                        print("❌ Invalid JSON response")
                else:
                    print(f"❌ HTTP Error: {response.status}")
                    
        except Exception as e:
            print(f"❌ Exception: {e}")


if __name__ == "__main__":
    asyncio.run(test_simple()) 
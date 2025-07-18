#!/usr/bin/env python3
"""
Basic usage example for the Quantum Randomness Service.
"""

import asyncio
import sys
import os

# Add the parent directory to the path so we can import the client
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from qrandom import QuantumRandom


async def main():
    """Demonstrate basic usage of the Quantum Randomness Service."""
    
    print("🌊 Quantum Randomness Service - Basic Usage Example")
    print("=" * 50)
    
    # Create client
    client = QuantumRandom()
    
    try:
        # Get a single random number
        print("\n1. Getting a single quantum random number...")
        random_number = await client.get_random()
        print(f"   Random number: {random_number}")
        
        # Get multiple random numbers
        print("\n2. Getting 10 quantum random numbers...")
        random_numbers = await client.get_random_batch(count=10)
        print(f"   Random numbers: {random_numbers}")
        
        # Get service statistics
        print("\n3. Getting service statistics...")
        stats = await client.get_stats()
        print(f"   Total requests: {stats.get('total_requests', 'N/A')}")
        print(f"   Cache hit rate: {stats.get('cache_hit_rate', 'N/A')}%")
        print(f"   Entropy quality: {stats.get('entropy_quality', 'N/A')}")
        
        # Stream random numbers
        # print("\n4. Streaming random numbers (press Ctrl+C to stop)...")
        # count = 0
        # async for number in client.stream_random():
        #     print(f"   Stream #{count}: {number}")
        #     count += 1
        #     if count >= 5:  # Stop after 5 numbers for demo
        #         break
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the Quantum Randomness Service is running on http://localhost:8000")
    
    finally:
        await client.close()


def sync_example():
    """Synchronous usage example."""
    print("\n" + "=" * 50)
    print("Synchronous Usage Example")
    print("=" * 50)
    
    try:
        # Synchronous usage
        client = QuantumRandom()
        
        print("\n1. Getting a single random number (sync)...")
        random_number = client.get_random_sync()
        print(f"   Random number: {random_number}")
        
        print("\n2. Getting 5 random numbers (sync)...")
        random_numbers = client.get_random_batch_sync(count=5)
        print(f"   Random numbers: {random_numbers}")
        
        print("\n3. Getting stats (sync)...")
        stats = client.get_stats_sync()
        print(f"   Uptime: {stats.get('uptime_seconds', 'N/A')} seconds")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the Quantum Randomness Service is running on http://localhost:8000")


if __name__ == "__main__":
    print("Starting Quantum Randomness Service examples...")
    
    # Run async example
    asyncio.run(main())
    
    # Run sync example
    sync_example()
    
    print("\n✅ Examples completed!") 
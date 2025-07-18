#!/usr/bin/env python3
"""
Example showing how to use the Quantum Randomness Service package.

This example demonstrates the Python client library usage.
"""

from qrandom import QuantumRandom
from qrandom.client import get_random, get_random_batch, get_service_stats
import asyncio


def sync_example():
    """Synchronous usage examples."""
    print("🔬 Synchronous Usage Examples")
    print("=" * 40)
    
    # Method 1: Using convenience functions
    print("\n1. Quick random number:")
    random_num = get_random()
    print(f"   Random number: {random_num}")
    
    print("\n2. Quick batch of numbers:")
    numbers = get_random_batch(5)
    print(f"   Random numbers: {numbers}")
    
    print("\n3. Service statistics:")
    stats = get_service_stats()
    print(f"   Total requests: {stats.get('total_requests', 'N/A')}")
    print(f"   Cache hit rate: {stats.get('cache_hit_rate', 'N/A')}%")
    print(f"   Entropy quality: {stats.get('entropy_quality', 'N/A')}")
    
    # Method 2: Using the client class
    print("\n4. Using client class:")
    client = QuantumRandom()
    
    # Get single random number with metadata
    result = client.get_random_sync()
    print(f"   Random number: {result['random_number']}")
    print(f"   Source: {result['source']}")
    print(f"   Timestamp: {result['timestamp']}")
    print(f"   Entropy score: {result.get('entropy_score', 'N/A')}")
    
    # Get batch with metadata
    batch_result = client.get_random_batch_sync(3)
    print(f"\n   Batch numbers: {batch_result['random_numbers']}")
    print(f"   Source: {batch_result['source']}")
    print(f"   Count: {batch_result['count']}")


async def async_example():
    """Asynchronous usage examples."""
    print("\n🔬 Asynchronous Usage Examples")
    print("=" * 40)
    
    client = QuantumRandom()
    
    try:
        # Get single random number
        result = await client.get_random()
        print(f"\n1. Async random number: {result['random_number']}")
        print(f"   Source: {result['source']}")
        
        # Get batch
        batch_result = await client.get_random_batch(4)
        print(f"\n2. Async batch: {batch_result['random_numbers']}")
        print(f"   Source: {batch_result['source']}")
        
        # Get stats
        stats = await client.get_stats()
        print(f"\n3. Async stats:")
        print(f"   Uptime: {stats.get('uptime_seconds', 'N/A')} seconds")
        print(f"   Active connections: {stats.get('active_connections', 'N/A')}")
        
    finally:
        await client.close()


def context_manager_example():
    """Context manager usage example."""
    print("\n🔬 Context Manager Example")
    print("=" * 40)
    
    with QuantumRandom() as client:
        # Get multiple random numbers
        numbers = client.get_random_numbers(10)
        print(f"   Random numbers: {numbers}")
        
        # Get stats
        stats = client.get_stats_sync()
        print(f"   Service uptime: {stats.get('uptime_seconds', 'N/A')} seconds")


def error_handling_example():
    """Error handling example."""
    print("\n🔬 Error Handling Example")
    print("=" * 40)
    
    try:
        # Try to connect to a non-existent service
        client = QuantumRandom("http://localhost:9999")
        result = client.get_random_sync()
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   Expected error: {e}")


def main():
    """Run all examples."""
    print("🌊 Quantum Randomness Service Package Examples")
    print("=" * 60)
    
    # Run synchronous examples
    sync_example()
    
    # Run context manager example
    context_manager_example()
    
    # Run error handling example
    error_handling_example()
    
    # Run asynchronous examples
    asyncio.run(async_example())
    
    print("\n✅ All examples completed!")
    print("\n📖 For more information, see the README.md file")


if __name__ == "__main__":
    main() 
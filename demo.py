#!/usr/bin/env python3
"""
Comprehensive demo of the Quantum Randomness Service.
"""

import asyncio
import time
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from qrandom import QuantumRandom


async def demo_basic_functionality():
    """Demonstrate basic functionality."""
    print("🔧 Basic Functionality Demo")
    print("=" * 40)
    
    client = QuantumRandom()
    
    try:
        # Single random number
        print("\n1. Getting a single quantum random number...")
        start_time = time.time()
        random_number = await client.get_random()
        response_time = (time.time() - start_time) * 1000
        print(f"   Random number: {random_number}")
        print(f"   Response time: {response_time:.2f}ms")
        
        # Batch of random numbers
        print("\n2. Getting 20 quantum random numbers...")
        start_time = time.time()
        random_numbers = await client.get_random_batch(count=20)
        response_time = (time.time() - start_time) * 1000
        print(f"   Numbers: {random_numbers[:5]}... (showing first 5)")
        print(f"   Response time: {response_time:.2f}ms")
        
        # Service statistics
        print("\n3. Getting service statistics...")
        stats = await client.get_stats()
        print(f"   Total requests: {stats.get('total_requests', 'N/A')}")
        print(f"   Cache hit rate: {stats.get('cache_hit_rate', 'N/A')}%")
        print(f"   Entropy quality: {stats.get('entropy_quality', 'N/A')}")
        print(f"   Uptime: {stats.get('uptime_seconds', 'N/A')} seconds")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("   Make sure the service is running on http://localhost:8000")
        return False
    
    finally:
        await client.close()
    
    return True


async def demo_streaming():
    """Demonstrate WebSocket streaming."""
    print("\n\n🔄 Streaming Demo")
    print("=" * 40)
    
    client = QuantumRandom()
    
    try:
        print("Streaming quantum random numbers (10 numbers)...")
        count = 0
        start_time = time.time()
        
        async for number in client.stream_random():
            count += 1
            print(f"   #{count}: {number}")
            
            if count >= 10:
                break
        
        total_time = time.time() - start_time
        rate = count / total_time
        print(f"\n   Streamed {count} numbers in {total_time:.2f}s")
        print(f"   Rate: {rate:.1f} numbers/second")
        
    except Exception as e:
        print(f"❌ Streaming error: {e}")
        return False
    
    finally:
        await client.close()
    
    return True


async def demo_entropy_analysis():
    """Demonstrate entropy analysis."""
    print("\n\n📊 Entropy Analysis Demo")
    print("=" * 40)
    
    client = QuantumRandom()
    
    try:
        # Get a larger batch for analysis
        print("Collecting 100 random numbers for entropy analysis...")
        numbers = await client.get_random_batch(count=100)
        
        # Basic statistics
        import statistics
        mean = statistics.mean(numbers)
        std = statistics.stdev(numbers)
        min_val = min(numbers)
        max_val = max(numbers)
        
        print(f"   Sample size: {len(numbers)}")
        print(f"   Mean: {mean:.2f}")
        print(f"   Standard deviation: {std:.2f}")
        print(f"   Range: {min_val} - {max_val}")
        
        # Distribution analysis
        from collections import Counter
        counter = Counter(numbers)
        unique_count = len(counter)
        print(f"   Unique values: {unique_count}/256 ({unique_count/256*100:.1f}%)")
        
        # Check for patterns
        consecutive_same = sum(1 for i in range(len(numbers)-1) if numbers[i] == numbers[i+1])
        print(f"   Consecutive duplicates: {consecutive_same}")
        
        # Entropy quality from service
        stats = await client.get_stats()
        entropy_quality = stats.get('entropy_quality', 0)
        quality_level = stats.get('quality_level', 'Unknown')
        print(f"   Service entropy quality: {entropy_quality:.2%}")
        print(f"   Quality level: {quality_level}")
        
    except Exception as e:
        print(f"❌ Entropy analysis error: {e}")
        return False
    
    finally:
        await client.close()
    
    return True


async def demo_cryptography():
    """Demonstrate cryptography applications."""
    print("\n\n🔐 Cryptography Demo")
    print("=" * 40)
    
    client = QuantumRandom()
    
    try:
        # Generate cryptographic nonce
        print("1. Generating cryptographic nonce...")
        nonce_numbers = await client.get_random_batch(count=32)
        nonce_bytes = bytes(nonce_numbers)
        import base64
        nonce_b64 = base64.b64encode(nonce_bytes).decode('utf-8')
        print(f"   Nonce (base64): {nonce_b64}")
        print(f"   Nonce (hex): {nonce_bytes.hex()}")
        
        # Generate encryption key
        print("\n2. Generating encryption key...")
        key_numbers = await client.get_random_batch(count=32)
        key_bytes = bytes(key_numbers)
        key_b64 = base64.b64encode(key_bytes).decode('utf-8')
        print(f"   Key (base64): {key_b64}")
        
        # Generate password salt
        print("\n3. Generating password salt...")
        salt_numbers = await client.get_random_batch(count=16)
        salt_bytes = bytes(salt_numbers)
        salt_b64 = base64.b64encode(salt_bytes).decode('utf-8')
        print(f"   Salt (base64): {salt_b64}")
        
        # Demonstrate password hashing
        print("\n4. Password hashing with quantum salt...")
        import hashlib
        password = "my_secure_password"
        password_bytes = password.encode('utf-8')
        combined = salt_bytes + password_bytes
        hash_obj = hashlib.sha256(combined)
        hash_hex = hash_obj.hexdigest()
        print(f"   Password: {password}")
        print(f"   Hashed: {hash_hex}")
        
    except Exception as e:
        print(f"❌ Cryptography demo error: {e}")
        return False
    
    finally:
        await client.close()
    
    return True


async def demo_performance():
    """Demonstrate performance characteristics."""
    print("\n\n⚡ Performance Demo")
    print("=" * 40)
    
    client = QuantumRandom()
    
    try:
        # Test single number performance
        print("Testing single number performance...")
        times = []
        for i in range(5):
            start_time = time.time()
            await client.get_random()
            response_time = (time.time() - start_time) * 1000
            times.append(response_time)
            print(f"   Request {i+1}: {response_time:.2f}ms")
        
        avg_time = sum(times) / len(times)
        print(f"   Average response time: {avg_time:.2f}ms")
        
        # Test batch performance
        print("\nTesting batch performance...")
        batch_sizes = [10, 50, 100]
        for size in batch_sizes:
            start_time = time.time()
            numbers = await client.get_random_batch(count=size)
            response_time = (time.time() - start_time) * 1000
            rate = size / (response_time / 1000)
            print(f"   {size} numbers: {response_time:.2f}ms ({rate:.1f} numbers/sec)")
        
        # Cache performance
        print("\nTesting cache performance...")
        stats = await client.get_stats()
        cache_hit_rate = stats.get('cache_hit_rate', 0)
        print(f"   Cache hit rate: {cache_hit_rate:.1f}%")
        
    except Exception as e:
        print(f"❌ Performance demo error: {e}")
        return False
    
    finally:
        await client.close()
    
    return True


async def main():
    """Run all demos."""
    print("🌊 Quantum Randomness Service - Comprehensive Demo")
    print("=" * 60)
    
    demos = [
        ("Basic Functionality", demo_basic_functionality),
        ("Streaming", demo_streaming),
        ("Entropy Analysis", demo_entropy_analysis),
        ("Cryptography", demo_cryptography),
        ("Performance", demo_performance),
    ]
    
    results = []
    
    for name, demo_func in demos:
        print(f"\n{'='*20} {name} {'='*20}")
        try:
            success = await demo_func()
            results.append((name, success))
        except Exception as e:
            print(f"❌ {name} demo failed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 Demo Summary")
    print("=" * 60)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {name}: {status}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\n   Overall: {passed}/{total} demos passed")
    
    if passed == total:
        print("\n🎉 All demos completed successfully!")
    else:
        print(f"\n⚠️  {total - passed} demo(s) failed. Check the service status.")


if __name__ == "__main__":
    print("Starting Quantum Randomness Service demo...")
    asyncio.run(main()) 
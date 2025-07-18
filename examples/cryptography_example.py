#!/usr/bin/env python3
"""
Cryptography example using quantum random numbers.
"""

import asyncio
import sys
import os
import secrets
import hashlib
import base64

# Add the parent directory to the path so we can import the client
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from qrandom import QuantumRandom


async def generate_quantum_nonce():
    """Generate a cryptographically secure nonce using quantum randomness."""
    client = QuantumRandom()
    
    try:
        # Get 32 random bytes (256 bits) for a strong nonce
        random_numbers = await client.get_random_batch(count=32)
        
        # Convert to bytes
        nonce_bytes = bytes(random_numbers)
        
        # Encode as base64 for easy handling
        nonce_b64 = base64.b64encode(nonce_bytes).decode('utf-8')
        
        return nonce_b64, nonce_bytes
        
    finally:
        await client.close()


async def generate_quantum_key(length: int = 256):
    """Generate a quantum random key of specified bit length."""
    client = QuantumRandom()
    
    try:
        # Calculate number of bytes needed
        byte_length = length // 8
        if length % 8 != 0:
            byte_length += 1
        
        # Get random numbers
        random_numbers = await client.get_random_batch(count=byte_length)
        
        # Convert to bytes
        key_bytes = bytes(random_numbers)
        
        # Truncate to exact bit length if needed
        if length % 8 != 0:
            # Clear unused bits
            mask = (1 << (length % 8)) - 1
            key_bytes = key_bytes[:-1] + bytes([key_bytes[-1] & mask])
        
        return key_bytes
        
    finally:
        await client.close()


async def quantum_password_salt():
    """Generate a quantum random salt for password hashing."""
    client = QuantumRandom()
    
    try:
        # Get 16 random bytes for salt
        random_numbers = await client.get_random_batch(count=16)
        salt_bytes = bytes(random_numbers)
        
        return salt_bytes
        
    finally:
        await client.close()


async def quantum_encryption_key():
    """Generate a quantum random encryption key."""
    client = QuantumRandom()
    
    try:
        # Get 32 random bytes for AES-256 key
        random_numbers = await client.get_random_batch(count=32)
        key_bytes = bytes(random_numbers)
        
        return key_bytes
        
    finally:
        await client.close()


def hash_with_quantum_salt(password: str, salt: bytes) -> str:
    """Hash a password with quantum random salt."""
    # Combine password and salt
    password_bytes = password.encode('utf-8')
    combined = salt + password_bytes
    
    # Hash with SHA-256
    hash_obj = hashlib.sha256(combined)
    hash_hex = hash_obj.hexdigest()
    
    # Return salt (base64) + hash
    salt_b64 = base64.b64encode(salt).decode('utf-8')
    return f"{salt_b64}:{hash_hex}"


async def main():
    """Demonstrate quantum randomness in cryptography."""
    
    print("🔐 Quantum Randomness in Cryptography")
    print("=" * 50)
    
    try:
        # 1. Generate quantum nonce
        print("\n1. Generating quantum random nonce...")
        nonce_b64, nonce_bytes = await generate_quantum_nonce()
        print(f"   Nonce (base64): {nonce_b64}")
        print(f"   Nonce (hex): {nonce_bytes.hex()}")
        
        # 2. Generate quantum encryption key
        print("\n2. Generating quantum random encryption key...")
        key_bytes = await quantum_encryption_key()
        print(f"   Key (base64): {base64.b64encode(key_bytes).decode('utf-8')}")
        print(f"   Key (hex): {key_bytes.hex()}")
        
        # 3. Generate quantum salt for password
        print("\n3. Generating quantum random salt for password...")
        salt_bytes = await quantum_password_salt()
        print(f"   Salt (base64): {base64.b64encode(salt_bytes).decode('utf-8')}")
        
        # 4. Hash password with quantum salt
        print("\n4. Hashing password with quantum salt...")
        password = "my_secure_password"
        hashed_password = hash_with_quantum_salt(password, salt_bytes)
        print(f"   Password: {password}")
        print(f"   Hashed: {hashed_password}")
        
        # 5. Generate quantum random number for session ID
        print("\n5. Generating quantum random session ID...")
        client = QuantumRandom()
        session_numbers = await client.get_random_batch(count=16)
        session_id = base64.b64encode(bytes(session_numbers)).decode('utf-8')
        print(f"   Session ID: {session_id}")
        await client.close()
        
        # 6. Demonstrate entropy quality
        print("\n6. Checking entropy quality...")
        client = QuantumRandom()
        stats = await client.get_stats()
        entropy_quality = stats.get('entropy_quality', 0)
        print(f"   Entropy Quality: {entropy_quality:.2%}")
        print(f"   Quality Level: {stats.get('quality_level', 'Unknown')}")
        await client.close()
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the Quantum Randomness Service is running on http://localhost:8000")


def compare_with_pseudorandom():
    """Compare quantum randomness with pseudorandom."""
    print("\n" + "=" * 50)
    print("Comparison: Quantum vs Pseudorandom")
    print("=" * 50)
    
    # Generate pseudorandom numbers
    print("\nPseudorandom numbers (Python secrets):")
    for i in range(5):
        number = secrets.randbelow(256)
        print(f"   {i+1}: {number}")
    
    print("\nNote: Quantum random numbers are truly random,")
    print("while pseudorandom numbers are deterministic and")
    print("potentially predictable given enough information.")


if __name__ == "__main__":
    print("Starting Quantum Cryptography examples...")
    
    # Run quantum cryptography examples
    asyncio.run(main())
    
    # Compare with pseudorandom
    compare_with_pseudorandom()
    
    print("\n✅ Cryptography examples completed!") 
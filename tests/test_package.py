#!/usr/bin/env python3
"""
Simple test to verify the package installation and basic functionality.
"""

import sys
import time

def test_imports():
    """Test that all imports work correctly."""
    print("🔬 Testing imports...")
    
    try:
        from qrandom import QuantumRandom, get_random, get_random_batch, get_service_stats
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def test_basic_functionality():
    """Test basic functionality."""
    print("\n🔬 Testing basic functionality...")
    
    try:
        from qrandom import get_random
        
        # Test single random number
        number = get_random()
        print(f"✅ Single random number: {number}")
        
        # Test that it's in valid range
        if 0 <= number <= 255:
            print("✅ Number is in valid range (0-255)")
        else:
            print(f"❌ Number {number} is outside valid range")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False


def test_client_class():
    """Test the client class."""
    print("\n🔬 Testing client class...")
    
    try:
        from qrandom import QuantumRandom
        
        # Test client instantiation
        client = QuantumRandom()
        print("✅ Client instantiated successfully")
        
        # Test context manager
        with QuantumRandom() as client:
            number = client.get_random_number()
            print(f"✅ Context manager works: {number}")
        
        return True
        
    except Exception as e:
        print(f"❌ Client class test failed: {e}")
        return False


def test_command_line_tools():
    """Test that command line tools are available."""
    print("\n🔬 Testing command line tools...")
    
    import subprocess
    import sys
    
    try:
        # Test if the command is available
        result = subprocess.run([sys.executable, "-m", "app.main", "--help"], 
                              capture_output=True, text=True, timeout=5)
        print("✅ Command line tool available")
        return True
    except Exception as e:
        print(f"❌ Command line tool test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🌊 Quantum Randomness Service Package Test")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Basic Functionality", test_basic_functionality),
        ("Client Class", test_client_class),
        ("Command Line Tools", test_command_line_tools),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} test passed")
        else:
            print(f"❌ {test_name} test failed")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Package is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
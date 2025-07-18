# Quantum Randomness Service - Package Summary

## 📦 Package Structure

```
quantum-randomness-service/
├── app/                    # Main service application
│   ├── __init__.py
│   ├── main.py            # FastAPI application
│   ├── config.py          # Configuration settings
│   ├── models.py          # Pydantic models
│   ├── qrng.py           # QRNG sources and manager
│   ├── cache.py          # Caching layer
│   └── entropy.py        # Entropy analysis
├── qrandom/              # Python client library
│   ├── __init__.py
│   └── client.py         # Client implementation
├── examples/             # Usage examples
├── tests/               # Test suite
├── setup.py             # Package configuration
├── requirements.txt      # Dependencies
├── README.md           # Documentation
└── MANIFEST.in         # Package files
```

## 🚀 Installation

### For Users

```bash
# Basic installation
pip install quantum-randomness-service

# With Redis support
pip install quantum-randomness-service[redis]

# With development dependencies
pip install quantum-randomness-service[dev]
```

### For Developers

```bash
# Clone and install in development mode
git clone <repository>
cd quantum-randomness-service
pip install -e .
```

## 📚 Usage

### Quick Start

```python
from qrandom import get_random, get_random_batch

# Get a single random number
number = get_random()
print(f"Random number: {number}")

# Get multiple random numbers
numbers = get_random_batch(10)
print(f"Random numbers: {numbers}")
```

### Advanced Usage

```python
from qrandom import QuantumRandom
import asyncio

# Synchronous usage
client = QuantumRandom()
result = client.get_random_sync()
print(f"Number: {result['random_number']}")
print(f"Source: {result['source']}")

# Asynchronous usage
async def main():
    client = QuantumRandom()
    result = await client.get_random()
    print(f"Number: {result['random_number']}")
    await client.close()

asyncio.run(main())

# Context manager usage
with QuantumRandom() as client:
    numbers = client.get_random_numbers(5)
    print(f"Numbers: {numbers}")
```

## 🔧 Command Line Tools

After installation, users can run the service using:

```bash
# Start the service
quantum-randomness-service

# Or use the short command
qrandom

# Or run directly with Python
python -m app.main
```

## 🌐 Service Features

- **True Quantum Randomness**: Direct from ANU QRNG
- **High-Performance API**: FastAPI backend with async support
- **Smart Caching**: Redis-based caching for performance
- **Real-time Streaming**: WebSocket support for live random numbers
- **Interactive Visualization**: Web interface for entropy analysis
- **Multiple Sources**: ANU QRNG + configurable fallback sources
- **Cryptographic Quality**: Suitable for security applications

## 📊 API Endpoints

- `GET /random` - Get a single random number
- `GET /random/batch?count=100` - Get multiple random numbers
- `GET /random/stream` - WebSocket stream of random numbers
- `GET /stats` - Service statistics and entropy metrics
- `GET /visualize` - Interactive entropy visualization
- `GET /docs` - Interactive API documentation

## 🧪 Testing


```bash
# Run tests
python -m pytest tests/

# Run package demo
python demo_package.py

# Test package installation
python test_package.py
```

## 🔍 ANU QRNG Integration

The service successfully integrates with ANU's Quantum Random Number Generator:

- ✅ **Working**: ANU QRNG API is functional
- ⚠️ **Rate Limited**: 1 request per minute (handled automatically)
- 🔄 **Intelligent Fallback**: Falls back to local QRNG when needed
- 💾 **Smart Caching**: Caches results to respect rate limits

## 🎯 Key Points

1. **✅ Package Structure**: Proper Python package with setup.py
2. **✅ Client Library**: Easy-to-use Python client
3. **✅ Command Line Tools**: Installable command-line interface
4. **✅ Documentation**: Comprehensive README 
5. **✅ Testing**: Test suite and package validation
6. **✅ Build System**: Automated build and distribution scripts
7. **✅ ANU Integration**: Working quantum randomness source
8. **✅ Fallback System**: Robust error handling and fallbacks

## 📖 Documentation

- **README.md**: Main documentation
- **examples/**: Usage examples
- **tests/**: Tests
- **demo_package.py**: Package demonstration
- **build_package.py**: Build automation


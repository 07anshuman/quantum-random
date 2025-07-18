# Quantum Randomness Service

A comprehensive service that provides true quantum random numbers from multiple sources including ANU's Quantum Random Number Generator (QRNG) and configurable custom sources.

## Features

- 🌊 **True Quantum Randomness** - Direct from quantum sources
- 🚀 **High-Performance API** - FastAPI backend with async support
- 📦 **Python Library** - Easy-to-use client library
- 💾 **Smart Caching** - Redis-based caching for performance
- 🔄 **Real-time Streaming** - WebSocket support for live random numbers
- 📊 **Entropy Visualization** - Interactive web interface
- 🔧 **Multiple Sources** - ANU QRNG + configurable sources
- 🛡️ **Cryptographic Quality** - Suitable for security applications

## Installation

### Option 1: Install as a Package (Recommended)

```bash
# Install the package
pip install quantum-randomness-service

# Or install with Redis support
pip install quantum-randomness-service[redis]

# Or install with development dependencies
pip install quantum-randomness-service[dev]
```

### Option 2: Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/quantum-randomness-service.git
cd quantum-randomness-service

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

## Quick Start

### Run the Service

```bash
# Method 1: Using the installed command
quantum-randomness-service

# Method 2: Using the short command
qrandom

# Method 3: Using Python directly
python -m app.main

# Method 4: Using uvicorn
uvicorn app.main:app --reload
```

### Use the Python Library

```python
from qrandom import QuantumRandom, get_random, get_random_batch

# Quick usage with convenience functions
random_number = get_random()
numbers = get_random_batch(10)

# Full client usage
qr = QuantumRandom()

# Synchronous methods
result = qr.get_random_sync()
print(f"Random number: {result['random_number']}")
print(f"Source: {result['source']}")

# Asynchronous methods
import asyncio
async def main():
    result = await qr.get_random()
    print(f"Random number: {result['random_number']}")

asyncio.run(main())

# Context manager usage
with QuantumRandom() as client:
    numbers = client.get_random_numbers(5)
    print(f"Numbers: {numbers}")
```

## API Endpoints

- `GET /random` - Get a single random number
- `GET /random/batch?count=100` - Get multiple random numbers
- `GET /random/stream` - WebSocket stream of random numbers
- `GET /stats` - Service statistics and entropy metrics
- `GET /visualize` - Interactive entropy visualization

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   ANU QRNG      │    │  Custom QRNG    │    │   Cache Layer   │
│   (Primary)     │    │   (Fallback)    │    │    (Redis)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   API Service   │
                    │   (FastAPI)     │
                    └─────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Python Client  │    │  Web Interface  │    │  WebSocket API  │
│   Library       │    │  (Visualization)│    │   (Streaming)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Use Cases

- **Cryptography**: Generate cryptographic keys and nonces
- **Simulations**: Monte Carlo methods, scientific simulations
- **Gaming**: Fair random number generation
- **Research**: Quantum computing and randomness studies
- **Security**: True randomness for security applications

## Configuration

Create a `.env` file:

```env
ANU_API_URL=https://qrng.anu.edu.au/API/jsonI.php
CACHE_TTL=300
REDIS_URL=redis://localhost:6379
CUSTOM_QRNG_URL=your-custom-qrng-url
```

## Examples

### Basic Usage

```python
from qrandom import get_random, get_random_batch

# Get a single random number
number = get_random()
print(f"Random number: {number}")

# Get multiple random numbers
numbers = get_random_batch(5)
print(f"Random numbers: {numbers}")
```

### Advanced Usage

```python
from qrandom import QuantumRandom
import asyncio

async def main():
    client = QuantumRandom()
    
    # Get random number with metadata
    result = await client.get_random()
    print(f"Number: {result['random_number']}")
    print(f"Source: {result['source']}")
    print(f"Entropy: {result['entropy_score']}")
    
    # Get service statistics
    stats = await client.get_stats()
    print(f"Total requests: {stats['total_requests']}")
    print(f"Cache hit rate: {stats['cache_hit_rate']}%")
    
    await client.close()

asyncio.run(main())
```

### Error Handling

```python
from qrandom import QuantumRandom

try:
    client = QuantumRandom("http://localhost:8000")
    result = client.get_random_sync()
    print(f"Success: {result}")
except Exception as e:
    print(f"Error: {e}")
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details. 

## How to Contribute and Release

### 1. Clone the Repository
```bash
git clone https://github.com/07anshuman/quantum-random.git
cd quantum-random
```

### 2. Create a Branch for Your Work
```bash
git checkout -b my-feature-branch
```

### 3. Make Changes and Commit
```bash
git add .
git commit -m "Describe your change"
```

### 4. Push and Create a Pull Request
```bash
git push origin my-feature-branch
```
- Go to GitHub and open a Pull Request from your branch.

### 5. Release to PyPI/TestPyPI

#### Build the package
```bash
python -m pip install --upgrade build twine
python -m build
```

#### Upload to TestPyPI (for testing)
```bash
twine upload --repository testpypi dist/*
```
- Use a TestPyPI API token from https://test.pypi.org/manage/account/#api-tokens

#### Upload to PyPI (for production)
```bash
twine upload dist/*
```
- Use a PyPI API token from https://pypi.org/manage/account/#api-tokens

#### Install from TestPyPI
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple quantum-randomness-service
```

#### Install from PyPI
```bash
pip install quantum-randomness-service
```

---

## Development Workflow

- Use a virtual environment: `python -m venv venv && source venv/bin/activate`
- Run tests and lint before pushing: `pytest` and `ruff .`
- Update the version in `setup.py` and `qrandom/__init__.py` before each release
- Never commit secrets or API tokens
- Keep the `README.md` and documentation up to date
- Use Pull Requests for all changes

---

For more details, see the comments in `setup.py` and the package source files. 
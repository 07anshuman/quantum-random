"""
Quantum Randomness Service Python Client

A simple client library for accessing quantum random numbers.
"""

__version__ = "1.0.0"
__author__ = "Quantum Randomness Service"
__email__ = "contact@example.com"

from .client import QuantumRandom, get_random, get_random_batch, get_service_stats

__all__ = ["QuantumRandom", "get_random", "get_random_batch", "get_service_stats", "__version__", "__author__", "__email__"] 
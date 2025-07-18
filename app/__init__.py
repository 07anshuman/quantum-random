"""
Quantum Randomness Service

A service providing true quantum random numbers from ANU QRNG and other sources.
"""

__version__ = "1.0.0"
__author__ = "Quantum Randomness Service"
__email__ = "contact@example.com"

from .main import app
from .qrng import qrng_manager
from .cache import cache_manager
from .entropy import entropy_analyzer

__all__ = [
    "app",
    "qrng_manager", 
    "cache_manager",
    "entropy_analyzer",
    "__version__",
    "__author__",
    "__email__",
] 
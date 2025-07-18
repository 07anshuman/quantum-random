#!/usr/bin/env python3
"""
Startup script for the Quantum Randomness Service.
"""

import uvicorn
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from app.main import app


def main():
    """Start the Quantum Randomness Service."""
    print("🌊 Starting Quantum Randomness Service...")
    print("=" * 50)
    print("Service will be available at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("Visualization: http://localhost:8000/visualize")
    print("=" * 50)
    
    # Run the FastAPI application
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main() 
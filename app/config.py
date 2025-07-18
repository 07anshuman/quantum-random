"""
Configuration settings for the Quantum Randomness Service.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # ANU QRNG API settings
    anu_api_url: str = "https://qrng.anu.edu.au/API/jsonI.php"
    anu_api_timeout: int = 10
    
    # Custom QRNG settings
    custom_qrng_url: Optional[str] = None
    custom_qrng_timeout: int = 10
    
    # Cache settings
    cache_ttl: int = 300  # 5 minutes
    redis_url: str = "redis://localhost:6379"
    
    # API settings
    api_title: str = "Quantum Randomness Service"
    api_description: str = "A service providing true quantum random numbers"
    api_version: str = "1.0.0"
    
    # Rate limiting
    rate_limit_per_minute: int = 1000
    
    # Entropy settings
    entropy_buffer_size: int = 1000
    entropy_check_interval: int = 60  # seconds
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings() 
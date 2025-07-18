"""
Pydantic models for request and response validation.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field  # type: ignore


class RandomNumberResponse(BaseModel):
    """Response model for a single random number."""
    random_number: int = Field(..., description="The quantum random number")
    source: str = Field(..., description="Source of the random number")
    timestamp: str = Field(..., description="ISO timestamp of generation")
    entropy_score: Optional[float] = Field(None, description="Entropy quality score")


class BatchRandomResponse(BaseModel):
    """Response model for multiple random numbers."""
    random_numbers: List[int] = Field(..., description="List of quantum random numbers")
    count: int = Field(..., description="Number of random numbers requested")
    source: str = Field(..., description="Source of the random numbers")
    timestamp: str = Field(..., description="ISO timestamp of generation")
    entropy_score: Optional[float] = Field(None, description="Average entropy quality score")


class ServiceStats(BaseModel):
    """Service statistics and metrics."""
    total_requests: int = Field(..., description="Total number of requests served")
    cache_hit_rate: float = Field(..., description="Cache hit rate percentage")
    average_response_time: float = Field(..., description="Average response time in milliseconds")
    entropy_quality: float = Field(..., description="Current entropy quality score")
    uptime_seconds: int = Field(..., description="Service uptime in seconds")
    active_connections: int = Field(..., description="Number of active WebSocket connections")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    error_code: str = Field(..., description="Error code")
    timestamp: str = Field(..., description="ISO timestamp of error")


class StreamMessage(BaseModel):
    """WebSocket stream message model."""
    random_number: int = Field(..., description="Quantum random number")
    sequence_number: int = Field(..., description="Sequence number in the stream")
    timestamp: str = Field(..., description="ISO timestamp")
    entropy_score: Optional[float] = Field(None, description="Entropy quality score") 
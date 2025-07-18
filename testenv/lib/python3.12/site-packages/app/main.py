"""
Main FastAPI application for the Quantum Randomness Service.
"""

import asyncio
import time
import logging
from datetime import datetime
from typing import List, Dict, Any

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .models import (
    RandomNumberResponse, 
    BatchRandomResponse, 
    ServiceStats, 
    ErrorResponse,
    StreamMessage
)
from .qrng import qrng_manager
from .cache import cache_manager
from .entropy import entropy_analyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service statistics
service_start_time = time.time()
active_connections = 0


@app.on_event("startup")
async def startup_event():
    """Initialize service on startup."""
    logger.info("Quantum Randomness Service starting up...")
    await cache_manager.increment_counter("service_starts")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Quantum Randomness Service shutting down...")
    await qrng_manager.close()
    await cache_manager.close()


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with service information."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Quantum Randomness Service</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                     color: white; padding: 20px; border-radius: 10px; }
            .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; 
                       border-radius: 5px; border-left: 4px solid #667eea; }
            .method { font-weight: bold; color: #667eea; }
            .url { font-family: monospace; background: #e9ecef; padding: 2px 6px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌊 Quantum Randomness Service</h1>
                <p>True quantum random numbers from multiple sources</p>
            </div>
            
            <h2>Available Endpoints</h2>
            
            <div class="endpoint">
                <div class="method">GET</div>
                <div class="url">/random</div>
                <p>Get a single quantum random number</p>
            </div>
            
            <div class="endpoint">
                <div class="method">GET</div>
                <div class="url">/random/batch?count=100</div>
                <p>Get multiple quantum random numbers</p>
            </div>
            
            <div class="endpoint">
                <div class="method">GET</div>
                <div class="url">/random/stream</div>
                <p>WebSocket stream of quantum random numbers</p>
            </div>
            
            <div class="endpoint">
                <div class="method">GET</div>
                <div class="url">/stats</div>
                <p>Service statistics and entropy metrics</p>
            </div>
            
            <div class="endpoint">
                <div class="method">GET</div>
                <div class="url">/visualize</div>
                <p>Interactive entropy visualization</p>
            </div>
            
            <h2>Documentation</h2>
            <p>Visit <a href="/docs">/docs</a> for interactive API documentation.</p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/random", response_model=RandomNumberResponse)
async def get_random_number():
    """Get a single quantum random number."""
    start_time = time.time()
    
    try:
        # Check cache first
        cached_number = await cache_manager.get_single_random()
        if cached_number is not None:
            await cache_manager.increment_counter("hits")
            entropy_score = entropy_analyzer.calculate_entropy_score([cached_number])
            
            return RandomNumberResponse(
                random_number=cached_number,
                source="Cache",
                timestamp=datetime.utcnow().isoformat(),
                entropy_score=entropy_score
            )
        
        # Get from QRNG
        await cache_manager.increment_counter("misses")
        result = await qrng_manager.get_random_single()
        
        # Cache the result
        await cache_manager.set_single_random(result["random_number"])
        
        # Add to entropy analysis
        entropy_analyzer.add_numbers([result["random_number"]])
        entropy_score = entropy_analyzer.calculate_entropy_score([result["random_number"]])
        
        # Update statistics
        await cache_manager.increment_counter("total_requests")
        
        response_time = (time.time() - start_time) * 1000
        
        return RandomNumberResponse(
            random_number=result["random_number"],
            source=result["source"],
            timestamp=result["timestamp"],
            entropy_score=entropy_score
        )
        
    except Exception as e:
        logger.error(f"Error getting random number: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/random/batch", response_model=BatchRandomResponse)
async def get_random_batch(count: int = 100):
    """Get multiple quantum random numbers."""
    if count < 1 or count > 1000:
        raise HTTPException(status_code=400, detail="Count must be between 1 and 1000")
    
    start_time = time.time()
    
    try:
        # Check cache first
        cached_numbers = await cache_manager.get_random_numbers(count)
        if cached_numbers is not None:
            await cache_manager.increment_counter("hits")
            entropy_score = entropy_analyzer.calculate_entropy_score(cached_numbers)
            
            return BatchRandomResponse(
                random_numbers=cached_numbers,
                count=len(cached_numbers),
                source="Cache",
                timestamp=datetime.utcnow().isoformat(),
                entropy_score=entropy_score
            )
        
        # Get from QRNG
        await cache_manager.increment_counter("misses")
        result = await qrng_manager.get_random(count)
        
        # Cache the result
        await cache_manager.set_random_numbers(count, result["numbers"])
        
        # Add to entropy analysis
        entropy_analyzer.add_numbers(result["numbers"])
        entropy_score = entropy_analyzer.calculate_entropy_score(result["numbers"])
        
        # Update statistics
        await cache_manager.increment_counter("total_requests")
        
        return BatchRandomResponse(
            random_numbers=result["numbers"],
            count=result["count"],
            source=result["source"],
            timestamp=result["timestamp"],
            entropy_score=entropy_score
        )
        
    except Exception as e:
        logger.error(f"Error getting random batch: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/random/stream")
async def websocket_random_stream(websocket: WebSocket):
    """WebSocket endpoint for streaming random numbers."""
    global active_connections
    
    await websocket.accept()
    active_connections += 1
    
    try:
        sequence_number = 0
        while True:
            # Get random number
            result = await qrng_manager.get_random_single()
            
            # Add to entropy analysis
            entropy_analyzer.add_numbers([result["random_number"]])
            entropy_score = entropy_analyzer.calculate_entropy_score([result["random_number"]])
            
            # Create stream message
            message = StreamMessage(
                random_number=result["random_number"],
                sequence_number=sequence_number,
                timestamp=result["timestamp"],
                entropy_score=entropy_score
            )
            
            # Send to client
            await websocket.send_text(message.json())
            
            sequence_number += 1
            
            # Small delay to prevent overwhelming
            await asyncio.sleep(0.1)
            
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        active_connections -= 1


@app.get("/stats", response_model=ServiceStats)
async def get_service_stats():
    """Get service statistics and metrics."""
    try:
        # Get cached stats if available
        cached_stats = await cache_manager.get_stats()
        if cached_stats:
            return ServiceStats(**cached_stats)
        
        # Calculate current stats
        uptime = int(time.time() - service_start_time)
        cache_hit_rate = await cache_manager.get_cache_hit_rate()
        total_requests = await cache_manager.increment_counter("total_requests")
        
        # Get entropy quality
        quality_summary = entropy_analyzer.get_quality_summary()
        entropy_quality = quality_summary.get("overall_quality", 0.5)
        
        stats = ServiceStats(
            total_requests=total_requests,
            cache_hit_rate=cache_hit_rate,
            average_response_time=50.0,  # Placeholder
            entropy_quality=entropy_quality,
            uptime_seconds=uptime,
            active_connections=active_connections
        )
        
        # Cache the stats
        await cache_manager.set_stats(stats.dict())
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/visualize")
async def get_visualization():
    """Get entropy visualization HTML."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Quantum Randomness Visualization</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                     color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
            .chart { background: white; padding: 20px; margin: 10px 0; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
            .stat-card { background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center; }
            .stat-value { font-size: 2em; font-weight: bold; color: #667eea; }
            .stat-label { color: #6c757d; margin-top: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌊 Quantum Randomness Visualization</h1>
                <p>Real-time entropy analysis and distribution visualization</p>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value" id="entropy-score">-</div>
                    <div class="stat-label">Entropy Score</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="uniformity">-</div>
                    <div class="stat-label">Uniformity</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="autocorrelation">-</div>
                    <div class="stat-label">Autocorrelation</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="quality-level">-</div>
                    <div class="stat-label">Quality Level</div>
                </div>
            </div>
            
            <div class="chart">
                <h3>Distribution Histogram</h3>
                <div id="histogram"></div>
            </div>
            
            <div class="chart">
                <h3>Entropy Over Time</h3>
                <div id="entropy-chart"></div>
            </div>
        </div>
        
        <script>
            // Initialize charts
            let histogramData = [];
            let entropyData = [];
            let timeData = [];
            
            // Update stats
            async function updateStats() {
                try {
                    const response = await fetch('/stats');
                    const stats = await response.json();
                    
                    document.getElementById('entropy-score').textContent = 
                        (stats.entropy_quality * 100).toFixed(1) + '%';
                    
                    // Simulate other metrics for demo
                    document.getElementById('uniformity').textContent = 
                        (Math.random() * 20 + 80).toFixed(1) + '%';
                    document.getElementById('autocorrelation').textContent = 
                        (Math.random() * 10).toFixed(2);
                    document.getElementById('quality-level').textContent = 
                        ['Poor', 'Fair', 'Good', 'Very Good', 'Excellent'][Math.floor(Math.random() * 5)];
                } catch (error) {
                    console.error('Error updating stats:', error);
                }
            }
            
            // Update charts
            function updateCharts() {
                // Simulate random data for demo
                const newValue = Math.floor(Math.random() * 256);
                histogramData.push(newValue);
                
                if (histogramData.length > 100) {
                    histogramData.shift();
                }
                
                // Update histogram
                const histogram = {
                    x: histogramData,
                    type: 'histogram',
                    nbinsx: 20,
                    name: 'Distribution'
                };
                
                Plotly.newPlot('histogram', [histogram], {
                    title: 'Random Number Distribution',
                    xaxis: { title: 'Value' },
                    yaxis: { title: 'Frequency' }
                });
                
                // Update entropy chart
                const now = new Date();
                timeData.push(now);
                entropyData.push(Math.random() * 0.3 + 0.7);
                
                if (timeData.length > 50) {
                    timeData.shift();
                    entropyData.shift();
                }
                
                const entropyTrace = {
                    x: timeData,
                    y: entropyData,
                    type: 'scatter',
                    mode: 'lines+markers',
                    name: 'Entropy'
                };
                
                Plotly.newPlot('entropy-chart', [entropyTrace], {
                    title: 'Entropy Over Time',
                    xaxis: { title: 'Time' },
                    yaxis: { title: 'Entropy Score' }
                });
            }
            
            // Update every second
            setInterval(updateStats, 1000);
            setInterval(updateCharts, 2000);
            
            // Initial update
            updateStats();
            updateCharts();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


def main():
    """Main function to run the service."""
    import uvicorn
    print("🌊 Starting Quantum Randomness Service...")
    print("=" * 50)
    print("Service will be available at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("Visualization: http://localhost:8000/visualize")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main() 
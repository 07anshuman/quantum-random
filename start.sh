#!/bin/bash

# Quantum Randomness Service Startup Script

echo "🌊 Quantum Randomness Service"
echo "================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   python3 setup.py"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "❌ Requirements not installed. Installing now..."
    pip install -r requirements.txt
fi

echo "✅ Environment ready!"
echo ""
echo "🚀 Starting Quantum Randomness Service..."
echo "   Service will be available at: http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo "   Visualization: http://localhost:8000/visualize"
echo ""
echo "Press Ctrl+C to stop the service"
echo ""

# Start the service
python run.py 
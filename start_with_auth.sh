#!/bin/bash
# Start ComfyUI with API Authentication

set -e

echo "🚀 Starting ComfyUI with API Authentication..."
echo ""

# Navigate to ComfyUI directory
cd "$(dirname "$0")"

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Make sure you're in the ComfyUI directory."
    exit 1
fi

# Check if port is already in use
if lsof -ti :8188 > /dev/null 2>&1; then
    echo "⚠️  Port 8188 is already in use."
    echo "   Stopping existing processes..."
    lsof -ti :8188 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# Set default port
PORT=${COMFYUI_PORT:-8188}

echo "📡 Starting ComfyUI on port $PORT with API authentication..."
echo ""
echo "✅ API Authentication: ENABLED (optional)"
echo "   - API keys are tracked but not required"
echo "   - Use --require-api-auth to make auth mandatory"
echo ""
echo "🌐 Access the UI at: http://localhost:$PORT"
echo "📚 API Documentation: http://localhost:$PORT/docs"
echo ""
echo "To create an API key:"
echo "  curl -X POST http://localhost:$PORT/api/keys \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"name\": \"My Key\", \"rate_limit\": 100}'"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start ComfyUI with authentication
python3 main.py --enable-api-auth --listen 0.0.0.0 --port "$PORT"


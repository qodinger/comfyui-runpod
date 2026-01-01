#!/bin/bash
# Stop ComfyUI Server Script

echo "🛑 Stopping ComfyUI server..."

# Find process on port 8188
PID=$(lsof -ti :8188)

if [ -z "$PID" ]; then
    echo "❌ No process found on port 8188"
    echo "   ComfyUI server is not running"
    exit 0
fi

echo "📋 Found process: PID $PID"

# Try graceful shutdown first (SIGTERM)
echo "⏳ Sending graceful shutdown signal..."
kill -TERM $PID 2>/dev/null

# Wait a bit for graceful shutdown
sleep 3

# Check if still running
if kill -0 $PID 2>/dev/null; then
    echo "⚠️  Process still running, forcing shutdown..."
    kill -9 $PID 2>/dev/null
    sleep 1
fi

# Verify it's stopped
if ! kill -0 $PID 2>/dev/null; then
    echo "✅ ComfyUI server stopped successfully"
else
    echo "❌ Failed to stop server (PID: $PID)"
    exit 1
fi

# Verify port is free
if lsof -ti :8188 > /dev/null 2>&1; then
    echo "⚠️  Warning: Port 8188 is still in use"
else
    echo "✅ Port 8188 is now free"
fi


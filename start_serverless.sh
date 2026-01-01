#!/bin/bash
# Startup script for RunPod serverless
# Starts ComfyUI in background, then runs the handler

set -e

echo "🚀 Starting ComfyUI Serverless Worker..."

# Start ComfyUI in background
echo "📡 Starting ComfyUI server..."
python main.py --listen 0.0.0.0 --port 8188 --enable-api-auth &
COMFYUI_PID=$!

# Wait for ComfyUI to be ready
echo "⏳ Waiting for ComfyUI to start..."
for i in {1..30}; do
  if curl -f http://localhost:8188/system_stats > /dev/null 2>&1; then
    echo "✅ ComfyUI is ready!"
    break
  fi
  if [ $i -eq 30 ]; then
    echo "❌ ComfyUI failed to start"
    exit 1
  fi
  sleep 2
done

# Start RunPod serverless handler
echo "🔧 Starting RunPod serverless handler..."
exec python -m runpod.serverless --handler handler.handler


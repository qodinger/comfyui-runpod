#!/bin/bash
# Startup script for RunPod serverless
# Starts ComfyUI in background, then runs the handler

set -e

echo "🚀 Starting ComfyUI Serverless Worker..."

# Check if we have a GPU available
if command -v nvidia-smi &> /dev/null && nvidia-smi &> /dev/null; then
    echo "✅ GPU detected, starting ComfyUI..."

    # Start ComfyUI in background
    echo "📡 Starting ComfyUI server..."
    python main.py --listen 0.0.0.0 --port 8188 &
    COMFYUI_PID=$!

    # Wait for ComfyUI to be ready
    echo "⏳ Waiting for ComfyUI to start..."
    for i in {1..60}; do
      if curl -f http://127.0.0.1:8188/ > /dev/null 2>&1; then
        echo "✅ ComfyUI is ready!"
        break
      fi
      if [ $i -eq 60 ]; then
        echo "⚠️ ComfyUI startup timeout, continuing anyway..."
      fi
      sleep 2
    done
else
    echo "⚠️ No GPU detected (CPU-only mode)"
    echo "   ComfyUI requires GPU - handler will fail without GPU"
fi

# Start RunPod serverless handler
echo "🔧 Starting RunPod serverless handler..."
exec python handler.py

#!/bin/bash
# ComfyUI Startup Script for RunPod
# This script starts ComfyUI with the correct settings for RunPod deployment

set -e

echo "🚀 Starting ComfyUI for RunPod..."

# Navigate to ComfyUI directory
cd "$(dirname "$0")"

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Make sure you're in the ComfyUI directory."
    exit 1
fi

# Set default port (RunPod typically uses 8000 or 7860)
PORT=${COMFYUI_PORT:-8000}

# Start ComfyUI
# --listen 0.0.0.0 allows external connections (required for RunPod)
# --port sets the port number
echo "📡 Starting ComfyUI on port $PORT..."
python3 main.py --listen 0.0.0.0 --port "$PORT"


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

# If HF_MODEL_ID is provided, attempt to download the model into the mounted models path
if [ -n "$HF_MODEL_ID" ]; then
    echo "📥 HF_MODEL_ID detected: $HF_MODEL_ID — attempting download into /app/models/checkpoints"
    # Ensure destination exists (mounted volume should be /app/models)
    mkdir -p /app/models/checkpoints

    # Ensure huggingface-hub is available (install if missing)
    python3 - <<'PY'
import pkgutil, subprocess, sys
if not pkgutil.find_loader('huggingface_hub'):
        print('Installing huggingface-hub...')
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'huggingface-hub'])
else:
        print('huggingface-hub already installed')
PY

    # Run the downloader script. If it fails we log and continue so ComfyUI still starts.
    if [ -n "$HF_MODEL_FILE" ]; then
        python3 scripts/download_hf_model.py --model-id="$HF_MODEL_ID" --filename="$HF_MODEL_FILE" --dest=/app/models/checkpoints || echo "⚠️ Model download failed (continuing startup)"
    else
        python3 scripts/download_hf_model.py --model-id="$HF_MODEL_ID" --dest=/app/models/checkpoints || echo "⚠️ Model download failed (continuing startup)"
    fi
fi

# Start ComfyUI
# --listen 0.0.0.0 allows external connections (required for RunPod)
# --port sets the port number
echo "📡 Starting ComfyUI on port $PORT..."
python3 main.py --listen 0.0.0.0 --port "$PORT"


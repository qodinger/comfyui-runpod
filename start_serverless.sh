#!/bin/bash
# Startup script for RunPod serverless
# Starts ComfyUI in background, then runs the handler

# Don't exit on error during model download (we handle it gracefully)
# set -e is enabled after model section

echo "🚀 Starting ComfyUI Serverless Worker..."

# =============================================================================
# MODEL DOWNLOAD SECTION
# Downloads model from HuggingFace if not already present
# =============================================================================

# Model configuration
# Note: Script runs from /app (WORKDIR in Dockerfile), so paths are relative to /app
MODEL_DIR="models/checkpoints"
MODEL_NAME="AnythingXL_xl.safetensors"
HF_REPO="tyecode/AnythingXL"
HF_FILE="AnythingXL_xl.safetensors"

# Check if model already exists (e.g., from network volume or previous run)
if [ ! -f "$MODEL_DIR/$MODEL_NAME" ]; then
    echo "📦 Model not found locally, downloading from HuggingFace..."
    
    # Ensure model directory exists
    mkdir -p "$MODEL_DIR"
    
    # Download from HuggingFace
    # Note: HF_TOKEN environment variable is required for gated models
    if [ -n "$HF_TOKEN" ]; then
        echo "⬇️ Downloading $MODEL_NAME from huggingface.co/$HF_REPO..."
        echo "   This may take several minutes for large models..."
        wget --header="Authorization: Bearer $HF_TOKEN" \
             --progress=bar:force \
             -O "$MODEL_DIR/$MODEL_NAME" \
             "https://huggingface.co/$HF_REPO/resolve/main/$HF_FILE"
    else
        # Try without token (for public models)
        echo "⚠️ No HF_TOKEN set! Your model requires authentication."
        echo "   Get your token at: https://huggingface.co/settings/tokens"
        echo "   Set it as HF_TOKEN environment variable in RunPod."
        echo ""
        echo "⬇️ Attempting download anyway (will fail for gated models)..."
        wget --progress=bar:force \
             -O "$MODEL_DIR/$MODEL_NAME" \
             "https://huggingface.co/$HF_REPO/resolve/main/$HF_FILE" || {
            echo "❌ Download failed. HF_TOKEN is required for gated models."
        }
    fi
    
    # Verify download succeeded
    if [ -f "$MODEL_DIR/$MODEL_NAME" ] && [ -s "$MODEL_DIR/$MODEL_NAME" ]; then
        echo "✅ Model downloaded successfully: $MODEL_NAME"
    else
        echo "❌ Model download failed or file is empty."
        rm -f "$MODEL_DIR/$MODEL_NAME"  # Clean up empty file
        
        # Fallback: Check network volume
        if [ -f "/runpod-volume/models/checkpoints/$MODEL_NAME" ]; then
            echo "📂 Found model in network volume, copying..."
            cp "/runpod-volume/models/checkpoints/$MODEL_NAME" "$MODEL_DIR/$MODEL_NAME"
        fi
    fi
else
    echo "✅ Model already exists: $MODEL_NAME"
fi

# =============================================================================

# Enable strict error handling from here
set -e

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

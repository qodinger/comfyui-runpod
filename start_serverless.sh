#!/bin/bash
# Startup script for RunPod serverless
# Starts ComfyUI in background, then runs the handler

# Don't exit on error during model download (we handle it gracefully)
# set -e is enabled after model section

echo "🚀 Starting ComfyUI Serverless Worker..."

# =============================================================================
# MODEL DOWNLOAD SECTION
# Downloads model from HuggingFace into a persistent volume if available
# =============================================================================

# Allow configuration via environment variables (preferred)
# - HF_MODEL_ID: owner/repo (e.g. 'tyecode/AnythingXL')
# - HF_MODEL_FILE: filename inside repo (e.g. 'AnythingXL_xl.safetensors')
# - HF_TOKEN: Hugging Face token (for gated models)

# Backwards-compat: keep old HF_REPO / HF_FILE / MODEL_NAME if present
if [ -n "$HF_MODEL_ID" ]; then
  HF_REPO="$HF_MODEL_ID"
fi
if [ -z "$HF_REPO" ]; then
  HF_REPO="tyecode/AnythingXL"
fi
if [ -n "$HF_MODEL_FILE" ]; then
  HF_FILE="$HF_MODEL_FILE"
fi
if [ -z "$HF_FILE" ]; then
  HF_FILE="AnythingXL_xl.safetensors"
fi
MODEL_NAME="${HF_FILE##*/}"

# Prefer persistent locations (RunPod exposes network volume at /runpod-volume in some setups)
if [ -d "/runpod-volume" ]; then
  PERSIST_PREFIX="/runpod-volume"
elif [ -d "/workspace" ]; then
  PERSIST_PREFIX="/workspace"
else
  PERSIST_PREFIX="/app"
fi
DEST_DIR="$PERSIST_PREFIX/models/checkpoints"
APP_MODELS_PATH="/app/models"

# Create persistent model directory
mkdir -p "$DEST_DIR"

# If /app/models doesn't exist, create a symlink to persistent location so ComfyUI sees models/...
if [ ! -L "$APP_MODELS_PATH" ]; then
  if [ -e "$APP_MODELS_PATH" ]; then
    echo "⚠️ /app/models exists and is not a symlink. Leaving as-is."
  else
    ln -s "$PERSIST_PREFIX/models" "$APP_MODELS_PATH" || true
    echo "🔗 Linked $APP_MODELS_PATH -> $PERSIST_PREFIX/models"
  fi
fi

# If we have a persistent prefix, ensure RunPod state files are stored there
# RunPod handler writes `.runpod_jobs.pkl` and a `.lock` in the app root; when /app
# is ephemeral this causes "No space left on device". Link them to persistent volume
if [ "$PERSIST_PREFIX" != "/app" ] && [ -d "$PERSIST_PREFIX" ]; then
  # create persistent placeholders
  touch "$PERSIST_PREFIX/.runpod_jobs.pkl" || true
  touch "$PERSIST_PREFIX/.runpod_jobs.pkl.lock" || true

  # symlink the main state file
  if [ -e "/app/.runpod_jobs.pkl" ] && [ ! -L "/app/.runpod_jobs.pkl" ]; then
    echo "⚠️ /app/.runpod_jobs.pkl exists and is not a symlink. Leaving as-is."
  else
    ln -sf "$PERSIST_PREFIX/.runpod_jobs.pkl" /app/.runpod_jobs.pkl || true
    echo "🔗 Linked /app/.runpod_jobs.pkl -> $PERSIST_PREFIX/.runpod_jobs.pkl"
  fi

  # symlink the lock file too
  if [ -e "/app/.runpod_jobs.pkl.lock" ] && [ ! -L "/app/.runpod_jobs.pkl.lock" ]; then
    echo "⚠️ /app/.runpod_jobs.pkl.lock exists and is not a symlink. Leaving as-is."
  else
    ln -sf "$PERSIST_PREFIX/.runpod_jobs.pkl.lock" /app/.runpod_jobs.pkl.lock || true
    echo "🔗 Linked /app/.runpod_jobs.pkl.lock -> $PERSIST_PREFIX/.runpod_jobs.pkl.lock"
  fi
fi

# Helper: check free space (in KB) for DEST_DIR filesystem
avail_kb=$(df -k --output=avail "$DEST_DIR" | tail -1 | tr -d '[:space:]') || avail_kb=0
# Require at least 5 GB free for large models (approx). Adjust if you know smaller/larger.
min_kb=$((5 * 1024 * 1024))
if [ "$avail_kb" -lt "$min_kb" ]; then
  echo "⚠️ Low disk space at $DEST_DIR (available: ${avail_kb} KB)."
  echo "   Recommend mounting a larger persistent volume to /runpod-volume or /workspace/models."
fi

# Compose final path we'll write to
FINAL_PATH="$DEST_DIR/$MODEL_NAME"

# If model is already available in persistent location, skip download
if [ -f "$FINAL_PATH" ] && [ -s "$FINAL_PATH" ]; then
  echo "✅ Model already present in persistent storage: $FINAL_PATH"
else
  echo "📦 Model not found in persistent storage. Preparing to download to $FINAL_PATH"

  # If very low disk space, warn and skip download to avoid filling container
  if [ "$avail_kb" -lt "$min_kb" ]; then
    echo "❌ Insufficient disk space to download model. Aborting download."
  else
    # Download using HF_TOKEN if present; prefer huggingface-hub but wget is fine here
    if [ -n "$HF_TOKEN" ]; then
      echo "⬇️ Downloading $MODEL_NAME from huggingface.co/$HF_REPO (auth provided)..."
      wget --header="Authorization: Bearer $HF_TOKEN" --progress=bar:force -O "$FINAL_PATH" "https://huggingface.co/$HF_REPO/resolve/main/$HF_FILE" || {
        echo "❌ Download failed (wget returned non-zero)."
        rm -f "$FINAL_PATH" || true
      }
    else
      echo "⬇️ Downloading $MODEL_NAME from huggingface.co/$HF_REPO (no token)..."
      wget --progress=bar:force -O "$FINAL_PATH" "https://huggingface.co/$HF_REPO/resolve/main/$HF_FILE" || {
        echo "❌ Download failed (no token or network error)."
        rm -f "$FINAL_PATH" || true
      }
    fi

    # Verify
    if [ -f "$FINAL_PATH" ] && [ -s "$FINAL_PATH" ]; then
      echo "✅ Model downloaded successfully: $FINAL_PATH"
    else
      echo "❌ Model not present after download. Checking for fallback copies..."
      # Fallback: maybe another process populated /runpod-volume/models
      if [ -f "/runpod-volume/models/checkpoints/$MODEL_NAME" ]; then
        echo "📂 Found model in /runpod-volume, copying to $FINAL_PATH"
        cp "/runpod-volume/models/checkpoints/$MODEL_NAME" "$FINAL_PATH" || true
      fi
    fi
  fi
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

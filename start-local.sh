#!/bin/bash
# Start ComfyUI locally for testing

cd "$(dirname "$0")"

echo "🚀 Starting ComfyUI locally..."
echo "📍 Location: $(pwd)"
echo "🌐 Will be available at: http://127.0.0.1:8188"
echo ""

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Make sure you're in the ComfyUI directory."
    exit 1
fi

# Check if models exist
if [ ! -d "models/checkpoints" ] || [ -z "$(ls -A models/checkpoints/*.safetensors 2>/dev/null)" ]; then
    echo "⚠️  Warning: No models found in models/checkpoints/"
    echo "   ComfyUI will start but you won't be able to generate images."
    echo "   Download a model or copy from ~/Documents/ComfyUI/models/checkpoints/"
    echo ""
fi

# Start ComfyUI
echo "▶️  Starting ComfyUI..."
python3 main.py


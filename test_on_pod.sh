#!/bin/bash
# ===========================================
# ComfyUI RunPod Handler Test Script
# Run this on your RunPod Pod to test locally
# ===========================================

set -e

echo "🧪 ComfyUI RunPod Handler Test Script"
echo "======================================"
echo ""

# Navigate to workspace
cd /workspace

# Check if repo exists, if not clone it
if [ ! -d "comfyui-runpod" ]; then
    echo "📥 Cloning repository..."
    git clone https://github.com/qodinger/comfyui-runpod.git
else
    echo "📂 Repository exists, pulling latest..."
    cd comfyui-runpod
    git pull
    cd ..
fi

cd comfyui-runpod

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -q runpod requests

# Test 1: Basic import test
echo ""
echo "🔍 Test 1: Import Test"
echo "----------------------"
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from handler import handler, build_workflow
    print('✅ Handler imports successfully')
except Exception as e:
    print(f'❌ Import failed: {e}')
"

# Test 2: Health check (without ComfyUI)
echo ""
echo "🔍 Test 2: Health Check (handler only)"
echo "--------------------------------------"
python3 -c "
import sys
sys.path.insert(0, '.')
from handler import handler

# Test health action
result = handler({'input': {'action': 'health'}})
print(f'Result: {result}')
if 'error' not in str(result).lower() or 'status' in str(result):
    print('✅ Health check handler works')
else:
    print('⚠️  Health check returned unexpected result')
"

# Check if ComfyUI is running
echo ""
echo "🔍 Test 3: Check ComfyUI Status"
echo "-------------------------------"
if curl -s -f http://localhost:8188/system_stats > /dev/null 2>&1; then
    echo "✅ ComfyUI is running on port 8188"
    COMFYUI_RUNNING=true
else
    echo "⚠️  ComfyUI is not running on port 8188"
    COMFYUI_RUNNING=false
fi

# If ComfyUI is running, test full health check
if [ "$COMFYUI_RUNNING" = true ]; then
    echo ""
    echo "🔍 Test 4: Full Health Check (with ComfyUI)"
    echo "-------------------------------------------"
    python3 -c "
import sys
sys.path.insert(0, '.')
from handler import handler

result = handler({'input': {'action': 'health'}})
print(f'Result: {result}')
if 'comfyui_status' in str(result):
    print('✅ Full health check works!')
"

    # Check for models
    echo ""
    echo "🔍 Test 5: Check Models"
    echo "-----------------------"
    if ls models/checkpoints/*.safetensors 2>/dev/null | head -1 > /dev/null; then
        MODEL=$(ls models/checkpoints/*.safetensors 2>/dev/null | head -1 | xargs basename)
        echo "✅ Found model: $MODEL"
        echo ""
        echo "🎨 You can test image generation with:"
        echo "   python3 handler.py --test_input '{\"input\": {\"prompt\": \"a cat\", \"checkpoint\": \"$MODEL\"}}'"
    else
        echo "⚠️  No models found in models/checkpoints/"
        echo "   Image generation won't work without a model."
        echo "   Download a model or check /workspace for existing models."
    fi
else
    echo ""
    echo "💡 To start ComfyUI and run full tests:"
    echo "   python main.py --listen 0.0.0.0 --port 8188 &"
    echo "   sleep 30"
    echo "   ./test_on_pod.sh"
fi

echo ""
echo "======================================"
echo "🏁 Tests Complete!"
echo ""
echo "📋 Quick Commands:"
echo "   - Start ComfyUI: python main.py --listen 0.0.0.0 --port 8188 &"
echo "   - Test handler:  python handler.py --test_input '{\"input\": {\"action\": \"health\"}}'"
echo "   - Local API:     python handler.py --rp_serve_api"
echo ""


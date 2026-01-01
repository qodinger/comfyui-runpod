# ComfyUI Local Setup Guide

This guide will help you run ComfyUI locally for testing before deploying to RunPod.

## 📋 Prerequisites

- Python 3.10 or 3.11 ✅ (You have Python 3.11.5)
- 8GB+ RAM (16GB+ recommended)
- GPU (optional, but recommended for faster generation)

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
cd /Users/tyecode/dev/projects/discord-bots/comfyui-runpod

# Option A: Install globally (simpler for testing)
pip3 install -r requirements.txt

# Option B: Use virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Note:** Installing dependencies may take 10-20 minutes, especially PyTorch.

### Step 2: Download Models (Optional but Recommended)

You need at least one checkpoint model to generate images. Download to `models/checkpoints/`:

```bash
# Create models directory
mkdir -p models/checkpoints

# Download AnythingXL_xl (recommended for anime/NSFW)
# Option 1: Direct download
cd models/checkpoints
curl -L -o AnythingXL_xl.safetensors "https://huggingface.co/andite/anything-xl/resolve/main/AnythingXL_xl.safetensors"

# Option 2: Use your existing model
# If you already have models in ~/Documents/ComfyUI/models/checkpoints/
# You can copy them:
# cp ~/Documents/ComfyUI/models/checkpoints/*.safetensors models/checkpoints/
```

**Popular Models:**
- **AnythingXL_xl.safetensors** - Best for anime/NSFW (XL model)
- **anything-v5-pruned.safetensors** - Good balance (smaller file)
- See `../role-reactor-bot/docs/COMFYUI_NSFW_GAME_MODELS.md` for more

### Step 3: Start ComfyUI

```bash
cd /Users/tyecode/dev/projects/discord-bots/comfyui-runpod

# If using virtual environment:
source .venv/bin/activate

# Start ComfyUI
python3 main.py
```

ComfyUI will start on `http://127.0.0.1:8188`

### Step 4: Verify It's Running

1. **Open in browser:** `http://127.0.0.1:8188`
2. **Test API:**
   ```bash
   curl http://127.0.0.1:8188/system_stats
   ```

### Step 5: Connect Your Bot

Update your bot's `.env` file:

```env
# In role-reactor-bot/.env
COMFYUI_API_URL=http://127.0.0.1:8188
COMFYUI_API_KEY=  # Leave empty for local
COMFYUI_WORKFLOW_ID=  # Leave empty (bot builds workflow automatically)
COMFYUI_CHECKPOINT=AnythingXL_xl.safetensors
```

Then restart your bot and test with `/imagine` command!

## 🔧 Troubleshooting

### "Module not found" errors

Install missing dependencies:
```bash
pip3 install <module-name>
```

### Port already in use

Use a different port:
```bash
python3 main.py --port 8189
```

Then update bot's `.env`: `COMFYUI_API_URL=http://127.0.0.1:8189`

### No models found

1. Check models are in `models/checkpoints/` directory
2. Verify filename matches exactly (case-sensitive)
3. Restart ComfyUI after adding models

### GPU not detected

ComfyUI will use CPU (slower but works). For GPU support:
- **NVIDIA:** Install CUDA-enabled PyTorch
- **AMD:** Install ROCm-enabled PyTorch
- **Apple Silicon:** Should work automatically with MPS

## 📝 Useful Commands

```bash
# Start with custom port
python3 main.py --port 8189

# Start with network access (for testing from other devices)
python3 main.py --listen 0.0.0.0

# Start with high-quality previews
python3 main.py --preview-method taesd

# View all options
python3 main.py --help
```

## 🎯 Next Steps

Once ComfyUI is running locally:

1. ✅ Test image generation in the web UI
2. ✅ Test bot connection with `/imagine` command
3. ✅ Verify models are working correctly
4. 🚀 Deploy to RunPod when ready (see `RUNPOD_SETUP.md`)

## 📚 Resources

- [ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI)
- [ComfyUI Documentation](https://github.com/comfyanonymous/ComfyUI/wiki)
- [Bot Setup Guide](../role-reactor-bot/docs/COMFYUI_LOCAL_SETUP.md)


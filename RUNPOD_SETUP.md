# ComfyUI RunPod Setup Guide

This guide will help you deploy ComfyUI to RunPod for use with the Role Reactor Bot.

## 📁 Project Structure

```
discord-bots/
├── role-reactor-bot/          # Your Discord bot (Node.js)
└── comfyui-runpod/            # ComfyUI for RunPod (Python) ← You are here
```

## 🚀 Quick Start for RunPod

### Option 1: Using RunPod Template (Recommended)

RunPod provides pre-built ComfyUI templates. This is the easiest way:

1. **Go to RunPod Dashboard** → **Templates**
2. **Search for "ComfyUI"**
3. **Select a ComfyUI template** (e.g., "ComfyUI Official")
4. **Deploy the pod**
5. **Get the endpoint URL** (e.g., `https://xxxxx-xxxxx.runpod.net`)

### Option 2: Custom Deployment

If you need custom configuration:

1. **Create a RunPod Pod** with:
   - GPU: RTX 3090, A40, or better
   - Container: `runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel`
   - Volume: Attach a persistent volume for models

2. **Connect to the pod** via SSH or Jupyter

3. **Install ComfyUI:**
   ```bash
   cd /workspace
   git clone https://github.com/comfyanonymous/ComfyUI.git
   cd ComfyUI
   pip install -r requirements.txt
   ```

4. **Download models** to `/workspace/ComfyUI/models/checkpoints/`

5. **Start ComfyUI:**
   ```bash
   python main.py --listen 0.0.0.0 --port 8000
   ```

6. **Expose the port** in RunPod:
   - Go to Pod settings
   - Add HTTP Service on port 8000
   - Get the public endpoint URL

## 🔧 Configuration

### Environment Variables (Optional)

Create a `.env` file or set in RunPod:

```env
# ComfyUI Configuration
COMFYUI_PORT=8000
COMFYUI_LISTEN=0.0.0.0
```

### Download Models

Recommended models for NSFW/anime content:

1. **AnythingXL_xl.safetensors** (Recommended)
   - Download to: `models/checkpoints/`
   - Direct link: [HuggingFace](https://huggingface.co/models)

2. **anything-v5-pruned.safetensors**
   - Download to: `models/checkpoints/`

3. **Other models:**
   - See `../role-reactor-bot/docs/COMFYUI_NSFW_GAME_MODELS.md` for more options

## 🔗 Connect Your Bot

Once ComfyUI is running on RunPod, update your bot's `.env`:

```env
# In role-reactor-bot/.env
COMFYUI_API_URL=https://your-pod-id.runpod.net
COMFYUI_API_KEY=  # Leave empty (or use RunPod API key if required)
COMFYUI_WORKFLOW_ID=  # Leave empty (bot builds workflow automatically)
COMFYUI_CHECKPOINT=AnythingXL_xl.safetensors
```

## 📝 RunPod-Specific Notes

### Port Configuration

- RunPod typically uses port **8000** or **7860** for HTTP services
- Make sure to expose the port in RunPod pod settings
- Use `--listen 0.0.0.0` to allow external connections

### Persistent Storage

- **Models**: Store in persistent volume (`/workspace/ComfyUI/models/`)
- **Outputs**: Can be stored in volume or downloaded via API
- **Config**: Save any custom configs to persistent volume

### Cost Optimization

- Use **Serverless** mode for pay-per-use (cheaper for low usage)
- Use **Dedicated** pods for consistent usage (better for high traffic)
- Stop pods when not in use to save costs

## 🧪 Testing

Test the API endpoint:

```bash
# Check if ComfyUI is running
curl https://your-pod-id.runpod.net/system_stats

# Should return JSON with system information
```

## 📚 Resources

- [RunPod Documentation](https://docs.runpod.io/)
- [ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI)
- [ComfyUI API Documentation](https://github.com/comfyanonymous/ComfyUI/wiki/API)
- [Bot Documentation](../role-reactor-bot/docs/COMFYUI_LOCAL_SETUP.md)

## 🆘 Troubleshooting

### Connection Issues

- Verify the RunPod endpoint URL is correct
- Check that the port is exposed in RunPod settings
- Ensure ComfyUI is running with `--listen 0.0.0.0`

### Model Not Found

- Verify model is in `models/checkpoints/` directory
- Check filename matches exactly (case-sensitive)
- Restart ComfyUI after adding models

### API Errors

- Check RunPod logs for ComfyUI errors
- Verify the API endpoint is accessible
- Test with `curl` first before using in bot

## 📦 Files in This Directory

- `main.py` - ComfyUI entry point
- `requirements.txt` - Python dependencies
- `README.md` - ComfyUI documentation
- `RUNPOD_SETUP.md` - This file


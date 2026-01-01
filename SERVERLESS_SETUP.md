# RunPod Serverless Setup Guide

This guide explains how to deploy your ComfyUI project as a RunPod serverless worker.

---

## 📋 Prerequisites

1. **RunPod Account** - Sign up at https://runpod.io
2. **Docker Hub Account** - For hosting your container image
3. **GitHub/GitLab** - For hosting your code (optional but recommended)

---

## 🚀 Quick Start

### Step 1: Build Docker Image

```bash
# Build the image
docker build -t your-dockerhub-username/comfyui-runpod:latest .

# Test locally (optional)
docker run -p 8188:8188 your-dockerhub-username/comfyui-runpod:latest
```

### Step 2: Push to Docker Hub

```bash
# Login to Docker Hub
docker login

# Push image
docker push your-dockerhub-username/comfyui-runpod:latest
```

### Step 3: Deploy to RunPod

1. Go to RunPod Dashboard → **Serverless**
2. Click **"Create Endpoint"**
3. Configure:
   - **Container Image:** `your-dockerhub-username/comfyui-runpod:latest`
   - **GPU Type:** RTX 3090, A40, or better
   - **Handler:** `handler.handler`
   - **Environment Variables:** (optional)
     - `COMFYUI_URL=http://localhost:8188`
     - `GENERATION_TIMEOUT=300`

### Step 4: Test Your Endpoint

```bash
# Get your endpoint URL from RunPod dashboard
ENDPOINT_URL="https://api.runpod.ai/v2/YOUR_ENDPOINT_ID"

# Test with a simple request
curl -X POST "$ENDPOINT_URL/runsync" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_RUNPOD_API_KEY" \
  -d '{
    "input": {
      "prompt": "a beautiful landscape",
      "width": 512,
      "height": 512,
      "steps": 30
    }
  }'
```

---

## 📝 Configuration

### Environment Variables

Set these in RunPod endpoint configuration:

| Variable | Default | Description |
|----------|---------|-------------|
| `COMFYUI_URL` | `http://localhost:8188` | ComfyUI server URL |
| `COMFYUI_API_KEY` | `None` | Optional API key for authentication |
| `GENERATION_TIMEOUT` | `300` | Max wait time for image generation (seconds) |
| `POLL_INTERVAL` | `1.0` | How often to check for completion (seconds) |

### Input Format

Your handler expects this input format:

```json
{
  "input": {
    "prompt": "your prompt text",
    "negative_prompt": "optional negative prompt",
    "checkpoint": "AnythingXL_xl.safetensors",
    "width": 512,
    "height": 512,
    "steps": 30,
    "cfg_scale": 7.5,
    "sampler": "euler_ancestral",
    "seed": 12345
  }
}
```

### Output Format

The handler returns:

```json
{
  "output": {
    "image_url": "http://localhost:8188/view?filename=...",
    "prompt_id": "uuid-here",
    "status": "success",
    "prompt": "your prompt",
    "parameters": {
      "width": 512,
      "height": 512,
      "steps": 30,
      "cfg_scale": 7.5,
      "sampler": "euler_ancestral",
      "seed": 12345,
      "checkpoint": "AnythingXL_xl.safetensors"
    }
  }
}
```

---

## 🔧 Customization

### Using Custom Workflows

To use a custom workflow instead of the default:

1. Modify `build_workflow()` in `handler.py`
2. Or load from a JSON file:

```python
def load_workflow_from_file(filepath: str) -> Dict[str, Any]:
    with open(filepath, 'r') as f:
        return json.load(f)

# In handler:
workflow = load_workflow_from_file("role-reactor-comfyui-workflow.json")
```

### Adding Authentication

If you want to use your custom API authentication:

1. Modify `handler.py` to check API keys
2. Add authentication logic before processing:

```python
def handler(job: Dict[str, Any]) -> Dict[str, Any]:
    # Check API key
    api_key = job.get("input", {}).get("api_key")
    if not validate_api_key(api_key):
        return {"error": "Invalid API key", "status": "error"}
    
    # Continue with generation...
```

---

## 🧪 Testing Locally

### Test Handler Directly

```python
# test_handler.py
from handler import handler

job = {
    "input": {
        "prompt": "a beautiful sunset",
        "width": 512,
        "height": 512
    }
}

result = handler(job)
print(result)
```

### Test with RunPod CLI

```bash
# Install RunPod CLI
pip install runpod

# Test locally
runpod serverless --handler handler.handler
```

---

## 📦 Adding to RunPod Hub

Once your serverless worker is working:

1. **Go to RunPod Hub** → **"Add your repo"**
2. **Connect your repository** (GitHub/GitLab)
3. **Configure:**
   - Repository URL
   - Dockerfile path: `Dockerfile`
   - Handler path: `handler.handler`
4. **Submit for review**

---

## 🐛 Troubleshooting

### Handler Not Found

- Check that `handler.py` is in the root directory
- Verify the handler function is named `handler`
- Check RunPod logs for errors

### ComfyUI Not Starting

- Ensure ComfyUI starts automatically in the container
- Check that port 8188 is accessible
- Verify models are in the correct directory

### Timeout Errors

- Increase `GENERATION_TIMEOUT` environment variable
- Check GPU memory (may need larger GPU)
- Reduce image resolution or steps

### Image Not Generated

- Check ComfyUI logs in RunPod
- Verify model checkpoint exists
- Test workflow in ComfyUI UI first

---

## 📚 Resources

- [RunPod Serverless Docs](https://docs.runpod.io/serverless)
- [RunPod Handler Examples](https://github.com/runpod/serverless)
- [ComfyUI API Docs](https://github.com/comfyanonymous/ComfyUI/wiki/API)

---

## ✅ Next Steps

1. ✅ Build and test Docker image locally
2. ✅ Push to Docker Hub
3. ✅ Deploy to RunPod Serverless
4. ✅ Test endpoint
5. ✅ Submit to RunPod Hub

---

**Need help?** Check the logs in RunPod dashboard or review the handler code.


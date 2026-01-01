# How to Load Workflow in ComfyUI

The workflow file `role-reactor-comfyui-workflow.json` is ready to use in ComfyUI.

## 🎯 Quick Method: Drag & Drop

1. **Open ComfyUI** in your browser: `http://127.0.0.1:8188` (or `http://localhost:8188`)
2. **Open Finder** and navigate to the project folder
3. **Drag** `role-reactor-comfyui-workflow.json` onto the ComfyUI canvas
4. **Done!** The workflow will load automatically

## 📋 Alternative Methods

### Method 2: Load Button

1. In ComfyUI, click **"Load"** button (top menu)
2. Navigate to the workflow file
3. Select and open

### Method 3: Save to ComfyUI Workflows Folder

You can also save it to ComfyUI's workflows folder for easy access:

```bash
# Copy to ComfyUI workflows folder (if it exists)
mkdir -p /Users/tyecode/dev/projects/discord-bots/comfyui-runpod/workflows
cp role-reactor-comfyui-workflow.json workflows/
```

Then load it from the workflows menu in ComfyUI.

## ✅ What the Workflow Contains

- **Model**: `AnythingXL_xl.safetensors` (optimized for anime/NSFW)
- **Settings**:
  - Steps: 30
  - CFG Scale: 7.5
  - Sampler: euler_ancestral
  - Seed: 0 (with randomize option)
- **Resolution**: 512x512 (default)
- **Negative Prompt**: Optimized for quality

## 🔧 After Loading

Once loaded, you can:
- Modify prompts in the CLIP Text Encode nodes
- Adjust KSampler settings
- Change image resolution in Empty Latent Image
- Test generation by clicking "Queue Prompt"

## 📝 Note

This workflow matches your bot's default settings, so images generated here will be similar to what your bot produces.


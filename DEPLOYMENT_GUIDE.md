# RunPod Deployment Guide - GitHub Integration

This guide explains how to deploy your ComfyUI project to RunPod Serverless directly from your GitHub repository **without needing Docker Hub**.

## Prerequisites

✅ Your project is already on GitHub (`qodinger/comfyui-runpod`)  
✅ You have a `Dockerfile` in the root directory  
✅ You have a `handler.py` file for RunPod serverless  
✅ You have a `runpod.yaml` configuration file

## Step-by-Step Deployment

### Step 1: Prepare Your Repository

Your repository should have the following structure:

```
comfyui-runpod/
├── handler.py          # RunPod serverless handler
├── Dockerfile          # Container build instructions
├── runpod.yaml         # RunPod configuration (optional)
├── start_serverless.sh # Startup script
├── requirements.txt    # Python dependencies
└── ... (other files)
```

✅ **All these files are already in your repository!**

### Step 2: Authorize RunPod to Access GitHub

1. **Log in to RunPod Console**

   - Go to [https://console.runpod.io/](https://console.runpod.io/)
   - Sign in with your RunPod account

2. **Connect GitHub**
   - Navigate to **Settings** → **Connections**
   - Find the **GitHub** card
   - Click **Connect**
   - Follow the GitHub authorization flow
   - Grant RunPod access to your repositories (or specific repos)

### Step 3: Deploy from GitHub

1. **Create New Endpoint**

   - In RunPod console, go to **Serverless** section
   - Click **New Endpoint**

2. **Import from GitHub**

   - Under **Import Git Repository**, select your repository:
     - Repository: `qodinger/comfyui-runpod`
     - Branch: `main` (or your default branch)
     - Dockerfile Path: `Dockerfile` (if in root, leave default)

3. **Configure Endpoint Settings**

   - **Endpoint Name**: `comfyui-with-auth` (or your preferred name)
   - **Endpoint Type**:
     - **Queue** - For traditional queue-based processing (recommended for serverless)
     - **Load Balancer** - For direct HTTP access
   - **GPU Configuration**:
     - Type: `NVIDIA`
     - Count: `1`
     - Memory: `24GB` (adjust based on your model requirements)
   - **Workers**: Configure number of workers (start with 1)
   - **Timeout**: Set appropriate timeout (default: 300 seconds)
   - **Environment Variables** (optional):
     ```
     COMFYUI_URL=http://localhost:8188
     GENERATION_TIMEOUT=300
     POLL_INTERVAL=1.0
     ```

4. **Deploy**
   - Click **Deploy Endpoint**
   - RunPod will automatically:
     - Pull your code from GitHub
     - Build the Docker image using your `Dockerfile`
     - Deploy to the endpoint
     - Start the serverless workers

### Step 4: Monitor Build Status

1. **View Build Progress**

   - Go to your endpoint's detail page
   - Click on the **Builds** tab
   - Monitor the build status:
     - **Pending** - Build is scheduled
     - **Building** - Docker image is being built
     - **Uploading** - Image is being uploaded to registry
     - **Testing** - Serverless worker is being tested
     - **Completed** - Build successful! ✅
     - **Failed** - Check build logs for errors ❌

2. **Check Build Logs**
   - Click on a build to view detailed logs
   - Look for any errors during the build process
   - Common issues:
     - Missing dependencies in `requirements.txt`
     - Dockerfile syntax errors
     - Missing files referenced in Dockerfile

### Step 5: Test Your Deployment

Once the build is complete:

1. **Get Your Endpoint URL**

   - In the endpoint details, find your endpoint URL
   - Format: `https://api.runpod.ai/v2/YOUR_ENDPOINT_ID`

2. **Test the Handler**

   ```bash
   curl -X POST https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync \
     -H "Content-Type: application/json" \
     -d '{
       "input": {
         "prompt": "a beautiful landscape",
         "width": 512,
         "height": 512,
         "steps": 30
       }
     }'
   ```

3. **Check Logs**
   - View real-time logs in the RunPod console
   - Monitor for any runtime errors

## Updating Your Deployment

### Method 1: GitHub Releases (Recommended)

1. **Make Changes**

   - Update your code in GitHub
   - Commit and push changes

2. **Create a Release**

   - Go to your GitHub repository
   - Click **Releases** → **Create a new release**
   - Tag version (e.g., `v1.0.1`)
   - Add release notes
   - Click **Publish release**

3. **Automatic Rebuild**
   - RunPod detects the new release
   - Automatically rebuilds and redeploys your endpoint
   - No manual intervention needed!

### Method 2: Manual Rebuild

1. **Trigger Rebuild**
   - Go to your endpoint in RunPod console
   - Click **Rebuild** or **Update**
   - Select the branch/commit to build from
   - Click **Rebuild**

## Configuration Options

### Using `runpod.yaml` (Optional)

If you have a `runpod.yaml` file, RunPod may use it for configuration. However, the GitHub integration primarily uses:

- **Dockerfile** - For building the container
- **handler.py** - For the serverless handler function
- **Console Settings** - For endpoint configuration

The `runpod.yaml` is more commonly used for RunPod Hub templates, but can provide default settings.

### Environment Variables

Set environment variables in the RunPod console:

- `COMFYUI_URL` - ComfyUI server URL (default: `http://localhost:8188`)
- `GENERATION_TIMEOUT` - Timeout for image generation (default: `300`)
- `POLL_INTERVAL` - Polling interval for checking status (default: `1.0`)

## Troubleshooting

### Build Fails

**Issue**: Build fails with dependency errors  
**Solution**:

- Check `requirements.txt` for all dependencies
- Ensure all packages are compatible
- Check Dockerfile for correct Python version

**Issue**: Build fails with file not found  
**Solution**:

- Verify all files referenced in Dockerfile exist
- Check `.dockerignore` isn't excluding needed files
- Ensure `start_serverless.sh` is included

### Runtime Errors

**Issue**: Handler not found  
**Solution**:

- Verify `handler.py` exists in root directory
- Check handler function is named `handler`
- Verify `start_serverless.sh` calls the correct handler

**Issue**: ComfyUI not starting  
**Solution**:

- Check logs for startup errors
- Verify port 8188 is accessible
- Check health check endpoint `/system_stats`

### Connection Issues

**Issue**: Can't connect to GitHub  
**Solution**:

- Re-authorize GitHub connection in Settings
- Check repository permissions
- Verify branch name is correct

## Best Practices

1. **Use GitHub Releases**

   - Create releases for stable versions
   - RunPod auto-rebuilds on new releases
   - Easier to track versions

2. **Monitor Build Logs**

   - Always check build logs after deployment
   - Fix issues before they affect production

3. **Test Locally First**

   - Test Docker build locally: `docker build -t test .`
   - Test handler function locally before deploying

4. **Use Environment Variables**

   - Don't hardcode secrets
   - Use RunPod's environment variable system
   - Keep sensitive data secure

5. **Version Control**
   - Tag releases in GitHub
   - Keep deployment history
   - Document changes in release notes

## Summary

✅ **No Docker Hub Required** - Deploy directly from GitHub  
✅ **Automatic Builds** - RunPod builds your Docker image automatically  
✅ **Easy Updates** - Create GitHub releases to trigger rebuilds  
✅ **Full Control** - Manage everything through RunPod console

Your project is ready to deploy! Just connect your GitHub account and follow the steps above.

## Additional Resources

- [RunPod GitHub Integration Docs](https://docs.runpod.io/serverless/github-integration)
- [RunPod Serverless Documentation](https://docs.runpod.io/serverless)
- [Example Worker Repository](https://github.com/runpod-workers/worker-basic)

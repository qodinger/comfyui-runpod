# ComfyUI RunPod Serverless

[![Runpod](https://api.runpod.io/badge/qodinger/comfyui-runpod)](https://console.runpod.io/hub/qodinger/comfyui-runpod)

A production-ready ComfyUI deployment for RunPod serverless with API authentication, rate limiting, and usage tracking.

## Features

- ✅ **API Authentication** - Secure API key-based authentication
- ✅ **Rate Limiting** - Per-key hourly rate limits with TOCTOU protection
- ✅ **Usage Tracking** - Comprehensive analytics and billing support
- ✅ **RunPod Serverless** - Ready for serverless deployment
- ✅ **Docker Support** - Containerized deployment with health checks

## Quick Start

### Local Development

```bash
# Start ComfyUI locally
./start-local.sh

# Start with API authentication enabled
./start_with_auth.sh
```

### RunPod Serverless Deployment

**Recommended: GitHub Deployment (No Docker Hub required)**

1. Connect GitHub in RunPod Settings → Connections
2. Create new Serverless endpoint
3. Select "Import Git Repository"
4. Choose your repository (`qodinger/comfyui-runpod`)
5. RunPod automatically builds from your `Dockerfile`
6. Configure GPU and settings
7. Deploy!

📖 **See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions**

## API Usage

### RunPod Serverless API

Send requests to your RunPod endpoint with workflow JSON:

```bash
curl -X POST https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/run \
  -H "Authorization: Bearer YOUR_RUNPOD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "workflow": {
        "3": {
          "inputs": {
            "seed": 12345,
            "steps": 20,
            "cfg": 7,
            "sampler_name": "euler_ancestral",
            "scheduler": "normal",
            "denoise": 1,
            "model": ["4", 0],
            "positive": ["6", 0],
            "negative": ["7", 0],
            "latent_image": ["5", 0]
          },
          "class_type": "KSampler"
        },
        "4": {
          "inputs": { "ckpt_name": "AnythingXL_xl.safetensors" },
          "class_type": "CheckpointLoaderSimple"
        },
        "5": {
          "inputs": { "width": 512, "height": 512, "batch_size": 1 },
          "class_type": "EmptyLatentImage"
        },
        "6": {
          "inputs": { "text": "a beautiful sunset", "clip": ["4", 1] },
          "class_type": "CLIPTextEncode"
        },
        "7": {
          "inputs": { "text": "low quality", "clip": ["4", 1] },
          "class_type": "CLIPTextEncode"
        },
        "8": {
          "inputs": { "samples": ["3", 0], "vae": ["4", 2] },
          "class_type": "VAEDecode"
        },
        "9": {
          "inputs": { "filename_prefix": "ComfyUI", "images": ["8", 0] },
          "class_type": "SaveImage"
        }
      }
    }
  }'
```

### Response Format

Images are returned as base64 or S3 URLs (if bucket configured):

```json
{
  "images": [
    {
      "filename": "ComfyUI_00001_.png",
      "type": "base64",
      "data": "iVBORw0KGgo..."
    }
  ]
}
```

### ComfyUI Local API

When running locally, API keys can be passed via:

- Header: `X-API-Key: your-api-key`
- Header: `Authorization: Bearer your-api-key`

## Configuration

### Environment Variables

Create a `.env` file (see `env.example`):

```bash
COMFYUI_URL=http://localhost:8188
GENERATION_TIMEOUT=300
POLL_INTERVAL=1.0
COMFYUI_API_KEY=  # Optional
```

### Command Line Arguments

```bash
# Enable API authentication (optional)
python main.py --enable-api-auth

# Require API authentication (mandatory)
python main.py --require-api-auth

# Custom port and listen address
python main.py --port 8080 --listen 0.0.0.0
```

## Project Structure

```
.
├── app/
│   ├── api_key_manager.py    # API key management
│   ├── usage_tracker.py       # Usage tracking
│   └── database/              # Database models
├── middleware/
│   ├── auth_middleware.py     # Authentication
│   ├── rate_limit_middleware.py  # Rate limiting
│   └── usage_tracking_middleware.py  # Usage tracking
├── handler.py                 # RunPod serverless handler
├── server.py                  # ComfyUI server
├── Dockerfile                 # Docker configuration
├── runpod.yaml                # RunPod configuration
└── start_serverless.sh        # Serverless startup script
```

## Security & Features

**Authentication:**

- API keys hashed with SHA-256 before storage
- Authentication required for sensitive endpoints
- No hardcoded secrets in code

**Rate Limiting:**

- Per-key hourly limits (configurable per key)
- Rate limit headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- TOCTOU protection for concurrent requests

**Usage Tracking:**

- Request counts, success/failure rates, response times
- Per-endpoint statistics and daily usage reports

## Health Checks

Health check endpoint: `/system_stats`

Docker health check: 30s interval, 10s timeout, 60s start period, 3 retries

## Troubleshooting

**API Key Issues:**

- Ensure authentication is enabled: `--enable-api-auth`
- Check API key is valid and active
- Verify rate limit hasn't been exceeded

**Deployment Issues:**

- Check Docker image builds successfully
- Verify all environment variables are set
- Ensure GPU requirements are met
- Check RunPod logs for errors

**Connection Issues:**

- Verify ComfyUI is running on correct port
- Check firewall/security group settings
- Ensure `--listen 0.0.0.0` for external access

## Documentation

- [Deployment Guide](DEPLOYMENT_GUIDE.md) - Step-by-step RunPod deployment
- [Alembic Database Migrations](alembic_db/README.md) - Database migration guide

## License

This project is based on ComfyUI, licensed under GNU GPL v3.0.

## Support

For issues and questions:

- Review API documentation at `/docs` endpoint when server is running
- Check logs for detailed error messages
- See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for deployment help

# ComfyUI RunPod - API Authentication & Serverless Deployment

ComfyUI deployment with API authentication, rate limiting, usage tracking, and RunPod serverless support.

## 🚀 Features

- ✅ **API Key Authentication** - Secure API access with key management
- ✅ **Rate Limiting** - Per-key request limits
- ✅ **Usage Tracking** - Monitor API usage and statistics
- ✅ **RunPod Serverless** - Deploy as serverless worker
- ✅ **NSFW Support** - Full support for NSFW/anime content generation
- ✅ **Custom Models** - Support for AnythingXL and custom checkpoints

## 📚 Documentation

See [DOCS_INDEX.md](DOCS_INDEX.md) for complete documentation.

### Quick Links

- **[API Documentation](API_DOCUMENTATION.md)** - Complete API reference
- **[API Setup Guide](API_SETUP_GUIDE.md)** - Quick start for API authentication
- **[Serverless Setup](SERVERLESS_SETUP.md)** - RunPod serverless deployment
- **[RunPod Setup](RUNPOD_SETUP.md)** - RunPod pod deployment

## 🛠️ Quick Start

### Local Development

```bash
# Start with authentication enabled
python main.py --enable-api-auth

# Or use the startup script
./start_with_auth.sh
```

### RunPod Serverless

   ```bash
# Build Docker image
docker build -t your-username/comfyui-runpod:latest .

# Push to Docker Hub
docker push your-username/comfyui-runpod:latest

# Deploy to RunPod Serverless
# See SERVERLESS_SETUP.md for details
```

## 📖 API Usage

### Create API Key

   ```bash
curl -X POST http://localhost:8188/api/keys \
  -H "Content-Type: application/json" \
  -d '{"name": "My Key", "rate_limit": 100}'
```

### Generate Image

```bash
curl -X POST http://localhost:8188/prompt \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"prompt": {...}}'
```

See [HOW_TO_GET_API_KEY.md](HOW_TO_GET_API_KEY.md) for more examples.

## 🔧 Configuration

- **Port**: Default `8188` (configurable)
- **Authentication**: Optional (`--enable-api-auth`) or Required (`--require-api-auth`)
- **Models**: Store in `models/checkpoints/`
- **API Keys**: Stored in `user/api_keys.json`

## 📦 Project Structure

```
├── handler.py              # RunPod serverless handler
├── Dockerfile              # Container configuration
├── server.py              # Main server with auth
├── app/                    # Application modules
│   ├── api_key_manager.py
│   └── usage_tracker.py
├── middleware/            # Auth & rate limiting
│   ├── auth_middleware.py
│   ├── rate_limit_middleware.py
│   └── usage_tracking_middleware.py
└── docs/                  # Documentation
```

## 🎯 Use Cases

- Discord bot image generation
- Commercial API service
- NSFW/anime content generation
- Custom model deployment

## 📝 License

Based on ComfyUI (see LICENSE file)

## 🔗 Links

- **Repository**: https://github.com/qodinger/comfyui-runpod
- **ComfyUI**: https://github.com/comfyanonymous/ComfyUI
- **RunPod**: https://runpod.io

---

**For detailed setup instructions, see [DOCS_INDEX.md](DOCS_INDEX.md)**

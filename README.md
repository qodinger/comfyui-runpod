# ComfyUI RunPod Serverless

A production-ready ComfyUI deployment for RunPod serverless with API authentication, rate limiting, and usage tracking.

## Features

- ✅ **API Authentication** - Secure API key-based authentication
- ✅ **Rate Limiting** - Per-key hourly rate limits with TOCTOU protection
- ✅ **Usage Tracking** - Comprehensive analytics and billing support
- ✅ **RunPod Serverless** - Ready for serverless deployment
- ✅ **Docker Support** - Containerized deployment with health checks
- ✅ **Error Handling** - Robust error handling and recovery

## Quick Start

### Local Development

```bash
# Start ComfyUI locally
./start-local.sh

# Start with API authentication enabled
./start_with_auth.sh
```

### RunPod Serverless Deployment

1. **Build Docker Image:**

   ```bash
   docker build -t your-username/comfyui-runpod:latest .
   ```

2. **Push to Registry:**

   ```bash
   docker push your-username/comfyui-runpod:latest
   ```

3. **Update `runpod.yaml`:**

   - Replace `your-dockerhub-username` with your Docker Hub username
   - Configure GPU requirements
   - Set environment variables

4. **Deploy to RunPod:**
   - Upload `runpod.yaml` to RunPod Hub
   - Configure persistent volumes for models
   - Enable health checks

## API Usage

### Authentication

API keys can be passed via:

- Header: `X-API-Key: your-api-key`
- Header: `Authorization: Bearer your-api-key`

### Creating an API Key

```bash
# First, create an initial API key (requires existing key or disable auth temporarily)
curl -X POST http://localhost:8188/api/keys \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: existing-key' \
  -d '{
    "name": "My API Key",
    "rate_limit": 100
  }'
```

### Using the API

```bash
# Generate an image
curl -X POST http://localhost:8188/api/prompt \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: your-api-key' \
  -d '{
    "prompt": "a beautiful landscape",
    "workflow": {...}
  }'
```

### API Key Management Endpoints

- `POST /api/keys` - Create new API key
- `GET /api/keys` - List all API keys
- `GET /api/keys/{key_id}` - Get key details with usage stats
- `PATCH /api/keys/{key_id}` - Update key (name, rate_limit, is_active)
- `DELETE /api/keys/{key_id}` - Delete API key
- `GET /api/usage/{key_id}` - Get usage statistics

## Configuration

### Environment Variables

Create a `.env` file (see `.env.example`):

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

# Custom port
python main.py --port 8080

# Listen on all interfaces
python main.py --listen 0.0.0.0
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

## Security

- API keys are hashed using SHA-256 before storage
- Rate limiting prevents abuse
- Authentication required for sensitive endpoints
- No hardcoded secrets in code

## Rate Limiting

- Per-key hourly limits
- Configurable rate limits per key
- Rate limit headers in responses:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

## Usage Tracking

Track API usage for:

- Request counts
- Success/failure rates
- Response times
- Per-endpoint statistics
- Daily usage reports

## Deployment

### Docker

```bash
docker build -t comfyui-runpod:latest .
docker run -p 8188:8188 comfyui-runpod:latest
```

### RunPod Serverless (GitHub Deployment - Recommended)

**No Docker Hub required!** Deploy directly from GitHub:

1. Connect GitHub in RunPod Settings → Connections
2. Create new Serverless endpoint
3. Select "Import Git Repository"
4. Choose your repository (`qodinger/comfyui-runpod`)
5. RunPod automatically builds from your `Dockerfile`
6. Configure GPU and settings
7. Deploy!

📖 **See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed step-by-step instructions**

### Alternative: Docker Hub Deployment

If you prefer Docker Hub:

1. Build Docker image: `docker build -t your-username/comfyui-runpod:latest .`
2. Push to Docker Hub: `docker push your-username/comfyui-runpod:latest`
3. Update `runpod.yaml` with your image
4. Deploy via RunPod Hub

## Health Checks

Health check endpoint: `/system_stats`

Docker health check configured with:

- Interval: 30s
- Timeout: 10s
- Start period: 60s
- Retries: 3

## Troubleshooting

### API Key Issues

- Ensure authentication is enabled: `--enable-api-auth`
- Check API key is valid and active
- Verify rate limit hasn't been exceeded

### Deployment Issues

- Check Docker image builds successfully
- Verify all environment variables are set
- Ensure GPU requirements are met
- Check RunPod logs for errors

### Connection Issues

- Verify ComfyUI is running on correct port
- Check firewall/security group settings
- Ensure `--listen 0.0.0.0` for external access

## Documentation

- [Alembic Database Migrations](alembic_db/README.md)
- [Production Readiness](PRODUCTION_READINESS.md)

## License

This project is based on ComfyUI, licensed under GNU GPL v3.0.

## Support

For issues and questions:

- Check the [Production Readiness](PRODUCTION_READINESS.md) document
- Review API documentation at `/docs` endpoint when server is running
- Check logs for detailed error messages

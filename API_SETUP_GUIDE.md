# API Authentication Setup Guide

Quick guide to enable and use API authentication in ComfyUI.

## Quick Start

### 1. Enable Authentication

```bash
# Start ComfyUI with optional authentication (recommended for testing)
python main.py --enable-api-auth

# Or require authentication for all API endpoints
python main.py --require-api-auth
```

### 2. Create Your First API Key

```bash
curl -X POST http://localhost:8188/api/keys \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My First Key",
    "rate_limit": 100
  }'
```

**Save the `api_key` from the response - you won't see it again!**

### 3. Use the API Key

```bash
curl -X POST http://localhost:8188/api/prompt \
  -H "X-API-Key: comfy_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{"prompt": {...}}'
```

## Configuration Options

### Command Line Arguments

- `--enable-api-auth` - Enable optional API authentication (keys tracked but not required)
- `--require-api-auth` - Require API authentication for all `/api/*` endpoints

### Rate Limits

Default: **100 requests/hour** per key

You can customize when creating or updating keys:

```bash
# Create key with custom rate limit
curl -X POST http://localhost:8188/api/keys \
  -H "Content-Type: application/json" \
  -d '{
    "name": "High Volume Key",
    "rate_limit": 1000
  }'
```

## File Locations

API keys and usage data are stored in:

- **API Keys:** `user/api_keys.json`
- **Usage Data:** `user/api_usage.json`

These files are created automatically when you first create an API key.

## Next Steps

1. **Read the full documentation:** [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
2. **Review the business plan:** [BUSINESS_IMPROVEMENT_PLAN.md](./BUSINESS_IMPROVEMENT_PLAN.md)
3. **Check project review:** [PROJECT_REVIEW.md](./PROJECT_REVIEW.md)

## Common Tasks

### List All Keys

```bash
curl http://localhost:8188/api/keys
```

### Check Usage

```bash
curl -H "X-API-Key: comfy_your_key_here" \
     http://localhost:8188/api/usage?days=7
```

### Update Rate Limit

```bash
curl -X PATCH http://localhost:8188/api/keys/{key_id} \
  -H "Content-Type: application/json" \
  -d '{"rate_limit": 200}'
```

### Delete a Key

```bash
curl -X DELETE http://localhost:8188/api/keys/{key_id}
```

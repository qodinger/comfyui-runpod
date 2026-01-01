# ComfyUI API Documentation

This document describes the API authentication and management features added to ComfyUI for commercial use.

## Table of Contents

- [Authentication](#authentication)
- [API Key Management](#api-key-management)
- [Rate Limiting](#rate-limiting)
- [Usage Tracking](#usage-tracking)
- [API Endpoints](#api-endpoints)
- [Examples](#examples)

---

## Authentication

### Overview

ComfyUI now supports API key authentication for external API access. This allows you to:

- Control access to your ComfyUI instance
- Track usage per API key
- Implement rate limiting
- Prepare for billing integration

### Enabling Authentication

Start ComfyUI with authentication enabled:

```bash
# Optional authentication (keys tracked but not required)
python main.py --enable-api-auth

# Required authentication (keys required for all /api/* endpoints)
python main.py --require-api-auth
```

### Using API Keys

Include your API key in requests using one of these methods:

**Method 1: X-API-Key Header (Recommended)**

```bash
curl -H "X-API-Key: comfy_your_api_key_here" \
     https://your-comfyui-instance.com/api/prompt
```

**Method 2: Authorization Header**

```bash
curl -H "Authorization: Bearer comfy_your_api_key_here" \
     https://your-comfyui-instance.com/api/prompt
```

### Public Endpoints

The following endpoints are always public (no authentication required):

- `/` - Web UI
- `/ws` - WebSocket connections
- `/system_stats` - System information
- `/features` - Feature flags
- `/object_info` - Node information
- `/extensions` - Extension list
- `/embeddings` - Embedding list
- `/models` - Model list
- `/view` - Image viewing
- `/docs` - API documentation

---

## API Key Management

### Create API Key

**Endpoint:** `POST /api/keys`

**Request Body:**

```json
{
  "name": "My API Key",
  "rate_limit": 100,
  "metadata": {
    "customer": "customer_id",
    "plan": "pro"
  }
}
```

**Response:**

```json
{
  "key_id": "abc123...",
  "api_key": "comfy_xxxxxxxxxxxxx",
  "name": "My API Key",
  "rate_limit": 100,
  "message": "API key created. Save this key - it will not be shown again."
}
```

**⚠️ Important:** The `api_key` field is only shown once. Save it immediately!

### List API Keys

**Endpoint:** `GET /api/keys`

**Response:**

```json
{
  "keys": [
    {
      "key_id": "abc123...",
      "name": "My API Key",
      "created_at": 1706457600.0,
      "last_used": 1706457800.0,
      "rate_limit": 100,
      "is_active": true,
      "metadata": {}
    }
  ]
}
```

### Get API Key Details

**Endpoint:** `GET /api/keys/{key_id}`

**Response:**

```json
{
  "key_id": "abc123...",
  "name": "My API Key",
  "created_at": 1706457600.0,
  "last_used": 1706457800.0,
  "rate_limit": 100,
  "is_active": true,
  "metadata": {},
  "usage_stats": {
    "total_requests": 150,
    "successful_requests": 148,
    "failed_requests": 2,
    "total_duration": 4500.5,
    "average_duration": 30.0,
    "requests_per_day": {
      "2025-01-28": 50,
      "2025-01-29": 100
    }
  }
}
```

### Update API Key

**Endpoint:** `PATCH /api/keys/{key_id}`

**Request Body:**

```json
{
  "name": "Updated Name",
  "rate_limit": 200,
  "is_active": true
}
```

**Response:**

```json
{
  "message": "API key updated"
}
```

### Delete API Key

**Endpoint:** `DELETE /api/keys/{key_id}`

**Response:**

```json
{
  "message": "API key deleted"
}
```

---

## Rate Limiting

### Overview

Rate limiting is automatically applied when authentication is enabled. Each API key has a configurable hourly request limit.

### Rate Limit Headers

All API responses include rate limit information:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1706461200
```

### Rate Limit Exceeded

When rate limit is exceeded, you'll receive:

**Status Code:** `429 Too Many Requests`

**Response:**

```json
{
  "error": "Rate limit exceeded",
  "error_code": "RATE_LIMIT_EXCEEDED",
  "limit": 100,
  "reset_in": 3600
}
```

### Default Limits

- New API keys: **100 requests/hour** (configurable)
- Can be adjusted per key via the update endpoint

---

## Usage Tracking

### Get Your Usage Statistics

**Endpoint:** `GET /api/usage?days=30`

**Headers:**

```
X-API-Key: comfy_your_api_key_here
```

**Response:**

```json
{
  "key_id": "abc123...",
  "key_name": "My API Key",
  "usage_stats": {
    "total_requests": 150,
    "successful_requests": 148,
    "failed_requests": 2,
    "total_duration": 4500.5,
    "average_duration": 30.0,
    "requests_per_day": {
      "2025-01-28": 50,
      "2025-01-29": 100
    }
  }
}
```

### Get All Usage Statistics (Admin)

**Endpoint:** `GET /api/usage/all?days=30`

**Response:**

```json
{
  "usage_stats": {
    "key_id_1": {
      "total_requests": 150,
      "successful_requests": 148,
      ...
    },
    "key_id_2": {
      "total_requests": 75,
      ...
    }
  }
}
```

---

## API Endpoints

### Standard ComfyUI Endpoints

All standard ComfyUI endpoints work with API keys:

- `POST /api/prompt` - Queue a prompt
- `GET /api/queue` - Get queue status
- `GET /api/history` - Get generation history
- `POST /api/interrupt` - Interrupt generation
- `POST /api/free` - Free memory

### New Management Endpoints

- `POST /api/keys` - Create API key
- `GET /api/keys` - List API keys
- `GET /api/keys/{key_id}` - Get key details
- `PATCH /api/keys/{key_id}` - Update key
- `DELETE /api/keys/{key_id}` - Delete key
- `GET /api/usage` - Get usage stats (authenticated)
- `GET /api/usage/all` - Get all usage stats

---

## Examples

### Python Example

```python
import requests

API_KEY = "comfy_your_api_key_here"
BASE_URL = "https://your-comfyui-instance.com"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

# Queue a prompt
response = requests.post(
    f"{BASE_URL}/api/prompt",
    headers=headers,
    json={
        "prompt": {
            "3": {
                "inputs": {
                    "text": "a beautiful landscape"
                },
                "class_type": "CLIPTextEncode"
            }
        }
    }
)

print(response.json())
```

### cURL Example

```bash
# Create an API key
curl -X POST https://your-comfyui-instance.com/api/keys \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Bot Key",
    "rate_limit": 200
  }'

# Use the API key
curl -X POST https://your-comfyui-instance.com/api/prompt \
  -H "X-API-Key: comfy_your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": {
      "3": {
        "inputs": {"text": "a beautiful landscape"},
        "class_type": "CLIPTextEncode"
      }
    }
  }'

# Check usage
curl -X GET "https://your-comfyui-instance.com/api/usage?days=7" \
  -H "X-API-Key: comfy_your_api_key_here"
```

### Node.js Example

```javascript
const axios = require("axios");

const API_KEY = "comfy_your_api_key_here";
const BASE_URL = "https://your-comfyui-instance.com";

const client = axios.create({
  baseURL: BASE_URL,
  headers: {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json",
  },
});

// Queue a prompt
async function queuePrompt(prompt) {
  const response = await client.post("/api/prompt", { prompt });
  return response.data;
}

// Get usage stats
async function getUsage(days = 30) {
  const response = await client.get(`/api/usage?days=${days}`);
  return response.data;
}
```

---

## Error Codes

| Error Code            | Description                       | HTTP Status |
| --------------------- | --------------------------------- | ----------- |
| `AUTH_REQUIRED`       | API key required but not provided | 401         |
| `INVALID_KEY`         | Invalid or inactive API key       | 401         |
| `RATE_LIMIT_EXCEEDED` | Rate limit exceeded               | 429         |
| `KEY_NOT_FOUND`       | API key not found                 | 404         |
| `KEY_CREATION_FAILED` | Failed to create API key          | 500         |

---

## Security Best Practices

1. **Store API keys securely** - Never commit keys to version control
2. **Use environment variables** - Store keys in environment variables
3. **Rotate keys regularly** - Delete old keys and create new ones
4. **Set appropriate rate limits** - Match rate limits to your use case
5. **Monitor usage** - Regularly check usage statistics for anomalies
6. **Use HTTPS** - Always use HTTPS in production

---

## Migration Guide

### From Unauthenticated to Authenticated

1. **Enable authentication:**

   ```bash
   python main.py --enable-api-auth
   ```

2. **Create API keys** for your clients:

   ```bash
   curl -X POST http://localhost:8188/api/keys \
     -H "Content-Type: application/json" \
     -d '{"name": "Client Key", "rate_limit": 100}'
   ```

3. **Update client code** to include API keys in requests

4. **Test thoroughly** before enabling `--require-api-auth`

5. **Enable required authentication:**
   ```bash
   python main.py --require-api-auth
   ```

---

## Troubleshooting

### "API key required" error

- Make sure you're including the API key in the request header
- Check that authentication is enabled: `--enable-api-auth` or `--require-api-auth`
- Verify the endpoint requires authentication (some endpoints are public)

### "Invalid API key" error

- Verify the API key is correct (copy-paste can introduce errors)
- Check that the key is active: `GET /api/keys/{key_id}`
- Ensure the key hasn't been deleted

### Rate limit exceeded

- Check your current usage: `GET /api/usage`
- Wait for the rate limit to reset (check `X-RateLimit-Reset` header)
- Consider increasing the rate limit: `PATCH /api/keys/{key_id}`

---

## Support

For issues or questions:

- Check the [ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI)
- Review the [Business Improvement Plan](./BUSINESS_IMPROVEMENT_PLAN.md)
- See [Project Review](./PROJECT_REVIEW.md) for architecture details

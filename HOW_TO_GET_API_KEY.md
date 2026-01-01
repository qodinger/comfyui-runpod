# How to Get an API Key

This guide shows you how to create and retrieve API keys for ComfyUI.

## Prerequisites

- ComfyUI server must be running with `--enable-api-auth` or `--require-api-auth`
- Server should be accessible at `http://localhost:8188` (or your configured address)

---

## Method 1: Using cURL (Command Line)

### Create a New API Key

```bash
curl -X POST http://localhost:8188/api/keys \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My API Key",
    "rate_limit": 100
  }'
```

**Response:**

```json
{
  "key_id": "4BWRV-e4Jclw...",
  "api_key": "comfy_Qp1z1J2msnFwJdhm3zqES4JY...",
  "name": "My API Key",
  "rate_limit": 100,
  "message": "API key created. Save this key - it will not be shown again."
}
```

⚠️ **IMPORTANT:** Save the `api_key` value immediately - it's only shown once!

### List All API Keys

```bash
curl http://localhost:8188/api/keys
```

**Response:**

```json
{
  "keys": [
    {
      "key_id": "4BWRV-e4Jclw...",
      "name": "My API Key",
      "created_at": 1706451234.567,
      "last_used": null,
      "rate_limit": 100,
      "is_active": true
    }
  ]
}
```

Note: The actual API key is NOT shown in the list for security reasons.

### Get Key Details

```bash
curl http://localhost:8188/api/keys/{key_id}
```

Replace `{key_id}` with your actual key ID.

---

## Method 2: Using Python

### Create a New API Key

```python
import requests

response = requests.post(
    'http://localhost:8188/api/keys',
    json={
        'name': 'My API Key',
        'rate_limit': 100,
        'metadata': {'project': 'my-project'}
    }
)

if response.status_code == 200:
    data = response.json()
    api_key = data['api_key']
    key_id = data['key_id']

    print(f"✅ API Key created!")
    print(f"Key ID: {key_id}")
    print(f"API Key: {api_key}")
    print("\n⚠️  Save this key - it won't be shown again!")

    # Save to file
    with open('api_key.txt', 'w') as f:
        f.write(api_key)
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
```

### List All Keys

```python
import requests

response = requests.get('http://localhost:8188/api/keys')
if response.status_code == 200:
    data = response.json()
    for key in data['keys']:
        print(f"Key ID: {key['key_id']}")
        print(f"Name: {key['name']}")
        print(f"Rate Limit: {key['rate_limit']}/hour")
        print(f"Active: {key['is_active']}")
        print("---")
```

---

## Method 3: Using JavaScript/Node.js

### Create a New API Key

```javascript
const fetch = require("node-fetch");

async function createAPIKey() {
  const response = await fetch("http://localhost:8188/api/keys", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: "My API Key",
      rate_limit: 100,
    }),
  });

  if (response.ok) {
    const data = await response.json();
    console.log("✅ API Key created!");
    console.log("Key ID:", data.key_id);
    console.log("API Key:", data.api_key);
    console.log("\n⚠️  Save this key - it won't be shown again!");
    return data.api_key;
  } else {
    console.error("❌ Error:", response.status, await response.text());
  }
}

createAPIKey();
```

---

## Method 4: Using the Test Script

The project includes a test script that creates a key:

```bash
python3 test_api_auth.py
```

This will create a test key and show it in the output.

---

## Using Your API Key

Once you have an API key, use it in requests:

### With cURL

```bash
curl -H "X-API-Key: comfy_your_key_here" \
     http://localhost:8188/api/usage
```

### With Python

```python
import requests

api_key = "comfy_your_key_here"

response = requests.get(
    'http://localhost:8188/api/usage',
    headers={'X-API-Key': api_key}
)

print(response.json())
```

### With Authorization Header (Alternative)

You can also use the `Authorization` header:

```bash
curl -H "Authorization: Bearer comfy_your_key_here" \
     http://localhost:8188/api/usage
```

---

## API Key Parameters

When creating a key, you can specify:

- **`name`** (required): A descriptive name for the key
- **`rate_limit`** (optional, default: 100): Requests per hour
- **`metadata`** (optional): Custom metadata dictionary

**Example with all parameters:**

```bash
curl -X POST http://localhost:8188/api/keys \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Production Key",
    "rate_limit": 1000,
    "metadata": {
      "project": "my-app",
      "environment": "production"
    }
  }'
```

---

## Security Best Practices

1. **Save the API key immediately** - It's only shown once when created
2. **Store securely** - Don't commit keys to version control
3. **Use environment variables**:
   ```bash
   export COMFYUI_API_KEY="comfy_your_key_here"
   ```
4. **Rotate keys regularly** - Delete old keys and create new ones
5. **Use different keys for different projects** - Easier to track and revoke

---

## Troubleshooting

### "405 Method Not Allowed"

- Make sure you're using `POST` for creating keys
- Check that the server is running with `--enable-api-auth`

### "404 Not Found"

- Verify the server is running: `curl http://localhost:8188/system_stats`
- Check that authentication is enabled

### "401 Unauthorized"

- Verify your API key is correct
- Check that the key is active (not deleted)

---

## Quick Reference

| Endpoint             | Method | Description                        |
| -------------------- | ------ | ---------------------------------- |
| `/api/keys`          | POST   | Create a new API key               |
| `/api/keys`          | GET    | List all API keys                  |
| `/api/keys/{key_id}` | GET    | Get key details                    |
| `/api/keys/{key_id}` | PATCH  | Update a key                       |
| `/api/keys/{key_id}` | DELETE | Delete a key                       |
| `/api/usage`         | GET    | Get usage stats (requires API key) |

---

**Need help?** Check the [API Documentation](API_DOCUMENTATION.md) for more details.

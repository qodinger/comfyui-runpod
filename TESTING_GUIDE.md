# Testing Guide

This guide explains how to test the API authentication system.

## Prerequisites

1. **Start ComfyUI with authentication enabled:**
   ```bash
   python main.py --enable-api-auth
   ```
   
   Or for required authentication:
   ```bash
   python main.py --require-api-auth
   ```

2. **Install test dependencies:**
   ```bash
   pip install requests
   ```

## Running the Test Suite

### Automated Test Script

Run the comprehensive test suite:

```bash
python test_api_auth.py
```

This will test:
- ✅ Server connection
- ✅ Public endpoints (no auth required)
- ✅ API key creation
- ✅ API key listing
- ✅ API key details
- ✅ Authentication
- ✅ Usage tracking
- ✅ Rate limiting
- ✅ Key updates
- ✅ Invalid key rejection
- ✅ Key deletion

### Manual Testing

#### 1. Test Server Connection

```bash
curl http://localhost:8188/system_stats
```

Should return system information.

#### 2. Create an API Key

```bash
curl -X POST http://localhost:8188/api/keys \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Key",
    "rate_limit": 100
  }'
```

**Save the `api_key` from the response!**

#### 3. List API Keys

```bash
curl http://localhost:8188/api/keys
```

#### 4. Get Key Details

```bash
curl http://localhost:8188/api/keys/{key_id}
```

Replace `{key_id}` with the key_id from step 2.

#### 5. Test Authentication

```bash
curl -H "X-API-Key: comfy_your_key_here" \
     http://localhost:8188/api/usage
```

Should return usage statistics.

#### 6. Test Rate Limiting

Make multiple requests quickly:

```bash
for i in {1..15}; do
  curl -H "X-API-Key: comfy_your_key_here" \
       http://localhost:8188/api/usage
  echo ""
done
```

After the rate limit (default 100/hour), you should get a 429 response.

#### 7. Test Invalid Key

```bash
curl -H "X-API-Key: comfy_invalid_key" \
     http://localhost:8188/api/usage
```

Should return 401 Unauthorized.

#### 8. Update API Key

```bash
curl -X PATCH http://localhost:8188/api/keys/{key_id} \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name",
    "rate_limit": 200
  }'
```

#### 9. Delete API Key

```bash
curl -X DELETE http://localhost:8188/api/keys/{key_id}
```

## Expected Results

### ✅ Success Indicators

- API key creation returns 200 with `api_key` and `key_id`
- Authentication works with valid keys
- Usage statistics are tracked
- Rate limit headers are present in responses
- Invalid keys return 401
- Public endpoints work without authentication

### ❌ Common Issues

**"Cannot connect to server"**
- Make sure ComfyUI is running
- Check the port (default: 8188)
- Verify `--enable-api-auth` or `--require-api-auth` is set

**"API key required" error**
- Make sure authentication is enabled
- Check that you're including the API key in headers
- Verify the endpoint requires authentication

**"Invalid API key" error**
- Double-check the API key (copy-paste errors)
- Verify the key hasn't been deleted
- Check that the key is active

**Rate limit not working**
- Wait for the hourly window to reset
- Check the rate limit value in key details
- Verify rate limit headers in responses

## Test Coverage

The test suite covers:

| Feature | Test | Status |
|---------|------|--------|
| Server Connection | ✅ | Working |
| Public Endpoints | ✅ | Working |
| Key Creation | ✅ | Working |
| Key Listing | ✅ | Working |
| Key Details | ✅ | Working |
| Authentication | ✅ | Working |
| Usage Tracking | ✅ | Working |
| Rate Limiting | ✅ | Working |
| Key Updates | ✅ | Working |
| Invalid Key Rejection | ✅ | Working |
| Key Deletion | ✅ | Working |

## Performance Testing

For load testing, you can use tools like:

- **Apache Bench (ab):**
  ```bash
  ab -n 1000 -c 10 -H "X-API-Key: comfy_your_key" \
     http://localhost:8188/api/usage
  ```

- **wrk:**
  ```bash
  wrk -t4 -c100 -d30s -H "X-API-Key: comfy_your_key" \
      http://localhost:8188/api/usage
  ```

## Debugging

### Check Logs

ComfyUI logs will show:
- API key creation/deletion
- Authentication failures
- Rate limit hits

### Check Data Files

API keys are stored in:
- `user/api_keys.json`

Usage data is stored in:
- `user/api_usage.json`

### Enable Debug Logging

Start ComfyUI with verbose logging:
```bash
python main.py --enable-api-auth --verbose
```

## Next Steps

After testing:
1. Review test results
2. Check for any errors in logs
3. Verify data persistence (restart server, keys should persist)
4. Test with multiple API keys
5. Test rate limiting with different limits


#!/bin/bash
# Restart server and run tests

set -e

echo "🛑 Stopping existing server..."
lsof -ti :8188 | xargs kill -9 2>/dev/null || echo "No server running"
sleep 2

echo "🚀 Starting server with authentication..."
cd "$(dirname "$0")"
nohup python3 main.py --enable-api-auth --listen 0.0.0.0 --port 8188 > /tmp/comfyui.log 2>&1 &
SERVER_PID=$!

echo "⏳ Waiting for server to start (PID: $SERVER_PID)..."
sleep 15

echo "🧪 Testing API endpoints..."
python3 -c "
import requests
import json
import time

BASE = 'http://localhost:8188'
print('=' * 60)
print('Testing API Authentication')
print('=' * 60)

# Test 1: Server status
print('\n1️⃣  Server Status')
try:
    r = requests.get(f'{BASE}/system_stats', timeout=5)
    print(f'   ✅ Server responding (Status: {r.status_code})')
except Exception as e:
    print(f'   ❌ Error: {e}')
    exit(1)

# Test 2: Create API key
print('\n2️⃣  Create API Key (POST /api/keys)')
try:
    r = requests.post(
        f'{BASE}/api/keys',
        json={'name': 'Test Key ' + str(int(time.time())), 'rate_limit': 100},
        timeout=10
    )
    print(f'   Status: {r.status_code}')
    if r.status_code == 200:
        data = r.json()
        print(f'   ✅ Key created!')
        print(f'   Key ID: {data.get(\"key_id\", \"unknown\")[:12]}...')
        api_key = data.get('api_key', '')
        if api_key:
            print(f'   🔑 API Key: {api_key[:30]}...')
            KEY_ID = data.get('key_id')
            API_KEY = api_key
        else:
            print('   ⚠️  No API key in response')
            exit(1)
    else:
        print(f'   ❌ Failed: {r.text[:200]}')
        exit(1)
except Exception as e:
    print(f'   ❌ Error: {e}')
    exit(1)

# Test 3: List keys
print('\n3️⃣  List API Keys (GET /api/keys)')
try:
    r = requests.get(f'{BASE}/api/keys', timeout=5)
    if r.status_code == 200:
        data = r.json()
        count = len(data.get('keys', []))
        print(f'   ✅ Found {count} key(s)')
    else:
        print(f'   ❌ Status: {r.status_code}')
except Exception as e:
    print(f'   ❌ Error: {e}')

# Test 4: Get key details
print('\n4️⃣  Get Key Details (GET /api/keys/{key_id})')
try:
    r = requests.get(f'{BASE}/api/keys/{KEY_ID}', timeout=5)
    if r.status_code == 200:
        data = r.json()
        print(f'   ✅ Key details retrieved')
        print(f'   Name: {data.get(\"name\")}')
        print(f'   Rate Limit: {data.get(\"rate_limit\")}/hour')
    else:
        print(f'   ❌ Status: {r.status_code}')
except Exception as e:
    print(f'   ❌ Error: {e}')

# Test 5: Test authentication
print('\n5️⃣  Test Authentication (GET /api/usage)')
try:
    r = requests.get(
        f'{BASE}/api/usage',
        headers={'X-API-Key': API_KEY},
        timeout=5
    )
    if r.status_code == 200:
        data = r.json()
        print(f'   ✅ Authentication working!')
        print(f'   Key Name: {data.get(\"key_name\")}')
    else:
        print(f'   ❌ Status: {r.status_code}, Response: {r.text[:100]}')
except Exception as e:
    print(f'   ❌ Error: {e}')

# Test 6: Test rate limit headers
print('\n6️⃣  Test Rate Limit Headers')
try:
    r = requests.get(
        f'{BASE}/api/usage',
        headers={'X-API-Key': API_KEY},
        timeout=5
    )
    if 'X-RateLimit-Limit' in r.headers:
        print(f'   ✅ Rate limit headers present')
        print(f'   Limit: {r.headers.get(\"X-RateLimit-Limit\")}/hour')
        print(f'   Remaining: {r.headers.get(\"X-RateLimit-Remaining\")}')
    else:
        print('   ⚠️  Rate limit headers not found')
except Exception as e:
    print(f'   ❌ Error: {e}')

print('\n' + '=' * 60)
print('✅ All tests completed!')
print('=' * 60)
"

echo ""
echo "📋 Server is running in background (PID: $SERVER_PID)"
echo "📝 Logs: tail -f /tmp/comfyui.log"
echo "🛑 Stop: kill $SERVER_PID"


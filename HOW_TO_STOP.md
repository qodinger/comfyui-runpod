# How to Stop ComfyUI Server

## Quick Methods

### Method 1: Using the Stop Script (Recommended)

```bash
./stop_server.sh
```

This script will:

- Find the process on port 8188
- Send a graceful shutdown signal
- Force kill if needed
- Verify the server is stopped

### Method 2: Manual Stop

**Find the process:**

```bash
lsof -ti :8188
```

**Stop gracefully:**

```bash
kill -TERM $(lsof -ti :8188)
```

**Force stop (if needed):**

```bash
kill -9 $(lsof -ti :8188)
```

### Method 3: If Running in Terminal

If you started ComfyUI in a terminal window:

- Press `Ctrl+C` to stop it gracefully
- The server will shut down cleanly

### Method 4: Stop All Python Processes (Use with Caution)

```bash
# Find all ComfyUI-related processes
ps aux | grep "main.py\|server.py" | grep -v grep

# Stop specific process by PID
kill -TERM <PID>
```

## Verify Server is Stopped

```bash
# Check if port is free
lsof -ti :8188 || echo "Server is stopped"

# Or use the status checker
python3 check_api_status.py
```

## Troubleshooting

### Port Still in Use

If port 8188 is still in use after stopping:

```bash
# Find what's using it
lsof -i :8188

# Force kill
kill -9 $(lsof -ti :8188)
```

### Multiple Processes

If multiple processes are running:

```bash
# List all processes on port 8188
lsof -ti :8188

# Stop all of them
lsof -ti :8188 | xargs kill -9
```

## Notes

- **Graceful shutdown** (SIGTERM) allows the server to finish current requests
- **Force kill** (SIGKILL) immediately stops the server (may lose data)
- Always try graceful shutdown first, then force kill if needed

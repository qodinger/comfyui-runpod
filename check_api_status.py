#!/usr/bin/env python3
"""Quick script to check if ComfyUI API is running"""
import socket
import sys

def check_port(host='localhost', port=8188):
    """Check if port is open"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"Error checking port: {e}")
        return False

def main():
    print("Checking ComfyUI API status...")
    print(f"{'='*50}")
    
    # Check port
    port_open = check_port()
    if port_open:
        print("✅ Port 8188 is OPEN - Server is listening")
        print("\nTo verify API is working, try:")
        print("  curl http://localhost:8188/system_stats")
        print("  curl http://localhost:8188/api/keys")
        print("\nOr open in browser:")
        print("  http://localhost:8188")
    else:
        print("❌ Port 8188 is CLOSED - Server is not running")
        print("\nTo start the server:")
        print("  python main.py --enable-api-auth")
    
    return 0 if port_open else 1

if __name__ == "__main__":
    sys.exit(main())


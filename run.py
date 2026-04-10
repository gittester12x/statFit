#!/usr/bin/env python3
"""Run the StatFit web application."""
import sys
import os
import socket

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

def find_available_port(start_port=5000, max_attempts=100):
    """Find an available port starting from start_port."""
    import platform

    # On macOS, try 0.0.0.0 first as it's more reliable for local development
    if platform.system() == 'Darwin':  # macOS
        hosts_to_try = ['0.0.0.0', 'localhost', '127.0.0.1']
    else:
        hosts_to_try = ['localhost', '127.0.0.1', '0.0.0.0']

    for host in hosts_to_try:
        for port in range(start_port, start_port + max_attempts):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.bind((host, port))
                    return port, host
            except OSError:
                continue
        # If we get here, try next host
        continue

    raise RuntimeError(f"No available ports found between {start_port} and {start_port + max_attempts - 1}")

if __name__ == '__main__':
    # Find an available port starting from 5000
    port, host = find_available_port(5000)

    print("🚀 Starting StatFit...")
    print(f"📱 Open your browser to: http://localhost:{port}")
    print(f"   Or try: http://127.0.0.1:{port}")
    print("❌ Press Ctrl+C to stop")
    print(f"🔧 Debug: Server bound to {host}:{port}")

    app.run(debug=True, host=host, port=port)
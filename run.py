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
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.bind(('0.0.0.0', port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"No available ports found between {start_port} and {start_port + max_attempts - 1}")

if __name__ == '__main__':
    # Find an available port starting from 5000
    port = find_available_port(5000)

    print("🚀 Starting StatFit...")
    print(f"📱 Open your browser to: http://localhost:{port}")
    print("❌ Press Ctrl+C to stop")
    app.run(debug=True, host='0.0.0.0', port=port)
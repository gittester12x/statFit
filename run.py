#!/usr/bin/env python3
"""Run the StatFit web application."""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == '__main__':
    print("🚀 Starting StatFit...")
    print("📱 Open your browser to: http://localhost:5000")
    print("❌ Press Ctrl+C to stop")
    app.run(debug=True, host='0.0.0.0', port=5000)
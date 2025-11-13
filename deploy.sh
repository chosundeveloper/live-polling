#!/bin/bash
# Simple deployment script that opens browser

# Kill any existing python server on port 8080
lsof -ti:8080 | xargs kill -9 2>/dev/null

# Start HTTP server in background
python3 -m http.server 8080 --bind 127.0.0.1 &

# Wait for server to start
sleep 1

# Open browser
open "http://localhost:8080/display.html?mock=1&question=1"

echo "🚀 Server running at http://localhost:8080"
echo "📝 Browser opened with display.html"
echo "💡 Press Ctrl+C to stop the server"

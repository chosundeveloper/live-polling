#!/bin/bash
# Deployment script with public URL support via LocalTunnel

# Kill any existing servers
lsof -ti:8080 | xargs kill -9 2>/dev/null
pkill -f "lt --port 8080" 2>/dev/null

# Get local IP
LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)

# Start HTTP server in background (bind to all interfaces)
python3 -m http.server 8080 --bind 0.0.0.0 > /dev/null 2>&1 &

# Wait for server to start
sleep 1

# Start LocalTunnel for public access
echo "🌐 Creating public URL with LocalTunnel..."
lt --port 8080 --subdomain live-polling-john > /tmp/localtunnel.log 2>&1 &
sleep 3

# Extract public URL
PUBLIC_URL=$(cat /tmp/localtunnel.log | grep "your url is:" | awk '{print $4}')

# Open browser with public URL
if [ -n "$PUBLIC_URL" ]; then
    open "${PUBLIC_URL}/display.html?question=1"
    echo "🚀 Server running!"
    echo "   Local: http://localhost:8080"
    echo "   Network: http://${LOCAL_IP}:8080"
    echo "   Public: ${PUBLIC_URL}"
    echo ""
    echo "📝 Browser opened with display.html"
    echo "📱 Scan QR code with phone to submit answers"
    echo "   (Works from anywhere - not just same WiFi!)"
    echo ""
    echo "💡 Press Ctrl+C to stop the server"
else
    echo "⚠️  LocalTunnel failed, opening local URL"
    open "http://${LOCAL_IP}:8080/display.html?question=1"
    echo "🚀 Server running at:"
    echo "   Local: http://localhost:8080"
    echo "   Network: http://${LOCAL_IP}:8080"
    echo "📝 Browser opened with display.html"
    echo "📱 Scan QR code with phone (same WiFi only)"
fi

#!/bin/bash

# DreamForge AI - Server Startup Script
echo "🚀 Starting DreamForge AI Servers..."

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port $1 is already in use"
        return 1
    else
        return 0
    fi
}

# Check if ports are available
echo "🔍 Checking ports..."
if ! check_port 8000; then
    echo "❌ Backend port 8000 is busy. Stop existing backend first."
    exit 1
fi

if ! check_port 3000; then
    echo "❌ Frontend port 3000 is busy. Stop existing frontend first."
    exit 1
fi

echo "✅ Ports are available"

# Start backend in background
echo "🔧 Starting Backend (FastAPI)..."
cd backend
source venv/bin/activate
cd app
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
cd ../..

# Wait a moment for backend to start
sleep 3

# Start frontend in background
echo "🎨 Starting Frontend (Next.js)..."
cd fronted
npm run dev &
FRONTEND_PID=$!
cd ..

# Wait for servers to start
echo "⏳ Waiting for servers to start..."
sleep 5

# Check if servers are running
echo "🔍 Checking server status..."

# Check backend
if curl -s http://localhost:8000/ > /dev/null; then
    echo "✅ Backend is running at http://localhost:8000"
else
    echo "❌ Backend failed to start"
fi

# Check frontend (this might take longer)
sleep 3
if curl -s http://localhost:3000/ > /dev/null; then
    echo "✅ Frontend is running at http://localhost:3000"
else
    echo "⏳ Frontend is starting... (may take a few more seconds)"
fi

echo ""
echo "🎉 DreamForge AI is starting up!"
echo "📋 Access your application:"
echo "   • Frontend UI: http://localhost:3000"
echo "   • Backend API: http://localhost:8000"
echo "   • API Docs: http://localhost:8000/docs"
echo ""
echo "💡 To stop the servers:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo "   or press Ctrl+C in each terminal"
echo ""
echo "📊 Process IDs:"
echo "   Backend PID: $BACKEND_PID"
echo "   Frontend PID: $FRONTEND_PID"

# Keep script running
wait

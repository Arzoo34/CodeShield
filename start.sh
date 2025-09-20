#!/bin/bash

echo "🚀 Starting CodeShield..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Build and start services
echo "📦 Building and starting services..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo "✅ CodeShield is running!"
    echo "🌐 Frontend: http://localhost:3000"
    echo "🔧 Backend: http://localhost:5000"
    echo "📊 API Health: http://localhost:5000/api/health"
    echo ""
    echo "To stop: docker-compose down"
else
    echo "❌ Failed to start services. Check logs with: docker-compose logs"
    exit 1
fi

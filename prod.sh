#!/bin/bash

# Production environment with Gunicorn
# This is the standard production setup

echo "🏭 Starting Tour System in PRODUCTION mode..."
echo ""

# Stop any running containers
docker-compose down

# Start services with production settings
docker-compose up -d

echo "✅ Production environment started!"
echo "View logs: docker-compose logs -f"

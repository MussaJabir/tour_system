#!/bin/bash

# Development environment with auto-reload
# This script runs Docker Compose in development mode with Django's runserver
# which automatically reloads when you make code changes

echo "🚀 Starting Tour System in DEVELOPMENT mode with auto-reload..."
echo ""

# Stop any running containers
docker-compose down

# Start services using both compose files
# Base file (docker-compose.yml) + Dev overrides (docker-compose.dev.yml)
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# To run in background, use:
# docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d


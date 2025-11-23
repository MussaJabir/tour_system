#!/bin/bash

# Manual Backup Script for Tour System Database
# Usage: ./backup.sh [backup_name]

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
# Sanitize backup name: replace spaces with underscores, remove special chars
BACKUP_NAME=$(echo "${1:-manual_backup_${TIMESTAMP}}" | tr ' ' '_' | tr -cd '[:alnum:]_-')
BACKUP_FILE="${BACKUP_DIR}/${BACKUP_NAME}.sql"
COMPRESSED_FILE="${BACKUP_FILE}.gz"

echo -e "${YELLOW}🔄 Starting database backup...${NC}"

# Create backup directory if it doesn't exist
mkdir -p ${BACKUP_DIR}

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo -e "${RED}❌ Error: .env file not found${NC}"
    exit 1
fi

# Check if postgres container is running
if ! docker-compose ps postgres | grep -q "Up"; then
    echo -e "${RED}❌ Error: PostgreSQL container is not running${NC}"
    echo "Start it with: docker-compose up -d postgres"
    exit 1
fi

echo "📦 Creating backup: ${BACKUP_NAME}.sql.gz"
echo "📍 Database: ${DB_NAME:-tour_system}"

# Create backup using pg_dump
docker-compose exec -T postgres pg_dump \
    -U ${DB_USER:-tour_admin} \
    -d ${DB_NAME:-tour_system} \
    --clean \
    --if-exists \
    --verbose \
    > "${BACKUP_FILE}" 2>/dev/null

# Check if backup was successful
if [ $? -eq 0 ] && [ -s "${BACKUP_FILE}" ]; then
    # Compress the backup
    gzip "${BACKUP_FILE}"
    
    # Get file size
    SIZE=$(du -h "${COMPRESSED_FILE}" | cut -f1)
    
    echo -e "${GREEN}✅ Backup completed successfully!${NC}"
    echo "📁 File: ${COMPRESSED_FILE}"
    echo "💾 Size: ${SIZE}"
    echo "🕐 Time: $(date)"
    
    # List recent backups
    echo ""
    echo "📋 Recent backups:"
    ls -lh ${BACKUP_DIR}/*.sql.gz 2>/dev/null | tail -5 || echo "No previous backups found"
else
    echo -e "${RED}❌ Backup failed!${NC}"
    rm -f "${BACKUP_FILE}"
    exit 1
fi


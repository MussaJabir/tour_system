#!/bin/bash

# Restore Script for Tour System Database
# Usage: ./restore.sh <backup_file.sql.gz>

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

BACKUP_FILE=$1

# Check if backup file is provided
if [ -z "$BACKUP_FILE" ]; then
    echo -e "${RED}❌ Error: No backup file specified${NC}"
    echo ""
    echo "Usage: ./restore.sh <backup_file.sql.gz>"
    echo ""
    echo "Available backups:"
    ls -lh ./backups/*.sql.gz 2>/dev/null || echo "No backups found"
    exit 1
fi

# Check if file exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo -e "${RED}❌ Error: Backup file not found: ${BACKUP_FILE}${NC}"
    exit 1
fi

echo -e "${YELLOW}⚠️  WARNING: This will REPLACE your current database!${NC}"
echo "Backup file: ${BACKUP_FILE}"
echo ""
read -p "Are you sure you want to continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "❌ Restore cancelled"
    exit 0
fi

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

echo -e "${YELLOW}🔄 Starting database restore...${NC}"

# Create a safety backup first
echo "📦 Creating safety backup before restore..."
SAFETY_BACKUP="./backups/pre_restore_$(date +%Y%m%d_%H%M%S).sql.gz"
docker-compose exec -T postgres pg_dump \
    -U ${DB_USER:-tour_admin} \
    -d ${DB_NAME:-tour_system} \
    | gzip > ${SAFETY_BACKUP}
echo "✅ Safety backup created: ${SAFETY_BACKUP}"

# Decompress if needed
TEMP_SQL="/tmp/restore_temp.sql"
if [[ $BACKUP_FILE == *.gz ]]; then
    echo "📂 Decompressing backup..."
    gunzip -c ${BACKUP_FILE} > ${TEMP_SQL}
else
    cp ${BACKUP_FILE} ${TEMP_SQL}
fi

# Restore database
echo "🔄 Restoring database..."
cat ${TEMP_SQL} | docker-compose exec -T postgres psql \
    -U ${DB_USER:-tour_admin} \
    -d ${DB_NAME:-tour_system} \
    --quiet

# Clean up
rm -f ${TEMP_SQL}

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Database restored successfully!${NC}"
    echo "🕐 Time: $(date)"
    echo ""
    echo "⚠️  Remember to restart your application:"
    echo "   docker-compose restart django"
else
    echo -e "${RED}❌ Restore failed!${NC}"
    echo "🔄 You can restore from safety backup:"
    echo "   ./restore.sh ${SAFETY_BACKUP}"
    exit 1
fi


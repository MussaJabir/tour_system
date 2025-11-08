# 🐳 Docker Setup Guide

## Overview

This project uses Docker Compose to orchestrate multiple services for the tour management system.

## Services Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Nginx (Port 80)                     │
│                    (Reverse Proxy + Static)                 │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   Django (Gunicorn)                         │
│                     (Port 8000)                             │
└──────┬──────────────────────────────────┬───────────────────┘
       │                                  │
       ▼                                  ▼
┌──────────────┐                  ┌──────────────┐
│  PostgreSQL  │                  │    Redis     │
│  (Port 5432) │                  │  (Port 6379) │
└──────────────┘                  └──────┬───────┘
                                         │
                                         ▼
                              ┌──────────────────┐
                              │  Celery Worker   │
                              │  + Celery Beat   │
                              └──────────────────┘
```

## Service Details

### 1. PostgreSQL Database
- **Image**: postgres:16-alpine
- **Port**: 5432
- **Purpose**: Main application database
- **Volume**: `postgres_data` for data persistence
- **Health Check**: Ensures database is ready before Django starts

### 2. Redis Cache
- **Image**: redis:7-alpine
- **Port**: 6379
- **Purpose**: 
  - Application caching
  - Session storage
  - Celery message broker
- **Volume**: `redis_data` for persistence
- **Configuration**: AOF (Append Only File) enabled

### 3. Django Application
- **Build**: Custom Dockerfile
- **Port**: 8000
- **Purpose**: Main web application
- **Workers**: 4 Gunicorn workers, 2 threads each
- **Volumes**:
  - Source code (development)
  - Static files
  - Media files
- **Dependencies**: Waits for PostgreSQL and Redis

### 4. Celery Worker
- **Build**: Same as Django
- **Purpose**: Background task processing
  - AI itinerary generation
  - PDF parsing
  - Email sending
  - Data processing
- **Concurrency**: 2 concurrent tasks
- **Monitoring**: Logs available via docker-compose logs

### 5. Celery Beat
- **Build**: Same as Django
- **Purpose**: Scheduled task execution
  - Periodic cache cleanup
  - Scheduled reports
  - Data synchronization
- **Schedule**: Defined in Django settings

### 6. Nginx Reverse Proxy
- **Image**: nginx:alpine
- **Port**: 80 (HTTP)
- **Purpose**:
  - Reverse proxy to Django
  - Serve static files
  - Serve media files
  - Gzip compression
  - Caching headers
- **Configuration**: `docker/nginx.conf`

## Volume Management

### Persistent Volumes

```yaml
postgres_data:    # Database data
redis_data:       # Redis persistence
static_volume:    # Collected static files
media_volume:     # User uploaded files
```

### Volume Operations

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect tour_system_postgres_data

# Remove specific volume (⚠️ Data loss!)
docker volume rm tour_system_postgres_data

# Remove all unused volumes
docker volume prune
```

## Environment Configuration

The application reads configuration from `.env` file. Key variables:

### Database
```env
DB_NAME=tour_system_db
DB_USER=tour_admin
DB_PASSWORD=your_secure_password
DB_HOST=postgres
DB_PORT=5432
```

### Redis
```env
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
```

### Django
```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### OpenAI
```env
OPENAI_API_KEY=sk-your-api-key
```

## Common Operations

### Initial Setup

```bash
# Clone and enter directory
git clone <repo-url>
cd tour_system

# Create environment file
cp .env.example .env
# Edit .env with your values

# Build and start
docker-compose up -d --build

# Create superuser
docker-compose exec django python manage.py createsuperuser
```

### Daily Operations

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart specific service
docker-compose restart django

# View logs (all services)
docker-compose logs -f

# View logs (specific service)
docker-compose logs -f django

# Check service status
docker-compose ps

# Execute Django command
docker-compose exec django python manage.py <command>
```

### Development

```bash
# Rebuild after code changes
docker-compose up -d --build django

# Run migrations
docker-compose exec django python manage.py migrate

# Collect static files
docker-compose exec django python manage.py collectstatic --noinput

# Access Django shell
docker-compose exec django python manage.py shell

# Access database
docker-compose exec postgres psql -U tour_admin -d tour_system_db

# Access Redis CLI
docker-compose exec redis redis-cli
```

### Debugging

```bash
# View container resource usage
docker stats

# Inspect container
docker inspect tour_django

# Access container shell
docker-compose exec django bash

# Check Django logs
docker-compose logs -f django

# Check Celery logs
docker-compose logs -f celery

# Check Nginx logs
docker-compose logs -f nginx
```

### Database Operations

```bash
# Backup database
docker-compose exec postgres pg_dump -U tour_admin tour_system_db > backup_$(date +%Y%m%d).sql

# Restore database
docker-compose exec -T postgres psql -U tour_admin tour_system_db < backup_20240101.sql

# Access database shell
docker-compose exec postgres psql -U tour_admin -d tour_system_db

# Run SQL file
docker-compose exec -T postgres psql -U tour_admin -d tour_system_db < script.sql
```

### Cleanup

```bash
# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes (⚠️ Data loss!)
docker-compose down -v

# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune

# Full cleanup (⚠️ Removes everything!)
docker system prune -a --volumes
```

## Production Deployment

### Pre-deployment Checklist

- [ ] Update `.env` with production values
- [ ] Set `DEBUG=False`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Set strong `SECRET_KEY`
- [ ] Configure SSL/TLS certificates
- [ ] Update Nginx config for HTTPS
- [ ] Set up backup strategy
- [ ] Configure monitoring
- [ ] Test all services

### Production Commands

```bash
# Build for production
docker-compose -f docker-compose.prod.yml up -d --build

# Scale workers
docker-compose up -d --scale celery=4

# View resource usage
docker stats

# Monitor logs
docker-compose logs -f --tail=100
```

## Troubleshooting

### Service Won't Start

```bash
# Check logs
docker-compose logs [service_name]

# Check if port is in use
sudo lsof -i :80
sudo lsof -i :8000
sudo lsof -i :5432

# Rebuild service
docker-compose up -d --build [service_name]
```

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check PostgreSQL logs
docker-compose logs postgres

# Verify credentials in .env

# Test connection
docker-compose exec postgres psql -U tour_admin -d tour_system_db -c "SELECT 1;"
```

### Static Files Not Serving

```bash
# Collect static files
docker-compose exec django python manage.py collectstatic --noinput

# Check Nginx config
docker-compose exec nginx nginx -t

# Restart Nginx
docker-compose restart nginx
```

### Celery Not Processing Tasks

```bash
# Check Celery logs
docker-compose logs celery

# Check Redis connection
docker-compose exec redis redis-cli ping

# Restart Celery
docker-compose restart celery celery-beat
```

## Performance Tuning

### Gunicorn Workers

Adjust in `docker/entrypoint.sh`:
```bash
--workers 4          # (2 x CPU cores) + 1
--threads 2          # For I/O bound operations
--timeout 60         # Request timeout
```

### Celery Concurrency

Adjust in `docker-compose.yml`:
```yaml
command: celery -A config worker --loglevel=info --concurrency=4
```

### PostgreSQL

Add to `docker-compose.yml`:
```yaml
environment:
  - POSTGRES_MAX_CONNECTIONS=100
  - POSTGRES_SHARED_BUFFERS=256MB
```

### Redis

Adjust in `docker-compose.yml`:
```yaml
command: redis-server --appendonly yes --maxmemory 512mb --maxmemory-policy allkeys-lru
```

## Security Considerations

1. **Never commit `.env` file** - Contains sensitive credentials
2. **Use strong passwords** - Especially for database
3. **Keep images updated** - Regular security updates
4. **Limit container privileges** - Don't run as root
5. **Use secrets management** - For production deployments
6. **Enable HTTPS** - Configure SSL/TLS in Nginx
7. **Regular backups** - Automated database backups
8. **Monitor logs** - Watch for suspicious activity

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [PostgreSQL Docker](https://hub.docker.com/_/postgres)
- [Redis Docker](https://hub.docker.com/_/redis)
- [Nginx Docker](https://hub.docker.com/_/nginx)


# 🌍 Tour Management System

A comprehensive tour management system built with Django, featuring a public website, custom admin dashboard, REST API, and AI-powered assistance for tour planning and management.

## 🚀 Features

### Public Website (Frontend)
- Browse tour packages and destinations
- View accommodations and activities
- Read customer reviews
- Dynamic content management (banners, featured packages)
- Responsive design using modern HTML templates

### Custom Admin Dashboard (Backend)
- Manage destinations with coordinates
- Add/edit accommodations (manual or AI-assisted PDF parsing)
- Create and manage tour packages
- Handle activities and moderate reviews
- AI assistant for:
  - Drafting safari itineraries
  - Parsing accommodation PDFs
  - Optimizing routes based on coordinates
  - Future: Customer inquiry management

### REST API
- Full REST API endpoints for Flutter mobile app
- Token-based authentication
- Paginated responses
- Rate limiting and throttling

## 🏗️ Tech Stack

- **Backend**: Django 5.2.8
- **Database**: PostgreSQL 16
- **Caching**: Redis 7
- **Task Queue**: Celery
- **Web Server**: Gunicorn + Nginx
- **API**: Django REST Framework
- **AI Integration**: OpenAI API
- **Containerization**: Docker & Docker Compose

## 📋 Prerequisites

- Docker & Docker Compose
- Git

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd tour_system
```

### 2. Create Environment File

Copy the example environment file and update with your credentials:

```bash
cp .env.example .env
```

Edit `.env` and update the following:
- `SECRET_KEY` - Generate a new Django secret key
- `DB_PASSWORD` - Set a secure database password
- `OPENAI_API_KEY` - Add your OpenAI API key
- Other configuration as needed

### 3. Build and Run with Docker

```bash
# Build and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Check service status
docker-compose ps
```

### 4. Access the Application

- **Public Website**: http://localhost
- **Admin Dashboard**: http://localhost/admin
- **API**: http://localhost/api
- **Django Admin**: http://localhost/admin (default Django admin)

### 5. Create Superuser

```bash
docker-compose exec django python manage.py createsuperuser
```

## 🐳 Docker Services

The application runs with the following services:

- **postgres**: PostgreSQL database
- **redis**: Redis for caching and Celery broker
- **django**: Main Django application (Gunicorn)
- **celery**: Celery worker for background tasks
- **celery-beat**: Celery beat for scheduled tasks
- **nginx**: Reverse proxy and static file serving

## 📦 Project Structure

```
tour_system/
├── accommodations/      # Accommodation management app
├── activities/          # Activities management app
├── ai_assistant/        # AI-powered features
├── api/                 # REST API endpoints
├── config/              # Django settings and configuration
├── core/                # Core/CMS functionality
├── destinations/        # Destination management app
├── docker/              # Docker configuration files
│   ├── entrypoint.sh
│   └── nginx.conf
├── packages/            # Tour package management app
├── reviews/             # Review management app
├── static/              # Static files (CSS, JS, images)
│   ├── frontend/        # Public website assets
│   └── backend/         # Admin dashboard assets
├── templates/           # HTML templates
│   ├── frontend/        # Public website templates
│   └── backend/         # Admin dashboard templates
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## 🔄 Development Workflow

### Branch Strategy

- `main` - Production-ready code
- `impl-destinations` - Destination implementation
- `impl-accommodations` - Accommodation implementation
- `impl-packages` - Tour packages implementation
- `impl-activities` - Activities implementation
- `impl-reviews` - Reviews implementation
- `impl-ai-assistant` - AI assistant implementation
- `impl-api` - REST API implementation
- `impl-core-cms` - CMS functionality

### Making Changes

1. Create/checkout feature branch
2. Make your changes
3. Test locally with Docker
4. Commit with clear messages
5. Push to GitHub
6. Create Pull Request to main

## 🛠️ Useful Commands

### Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart a service
docker-compose restart django

# View logs
docker-compose logs -f [service_name]

# Execute command in container
docker-compose exec django python manage.py [command]

# Rebuild services
docker-compose up -d --build
```

### Django Commands

```bash
# Run migrations
docker-compose exec django python manage.py migrate

# Create migrations
docker-compose exec django python manage.py makemigrations

# Collect static files
docker-compose exec django python manage.py collectstatic

# Create superuser
docker-compose exec django python manage.py createsuperuser

# Django shell
docker-compose exec django python manage.py shell
```

### Database Commands

```bash
# Access PostgreSQL
docker-compose exec postgres psql -U tour_admin -d tour_system_db

# Backup database
docker-compose exec postgres pg_dump -U tour_admin tour_system_db > backup.sql

# Restore database
docker-compose exec -T postgres psql -U tour_admin tour_system_db < backup.sql
```

## ⚡ Performance Optimizations

- **Database Connection Pooling**: Persistent connections for better performance
- **Redis Caching**: Caches frequently accessed data
- **Celery Background Tasks**: Async processing for AI and heavy operations
- **Nginx Static Files**: Efficient static file serving with caching
- **Gunicorn Workers**: Multiple workers for concurrent request handling
- **API Pagination**: Paginated responses for large datasets
- **Rate Limiting**: API throttling to prevent abuse

## 🔒 Security

- Environment variables for sensitive data
- HTTPS enforcement in production
- CSRF protection
- Secure session cookies
- XSS protection headers
- Database connection encryption
- Rate limiting on API endpoints

## 📝 License

Proprietary - All rights reserved

## 👥 Contributors

- Tour System Development Team

## 📧 Support

For support and questions, please contact the development team.


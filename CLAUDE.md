# Tour System — Claude Code Instructions

## Project Overview
Django-based tour management SaaS for a Tanzanian tourism operator.
Dual interface: public-facing website + internal staff dashboard + REST API for a Flutter mobile app.

## Tech Stack
- **Backend**: Django 5.2.8 + Django REST Framework
- **Database**: PostgreSQL 16 (via Docker, port 5433)
- **Cache / Broker**: Redis 7
- **Task Queue**: Celery + Celery Beat
- **Web Server**: Gunicorn behind Nginx
- **AI**: OpenAI API
- **Containerization**: Docker Compose

## Project Structure

```
config/          Django settings, URLs, Celery config
core/            Abstract base models, contact forms, newsletter, FAQ, testimonials, dashboard home
destinations/    Destination CRUD, API, public pages
accommodations/  Hotel/lodge CRUD, rooms, images, API, public pages
activities/      Activity CRUD, images, API, public pages
packages/        Tour packages, itinerary, inclusions, inquiry system, custom package builder, emails
reviews/         STUB — not implemented yet
ai_assistant/    STUB — not implemented yet
api/             Central API router (delegates to per-app api_urls.py)
templates/
  frontend/      Public website templates
  backend/       Staff dashboard templates
static/
  frontend/      Public site assets
  backend/       Dashboard assets
```

## Abstract Base Models (core/models.py)
All content models inherit from these — do not duplicate these fields:
- `TimeStampedModel` — `created_at`, `updated_at`
- `SEOMixin` — `meta_title`, `meta_description`, `meta_keywords`
- `PublishableMixin` — `is_active`, `is_featured`, `order`, `created_by`
- `SlugMixin` — `slug` (auto-generated from `name`)
- `ViewCountMixin` — `view_count` with `increment_view_count()`
- `BaseModel` — all of the above combined

## Django Conventions in This Project

### Views
- Dashboard views: function-based, decorated with `@login_required` + `@staff_member_required`
- Public views: function-based, no auth required
- API views: DRF ViewSets in `api_views.py`; write operations check `is_staff`

### URL layout per app
```
urls.py         Web routes (public + dashboard)
api_urls.py     REST API routes, registered in api/urls.py
```

### Templates
- Dashboard templates: `templates/backend/<app>/`
- Public templates: `templates/frontend/<app>/` or `<app>/templates/<app>/`

### Email
Email helpers live in `<app>/emails.py` (e.g., `packages/emails.py`).
Staff notification lists are pulled from `User.objects.filter(is_staff=True)`.
Console backend used in dev; SMTP in production via `.env`.

## Environment Variables
All config via `.env` using `python-decouple`. See `.env.example`.
Key vars: `SECRET_KEY`, `DB_*`, `REDIS_*`, `OPENAI_API_KEY`, `EMAIL_*`, `STAFF_NOTIFICATION_EMAILS`, `SITE_URL`.

## Running the Project

```bash
# Start all services
docker-compose up -d

# Run migrations
docker-compose exec django python manage.py migrate

# Create superuser
docker-compose exec django python manage.py createsuperuser

# Tail logs
docker-compose logs -f django

# Dev (without Docker)
source venv/bin/activate
python manage.py runserver
```

## Development Rules

### Before committing
1. `python manage.py test` — must pass
2. No bare `except: pass` blocks — log errors at minimum
3. All new dashboard views must have BOTH `@login_required` AND `@staff_member_required`
4. All new API write endpoints must check `request.user.is_staff`

### Adding a new app
1. Create with `python manage.py startapp <name>`
2. Add to `INSTALLED_APPS` in `config/settings.py`
3. Inherit from `BaseModel` (or individual mixins) — never re-implement timestamps/slugs/SEO
4. Add `api_urls.py` and register in `api/urls.py`
5. Add web `urls.py` and register in `config/urls.py`

### Adding a new model
- Use `BaseModel` as base for any content that has a public page
- Use `TimeStampedModel` for transactional/support models (contact messages, inquiries)
- Always add `db_index=True` on fields used in filters/queries
- Always define `__str__`, `Meta.verbose_name`, and `Meta.ordering`

## Known Issues / Technical Debt
- Dashboard views currently use `@login_required` only — must migrate to `@staff_member_required`
- No custom User model — extending later will require data migration
- DRF only has `SessionAuthentication` — `TokenAuthentication` needed for the Flutter mobile app
- `reviews` and `ai_assistant` apps are empty stubs installed in INSTALLED_APPS
- Duplicate email settings block in `config/settings.py` (lines ~110 and ~180) — remove second block
- Template directory has `index_new.html` and `index_old.html.bak` — clean up

## What's NOT Done Yet
- `reviews` app — customer reviews with ratings
- `ai_assistant` app — itinerary drafting, PDF parsing, route optimization
- Booking / reservation system (inquiry → confirmed booking flow)
- Payment integration
- Token auth for Flutter mobile app
- Login/logout views for the staff dashboard

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

## Frontend Design Systems

This project has **two parallel design systems** — one for the public marketing site, one for the internal staff dashboard. They share the Tailwind v4 build pipeline and one accent colour (`bush-600`) but are otherwise distinct.

### Safari Editorial — public site (Phase 6, complete)

- **Where**: any template that extends `templates/frontend/base_modern.html`
- **Feel**: cinematic, magazine-grade, editorial. Slow motion, generous whitespace.
- **Stack**: Tailwind v4 + Alpine.js + GSAP + ScrollTrigger + Lenis + variable fonts (Fraunces + Inter)
- **Palette**: warm earth tones — `sand` / `bush` / `clay` ramps + `ivory` / `bone` / `mist` / `charcoal` / `graphite`
- **Typography**: Fraunces (display, serif) for headings, Inter for body
- **Reference**: `/styleguide/` (DEBUG-only)
- **Rule**: every new public page extends `base_modern.html` and uses utilities defined in `static/frontend/src/tailwind.css`. Do NOT extend the deleted legacy `frontend/base.html`.

### Operations Slate — staff dashboard (Phase 7, planned)

- **Where**: any template that will extend `templates/backend/base_dashboard.html` (to be built in Phase 7.0)
- **Feel**: dense, fast, functional. Stripe-meets-Linear. Productivity tool, not a brochure.
- **Stack**: Tailwind v4 + Alpine.js + Chart.js + Font Awesome (no GSAP, no Lenis)
- **Palette**: cool neutrals — `slate-50` → `slate-900` for backgrounds/text + `bush-600` (carried from Safari Editorial) for primary actions + `emerald-500` / `amber-500` / `rose-500` / `sky-500` for semantic statuses
- **Typography**: **Inter only** — no Fraunces in the dashboard. Tighter scale (14px base body vs 16px on public).
- **Reference**: `/dashboard/styleguide/` (DEBUG-only, to be built in Phase 7.0)
- **Rules**:
  1. Every new dashboard page extends `base_dashboard.html` (NOT `base_modern.html`)
  2. No cinematic motion. Transitions are 150–250ms ease, no scroll-triggered reveals.
  3. Use the shared dashboard partials (`_dashboard_sidebar`, `_dashboard_topbar`, `_stat_card`, `_data_table`, `_status_badge`, `_page_header`, `_breadcrumb`, `_empty_state`).
  4. Status badges always use the semantic colour scale, not the brand accent.
  5. Inline edit / quick actions are preferred over modal flows where possible.

### Shared infrastructure

Both systems share one Tailwind build (`static/frontend/src/tailwind.css` → `static/frontend/css/tailwind.css`). Add new tokens inside the same `@theme` block; namespace dashboard-only utilities with the `dashboard-` prefix if a token only makes sense in one context.

**Build command** (run after editing `tailwind.css` or adding utilities to any template):

```bash
tailwindcss -i static/frontend/src/tailwind.css \
            -o static/frontend/css/tailwind.css \
            --minify
# Then bump the ?v= querystring on the link tag in both base templates
# and re-run `docker compose exec django python manage.py collectstatic --noinput --clear`
```

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

## Branch & PR Workflow

**IMPORTANT — Follow this for every implementation task without exception.**

```
main        ← production-ready, user merges here manually only
  └── develop   ← integration branch, all features PR here
        └── feature/<descriptive-name>   ← one branch per task
        └── fix/<descriptive-name>
```

### Rules
1. Never commit implementation work directly to `main` or `develop`
2. Always create a feature branch from `develop`:
   ```bash
   git checkout develop && git pull origin develop
   git checkout -b feature/<descriptive-name>
   ```
3. Branch naming:
   - `feature/staff-dashboard-auth-gate` — new feature or security fix
   - `feature/booking-reservation-system` — larger feature
   - `fix/duplicate-email-settings` — bug fix
   - `fix/bare-exception-handlers` — code quality fix
4. Before opening a PR to `develop`: run `python manage.py test` — all tests must pass
5. Open a PR from the feature branch → `develop` with a clear description
6. User manually reviews and merges `develop` → `main` when ready for production

### Claude's responsibility per task
- Create the branch
- Implement the change
- Write or update tests covering the change
- Confirm tests pass
- Push the branch and open a PR to `develop`
- Update `session.md` with what was done
- Mark the item in `todo.md` as `[x]` done

---

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

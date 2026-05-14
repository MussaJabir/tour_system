# Tour System — Session Log

Running record of every working session. Most recent at the top.

---

## Session 001 — 2026-05-14

**Type:** Audit + Setup
**Branch:** `main` (housekeeping only, no features)

### What we did
1. **Full codebase audit** — analysed all 8 apps, models, views, serializers, templates, Docker config, and settings
2. **Removed `.cursor/` from git tracking** — `git rm --cached .cursor/worktrees.json`, added `.cursor/` to `.gitignore`, deleted the directory locally
3. **Created `CLAUDE.md`** — full project context file: stack, structure, conventions, known issues, development rules
4. **Created `todo.md`** — prioritized product roadmap across 5 phases
5. **Created `session.md`** — this file; tracks all working sessions
6. **Established branch workflow** — all future work goes on feature branches → PR into `develop` → user manually merges `develop` → `main`
7. **Created `develop` branch** on GitHub
8. **Pushed everything to GitHub**

### Key findings from audit
- Dashboard views use `@login_required` only — **security hole**, any logged-in user can access staff dashboard
- No token auth — Flutter mobile app cannot work with current DRF `SessionAuthentication` only
- `reviews` and `ai_assistant` apps are empty stubs but installed in `INSTALLED_APPS`
- Duplicate email config block in `settings.py`
- No booking/reservation system — inquiry-to-booking loop is not closed
- No login/logout views for the dashboard
- `packages/views.py` has bare `pass` exception handlers

### Decisions made
- Branch strategy: `feature/<name>` or `fix/<name>` → `develop` → `main`
- Tests must pass on the feature branch before PRing into `develop`
- User manually PRs `develop` → `main`
- All future sessions logged here with branch name and what was done

---

## Session 002 — 2026-05-14

**Type:** Phase 1 — Security & Stability
**Branch:** `feature/phase-1-security-and-stability` → PR #2 → `develop`

### What we did
1. **Fixed Docker installation** — removed conflicting Docker Desktop + Docker CE, clean reinstall of Docker CE, fixed leftover `docker-credential-desktop` in `~/.docker/config.json`
2. **Fixed Docker port conflicts** — changed postgres host port `5433→5434` (ghost socket), nginx `80→8080` (Apache2 on port 80)
3. **Brought the system up** — all 6 containers running: postgres, redis, django, celery, celery-beat, nginx
4. **Staff auth gate** — added `@staff_member_required` to all dashboard views in `core`, `destinations`, `accommodations`, `activities`, `packages`
5. **Login/logout views** — `staff_login` and `staff_logout` added to `core/views.py`, wired to `/dashboard/login/` and `/dashboard/logout/`
6. **Settings `LOGIN_URL`** — set to `/dashboard/login/` so `@login_required` redirects correctly
7. **Removed duplicate email config** — second `EMAIL_*` block removed from `settings.py`
8. **Fixed exception handlers** — replaced 4 bare `pass` blocks in `packages/views.py` with `logger.warning`
9. **Template cleanup** — deleted `index_new.html` and `index_old.html.bak`
10. **Tests** — 10/10 tests passing; PR opened to `develop`

### PR
- https://github.com/MussaJabir/tour_system/pull/2

---

## Session 003 — 2026-05-14

**Type:** Phase 2 — Booking & Payment System
**Branch:** `feature/phase-2-booking-and-payments` → PR #3 → `develop`

### What we did
1. **Booking model** — `Booking` with auto-generated `BKG-YYYYMMDD-NNNNN` reference, 7-state status workflow, balance tracking (`total_paid`, `balance_due`, `is_fully_paid`), email hooks
2. **Passenger model** — per-booking passenger records: name, passport, DOB, dietary/medical notes, emergency contact, lead passenger flag
3. **Payment model** — 5 payment types, 6 methods, status tracking; auto-advances booking status on deposit/full payment
4. **Email notifications** — `booking_emails.py`: `send_booking_confirmation`, `send_booking_status_update`, `send_payment_received`; sends to customer + all staff
5. **10 dashboard views** — booking list/create/edit/cancel, passenger add/edit/delete, payment record/delete; all behind `@staff_member_required`
6. **5 booking dashboard templates** — list, detail (with inline passenger/payment panels), form, cancel confirm, passenger edit
7. **Django admin** — `BookingAdmin` with `PassengerInline` + `PaymentInline`; `PassengerAdmin`; `PaymentAdmin` with status badges
8. **Migration 0005** — applied cleanly
9. **25 tests** — 25/25 passing: model reference generation, paid/balance logic, view auth gates, passenger/payment CRUD flows

### PR
- https://github.com/MussaJabir/tour_system/pull/3

---

## Session 004 — 2026-05-14

**Type:** Phase 3 — Custom User Model & Token Authentication
**Branch:** `feature/phase-3-token-auth-and-user-model` → PR #5 → `develop`

### What we did
1. **Custom User model** — created `accounts` app with `CustomUser(AbstractUser)`: adds `phone`, `profile_photo`, `preferred_currency`, `nationality`; set `AUTH_USER_MODEL = 'accounts.CustomUser'`
2. **DB wipe and rebuild** — dropped `tour_system` PostgreSQL database, deleted all migration files, ran fresh `makemigrations` (all apps now have a single `0001_initial` referencing `accounts.CustomUser`), applied migrations to new DB
3. **Token authentication** — `rest_framework.authtoken` + `TokenAuthentication` added to DRF config alongside session auth; Flutter app can now authenticate with `Authorization: Token <key>` header
4. **Auth API endpoints** — 5 endpoints at `/api/v1/auth/*`:
   - `POST /auth/register/` — customer self-registration → creates user + returns token
   - `POST /auth/login/` — credentials → token + user profile
   - `POST /auth/logout/` — deletes token
   - `GET/PATCH /auth/profile/` — read and update own profile
   - `POST /auth/change-password/` — rotates token on success
5. **CustomUserAdmin** — extends Django's UserAdmin with profile fieldset
6. **Bug fix** — `destinations/models.py` was using `from django.contrib.auth.models import User` directly (hardcoded); replaced with `get_user_model()`; same fix applied to test imports in `core/tests.py` and `packages/tests.py`
7. **Superuser recreated** — `admin` / `mussajabir937@gmail.com` / `admin1234`
8. **51 tests passing** (16 new accounts tests + 35 existing)

### PR
- https://github.com/MussaJabir/tour_system/pull/5

---

## Session 005 — 2026-05-14

**Type:** Phase 4 — Reviews App
**Branch:** `feature/phase-4-reviews-app` → PR #6 → `develop`

### What we did
1. **Review model** — `Review` (Package + User + Booking, 1–5 stars, title/body, status workflow: pending/approved/rejected, featured flag) and `ReviewPhoto` (multiple photos per review)
2. **Moderation workflow** — `approve()` calls `Package.update_rating()` to recalculate `rating_average` and `review_count`; `reject()` records reason; both trigger on approve/reject bulk admin actions
3. **Staff dashboard views** — list with status filter tabs + counts; detail with reviewer info and booking link; approve/reject/delete confirm flows; all behind `@staff_member_required`
4. **Public views** — review list with rating breakdown sidebar, star/sort filters, pagination; review submit form with completed-booking eligibility check
5. **JSON-LD schema markup** — `AggregateRating` structured data for Google rich snippets on the review list page
6. **REST API** — `GET /api/v1/packages/<slug>/reviews/` (approved only, public); `POST /api/v1/reviews/` (authenticated, creates as pending)
7. **Django admin** — `ReviewAdmin` with approve/reject/feature bulk actions, `ReviewPhotoInline`; `ReviewPhotoAdmin`
8. **19 new tests** — model (approve, reject, rating update), dashboard views (auth gates, CRUD flows), public views, API endpoints
9. **70/70 total tests passing**

### PR
- https://github.com/MussaJabir/tour_system/pull/6

---

## Session 006 — 2026-05-14

**Type:** Phase 4 Part 2 — AI Assistant App
**Branch:** `feature/phase-4-ai-assistant` → PR #7 → `develop`

### What we did
1. **AIConfiguration singleton model** — admin-configurable AI vendor/key: vendor (OpenAI/Anthropic), `api_key` (encrypted at rest via custom `EncryptedCharField` using Fernet + SECRET_KEY derivation), model_name, max_tokens, temperature, is_active; enforced as singleton (pk=1 always); admin blocks add when one exists, blocks delete
2. **Custom encrypted field** (`ai_assistant/fields.py`) — `EncryptedCharField(TextField)` using `cryptography.fernet` derived from `SECRET_KEY`; transparent encrypt on write, decrypt on read; no external key management needed; works with Django 5.2 (both `django-fernet-fields` and `django-cryptography` had Django 5.x incompatibilities)
3. **BaseAIJob abstract model** — `status` (pending/processing/done/failed), `error_message`, `started_at`, `completed_at`, `created_by`; `mark_processing()`, `mark_done()`, `mark_failed()`, `is_running` property
4. **4 job models** — `BrochureParseJob` (pdf_file + target_accommodation + extracted_data JSON), `ItineraryGenerationJob` (destination FK + duration/budget/group_size/interests + raw_output), `QuoteSuggestionJob` (inquiry FK + suggestions JSON), `RouteOptimizationJob` (destination_names text + optimized_route JSON)
5. **AI client** (`ai_assistant/ai_client.py`) — `get_ai_response(prompt, system_prompt)` reads from DB config first, falls back to `settings.OPENAI_API_KEY`; dispatches to `_call_openai()` or `_call_anthropic()` based on vendor; raises `AIServiceError` on failure
6. **4 Celery tasks** (`ai_assistant/tasks.py`) — `parse_brochure_task`, `generate_itinerary_task`, `build_custom_quote_task`, `optimize_route_task`; all async `@shared_task(bind=True, max_retries=2)`; PDF text extracted via `pdfplumber` → `PyPDF2` fallback; AI JSON responses stripped of markdown code fences before `json.loads`
7. **7 dashboard views** — `dashboard_ai_home`, `brochure_upload/result`, `itinerary_generate/result`, `quote_from_inquiry/result`, `route_optimize/result`; all behind `@staff_member_required`; result pages auto-refresh every 4s via `<meta http-equiv="refresh">` while job is running
8. **7 templates** — home hub (config status + 4 feature cards), brochure upload form + result with extracted fields preview, itinerary form + result with copy button, quote result with match-score cards, route form + result with ordered table
9. **Django admin** — `AIConfigurationAdmin` (blocks add if config exists, blocks delete), plus admin classes for all 4 job types with status badges and readonly result fields
10. **Dependencies** — added `anthropic>=0.40.0` to requirements.txt; `cryptography` already present
11. **25 new tests** — singleton enforcement, `get_active` logic, job lifecycle (mark_processing/done/failed, is_running), all 4 task functions mocked, view auth gates, form POST → job creation, result page access; **95/95 total tests passing**

### PR
- https://github.com/MussaJabir/tour_system/pull/7

---

## Session 007 — 2026-05-14

**Type:** Phase 2 — Availability Calendar
**Branch:** `feature/phase-2-availability-calendar` → PR #8 → `develop`

### What we did
1. **Departure model** — `Departure` (package FK, departure_date, max_seats, booked_seats, status: available/sold_out/cancelled); `unique_together` on (package, departure_date); `lock_seat()` auto-sets sold_out when full; `release_seat()` restores available; `seats_remaining` and `is_available` properties
2. **Booking seat locking** — added `departure` FK (nullable) to `Booking`; `Booking.save()` calls `departure.lock_seat()` on first creation; `Booking.cancel()` helper sets status=cancelled and calls `departure.release_seat()`
3. **Cancel view updated** — `dashboard_booking_cancel` now calls `booking.cancel()` instead of raw field set, ensuring seat release is always triggered
4. **Staff dashboard** — 4 views (list / create / edit / delete) per package; delete blocked if departure has booked_seats > 0; all behind `@staff_member_required`
5. **Public detail** — upcoming available departures shown in the booking card with date and seats remaining
6. **DepartureForm** — with past-date validation on create
7. **Templates** — 3 new dashboard templates (list, form, delete_confirm); booking card section updated on public detail
8. **Departures link** — added "Manage Departures" card to the package edit dashboard template
9. **API** — `DepartureSerializer` + read-only `DepartureViewSet` (filters by package slug/id; future+available by default; staff can pass `?all=1`); `PackageDetailSerializer` includes `upcoming_departures`
10. **Admin** — `DepartureInline` on `PackageAdmin`; standalone `DepartureAdmin` with remaining seats display
11. **20 new tests** — model lifecycle, seat locking via booking, cancel release, view auth gates, CRUD flows; **115/115 total tests passing**

### PR
- https://github.com/MussaJabir/tour_system/pull/8

---

## Session 008 — 2026-05-14

**Type:** Phase 3 — Customer-facing API (Flutter)
**Branch:** `feature/phase-3-customer-api` → PR #9 → `develop`

### What we did
1. **SavedPackage model** — `user + package` unique wishlist; `TimeStampedModel`; migration 0003
2. **6 customer API endpoints** under `/api/v1/customer/` — all require token auth, data scoped to `request.user`:
   - `GET /customer/bookings/` — own booking list matched by `inquiry__customer_email`
   - `GET /customer/bookings/{reference}/` — full detail with passengers + payment history
   - `GET /customer/inquiries/` — own inquiry history matched by `customer_email`
   - `GET /customer/inquiries/{reference}/` — detail; includes secure quote URL if staff sent a custom package
   - `GET /customer/saved-packages/` — wishlist with full package data
   - `POST /DELETE /customer/packages/{slug}/save/` — save/unsave (POST is idempotent)
3. **Serializers** (`packages/customer_serializers.py`) — dedicated serializers for all customer views; no passport/internal data exposed
4. **Admin** — `SavedPackageAdmin` registered
5. **15 new tests** — auth enforcement, own-data isolation, 404 on cross-user access, idempotent save, unsave, saved list; **130/130 total tests passing**

### PR
- https://github.com/MussaJabir/tour_system/pull/9

---

## Session 009 — 2026-05-14

**Type:** Phase 5 — SEO Meta Tags & Sitemap
**Branch:** `feature/phase-5-seo-sitemap` → PR #10 → `develop`

### What we did
1. **Base template SEO blocks** (`templates/frontend/base.html`) — added `{% block canonical %}`, `{% block og_type %}`, `{% block og_title %}`, `{% block og_description %}`, `{% block og_image %}`, `{% block og_url %}` after the existing meta keywords block; defaults to sensible fallbacks
2. **Package detail template** — wired all 6 SEO blocks using `package.get_meta_title()`, `package.get_meta_description()`, `package.meta_keywords`; og:image inside the block with `{% if %}` (not wrapping the block)
3. **Destination detail template** — same SEO blocks wired to `destination.*`
4. **Activity detail template** — same SEO blocks wired to `activity.*`
5. **Accommodation detail template** — same SEO blocks wired to `accommodation.*`
6. **Bug fix** — fixed `{% if obj.image %}{% block og_image %}...{% endblock %}{% endif %}` anti-pattern in all four templates; Django evaluates block tags before if conditions so the if must go inside the block
7. **Model helpers** — added `get_meta_title()` and `get_meta_description()` to `Destination`, `Activity`, and `Accommodation` (they pre-dated `SEOMixin` and had the fields inline but not the fallback methods)
8. **Sitemap** (`core/sitemaps.py`) — `PackageSitemap` (priority 0.9, weekly), `DestinationSitemap` (0.8, monthly), `ActivitySitemap` (0.7, monthly), `AccommodationSitemap` (0.6, monthly), `StaticSitemap` (0.5, weekly for home/list pages); registered at `/sitemap.xml` in `config/urls.py`
9. **`django.contrib.sitemaps` added** to `INSTALLED_APPS` in `config/settings.py`
10. **13 new tests** (`core/tests_sitemaps.py`) — sitemap 200 status, XML validity, slug presence for all 4 content types in sitemap, meta title on all 4 detail page types; **128/128 total tests passing**

### PR
- https://github.com/MussaJabir/tour_system/pull/10

---

_Add new sessions above this line._

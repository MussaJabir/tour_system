# Tour System — Product Roadmap & TODO

Last updated: 2026-05-14
Status key: `[ ]` not started · `[~]` in progress · `[x]` done

---

## Phase 1 — Fix the Holes (Security & Stability)
> These are not features. The app is not production-safe without them.

- [x] **Staff gate on all dashboard views** — add `@staff_member_required` alongside `@login_required` on every dashboard view across `core`, `destinations`, `accommodations`, `activities`, `packages`. Any logged-in user can currently hit the dashboard.
- [x] **Login / logout views for the staff dashboard** — `@login_required` redirects to `/accounts/login/` which 404s. Staff cannot log in through the dashboard. Add Django's built-in auth URLs or a minimal custom login/logout view.
- [x] **Remove duplicate email config in `settings.py`** — `EMAIL_*` vars are defined twice (around line 110 and again at line 180). Delete the second block.
- [x] **Remove bare `pass` in exception handlers** — `packages/views.py:409, 414, 423, 428` silently swallow exceptions. At minimum log them with `logger.exception(...)`.
- [x] **Clean up template directory** — delete `templates/frontend/index_new.html` and `templates/frontend/index_old.html.bak`. Commit hygiene.

---

## Phase 2 — Revenue Loop (Core Business Gap)
> Inquiry system exists. Closing the booking loop is what makes this a product.

- [x] **Booking + Reservation model** — turn inquiries into confirmed bookings:
  - `Booking` model: links inquiry → package → passengers
  - Status workflow: `pending_deposit` → `deposit_paid` → `confirmed` → `in_progress` → `completed` → `cancelled` / `refunded`
  - Auto-generated booking reference (`BKG-YYYYMMDD-NNNNN`)
  - `Passenger` model: names, passport, DOB, dietary/medical, emergency contacts, lead passenger flag
  - Email triggers: booking confirmation, status change, payment received
  - Dashboard: staff can create/edit/cancel bookings, manage passengers and payments

- [x] **Payment tracking (manual first)** — before building a full gateway:
  - `Payment` model: type (deposit/balance/full/extra/refund), method (cash/bank/M-Pesa/card/Stripe), status, reference
  - Balance auto-calculated from confirmed payments vs quoted price
  - Status auto-advances: deposit recorded → `deposit_paid`, fully paid → `confirmed`

- [ ] **Availability calendar** — packages need departure dates and seat limits:
  - `Departure` model: package + date + max_seats + booked_seats
  - Public listing shows available dates
  - Booking locks a seat on a departure
  - Sold out state auto-triggers from seat count

- [ ] **Payment gateway integration** — after manual tracking is proven:
  - Stripe for international (USD/EUR/GBP) clients
  - M-Pesa (Vodacom Tanzania) for local clients
  - Deposit + balance split payment flow

---

## Phase 3 — Mobile App (Token Auth)
> The README claims token auth exists. It does not.

- [x] **Token authentication** — `rest_framework.authtoken` + `TokenAuthentication` added to DRF; `/api/v1/auth/login/` returns DRF token for Flutter app
- [x] **Custom User model** — `accounts.CustomUser(AbstractUser)` with phone, profile_photo, preferred_currency, nationality; `AUTH_USER_MODEL` set; DB wiped and rebuilt
- [x] **Auth API endpoints** — register, login (token), logout, profile (GET/PATCH), change-password (rotates token)
- [ ] **Customer-facing API endpoints** — bookings, saved packages, inquiry status for the Flutter app (next iteration)

---

## Phase 4 — Reviews + AI (Differentiators)

- [ ] **Reviews app** — implement the stub:
  - `Review` model: linked to `Package` + `User` + `Booking` (only completed-booking guests can review)
  - Fields: rating (1–5), title, body, optional photos
  - Staff moderation (approve/reject workflow)
  - Aggregate rating cached on `Package` model
  - Schema markup for Google rich snippets
  - Public display with filtering and sorting

- [ ] **AI Assistant app** — implement the stub, all as async Celery tasks:
  - **PDF parser**: upload lodge PDF brochure → auto-populate `Accommodation` fields
  - **Itinerary generator**: destination + duration + budget → draft day-by-day itinerary
  - **Custom quote builder**: AI suggests packages from inquiry requirements
  - **Route optimizer**: selected parks/destinations → optimal driving order suggestion

---

## Phase 5 — Growth & Polish

- [ ] **SEO meta tags in templates** — base templates don't use the `meta_title` / `meta_description` fields that are on every model. Wire `get_meta_title()` and `get_meta_description()` into `<head>`. Free organic traffic.
- [ ] **Sitemap** — add Django's sitemaps framework for destinations, packages, activities. Submittable to Google Search Console.
- [ ] **Multi-currency display** — `Package` model already has currency choices. Wire to exchange rates so the public site shows prices in visitor's currency.
- [ ] **Analytics dashboard** — `view_count` is already tracked on every model. Surface it:
  - Most viewed packages / destinations
  - Inquiry → booking conversion rate
  - Revenue by month
  - Top traffic sources
- [ ] **Inquiry auto-follow-up** — Celery Beat jobs:
  - Immediate confirmation email to customer on inquiry submit
  - Follow-up if no staff reply in 48 hours
  - Escalation alert to manager at 72 hours
- [ ] **Newsletter campaigns** — use the existing `NewsletterSubscriber` list to send targeted promotions (new packages, seasonal offers)

---

## Priority Order (Impact vs Effort)

| # | Item | Impact | Effort |
|---|---|---|---|
| 1 | Staff gate on dashboard | Security | 1 hour |
| 2 | Login / logout views | Usability | 2 hours |
| 3 | Remove duplicate email config | Stability | 15 min |
| 4 | Fix bare `pass` exception handlers | Stability | 30 min |
| 5 | Booking model + status workflow | Revenue | 1 week |
| 6 | Token auth + Flutter wiring | Mobile | 1 day |
| 7 | Availability calendar | Sales | 3 days |
| 8 | Payment tracking (manual) | Revenue | 2 days |
| 9 | SEO meta tags in templates | Traffic | 4 hours |
| 10 | Custom User model | Foundation | 1 day |
| 11 | Reviews app | Trust / SEO | 3 days |
| 12 | Payment gateway (Stripe + M-Pesa) | Revenue | 1 week |
| 13 | Inquiry auto-follow-up (Celery) | Conversion | 2 days |
| 14 | Analytics dashboard | Visibility | 3 days |
| 15 | AI Assistant | Differentiation | 2 weeks |

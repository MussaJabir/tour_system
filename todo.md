# Tour System — Product Roadmap & TODO

Last updated: 2026-05-16
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

- [x] **Availability calendar** — packages need departure dates and seat limits:
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
- [x] **Customer-facing API endpoints** — bookings, saved packages, inquiry status for the Flutter app (next iteration)

---

## Phase 4 — Reviews + AI (Differentiators)

- [x] **Reviews app** — implement the stub:
  - `Review` model: Package + User + Booking + rating (1–5) + title/body + photos
  - Staff moderation: approve (publishes + updates package rating) / reject (with reason) / delete
  - Aggregate rating auto-updated in `Package.rating_average` via `update_rating()`
  - JSON-LD schema markup for Google rich snippets (AggregateRating)
  - Public display with rating breakdown, star filter, sort; submit form with eligibility check
  - REST API: GET approved reviews per package, POST create review (token auth)

- [x] **AI Assistant app** — implement the stub, all as async Celery tasks:
  - **PDF parser**: upload lodge PDF brochure → auto-populate `Accommodation` fields
  - **Itinerary generator**: destination + duration + budget → draft day-by-day itinerary
  - **Custom quote builder**: AI suggests packages from inquiry requirements
  - **Route optimizer**: selected parks/destinations → optimal driving order suggestion

---

## Phase 5 — Growth & Polish

- [x] **SEO meta tags in templates** — base templates don't use the `meta_title` / `meta_description` fields that are on every model. Wire `get_meta_title()` and `get_meta_description()` into `<head>`. Free organic traffic.
- [x] **Sitemap** — add Django's sitemaps framework for destinations, packages, activities. Submittable to Google Search Console.
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

## Phase 6 — Frontend Visual Overhaul (Safari Editorial)
> Replace the Ravelo Bootstrap template with a modern, cinematic Safari-editorial UI built on Tailwind + Alpine + GSAP + Lenis. Backend untouched — Django templates only.

**Direction:** Safari Editorial (National Geographic vibe — warm earth tones, serif headlines, magazine-style layouts)
**Photography:** Stock/Unsplash to start, swap to commissioned later
**Dev environment:** Docker stack at `http://localhost:8080`

### Stack decisions
- Keep: Django 5.2 templates, Leaflet (maps), Font Awesome (icons)
- Add: Tailwind CSS (PostCSS build), Alpine.js, GSAP + ScrollTrigger, Lenis (smooth scroll), django-imagekit (responsive images), variable fonts (Fraunces + Inter)
- Remove (gradually as pages are migrated): jQuery, Bootstrap JS, AOS, Slick, Magnific Popup, nice-select, jquery-ui

### Design principles (enforced on every page)
- One hero per page, full-bleed, real photography
- Generous whitespace
- Display serif (Fraunces) for headings, Inter for body
- Slow, deliberate motion (0.6–1.2s eases)
- Mobile-first
- Progressive enhancement (works without JS)
- Perf budget: LCP <2s, CSS <100kb, JS <80kb (excl GSAP)
- Accessibility WCAG AA (keyboard nav, contrast 4.5:1, alt text)

### Phase 6.0 — Foundation & Design System (2 days)
Branch: `feature/frontend-foundation` → PR → `develop`
- [x] Install Tailwind CSS via `pytailwindcss` (standalone CLI v4, no Node) — uses inline `@theme` instead of `tailwind.config.js`
- [x] Configure Safari Editorial tokens — full sand/bush/clay 50–900 ramps + ivory, bone, mist, charcoal, graphite
- [x] Install Alpine.js (3.14.3) + GSAP (3.12.5) + ScrollTrigger + Lenis (1.1.20) to `static/frontend/vendor/`
- [x] Add Google variable fonts — Fraunces (display) + Inter (body), preconnect tuned
- [x] Built new `base_modern.html` from scratch (legacy `base.html` left untouched; pages migrate one-by-one in 6.1+)
- [x] Created reusable partials: `_nav.html`, `_footer.html`, `_button.html`, `_card.html`, `_section_header.html`
- [x] Installed + configured `django-imagekit` (`imagekit` in INSTALLED_APPS)
- [x] Built `_styleguide.html` at `/styleguide/` (DEBUG-only, returns 404 in production)

### Phase 6.1 — Homepage (3 days)
Branch: `feature/frontend-homepage` → PR → `develop`
- [x] Cinematic hero — full-bleed Tanzania photo, Ken Burns zoom, GSAP staggered headline fade, scroll cue
- [x] Sticky nav that morphs on scroll (transparent → solid) — already done in Phase 6.0 partial
- [x] Featured destinations asymmetric magazine grid (1 hero card + 4 secondary) with hover zoom + caption reveal
- [x] Featured packages large editorial cards with price, duration, category eyebrow, hover arrow
- [x] Activities preview — horizontal scroll showcase with difficulty badge + category eyebrow
- [x] Stats trust strip — 4 scroll-triggered GSAP counters (destinations, tours, activities, lodges)
- [x] Testimonials section — 3-up quote cards with photo, location, star rating
- [x] Editorial pull-quote section (charcoal background) — "Why us" + 3 value pillars
- [x] Final CTA strip — full-bleed bush-green with mix-blend overlay, double CTA

### Phase 6.2 — Listing Pages (2 days)
Branch: `feature/frontend-listings` → PR → `develop`
- [x] `destinations/list.html` — Safari Editorial, sticky filter sidebar, country + search filters
- [x] `packages/list.html` — 6-filter sidebar (search, category, difficulty, destination, price range, days range, sort)
- [x] `activities/list.html` — search + category + difficulty + destination filters; difficulty badge on each card
- [x] `accommodations/list.html` — search + type + star rating + destination; star-rating badge on each card
- [x] Sticky filter sidebar (desktop, `lg:sticky top-28`) + Alpine.js mobile toggle slide-up
- [x] Active-filter pills with × dismiss (destination list — pattern reusable)
- [x] Shared `_listing_hero`, `_listing_pagination`, `_listing_empty` partials
- [ ] Grid ↔ list view toggle (deferred — not needed for v1)

### Phase 6.3 — Detail Pages (3 days)
Branch: `feature/frontend-detail-pages` → PR → `develop`
- [x] `packages/detail.html` — sticky booking sidebar (price + departures + facts), itinerary timeline with day markers, inclusions/exclusions, gallery, in-page CTA, related tours
- [x] `destinations/detail.html` — magazine-style long form (about, wildlife, climate, gallery), sticky quick-facts card, Leaflet map, activities + accommodations grids, related destinations
- [x] `activities/detail.html` — hero with difficulty + duration + min age, sticky price card, requirements/included/excluded, gallery, related activities
- [x] `accommodations/detail.html` — hero with star rating, sticky stay-here card, rooms list with prices + bed/occupancy/size, amenities, gallery, related lodges
- [x] Shared partials added: `_detail_hero.html`, `_gallery.html`, `_related_grid.html`

### Phase 6.4 — Conversion Flows (2 days)
Branch: `feature/frontend-conversion` → PR → `develop`
- [x] Inquiry form — 4-step Alpine.js wizard (single POST), progress bar with %, step labels, prev/next/submit nav, trust line at bottom
- [x] Contact page — `[1.4fr_1fr]` split layout: form left (name/email/phone/subject/message), info card + 3-step "what to expect" + Leaflet map of Arusha on right
- [x] Custom package quote view — token-protected page styled for clients receiving a tailor-made quote; sticky price-and-actions sidebar (Accept &amp; Book / Request changes), itinerary timeline, expiry banners
- [x] Inquiry success page — branded confirmation with reference card, 3-step "what happens next" timeline, links back to tours
- [x] Shared `_form_field.html` partial + base styles for all inputs/selects/textareas (Tailwind component layer)

### Phase 6.5 — Static Pages + Auth (1 day)
Branch: `feature/frontend-static` → PR → `develop`
- [x] **About us** — new `/about/` route + template. Cinematic hero, story section, 3 values cards (Local / Bespoke / Honest pricing), team grid placeholder, bush-green final CTA. Wired into nav + footer.
- [x] **FAQ** — category filter chips (with counts), Alpine.js accordion with single-open behaviour and smooth `x-transition`, "still stuck" CTA strip
- [x] **404** — branded "That trail's overgrown" page with helpful nav links
- [x] **500** — self-contained branded server-error page (doesn't extend base_modern since RequestContext isn't guaranteed)
- [x] **Staff dashboard login** — clean 2-col split (brand panel left with safari image + pull-quote, form right), Safari Editorial palette but utility-app feel

### Phase 6.6 — Polish & Performance (2 days)
Branch: `feature/frontend-polish` → PR → `develop`
- [x] Migrated last 3 templates off legacy base.html (reviews list + submit, newsletter unsubscribe)
- [x] **Deleted legacy Ravelo assets** — 17MB → 1.2MB of static assets (93% reduction): all old CSS (bootstrap, aos, slick, magnific-popup, nice-select, jquery-ui, flaticon, style), all old JS (jquery, bootstrap, slick, magnific, isotope, appear, skill.bars, imagesloaded, form-validator), the entire `assets/php/` + `assets/sass/` + most of `assets/images/` (kept only logos/), flaticon font files, plus FA `.eot/.svg/.ttf/.woff` variants (kept only `.woff2`)
- [x] **Deleted legacy templates** — `templates/frontend/base.html`, `templates/frontend/partials/header.html`, `templates/frontend/partials/footer.html`
- [x] Skip-to-content link in base_modern.html (sr-only by default, focus-revealed)
- [x] `<main id="content" tabindex="-1">` so the skip link actually focuses
- [x] `robots.txt` route + sitemap reference + admin/dashboard/api disallow
- [x] Mobile pass via Playwright at 390×844 (iPhone 14 width)
- [x] Perf check: HTML 20 KB · Tailwind CSS 55 KB · Vendor JS 171 KB — well within budget
- [ ] Lighthouse audit (not run — no CLI in this env; user can run from browser)
- [ ] Cross-browser test (Playwright only ships Chromium here; user can spot-check Safari + Firefox)
- [ ] Image optimization pipeline via django-imagekit (deferred to when real photos are uploaded)

**Phase 6 complete.** All 9 public route groups now live on `base_modern.html` with the Safari Editorial system.

**Total estimate:** 13–15 focused days, 7 PRs to `develop`.

---

## Phase 7 — Dashboard Visual Overhaul (Operations Slate)
> Apply a parallel design system to the internal staff dashboard. Built on the same Tailwind v4 + Alpine.js foundation as Phase 6, but with a denser, cooler, productivity-tool feel. Backend untouched — Django templates only.

**Direction:** Operations Slate (Stripe-meets-Linear — cool neutrals, dense layouts, semantic status colours, no editorial motion)
**Palette continuity:** keeps `bush-600` from Safari Editorial for brand consistency; everything else is fresh
**Dev environment:** existing Docker stack at `http://localhost:8080/dashboard/`

### Stack decisions
- Keep: Tailwind v4, Alpine.js, Font Awesome
- Add: **Chart.js** (~60 KB) for analytics dashboard charts
- Drop in dashboard context: GSAP, ScrollTrigger, Lenis (no cinematic motion in productivity tools)
- Typography: **Inter only** (no Fraunces); 14px base body (vs 16px on public)

### Operations Slate tokens (full list)
- **Backgrounds**: `slate-50` page bg, `white` cards, `slate-100` hover rows, `slate-200/300` borders
- **Text**: `slate-900` headings, `slate-700` body, `slate-500` labels/secondary
- **Brand**: `bush-600` for primary actions, active nav, focus rings; `bush-50` for primary hover
- **Semantic**: `emerald-500` success, `amber-500` warning, `rose-500` danger, `sky-500` info
- **Dark mode**: deferred to Phase 8

### Design principles (enforced on every dashboard page)
- Information density over whitespace
- Single accent colour (`bush-600`); no decorative gradients
- Transitions 150–250ms only — no scroll-triggered reveals
- Semantic status badges always use the semantic colour scale, never the brand accent
- Inline edit / quick actions preferred over modal flows
- Every list page has: search, filter pills, bulk-action bar, empty state, pagination

### Phase 7.0 — Foundation & Dashboard Styleguide (2 days)
Branch: `feature/dashboard-foundation` → PR → `develop`
- [x] Extended `tailwind.css` `@theme` — slate 50→900, semantic emerald/amber/rose/sky ramps. ~25 dashboard component classes (`dash-shell`, `dash-sidebar`, `dash-nav-link`, `dash-topbar`, `dash-page-title`, `dash-card`, `dash-stat`, `dash-btn`, `dash-btn-primary`, `dash-btn-danger`, `dash-badge` + variants, `dash-table`, `dash-input`, `dash-label`)
- [x] Chart.js 4.4.1 downloaded to `static/frontend/vendor/chart.min.js` (200 KB; loaded per-page, not globally)
- [x] Built `templates/backend/base_dashboard.html` — sidebar + topbar + main shell with Alpine off-canvas mobile nav + skip-to-content link + Django messages renderer
- [x] 8 reusable partials in `templates/backend/partials/` — `_dashboard_sidebar`, `_dashboard_topbar`, `_page_header`, `_breadcrumb`, `_stat_card`, `_status_badge`, `_empty_state`, `_data_table`
- [x] `/dashboard/styleguide/` page (DEBUG-only) showing every token, partial, badge, button, table, form field, motion guidance

### Phase 7.1 — Dashboard home (1–2 days)
Branch: `feature/dashboard-home` → PR → `develop`
- [x] **4-card KPI grid** — inquiries 30d, bookings 30d, revenue 30d, conversion %; each with vs-prior-30d trend chip (up/down arrow, signed %)
- [x] **Chart.js daily booking trend** — last 30 days, line chart with bush-green stroke + fill
- [x] **Chart.js revenue by month** — last 6 months, bar chart with bush hover state
- [x] **Recent inquiries table** — top 6 with status badges
- [x] **Recent bookings table** — top 6 with status badges and totals
- [x] **Action queue card** — pending inquiries / quotes awaiting send / unread messages with click-through
- [x] **Catalog totals card** — package / destination / activity / lodge counts, all clickable to their list pages
- [x] **Quick-create card** — 4 secondary buttons + primary "New booking" CTA

### Phase 7.2 — Dashboard listings (3–4 days · biggest sub-phase)
Branch: `feature/dashboard-listings` → PR → `develop`
- [x] All 12 dashboard list templates migrated to `base_dashboard.html`:
    - destinations, packages, activities, accommodations
    - inquiries, custom quotes, bookings, reviews
    - contacts, FAQs, newsletter, testimonials
- [x] Every list uses `.dash-table` for the data table + `.dash-input` / `.dash-select` for filters
- [x] Semantic status badges (via `_status_badge.html`) on every list with status
- [x] Status filter tabs with counts on inquiries, custom quotes, bookings, reviews, contacts, newsletter
- [x] Empty states with helpful CTAs via `_empty_state.html`
- [x] Per-row action buttons (edit / departures / delete / open / approve etc.)
- [x] Topbar "+ New X" CTAs on every applicable list
- [x] Pagination preserves filter querystring
- [ ] Sortable column headers — deferred to Phase 7.6 polish (not blocking; views still order by sensible defaults)
- [ ] Bulk-action toolbar — deferred to Phase 7.6 (only reviews + newsletter need it)
- [ ] Per-row Alpine dropdown menu — deferred (inline icon buttons work for v1)

### Phase 7.3 — Dashboard forms (2–3 days)
Branch: `feature/dashboard-forms` → PR → `develop`
- [x] **2-column layout** — form left (`1fr`), sticky publish sidebar right (`280px`) — saves/cancels/active toggle/featured toggle/danger zone
- [x] **Section cards** — every form is split into titled `dash-card`s (Basics / Pricing / Media / SEO, etc.)
- [x] **`.dash-form-field` wrapper class** — Tailwind component layer styles ALL input/select/textarea descendants so existing Django widget attrs (`form-control`) become visual no-ops; no widget rewrites needed
- [x] **Inline validation** — `dash-form-field--error` red border + per-field error list with `fa-exclamation-circle` icon
- [x] **Migrated 11 form templates**:
    - destinations · packages · activities · accommodations
    - faq · testimonial
    - booking · passenger
    - itinerary (package) · departure · custom-itinerary (custom quote)
- [x] Auto-render pattern via `{% for field in form %}` for the simpler forms; explicit section-by-section markup for packages (the most complex)
- [ ] Tabs for multi-section forms — deferred (Alpine.js tabs would be nice but section cards work well; revisit only if user feedback says forms are too long)

### Phase 7.4 — Dashboard detail pages (2 days)
Branch: `feature/dashboard-detail-pages` → PR → `develop`
- [x] **Booking detail** — header with reference + status badge, Customer card, Passengers table with row actions, Payments table with semantic status badges, Special requirements card, Staff notes (amber-tinted), sticky sidebar with financial summary (Total / Deposit / Paid / Balance) + Trip facts + Timeline
- [x] **Inquiry detail** — Customer + Trip request cards, Custom-quotes-for-this-inquiry list, threaded Messages with reply form, sticky sidebar with InquiryManagementForm + contact preferences
- [x] **Custom-package detail** — Overview + modifications + designer note, Itinerary days timeline with edit/delete per day + "Copy from base" action, edit form, sticky sidebar with Total price + price-difference vs base + Secure-client-link copy box + Inquiry link + Validity card
- [x] **Contact-message detail** — message body, reply form, amber-tinted Internal notes form, sticky From-customer info card
- [x] **Review moderation detail** — review body + star rating, attached photos grid, rejection-reason card (when rejected), sticky sidebar with Approve/Reject/Delete actions + Reviewer info + Package context
- [x] **Destinations / Activities / Accommodations detail** — hero image, About + Wildlife/Climate/Requirements/Amenities cards, Gallery grid, Rooms table (accommodations), sticky Quick-facts sidebar; topbar actions for "Public page" + "Edit"
- [x] Per-entity action menus in topbar (Edit / Cancel booking / Send quote / Delete message etc.)

### Phase 7.5 — Special workflows (2 days)
Branch: `feature/dashboard-workflows` → PR → `develop`
- [x] **Reviews moderation** — approve_confirm (emerald), reject_confirm (rose + reason textarea), delete_confirm (rose, permanent warning)
- [x] **6 catalog delete confirms** — destinations, activities, accommodations, packages, departures, custom-itinerary; fixes pre-existing bug where `packages/views.py` rendered `delete_confirm.html` but only `delete.html` existed
- [x] **Booking cancel confirm** — amber-tinted, inline cancellation-reason textarea, "Keep booking" escape hatch
- [x] **Custom-package builder** — 4-section staff form (Basics / Pricing / Modifications &amp; notes / Validity &amp; media) on 2-col layout with inquiry + base-package context in sidebar
- [x] **AI Assistant home** — 4 stat cards + 4 action tiles + setup-required banner if no AI config
- [x] **AI brochure parser** — upload form + result page with auto-refresh while running, JSON preview, copy-to-clipboard
- [x] **AI itinerary generator** — trip parameters form + result page with copy-to-clipboard
- [x] **AI route optimiser** — destinations input + ordered numbered-list result
- [x] **AI quote suggestions result** — match-score cards with reasoning
- [x] Shared `_confirm_action.html` reference partial documenting the icon + color variant pattern
- [ ] Booking status workflow transition guards — deferred (UI hides Cancel when already cancelled; deeper guards belong in `Booking.save()` not template)

### Phase 7.6 — Polish + a11y + cleanup (1–2 days)
Branch: `feature/dashboard-polish` → PR → `develop`
- [x] **Migrated last 8 templates** off `backend/base.html`: departures list, 3 add-image forms (destinations/activities/accommodations), add-room form, custom-itinerary copy + custom-package send confirm
- [x] **Deleted `templates/backend/base.html`** + legacy index/sidebar/topbar partials + obsolete `packages/dashboard/delete.html`
- [x] **Deleted `static/backend/`** — **54 MB → 1.5 MB** (97% reduction). All Bootstrap admin theme libs, jQuery plugins, Sass sources, demo images removed.
- [x] **Mobile audit** at 390×844 — sidebar off-canvas (`x: -256`), hamburger toggle slides it in (`x: 0`), Alpine state works correctly
- [x] **Perf budget**: HTML 20 KB · Tailwind 69 KB · Alpine 44 KB · Chart.js 201 KB (loaded per-page only). ~330 KB uncompressed, ~100 KB gzipped on dashboard home.
- [x] **3 polish tests** asserting (a) no template extends `backend/base.html` anymore, (b) `templates/backend/base.html` is deleted, (c) `static/backend/` is deleted
- [x] Skip-to-content link + focus-visible rings already wired in Phase 6.0 base — verified working on dashboard
- [ ] Toast notifications via Alpine — deferred (current Django messages renderer works fine; toast would be polish only)
- [ ] Lighthouse run — deferred (needs login; user can run from Chrome DevTools and report any reds)

**Phase 7 complete.** All dashboard routes live on `base_dashboard.html`. Total assets purged: **107 MB → 2.7 MB** across Phase 6 + Phase 7.

**Total estimate:** 13–17 focused days, 7 PRs to `develop`.

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

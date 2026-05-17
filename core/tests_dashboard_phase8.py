"""
Phase 8 — Dashboard P0 fixes.

Covers:
- Topbar block regression: `{% block topbar_extras %}` overrides on child
  templates must actually render. Previously the block lived inside an
  `{% include %}d` partial, which silently dropped every override across
  ~16 dashboard pages.
- Get-started checklist: visible on a fresh, empty catalog; auto-hides
  once all four catalog buckets (destinations, activities, accommodations,
  packages) have at least one active row.
"""
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


def make_staff_user(username='phase8staff', password='pw1234'):
    u = User.objects.create_user(
        username=username, email=f'{username}@example.com', password=password
    )
    u.is_staff = True
    u.save()
    return u


def make_destination():
    from destinations.models import Destination
    return Destination.objects.create(
        name='Serengeti', slug='serengeti',
        short_description='Wildlife paradise',
        description='Full description of Serengeti.',
        latitude='2.3333', longitude='34.8333',
        is_active=True,
    )


def make_activity(destination=None):
    from activities.models import Activity
    if destination is None:
        destination = make_destination()
    return Activity.objects.create(
        name='Hot Air Balloon', slug='hot-air-balloon',
        short_description='Sunrise balloon ride',
        description='Float above the plains.',
        destination=destination,
        duration=Decimal('3.0'), duration_unit='hours',
        price_per_person=Decimal('200.00'),
        is_active=True,
    )


def make_accommodation():
    from accommodations.models import Accommodation
    return Accommodation.objects.create(
        name='Serengeti Lodge', slug='serengeti-lodge',
        short_description='Luxury lodge',
        description='A beautiful lodge.',
        is_active=True,
    )


def make_package():
    from packages.models import Package
    return Package.objects.create(
        name='Sitemap Safari', slug='phase8-safari',
        short_description='A test safari',
        description='Full description.',
        duration_days=5, duration_nights=4,
        price_per_person=Decimal('1500.00'),
        is_active=True,
    )


# =========================================================================
# Regression: topbar_extras block reaches through the extends chain.
# =========================================================================
class TopbarExtrasBlockRegressionTests(TestCase):
    """
    Before Phase 8: `{% block topbar_extras %}` was declared inside
    `_dashboard_topbar.html` which is `{% include %}d` into
    `base_dashboard.html`. Django block inheritance does not cross
    `include` — so every page overriding `topbar_extras` was silently
    ignored.

    Phase 8 inlines the topbar markup directly into `base_dashboard.html`
    so the block lives in the same template that child pages extend.
    """

    @classmethod
    def setUpTestData(cls):
        cls.staff = make_staff_user()

    def setUp(self):
        self.client.force_login(self.staff)

    def test_packages_list_renders_new_package_cta(self):
        """packages/dashboard/list.html overrides topbar_extras with the
        'New package' CTA. The rendered HTML must contain it."""
        response = self.client.get(reverse('packages:dashboard_package_list'))
        self.assertEqual(response.status_code, 200)
        # Both the button label and the href to the create URL.
        self.assertContains(response, 'New package')
        self.assertContains(response, reverse('packages:dashboard_package_create'))

    def test_destinations_list_renders_new_destination_cta(self):
        response = self.client.get(reverse('dashboard_destination_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('dashboard_destination_create'))

    def test_view_site_link_still_renders(self):
        """The static 'View site' link (not inside a block) must still
        render — confirms we didn't accidentally drop the surrounding
        topbar markup when inlining."""
        response = self.client.get(reverse('dashboard_home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'View site')

    def test_topbar_partial_file_is_deleted(self):
        """The old partial must be gone — otherwise a future include
        could silently bring the bug back."""
        from pathlib import Path
        from django.conf import settings
        partial = Path(settings.BASE_DIR) / 'templates' / 'backend' / 'partials' / '_dashboard_topbar.html'
        self.assertFalse(
            partial.exists(),
            f'{partial} should be deleted; topbar markup now lives in base_dashboard.html'
        )


# =========================================================================
# Get-started checklist on the dashboard home.
# =========================================================================
class GettingStartedChecklistTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.staff = make_staff_user()

    def setUp(self):
        self.client.force_login(self.staff)

    # --- Empty catalog ---------------------------------------------------

    def test_visible_when_catalog_is_empty(self):
        response = self.client.get(reverse('dashboard_home'))
        self.assertTrue(response.context['getting_started_visible'])
        self.assertEqual(response.context['getting_started_done_count'], 0)
        self.assertEqual(response.context['getting_started_total'], 4)
        self.assertContains(response, 'Set up your catalog')
        self.assertContains(response, 'data-getting-started')

    def test_renders_all_four_steps_when_empty(self):
        response = self.client.get(reverse('dashboard_home'))
        for label in ('Add your first destination',
                      'Add an activity',
                      'Add a lodge or camp',
                      'Build your first tour package'):
            self.assertContains(response, label)

    def test_step_links_resolve(self):
        response = self.client.get(reverse('dashboard_home'))
        for url_name in ('dashboard_destination_create',
                         'dashboard_activity_create',
                         'dashboard_accommodation_create'):
            self.assertContains(response, reverse(url_name))
        self.assertContains(response, reverse('packages:dashboard_package_create'))

    # --- Partial progress ------------------------------------------------

    def test_partial_progress_shows_count(self):
        dest = make_destination()
        make_activity(destination=dest)
        response = self.client.get(reverse('dashboard_home'))
        self.assertTrue(response.context['getting_started_visible'])
        self.assertEqual(response.context['getting_started_done_count'], 2)
        # Done steps render with the line-through styling marker.
        self.assertContains(response, 'line-through')

    # --- Fully seeded ----------------------------------------------------

    def test_hides_when_all_catalog_buckets_seeded(self):
        dest = make_destination()
        make_activity(destination=dest)
        make_accommodation()
        make_package()
        response = self.client.get(reverse('dashboard_home'))
        self.assertFalse(response.context['getting_started_visible'])
        self.assertNotContains(response, 'Set up your catalog')
        self.assertNotContains(response, 'data-getting-started')

    def test_inactive_rows_do_not_count_toward_completion(self):
        """A soft-deleted (is_active=False) destination should NOT mark
        the destination step as done — the dashboard counts only the
        live catalog."""
        from destinations.models import Destination
        Destination.objects.create(
            name='Hidden', slug='hidden',
            short_description='-', description='-',
            latitude='0', longitude='0',
            is_active=False,
        )
        response = self.client.get(reverse('dashboard_home'))
        self.assertTrue(response.context['getting_started_visible'])
        # Destination step still not marked done.
        steps = response.context['getting_started_steps']
        destination_step = next(s for s in steps if 'destination' in s['label'].lower())
        self.assertFalse(destination_step['done'])

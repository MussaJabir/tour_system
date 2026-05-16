"""
Phase 6.1 — Homepage tests.

Verifies the new Safari Editorial homepage:
- /  returns 200 and uses base_modern.html + index.html
- Hero section renders with full set of CTAs + scroll cue
- Stat counters include all four numbers from the view context
- Featured sections (destinations, packages, activities, testimonials)
  render headers and a CTA link to the relevant listing page
- Final CTA strip is present
- View context includes the new keys: featured_packages, featured_testimonials, total_packages
"""
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify

from destinations.models import Destination
from packages.models import Package
from activities.models import Activity
from core.models import Testimonial


def make_destination(name, **extra):
    return Destination.objects.create(
        name=name,
        slug=slugify(name),
        country=extra.pop('country', 'Tanzania'),
        description=extra.pop('description', 'A wonderful place to visit'),
        latitude=extra.pop('latitude', -2.333333),
        longitude=extra.pop('longitude', 34.833333),
        is_active=True,
        is_featured=extra.pop('is_featured', True),
        **extra,
    )


def make_package(name, **extra):
    return Package.objects.create(
        name=name,
        slug=slugify(name),
        short_description=extra.pop('short_description', "A short description"),
        description="A long description",
        duration_days=extra.pop('duration_days', 5),
        duration_nights=extra.pop('duration_nights', 4),
        price_per_person=extra.pop('price_per_person', 1500),
        currency='USD',
        category=extra.pop('category', 'adventure'),
        is_active=True,
        is_featured=extra.pop('is_featured', True),
        **extra,
    )


def make_activity(name, dest, **extra):
    return Activity.objects.create(
        name=name,
        slug=slugify(name),
        destination=dest,
        short_description="A short activity description",
        description="A full activity description",
        category=extra.pop('category', 'safari'),
        difficulty=extra.pop('difficulty', 'easy'),
        duration=extra.pop('duration', 4),
        duration_unit=extra.pop('duration_unit', 'hours'),
        price_per_person=extra.pop('price_per_person', 75),
        currency='USD',
        is_active=True,
        is_featured=extra.pop('is_featured', True),
        **extra,
    )


def make_testimonial(name, **extra):
    return Testimonial.objects.create(
        customer_name=name,
        customer_location=extra.pop('customer_location', 'Toronto, Canada'),
        quote=extra.pop('quote', 'Best trip of our lives.'),
        rating=extra.pop('rating', 5),
        is_active=True,
        is_featured=extra.pop('is_featured', True),
        **extra,
    )


class HomepageRenderTests(TestCase):
    """The /  route renders, uses the modern base, and includes every section."""

    @classmethod
    def setUpTestData(cls):
        cls.dest = make_destination("Serengeti")
        make_destination("Ngorongoro")
        cls.pkg = make_package("Northern Circuit Classic")
        cls.act = make_activity("Game drive at dawn", cls.dest)
        cls.tst = make_testimonial("Jane Doe")
        # Non-featured items: should not appear in featured lists
        make_destination("Hidden Park", is_featured=False)
        make_package("Hidden Tour", is_featured=False)

    def test_home_returns_200(self):
        response = self.client.get(reverse('public_home'))
        self.assertEqual(response.status_code, 200)

    def test_home_uses_base_modern(self):
        response = self.client.get(reverse('public_home'))
        self.assertTemplateUsed(response, 'frontend/base_modern.html')
        self.assertTemplateUsed(response, 'frontend/index.html')

    def test_home_renders_hero_block(self):
        response = self.client.get(reverse('public_home'))
        self.assertContains(response, 'data-hero-image')
        self.assertContains(response, 'data-hero-stagger')
        self.assertContains(response, 'Wild seasons')

    def test_home_includes_all_section_anchors(self):
        response = self.client.get(reverse('public_home'))
        for phrase in [
            '01 — Destinations',
            '02 — Tours',
            '03 — Activities',
            '04 — Travellers',
            'Ready when you are',
        ]:
            self.assertContains(response, phrase)

    def test_home_lists_only_featured_destinations(self):
        response = self.client.get(reverse('public_home'))
        self.assertContains(response, 'Serengeti')
        self.assertNotContains(response, 'Hidden Park')

    def test_home_lists_only_featured_packages(self):
        response = self.client.get(reverse('public_home'))
        self.assertContains(response, 'Northern Circuit Classic')
        self.assertNotContains(response, 'Hidden Tour')

    def test_home_lists_featured_activity(self):
        response = self.client.get(reverse('public_home'))
        self.assertContains(response, 'Game drive at dawn')

    def test_home_renders_testimonial(self):
        response = self.client.get(reverse('public_home'))
        self.assertContains(response, 'Jane Doe')
        self.assertContains(response, 'Best trip of our lives.')

    def test_home_stats_counters_present(self):
        response = self.client.get(reverse('public_home'))
        # All four data-counter widgets should be present (use data-to= which
        # is unique to the markup; data-counter appears in inline JS too).
        self.assertEqual(response.content.decode().count('data-to='), 4)

    def test_home_links_to_listing_pages(self):
        response = self.client.get(reverse('public_home'))
        self.assertContains(response, reverse('public_destination_list'))
        self.assertContains(response, reverse('packages:public_package_list'))
        self.assertContains(response, reverse('contact_page'))


class HomepageContextTests(TestCase):
    """The view's context must expose the new Phase 6.1 keys."""

    REQUIRED_KEYS = [
        'featured_destinations',
        'featured_packages',
        'featured_activities',
        'featured_accommodations',
        'featured_testimonials',
        'total_destinations',
        'total_activities',
        'total_accommodations',
        'total_packages',
    ]

    def test_context_contains_required_keys(self):
        response = self.client.get(reverse('public_home'))
        for key in self.REQUIRED_KEYS:
            self.assertIn(key, response.context, f"missing context key: {key}")

    def test_context_counts_are_integers(self):
        response = self.client.get(reverse('public_home'))
        for key in ('total_destinations', 'total_packages',
                    'total_activities', 'total_accommodations'):
            self.assertIsInstance(response.context[key], int)

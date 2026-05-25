"""
Phase 6.2 — Listing page tests.

Verifies that all four public list pages migrated to base_modern.html
render correctly with their filter sidebars, results grid, and pagination.

Test factories live in destinations.tests_homepage; we reuse them here
to stay DRY and keep one source of model defaults.
"""
from django.test import TestCase
from django.urls import reverse

from destinations.tests_homepage import (
    make_destination,
    make_package,
    make_activity,
    make_testimonial,
)
from accommodations.models import Accommodation


def make_accommodation(name, destination, **extra):
    """Local factory — accommodation isn't used by the homepage tests."""
    return Accommodation.objects.create(
        name=name,
        slug=name.lower().replace(' ', '-'),
        destination=destination,
        short_description="A short description",
        description="A full description",
        accommodation_type=extra.pop('accommodation_type', 'lodge'),
        star_rating=extra.pop('star_rating', 4),
        is_active=True,
        is_featured=extra.pop('is_featured', True),
        **extra,
    )


class DestinationListTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        make_destination("Serengeti", country="Tanzania")
        make_destination("Maasai Mara", country="Kenya")

    def test_returns_200(self):
        response = self.client.get(reverse('public_destination_list'))
        self.assertEqual(response.status_code, 200)

    def test_uses_base_modern(self):
        response = self.client.get(reverse('public_destination_list'))
        self.assertTemplateUsed(response, 'frontend/base_modern.html')
        self.assertTemplateUsed(response, 'destinations/public/list.html')

    def test_renders_filter_form(self):
        response = self.client.get(reverse('public_destination_list'))
        self.assertContains(response, 'name="search"')
        self.assertContains(response, 'name="country"')

    def test_renders_count(self):
        response = self.client.get(reverse('public_destination_list'))
        self.assertContains(response, '2 destinations')

    def test_renders_destination_names(self):
        response = self.client.get(reverse('public_destination_list'))
        self.assertContains(response, 'Serengeti')
        self.assertContains(response, 'Maasai Mara')

    def test_search_filters_results(self):
        response = self.client.get(reverse('public_destination_list'), {'search': 'Serengeti'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Serengeti')
        self.assertNotContains(response, 'Maasai Mara')


class PackageListTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        dest = make_destination("Serengeti NP", country="Tanzania")
        p1 = make_package("Northern Circuit Classic")
        p2 = make_package("Kilimanjaro Climb")
        p1.destinations.add(dest)
        p2.destinations.add(dest)

    def test_returns_200(self):
        response = self.client.get(reverse('packages:public_package_list'))
        self.assertEqual(response.status_code, 200)

    def test_uses_base_modern(self):
        response = self.client.get(reverse('packages:public_package_list'))
        self.assertTemplateUsed(response, 'frontend/base_modern.html')
        self.assertTemplateUsed(response, 'packages/public/list.html')

    def test_renders_filter_form(self):
        response = self.client.get(reverse('packages:public_package_list'))
        for fname in ('search', 'category', 'difficulty', 'destination',
                      'min_price', 'max_price', 'min_days', 'max_days'):
            self.assertContains(response, f'name="{fname}"',
                                msg_prefix=f"missing filter: {fname}")

    def test_renders_count(self):
        response = self.client.get(reverse('packages:public_package_list'))
        self.assertContains(response, '2 tours')

    def test_renders_package_names(self):
        response = self.client.get(reverse('packages:public_package_list'))
        self.assertContains(response, 'Northern Circuit Classic')
        self.assertContains(response, 'Kilimanjaro Climb')


class ActivityListTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.dest = make_destination("Tarangire")
        make_activity("Game drive at dawn", cls.dest)
        make_activity("Walking safari", cls.dest)

    def test_returns_200(self):
        response = self.client.get(reverse('public_activity_list'))
        self.assertEqual(response.status_code, 200)

    def test_uses_base_modern(self):
        response = self.client.get(reverse('public_activity_list'))
        self.assertTemplateUsed(response, 'frontend/base_modern.html')
        self.assertTemplateUsed(response, 'activities/public/list.html')

    def test_renders_filter_form(self):
        response = self.client.get(reverse('public_activity_list'))
        for fname in ('search', 'category', 'difficulty', 'destination'):
            self.assertContains(response, f'name="{fname}"',
                                msg_prefix=f"missing filter: {fname}")

    def test_renders_count(self):
        response = self.client.get(reverse('public_activity_list'))
        self.assertContains(response, '2 activities')

    def test_renders_activity_names(self):
        response = self.client.get(reverse('public_activity_list'))
        self.assertContains(response, 'Game drive at dawn')
        self.assertContains(response, 'Walking safari')


class AccommodationListTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.dest = make_destination("Ngorongoro")
        make_accommodation("Crater Lodge", cls.dest, accommodation_type='lodge', star_rating=5)
        make_accommodation("Mobile Camp", cls.dest, accommodation_type='camp', star_rating=4)

    def test_returns_200(self):
        response = self.client.get(reverse('public_accommodation_list'))
        self.assertEqual(response.status_code, 200)

    def test_uses_base_modern(self):
        response = self.client.get(reverse('public_accommodation_list'))
        self.assertTemplateUsed(response, 'frontend/base_modern.html')
        self.assertTemplateUsed(response, 'accommodations/public/list.html')

    def test_renders_filter_form(self):
        response = self.client.get(reverse('public_accommodation_list'))
        for fname in ('search', 'type', 'rating', 'destination'):
            self.assertContains(response, f'name="{fname}"',
                                msg_prefix=f"missing filter: {fname}")

    def test_renders_count(self):
        response = self.client.get(reverse('public_accommodation_list'))
        self.assertContains(response, '2 lodges')

    def test_renders_lodge_names(self):
        response = self.client.get(reverse('public_accommodation_list'))
        self.assertContains(response, 'Crater Lodge')
        self.assertContains(response, 'Mobile Camp')


class EmptyStateTests(TestCase):
    """When a filter eliminates all results, the empty-state partial renders."""

    def test_destination_empty_state(self):
        response = self.client.get(reverse('public_destination_list'), {'search': 'nope-no-match'})
        self.assertContains(response, 'Reset filters')

    def test_package_empty_state(self):
        response = self.client.get(reverse('packages:public_package_list'), {'search': 'nope-no-match'})
        self.assertContains(response, 'Reset filters')

    def test_activity_empty_state(self):
        response = self.client.get(reverse('public_activity_list'), {'search': 'nope-no-match'})
        self.assertContains(response, 'Reset filters')

    def test_accommodation_empty_state(self):
        response = self.client.get(reverse('public_accommodation_list'), {'search': 'nope-no-match'})
        self.assertContains(response, 'Reset filters')

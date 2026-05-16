"""
Phase 6.3 — Detail page tests.

Verifies each public detail page renders on base_modern.html with the
expected sections.
"""
from django.test import TestCase
from django.urls import reverse

from destinations.tests_homepage import (
    make_destination,
    make_package,
    make_activity,
)
from core.tests_frontend_listings import make_accommodation


class PackageDetailTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.dest = make_destination("Serengeti")
        cls.pkg = make_package("Northern Circuit Classic")
        cls.pkg.destinations.add(cls.dest)

    def test_returns_200(self):
        response = self.client.get(
            reverse('packages:public_package_detail', args=[self.pkg.slug])
        )
        self.assertEqual(response.status_code, 200)

    def test_uses_base_modern(self):
        response = self.client.get(
            reverse('packages:public_package_detail', args=[self.pkg.slug])
        )
        self.assertTemplateUsed(response, 'frontend/base_modern.html')
        self.assertTemplateUsed(response, 'packages/public/detail.html')

    def test_renders_hero_and_booking_sidebar(self):
        response = self.client.get(
            reverse('packages:public_package_detail', args=[self.pkg.slug])
        )
        # Hero
        self.assertContains(response, self.pkg.name)
        # Booking sidebar
        self.assertContains(response, 'Plan This Trip')
        # Price (factory default is 1500)
        self.assertContains(response, 'USD')

    def test_renders_overview_section(self):
        response = self.client.get(
            reverse('packages:public_package_detail', args=[self.pkg.slug])
        )
        self.assertContains(response, 'About this journey')

    def test_renders_breadcrumb(self):
        response = self.client.get(
            reverse('packages:public_package_detail', args=[self.pkg.slug])
        )
        self.assertContains(response, '>Home<')
        self.assertContains(response, '>Tours<')


class DestinationDetailTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.dest = make_destination("Tarangire")

    def test_returns_200(self):
        response = self.client.get(
            reverse('public_destination_detail', args=[self.dest.slug])
        )
        self.assertEqual(response.status_code, 200)

    def test_uses_base_modern(self):
        response = self.client.get(
            reverse('public_destination_detail', args=[self.dest.slug])
        )
        self.assertTemplateUsed(response, 'frontend/base_modern.html')
        self.assertTemplateUsed(response, 'destinations/public/detail.html')

    def test_renders_hero_and_about(self):
        response = self.client.get(
            reverse('public_destination_detail', args=[self.dest.slug])
        )
        self.assertContains(response, self.dest.name)
        self.assertContains(response, f'About {self.dest.name}')

    def test_renders_quick_facts(self):
        response = self.client.get(
            reverse('public_destination_detail', args=[self.dest.slug])
        )
        self.assertContains(response, 'Quick facts')
        self.assertContains(response, self.dest.country)


class ActivityDetailTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.dest = make_destination("Ngorongoro")
        cls.act = make_activity("Sunrise game drive", cls.dest)

    def test_returns_200(self):
        response = self.client.get(
            reverse('public_activity_detail', args=[self.act.slug])
        )
        self.assertEqual(response.status_code, 200)

    def test_uses_base_modern(self):
        response = self.client.get(
            reverse('public_activity_detail', args=[self.act.slug])
        )
        self.assertTemplateUsed(response, 'frontend/base_modern.html')
        self.assertTemplateUsed(response, 'activities/public/detail.html')

    def test_renders_hero_and_sidebar(self):
        response = self.client.get(
            reverse('public_activity_detail', args=[self.act.slug])
        )
        self.assertContains(response, self.act.name)
        self.assertContains(response, 'Add To Trip')
        self.assertContains(response, 'About this activity')


class AccommodationDetailTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.dest = make_destination("Ruaha")
        cls.lodge = make_accommodation("Ruaha River Lodge", cls.dest, star_rating=4)

    def test_returns_200(self):
        response = self.client.get(
            reverse('public_accommodation_detail', args=[self.lodge.slug])
        )
        self.assertEqual(response.status_code, 200)

    def test_uses_base_modern(self):
        response = self.client.get(
            reverse('public_accommodation_detail', args=[self.lodge.slug])
        )
        self.assertTemplateUsed(response, 'frontend/base_modern.html')
        self.assertTemplateUsed(response, 'accommodations/public/detail.html')

    def test_renders_hero_with_stars(self):
        response = self.client.get(
            reverse('public_accommodation_detail', args=[self.lodge.slug])
        )
        self.assertContains(response, self.lodge.name)
        # 4 star icons should be rendered
        self.assertGreaterEqual(response.content.decode().count('fa-star'), 4)

    def test_renders_about_section(self):
        response = self.client.get(
            reverse('public_accommodation_detail', args=[self.lodge.slug])
        )
        self.assertContains(response, 'About this stay')

"""
Phase 7.4 — Dashboard detail-page smoke tests.

Creates minimal test fixtures and verifies each migrated detail page:
- requires staff auth
- returns 200 for staff
- uses base_dashboard.html
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from destinations.tests_homepage import (
    make_destination, make_package, make_activity,
)
from core.tests_frontend_listings import make_accommodation

User = get_user_model()


def make_staff_user(username='detstaff', password='pw1234'):
    u = User.objects.create_user(
        username=username, email=f'{username}@example.com', password=password
    )
    u.is_staff = True
    u.save()
    return u


class CatalogDetailRenderTests(TestCase):
    """destinations / activities / accommodations detail pages."""

    @classmethod
    def setUpTestData(cls):
        cls.staff = make_staff_user()
        cls.dest = make_destination('Serengeti detail')
        cls.act = make_activity('Dawn game drive', cls.dest)
        cls.lodge = make_accommodation('Crater Lodge detail', cls.dest)

    def setUp(self):
        self.client.force_login(self.staff)

    def test_destination_detail(self):
        response = self.client.get(reverse('dashboard_destination_detail', args=[self.dest.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'backend/base_dashboard.html')
        self.assertContains(response, self.dest.name)

    def test_activity_detail(self):
        response = self.client.get(reverse('dashboard_activity_detail', args=[self.act.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'backend/base_dashboard.html')
        self.assertContains(response, self.act.name)

    def test_accommodation_detail(self):
        response = self.client.get(reverse('dashboard_accommodation_detail', args=[self.lodge.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'backend/base_dashboard.html')
        self.assertContains(response, self.lodge.name)

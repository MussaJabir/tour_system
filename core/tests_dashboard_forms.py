"""
Phase 7.3 — Dashboard forms smoke tests.

For each create endpoint, verify:
- requires staff auth
- returns 200 for staff
- uses base_dashboard.html
- contains the dash-form-field wrapper class
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


def make_staff_user(username='formstaff', password='pw1234'):
    u = User.objects.create_user(
        username=username, email=f'{username}@example.com', password=password
    )
    u.is_staff = True
    u.save()
    return u


class DashboardFormCreateRenderTests(TestCase):
    """Each create route renders the migrated form template for staff."""

    CREATE_URLS = [
        ('dashboard_destination_create', []),
        ('packages:dashboard_package_create', []),
        ('dashboard_activity_create', []),
        ('dashboard_accommodation_create', []),
        ('dashboard_faq_create', []),
        ('dashboard_testimonial_create', []),
        ('packages:dashboard_booking_create', []),
    ]

    @classmethod
    def setUpTestData(cls):
        cls.staff = make_staff_user()

    def setUp(self):
        self.client.force_login(self.staff)

    def test_all_creates_return_200(self):
        for name, args in self.CREATE_URLS:
            with self.subTest(route=name):
                response = self.client.get(reverse(name, args=args))
                self.assertEqual(response.status_code, 200,
                                 f"{name} returned {response.status_code}")

    def test_all_creates_use_base_dashboard(self):
        for name, args in self.CREATE_URLS:
            with self.subTest(route=name):
                response = self.client.get(reverse(name, args=args))
                self.assertTemplateUsed(response, 'backend/base_dashboard.html',
                                        msg_prefix=f"{name}: ")

    def test_all_creates_render_form_fields(self):
        """Each form page should contain at least one dash-form-field wrapper."""
        for name, args in self.CREATE_URLS:
            with self.subTest(route=name):
                response = self.client.get(reverse(name, args=args))
                self.assertContains(response, 'dash-form-field',
                                    msg_prefix=f"{name}: ")

    def test_all_creates_have_submit_button(self):
        for name, args in self.CREATE_URLS:
            with self.subTest(route=name):
                response = self.client.get(reverse(name, args=args))
                self.assertContains(response, 'type="submit"',
                                    msg_prefix=f"{name}: ")


class DashboardFormAuthTests(TestCase):
    """Forms require @staff_member_required."""

    def test_anonymous_redirects(self):
        for name in ('dashboard_destination_create', 'dashboard_faq_create'):
            with self.subTest(route=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 302)

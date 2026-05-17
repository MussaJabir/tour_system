"""
Phase 7.2 — Dashboard listings smoke tests.

Verifies every migrated dashboard list page:
- requires staff auth
- returns 200 for staff
- uses base_dashboard.html
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


def make_staff_user(username='staffdash', password='pw1234'):
    u = User.objects.create_user(
        username=username, email=f'{username}@example.com', password=password
    )
    u.is_staff = True
    u.save()
    return u


class DashboardListingsRenderTests(TestCase):
    """Each dashboard list page must render on base_dashboard.html for staff."""

    LISTING_URLS = [
        # (route_name, url_args)
        ('dashboard_destination_list', []),
        ('packages:dashboard_package_list', []),
        ('dashboard_activity_list', []),
        ('dashboard_accommodation_list', []),
        ('packages:dashboard_inquiry_list', []),
        ('packages:dashboard_custom_package_list', []),
        ('packages:dashboard_booking_list', []),
        ('reviews:dashboard_review_list', []),
        ('dashboard_contact_list', []),
        ('dashboard_faq_list', []),
        ('dashboard_newsletter_list', []),
        ('dashboard_testimonial_list', []),
    ]

    @classmethod
    def setUpTestData(cls):
        cls.staff = make_staff_user()

    def setUp(self):
        self.client.force_login(self.staff)

    def test_all_listings_return_200_for_staff(self):
        for name, args in self.LISTING_URLS:
            with self.subTest(route=name):
                response = self.client.get(reverse(name, args=args))
                self.assertEqual(response.status_code, 200,
                                 f"{name} returned {response.status_code}")

    def test_all_listings_use_base_dashboard(self):
        for name, args in self.LISTING_URLS:
            with self.subTest(route=name):
                response = self.client.get(reverse(name, args=args))
                self.assertTemplateUsed(response, 'backend/base_dashboard.html',
                                        msg_prefix=f"{name}: ")

    def test_all_listings_render_a_data_table(self):
        for name, args in self.LISTING_URLS:
            with self.subTest(route=name):
                response = self.client.get(reverse(name, args=args))
                self.assertContains(response, 'dash-table',
                                    msg_prefix=f"{name}: ")

    def test_destinations_list_has_search_field(self):
        """Spot-check that filter forms render on at least one list."""
        response = self.client.get(reverse('dashboard_destination_list'))
        self.assertContains(response, 'name="search"')
        self.assertContains(response, 'name="country"')
        self.assertContains(response, 'name="status"')


class DashboardListingsAuthTests(TestCase):
    """Listings require @staff_member_required."""

    def test_anonymous_redirects(self):
        for name in ('dashboard_destination_list', 'dashboard_faq_list'):
            with self.subTest(route=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 302)

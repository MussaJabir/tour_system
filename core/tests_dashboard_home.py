"""
Phase 7.1 — Dashboard home tests.

Verifies the Operations Slate dashboard home:
- /dashboard/ requires staff auth
- Renders all 4 KPI cards, 2 chart canvases, both recent-activity tables
- Loads Chart.js (per-page, not global)
- View context exposes all required keys
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


def make_staff_user(username='staff', password='pw1234'):
    u = User.objects.create_user(username=username, email=f'{username}@example.com',
                                 password=password)
    u.is_staff = True
    u.save()
    return u


class DashboardHomeAccessTests(TestCase):

    def test_anonymous_redirects_to_login(self):
        response = self.client.get(reverse('dashboard_home'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response['Location'])

    def test_non_staff_redirects_to_login(self):
        u = User.objects.create_user(username='normie', email='n@x.com', password='pw')
        self.client.force_login(u)
        response = self.client.get(reverse('dashboard_home'))
        # @staff_member_required redirects to admin login
        self.assertEqual(response.status_code, 302)

    def test_staff_gets_200(self):
        self.client.force_login(make_staff_user())
        response = self.client.get(reverse('dashboard_home'))
        self.assertEqual(response.status_code, 200)


class DashboardHomeRenderTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.staff = make_staff_user()

    def setUp(self):
        self.client.force_login(self.staff)

    def test_uses_base_dashboard(self):
        response = self.client.get(reverse('dashboard_home'))
        self.assertTemplateUsed(response, 'backend/base_dashboard.html')
        self.assertTemplateUsed(response, 'core/dashboard/index.html')

    def test_renders_welcome_header(self):
        response = self.client.get(reverse('dashboard_home'))
        self.assertContains(response, 'Welcome back')
        self.assertContains(response, self.staff.username)

    def test_four_kpi_cards_present(self):
        response = self.client.get(reverse('dashboard_home'))
        for label in ('Inquiries · 30d', 'Bookings · 30d', 'Revenue · 30d', 'Conversion'):
            self.assertContains(response, label)

    def test_chart_canvases_present(self):
        response = self.client.get(reverse('dashboard_home'))
        self.assertContains(response, 'id="bookings-trend-chart"')
        self.assertContains(response, 'id="revenue-chart"')

    def test_chart_data_json_scripts_present(self):
        response = self.client.get(reverse('dashboard_home'))
        for json_id in ('booking-trend-labels', 'booking-trend-data',
                        'revenue-labels', 'revenue-data'):
            self.assertContains(response, f'id="{json_id}"')

    def test_chart_js_loaded(self):
        response = self.client.get(reverse('dashboard_home'))
        self.assertContains(response, 'chart.min.js')

    def test_recent_inquiries_table_present(self):
        response = self.client.get(reverse('dashboard_home'))
        self.assertContains(response, 'Recent inquiries')

    def test_recent_bookings_table_present(self):
        response = self.client.get(reverse('dashboard_home'))
        self.assertContains(response, 'Recent bookings')

    def test_action_queue_card_present(self):
        response = self.client.get(reverse('dashboard_home'))
        self.assertContains(response, 'Needs your attention')

    def test_catalog_card_present(self):
        response = self.client.get(reverse('dashboard_home'))
        self.assertContains(response, '>Catalog<')


class DashboardHomeContextTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.staff = make_staff_user()

    def setUp(self):
        self.client.force_login(self.staff)

    REQUIRED_KEYS = [
        'inquiries_30d', 'bookings_30d', 'revenue_30d', 'conversion_pct',
        'kpi_trends', 'booking_trend_labels', 'booking_trend_data',
        'revenue_labels', 'revenue_data',
        'recent_inquiries', 'recent_bookings',
        'pending_inquiries', 'pending_quotes', 'new_messages',
        'total_packages', 'total_destinations', 'total_activities', 'total_accommodations',
    ]

    def test_context_keys(self):
        response = self.client.get(reverse('dashboard_home'))
        for key in self.REQUIRED_KEYS:
            self.assertIn(key, response.context, f'missing context key: {key}')

    def test_booking_trend_arrays_have_30_days(self):
        response = self.client.get(reverse('dashboard_home'))
        self.assertEqual(len(response.context['booking_trend_labels']), 30)
        self.assertEqual(len(response.context['booking_trend_data']), 30)

    def test_counts_are_integers(self):
        response = self.client.get(reverse('dashboard_home'))
        for key in ('inquiries_30d', 'bookings_30d',
                    'pending_inquiries', 'pending_quotes', 'new_messages',
                    'total_packages', 'total_destinations'):
            self.assertIsInstance(response.context[key], int,
                                  f'{key} should be int, got {type(response.context[key])}')

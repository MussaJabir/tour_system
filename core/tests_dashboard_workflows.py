"""
Phase 7.5 — Special workflows smoke tests.

Confirms that the migrated confirm-pages and AI Assistant pages return
200 for staff and extend base_dashboard.html.
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


def make_staff_user(username='wfstaff', password='pw1234'):
    u = User.objects.create_user(
        username=username, email=f'{username}@example.com', password=password
    )
    u.is_staff = True
    u.save()
    return u


class AIAssistantDashboardTests(TestCase):

    URLS = [
        ('ai_assistant:home', []),
        ('ai_assistant:brochure_upload', []),
        ('ai_assistant:itinerary_generate', []),
        ('ai_assistant:route_optimize', []),
    ]

    @classmethod
    def setUpTestData(cls):
        cls.staff = make_staff_user()

    def setUp(self):
        self.client.force_login(self.staff)

    def test_all_ai_pages_return_200(self):
        for name, args in self.URLS:
            with self.subTest(route=name):
                response = self.client.get(reverse(name, args=args))
                self.assertEqual(response.status_code, 200,
                                 f"{name} returned {response.status_code}")

    def test_all_ai_pages_use_base_dashboard(self):
        for name, args in self.URLS:
            with self.subTest(route=name):
                response = self.client.get(reverse(name, args=args))
                self.assertTemplateUsed(response, 'backend/base_dashboard.html',
                                        msg_prefix=f"{name}: ")

    def test_anonymous_redirects(self):
        for name, args in self.URLS:
            with self.subTest(route=name):
                self.client.logout()
                response = self.client.get(reverse(name, args=args))
                self.assertEqual(response.status_code, 302)

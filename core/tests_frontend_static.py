"""
Phase 6.5 — Static + auth page tests.

Verifies:
- /about/             — new About Us page
- /faq/               — FAQ with accordion + category filter
- /dashboard/login/   — staff dashboard login page
- 404 rendering       — DEBUG must be False for handler404 to fire,
                         so we test by hitting a non-existent URL with
                         DEBUG=False and verifying the branded copy.
"""
from django.test import TestCase, override_settings
from django.urls import reverse

from core.models import FAQ


class AboutPageTests(TestCase):

    def test_about_returns_200(self):
        response = self.client.get(reverse('about_page'))
        self.assertEqual(response.status_code, 200)

    def test_about_uses_base_modern(self):
        response = self.client.get(reverse('about_page'))
        self.assertTemplateUsed(response, 'frontend/base_modern.html')
        self.assertTemplateUsed(response, 'core/public/about.html')

    def test_about_renders_key_sections(self):
        response = self.client.get(reverse('about_page'))
        for phrase in ('Our story', 'What we stand for', 'The team', 'Got a trip in mind'):
            self.assertContains(response, phrase)


class FaqPageTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        FAQ.objects.create(
            category='booking',
            question='How far in advance should I book?',
            answer='Most safaris should be booked 3–6 months ahead.',
            is_active=True,
            is_featured=True,
            order=1,
        )
        FAQ.objects.create(
            category='payment',
            question='What payment methods do you accept?',
            answer='Bank transfer, card, and M-Pesa.',
            is_active=True,
            order=2,
        )

    def test_faq_returns_200(self):
        response = self.client.get(reverse('faq_page'))
        self.assertEqual(response.status_code, 200)

    def test_faq_uses_base_modern(self):
        response = self.client.get(reverse('faq_page'))
        self.assertTemplateUsed(response, 'frontend/base_modern.html')

    def test_faq_renders_category_chips_and_questions(self):
        response = self.client.get(reverse('faq_page'))
        # Both questions present
        self.assertContains(response, 'How far in advance should I book?')
        self.assertContains(response, 'What payment methods do you accept?')
        # Category chips: "All" link + a category chip link
        self.assertContains(response, 'aria-label="FAQ categories"')
        # Each FAQ has an accordion button keyed by PK
        self.assertContains(response, 'openId =')
        # Still-stuck CTA
        self.assertContains(response, 'Ask a real human.')

    def test_faq_category_filter_narrows_results(self):
        response = self.client.get(reverse('faq_page'), {'category': 'booking'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'How far in advance should I book?')
        self.assertNotContains(response, 'What payment methods do you accept?')


class StaffLoginPageTests(TestCase):

    def test_login_returns_200(self):
        response = self.client.get(reverse('staff_login'))
        self.assertEqual(response.status_code, 200)

    def test_login_renders_form_and_brand_panel(self):
        response = self.client.get(reverse('staff_login'))
        self.assertContains(response, 'Welcome back.')
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password"')
        self.assertContains(response, 'Sign In')
        # Quote pull-line from the brand panel
        self.assertContains(response, "We don't run tours.")


@override_settings(DEBUG=False, ALLOWED_HOSTS=['*'])
class ErrorPageTests(TestCase):
    """404 / 500 templates render properly when invoked by Django's handlers."""

    def test_404_serves_branded_copy(self):
        response = self.client.get('/this-url-does-not-exist-anywhere/')
        self.assertEqual(response.status_code, 404)
        # Don't bother checking content for 500 (would need a forced server
        # error). The 404 should contain our copy.
        self.assertIn(b"That trail's overgrown.", response.content)

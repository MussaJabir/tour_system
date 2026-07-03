"""
WhatsApp click-to-chat — phone normalization, template tag, and page rendering.

Covers:
- normalize_whatsapp_number handles the phone formats customers actually type
- the whatsapp_url template tag builds correct wa.me links (and hides bad numbers)
- the floating button renders site-wide only when WHATSAPP_BUSINESS_NUMBER is set
- staff dashboard inquiry detail shows a "Reply on WhatsApp" link with the
  customer's normalized number
"""
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from core.models import SiteSettings
from core.templatetags.whatsapp_tags import whatsapp_url
from core.utils import normalize_whatsapp_number
from destinations.tests_homepage import make_package
from packages.models import BookingInquiry

User = get_user_model()


class SiteSettingsCacheCleanupMixin:
    """
    The SiteSettings singleton is cached in Redis, which the test runner
    shares with the dev server. Drop the key around every test so tests
    never read each other's (or the dev server's) cached row — and never
    leave a test-database object behind for the dev server to pick up.
    """

    def setUp(self):
        super().setUp()
        cache.delete(SiteSettings.CACHE_KEY)

    def tearDown(self):
        cache.delete(SiteSettings.CACHE_KEY)
        super().tearDown()


class NormalizeWhatsappNumberTests(TestCase):

    def test_international_with_plus(self):
        self.assertEqual(normalize_whatsapp_number('+255 744 123 456'), '255744123456')

    def test_international_with_double_zero(self):
        self.assertEqual(normalize_whatsapp_number('00255744123456'), '255744123456')

    def test_local_with_leading_zero(self):
        self.assertEqual(normalize_whatsapp_number('0744 123 456'), '255744123456')

    def test_local_without_leading_zero(self):
        self.assertEqual(normalize_whatsapp_number('744123456'), '255744123456')

    def test_formatting_noise_stripped(self):
        self.assertEqual(normalize_whatsapp_number('+255 (744) 123-456'), '255744123456')

    def test_non_tanzanian_international(self):
        self.assertEqual(normalize_whatsapp_number('+44 7911 123456'), '447911123456')

    def test_custom_default_country_code(self):
        self.assertEqual(
            normalize_whatsapp_number('0712345678', default_country_code='254'),
            '254712345678',
        )

    def test_empty_and_none(self):
        self.assertEqual(normalize_whatsapp_number(''), '')
        self.assertEqual(normalize_whatsapp_number(None), '')

    def test_too_short_rejected(self):
        self.assertEqual(normalize_whatsapp_number('0744123'), '')
        self.assertEqual(normalize_whatsapp_number('abc'), '')

    def test_too_long_rejected(self):
        self.assertEqual(normalize_whatsapp_number('+1234567890123456'), '')


class WhatsappUrlTagTests(TestCase):

    def test_plain_link(self):
        self.assertEqual(whatsapp_url('+255744123456'), 'https://wa.me/255744123456')

    def test_message_is_urlencoded(self):
        url = whatsapp_url('+255744123456', "Hi! I'm interested in the Serengeti tour.")
        self.assertTrue(url.startswith('https://wa.me/255744123456?text='))
        self.assertNotIn(' ', url)
        self.assertIn('Serengeti', url)

    def test_invalid_number_returns_empty(self):
        self.assertEqual(whatsapp_url('not-a-phone'), '')
        self.assertEqual(whatsapp_url('', 'hello'), '')


@override_settings(WHATSAPP_BUSINESS_NUMBER='+255700000001')
class FloatingButtonRenderTests(SiteSettingsCacheCleanupMixin, TestCase):

    def test_home_page_shows_floating_button(self):
        response = self.client.get(reverse('public_home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'wa.me/255700000001')
        self.assertContains(response, 'Chat with us on WhatsApp')

    def test_package_detail_prefills_package_name(self):
        package = make_package('Serengeti Migration Safari')
        response = self.client.get(
            reverse('packages:public_package_detail', args=[package.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'wa.me/255700000001')
        # Package name is urlencoded into the prefill text
        self.assertContains(response, 'Serengeti%20Migration%20Safari')

    @override_settings(WHATSAPP_BUSINESS_NUMBER='')
    def test_hidden_when_number_not_configured(self):
        response = self.client.get(reverse('public_home'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'wa.me/')


@override_settings(WHATSAPP_BUSINESS_NUMBER='+255700000001')
class DashboardWhatsappActionTests(SiteSettingsCacheCleanupMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.staff = User.objects.create_user(
            username='wastaff', email='wastaff@example.com',
            password='pw1234', is_staff=True,
        )
        cls.package = make_package('Ngorongoro Explorer')
        cls.inquiry = BookingInquiry.objects.create(
            base_package=cls.package,
            customer_name='Jane Doe',
            customer_email='jane@example.com',
            customer_phone='0744 123 456',
            prefer_whatsapp=True,
        )

    def setUp(self):
        self.client.login(username='wastaff', password='pw1234')

    def test_inquiry_detail_has_reply_on_whatsapp(self):
        response = self.client.get(
            reverse('packages:dashboard_inquiry_detail', args=[self.inquiry.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reply on WhatsApp')
        # Customer's local number normalized to international wa.me format
        self.assertContains(response, 'wa.me/255744123456')
        # Prefill references the inquiry
        self.assertContains(response, self.inquiry.inquiry_reference)

    def test_inquiry_detail_hides_button_for_unusable_phone(self):
        inquiry = BookingInquiry.objects.create(
            base_package=self.package,
            customer_name='No Phone',
            customer_email='nophone@example.com',
            customer_phone='n/a',
        )
        response = self.client.get(
            reverse('packages:dashboard_inquiry_detail', args=[inquiry.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Reply on WhatsApp')

    def test_inquiry_list_shows_whatsapp_preference_badge(self):
        response = self.client.get(reverse('packages:dashboard_inquiry_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Prefers WhatsApp')


class SiteSettingsModelTests(SiteSettingsCacheCleanupMixin, TestCase):

    def test_load_creates_singleton(self):
        self.assertEqual(SiteSettings.objects.count(), 0)
        obj = SiteSettings.load()
        self.assertEqual(obj.pk, 1)
        self.assertEqual(SiteSettings.objects.count(), 1)

    def test_save_enforces_single_row(self):
        SiteSettings.load()
        another = SiteSettings(whatsapp_number='+255744123456')
        another.save()
        self.assertEqual(SiteSettings.objects.count(), 1)
        self.assertEqual(SiteSettings.load().whatsapp_number, '+255744123456')

    def test_save_invalidates_cache(self):
        SiteSettings.load()  # primes the cache
        obj = SiteSettings.objects.get(pk=1)
        obj.whatsapp_number = '+255744999888'
        obj.save()
        self.assertEqual(SiteSettings.load().whatsapp_number, '+255744999888')


@override_settings(WHATSAPP_BUSINESS_NUMBER='+255700000001')
class WhatsappFallbackChainTests(SiteSettingsCacheCleanupMixin, TestCase):
    """Resolution order: dashboard Site Settings → env var → hidden."""

    def test_dashboard_value_overrides_env(self):
        SiteSettings(whatsapp_number='0744 555 666').save()
        response = self.client.get(reverse('public_home'))
        self.assertContains(response, 'wa.me/255744555666')
        self.assertNotContains(response, 'wa.me/255700000001')

    def test_env_used_when_dashboard_blank(self):
        SiteSettings.load()  # row exists, whatsapp_number blank
        response = self.client.get(reverse('public_home'))
        self.assertContains(response, 'wa.me/255700000001')

    @override_settings(WHATSAPP_BUSINESS_NUMBER='')
    def test_hidden_when_both_blank(self):
        response = self.client.get(reverse('public_home'))
        self.assertNotContains(response, 'wa.me/')


@override_settings(WHATSAPP_BUSINESS_NUMBER='')
class DashboardSettingsViewTests(SiteSettingsCacheCleanupMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.staff = User.objects.create_user(
            username='setstaff', email='setstaff@example.com',
            password='pw1234', is_staff=True,
        )
        cls.nonstaff = User.objects.create_user(
            username='plainuser', email='plain@example.com', password='pw1234',
        )

    def test_requires_staff(self):
        response = self.client.get(reverse('dashboard_settings'))
        self.assertEqual(response.status_code, 302)  # anonymous → login

        self.client.login(username='plainuser', password='pw1234')
        response = self.client.get(reverse('dashboard_settings'))
        self.assertEqual(response.status_code, 302)  # non-staff → blocked

    def test_staff_can_view_and_save(self):
        self.client.login(username='setstaff', password='pw1234')
        response = self.client.get(reverse('dashboard_settings'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'WhatsApp Number')

        response = self.client.post(
            reverse('dashboard_settings'),
            {'whatsapp_number': '0744 123 456'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SiteSettings.load().whatsapp_number, '0744 123 456')

        # The public site now uses the dashboard value
        response = self.client.get(reverse('public_home'))
        self.assertContains(response, 'wa.me/255744123456')

    def test_invalid_number_rejected(self):
        self.client.login(username='setstaff', password='pw1234')
        response = self.client.post(
            reverse('dashboard_settings'), {'whatsapp_number': 'not-a-phone'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'valid phone number')
        self.assertEqual(SiteSettings.load().whatsapp_number, '')

    def test_page_shows_live_status_with_effective_number(self):
        SiteSettings(whatsapp_number='+255744123456').save()
        self.client.login(username='setstaff', password='pw1234')
        response = self.client.get(reverse('dashboard_settings'))
        self.assertContains(response, 'Live')
        self.assertContains(response, 'wa.me/255744123456')

"""Tests for the branded, dashboard-editable contact reply email."""
from django.core import cache as cache_module
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.core import mail

from core.models import ContactMessage, SiteSettings


@override_settings(SITE_NAME='Enteipa Adventures',
                   EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class ContactReplyEmailTests(TestCase):

    def setUp(self):
        cache.delete(SiteSettings.CACHE_KEY)
        self.msg = ContactMessage.objects.create(
            name='Amina Juma', email='amina@example.com',
            subject='Safari in August', message='Interested in a Serengeti trip.',
        )

    def tearDown(self):
        cache.delete(SiteSettings.CACHE_KEY)

    def _send(self):
        from core.views import send_contact_reply_email
        send_contact_reply_email(self.msg, 'Yes! We can arrange that for you.')
        return mail.outbox[-1]

    def test_reply_is_branded_not_tour_management(self):
        sent = self._send()
        html = sent.alternatives[0][0]
        self.assertNotIn('Tour Management Team', html)
        self.assertNotIn('Tour Management Team', sent.body)
        self.assertIn('Enteipa Adventures', html)

    def test_default_signature_from_site_name(self):
        sent = self._send()
        self.assertIn('Enteipa Adventures Team', sent.alternatives[0][0])

    def test_custom_signature_from_dashboard(self):
        site = SiteSettings.load()
        site.email_signature = 'Warm regards,\nMussa — Enteipa Adventures, Arusha'
        site.save()
        sent = self._send()
        html = sent.alternatives[0][0]
        self.assertIn('Mussa — Enteipa Adventures, Arusha', html)
        # default sign-off no longer used
        self.assertNotIn('Enteipa Adventures Team', html)

    def test_reply_goes_to_customer_with_html_part(self):
        sent = self._send()
        self.assertEqual(sent.to, ['amina@example.com'])
        self.assertEqual(sent.alternatives[0][1], 'text/html')
        self.assertEqual(sent.subject, 'Re: Safari in August')

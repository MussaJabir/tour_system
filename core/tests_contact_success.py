"""Contact form success-state (PRG → confirmation panel) tests."""
from django.test import TestCase

from core.models import ContactMessage


class ContactSuccessFlowTests(TestCase):
    def _payload(self, **over):
        data = {
            'name': 'Mussa Jabir', 'email': 'test@example.com',
            'phone': '0744000000', 'subject': 'Safari question',
            'message': 'Hello, I would like a 5-day trip.', 'website': '',
        }
        data.update(over)
        return data

    def test_valid_post_redirects_to_sent_state(self):
        r = self.client.post('/contact/', self._payload())
        self.assertEqual(r.status_code, 302)
        self.assertIn('sent=1', r['Location'])
        self.assertTrue(ContactMessage.objects.filter(email='test@example.com').exists())

    def test_success_panel_greets_by_first_name_and_hides_form(self):
        self.client.post('/contact/', self._payload())
        r = self.client.get('/contact/?sent=1')
        body = r.content.decode()
        self.assertContains(r, 'Thank you, Mussa.')
        self.assertIn('reached our Arusha team', body)
        self.assertNotIn('Send Message', body)   # form replaced by panel

    def test_honeypot_filled_is_rejected(self):
        r = self.client.post('/contact/', self._payload(website='http://spam'))
        self.assertFalse(ContactMessage.objects.filter(email='test@example.com').exists())

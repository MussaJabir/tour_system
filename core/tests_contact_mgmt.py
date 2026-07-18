"""Tests for contact conversation thread + bulk message actions."""
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from core.models import ContactMessage, ContactReply, SiteSettings

User = get_user_model()


def _staff():
    u = User.objects.create_user(username='cmstaff', password='pw1234', is_staff=True)
    return u


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
                   SITE_NAME='Enteipa Adventures')
class ConversationThreadTests(TestCase):
    def setUp(self):
        cache.delete(SiteSettings.CACHE_KEY)
        self.staff = _staff()
        self.client.login(username='cmstaff', password='pw1234')
        self.msg = ContactMessage.objects.create(
            name='Amina', email='amina@example.com',
            subject='Trip', message='Hello there.',
        )

    def tearDown(self):
        cache.delete(SiteSettings.CACHE_KEY)

    def test_sending_reply_stores_it(self):
        url = reverse('dashboard_contact_detail', args=[self.msg.pk])
        resp = self.client.post(url, {
            'send_reply': '1',
            'reply_message': 'Thanks for reaching out, here are the details.',
            'mark_as_replied': 'on',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(self.msg.replies.count(), 1)
        reply = self.msg.replies.first()
        self.assertEqual(reply.sent_by, self.staff)
        self.assertIn('here are the details', reply.body)

    def test_thread_shows_on_detail_page(self):
        ContactReply.objects.create(
            contact_message=self.msg, body='Earlier reply text.', sent_by=self.staff,
        )
        resp = self.client.get(reverse('dashboard_contact_detail', args=[self.msg.pk]))
        self.assertContains(resp, 'Earlier reply text.')
        self.assertContains(resp, 'Conversation')


class BulkActionTests(TestCase):
    def setUp(self):
        self.staff = _staff()
        self.client.login(username='cmstaff', password='pw1234')
        self.m_read1 = ContactMessage.objects.create(name='R1', email='r1@x.com', message='m', status='read')
        self.m_read2 = ContactMessage.objects.create(name='R2', email='r2@x.com', message='m', status='read')
        self.m_new = ContactMessage.objects.create(name='N', email='n@x.com', message='m', status='new')

    def test_delete_selected(self):
        url = reverse('dashboard_contact_list')
        resp = self.client.post(url, {
            'bulk_action': 'delete_selected',
            'selected': [str(self.m_read1.pk), str(self.m_new.pk)],
        })
        self.assertEqual(resp.status_code, 302)
        remaining = set(ContactMessage.objects.values_list('pk', flat=True))
        self.assertEqual(remaining, {self.m_read2.pk})

    def test_delete_all_read(self):
        url = reverse('dashboard_contact_list')
        resp = self.client.post(url, {'bulk_action': 'delete_read'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(ContactMessage.objects.filter(status='read').count(), 0)
        # the 'new' one survives
        self.assertTrue(ContactMessage.objects.filter(pk=self.m_new.pk).exists())

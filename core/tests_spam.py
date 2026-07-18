"""Honeypot anti-spam tests for the public contact + inquiry forms."""
from django.test import TestCase

from core.forms import ContactForm


def _valid_contact_data(**overrides):
    data = {
        'name': 'Jane Traveller',
        'email': 'jane@example.com',
        'phone': '+255700000000',
        'subject': 'Serengeti trip in August',
        'message': 'Hi, I would like a 5-day Serengeti safari for two people in August.',
        'website': '',  # honeypot left empty (as a human would)
    }
    data.update(overrides)
    return data


class ContactHoneypotTests(TestCase):

    def test_human_submission_passes(self):
        form = ContactForm(data=_valid_contact_data())
        self.assertTrue(form.is_valid(), form.errors)

    def test_bot_filling_honeypot_is_rejected(self):
        form = ContactForm(data=_valid_contact_data(website='http://spam.example'))
        self.assertFalse(form.is_valid())
        self.assertIn('website', form.errors)

    def test_honeypot_field_exists_and_is_optional_for_humans(self):
        # Field present so the template can render it, but not required.
        form = ContactForm()
        self.assertIn('website', form.fields)
        self.assertFalse(form.fields['website'].required)


class InquiryHoneypotTests(TestCase):

    def test_inquiry_form_has_honeypot(self):
        from packages.forms import BookingInquiryForm
        form = BookingInquiryForm()
        self.assertIn('website', form.fields)

    def test_inquiry_bot_rejected(self):
        from packages.forms import BookingInquiryForm
        # Even with other fields missing, a filled honeypot must invalidate.
        form = BookingInquiryForm(data={'website': 'http://spam.example'})
        self.assertFalse(form.is_valid())
        self.assertIn('website', form.errors)

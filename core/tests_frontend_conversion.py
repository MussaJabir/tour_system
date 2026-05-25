"""
Phase 6.4 — Conversion flow tests.

Verifies the public-facing conversion pages:
- /contact/         — split layout with form + info
- /inquiry/         — 4-step wizard (single POST)
- /inquiry/<pkg>/   — wizard pre-bound to a package
- /inquiry/success/<ref>/ — confirmation page
"""
from django.test import TestCase
from django.urls import reverse

from destinations.tests_homepage import make_package
from packages.models import BookingInquiry


class ContactPageTests(TestCase):

    def test_contact_returns_200(self):
        response = self.client.get(reverse('contact_page'))
        self.assertEqual(response.status_code, 200)

    def test_contact_uses_base_modern(self):
        response = self.client.get(reverse('contact_page'))
        self.assertTemplateUsed(response, 'frontend/base_modern.html')

    def test_contact_renders_form_and_info(self):
        response = self.client.get(reverse('contact_page'))
        self.assertContains(response, 'Drop us a line')
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="subject"')
        self.assertContains(response, 'name="message"')
        # Info column
        self.assertContains(response, 'What to expect')
        self.assertContains(response, 'contact-map')


class InquiryWizardTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.pkg = make_package("Serengeti Classic")

    def test_inquiry_generic_returns_200(self):
        response = self.client.get(reverse('packages:inquiry_create'))
        self.assertEqual(response.status_code, 200)

    def test_inquiry_with_package_returns_200(self):
        response = self.client.get(
            reverse('packages:inquiry_create_package', args=[self.pkg.slug])
        )
        self.assertEqual(response.status_code, 200)

    def test_inquiry_uses_base_modern(self):
        response = self.client.get(reverse('packages:inquiry_create'))
        self.assertTemplateUsed(response, 'frontend/base_modern.html')

    def test_inquiry_renders_4_steps_progress(self):
        response = self.client.get(reverse('packages:inquiry_create'))
        for step_label in ('01', '02', '03', '04'):
            self.assertContains(response, step_label)
        self.assertContains(response, 'Step 1')
        self.assertContains(response, 'Submit Inquiry')

    def test_inquiry_renders_all_field_names_in_single_form(self):
        """All form fields must be present in the DOM for the single POST."""
        response = self.client.get(reverse('packages:inquiry_create'))
        for fname in ('customer_name', 'customer_email', 'customer_phone',
                      'number_of_adults', 'preferred_travel_date',
                      'special_requests'):
            self.assertContains(response, f'name="{fname}"',
                                msg_prefix=f"missing field: {fname}")

    def test_inquiry_with_package_prefills_hidden_input(self):
        response = self.client.get(
            reverse('packages:inquiry_create_package', args=[self.pkg.slug])
        )
        self.assertContains(
            response,
            f'name="base_package" value="{self.pkg.pk}"',
        )


class InquirySuccessTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.inquiry = BookingInquiry.objects.create(
            customer_name='Test User',
            customer_email='test@example.com',
            number_of_adults=2,
            preferred_travel_date='2026-09-15',
        )

    def test_success_returns_200(self):
        response = self.client.get(
            reverse('packages:inquiry_success', args=[self.inquiry.inquiry_reference])
        )
        self.assertEqual(response.status_code, 200)

    def test_success_uses_base_modern(self):
        response = self.client.get(
            reverse('packages:inquiry_success', args=[self.inquiry.inquiry_reference])
        )
        self.assertTemplateUsed(response, 'frontend/base_modern.html')

    def test_success_shows_reference_and_next_steps(self):
        response = self.client.get(
            reverse('packages:inquiry_success', args=[self.inquiry.inquiry_reference])
        )
        self.assertContains(response, self.inquiry.inquiry_reference)
        self.assertContains(response, 'Inquiry received')
        self.assertContains(response, 'Draft itinerary')
        self.assertContains(response, self.inquiry.customer_email)

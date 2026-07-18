"""Tests for the custom-package send email (500 fix) + day-image copy."""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from packages.models import (
    PackageItinerary, BookingInquiry, CustomPackage, CustomPackageItinerary,
)
from packages.tests import make_package
from destinations.tests_homepage import make_destination
from core.tests_frontend_listings import make_accommodation

User = get_user_model()


def _custom_package(pkg, inquiry):
    return CustomPackage.objects.create(
        custom_reference='CUST-TEST-00001',
        inquiry=inquiry,
        base_package=pkg,
        name='Custom Serengeti',
        short_description='A tailored trip.',
        description='Full details.',
        duration_days=3,
        duration_nights=2,
        original_price=Decimal('3000'),
        adjusted_price=Decimal('2800'),
    )


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
                   SITE_URL='https://enteipa.com', SITE_NAME='Enteipa Adventures')
class CustomPackageSendEmailTests(TestCase):
    def setUp(self):
        self.pkg = make_package()
        self.inquiry = BookingInquiry.objects.create(
            base_package=self.pkg, customer_name='Amina',
            customer_email='amina@example.com', customer_phone='0744123456',
        )
        self.cp = _custom_package(self.pkg, self.inquiry)

    def test_send_does_not_raise_and_uses_correct_link(self):
        from packages.emails import send_custom_package_to_client
        ok = send_custom_package_to_client(self.cp)  # would raise before the fix
        self.assertTrue(ok)
        self.assertEqual(len(mail.outbox), 1)
        sent = mail.outbox[0]
        self.assertEqual(sent.to, ['amina@example.com'])
        html = sent.alternatives[0][0]
        self.assertIn(f'/custom/{self.cp.access_token}/', html)
        self.assertNotIn('/packages/custom/', html)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
                   DEFAULT_FROM_EMAIL='Enteipa Adventures <info@enteipa.com>',
                   SITE_NAME='Enteipa Adventures')
class InquiryConfirmationEmailTests(TestCase):
    def test_contact_line_uses_our_email_not_customers(self):
        pkg = make_package()
        inquiry = BookingInquiry.objects.create(
            base_package=pkg, customer_name='Amina',
            customer_email='amina@example.com', customer_phone='0744123456',
        )
        from packages.emails import send_inquiry_confirmation_email
        send_inquiry_confirmation_email(inquiry)
        html = mail.outbox[0].alternatives[0][0]
        self.assertIn('contact us at info@enteipa.com', html)
        self.assertNotIn('contact us at amina@example.com', html)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
                   SITE_URL='https://enteipa.com', SITE_NAME='Enteipa Adventures')
class CustomPackageExpiryInEmailTests(TestCase):
    def test_expiry_date_renders(self):
        from datetime import timedelta
        from django.utils import timezone
        pkg = make_package()
        inquiry = BookingInquiry.objects.create(
            base_package=pkg, customer_name='X', customer_email='x@e.com',
            customer_phone='0744000000',
        )
        cp = _custom_package(pkg, inquiry)
        cp.expires_at = timezone.now() + timedelta(days=7)
        cp.save()
        from packages.emails import send_custom_package_to_client
        send_custom_package_to_client(cp)
        html = mail.outbox[0].alternatives[0][0]
        self.assertNotIn('valid until .', html)           # not the empty bug
        self.assertIn(str(cp.expires_at.year), html)      # the date rendered


class CustomItineraryCopyImageTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user('cpstaff', password='pw1234', is_staff=True)
        self.client.login(username='cpstaff', password='pw1234')
        self.pkg = make_package()
        self.dest = make_destination('Serengeti CP')
        self.acc = make_accommodation('Sample Lodge CP', self.dest)
        self.acc.featured_image = 'accommodations/lodge.jpg'
        self.acc.save()
        PackageItinerary.objects.create(
            package=self.pkg, day_number=1, end_day_number=1,
            title='Day 1', description='Arrive', accommodation=self.acc, order=0,
        )
        self.inquiry = BookingInquiry.objects.create(
            base_package=self.pkg, customer_name='X',
            customer_email='x@e.com', customer_phone='0744000000',
        )
        self.cp = _custom_package(self.pkg, self.inquiry)

    def test_copy_references_accommodation_image_path(self):
        url = reverse('packages:dashboard_custom_itinerary_copy', args=[self.cp.pk])
        resp = self.client.post(url)
        self.assertIn(resp.status_code, (302, 200))
        day = self.cp.itinerary_days.first()
        self.assertIsNotNone(day)
        # Path referenced (not a duplicated file)
        self.assertEqual(day.featured_image.name, 'accommodations/lodge.jpg')

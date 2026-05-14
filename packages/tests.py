from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Package, Booking, Passenger, Payment


def make_package(**kwargs):
    defaults = dict(
        name='Test Safari',
        slug='test-safari',
        short_description='A test safari',
        description='Full description',
        duration_days=5,
        duration_nights=4,
        price_per_person=Decimal('1200.00'),
        availability_status='available',
        is_active=True,
    )
    defaults.update(kwargs)
    return Package.objects.create(**defaults)


def make_booking(package, **kwargs):
    defaults = dict(
        package=package,
        departure_date='2026-08-01',
        num_adults=2,
        num_children=0,
        quoted_price=Decimal('2400.00'),
        deposit_amount=Decimal('600.00'),
        currency='USD',
        status='pending_deposit',
    )
    defaults.update(kwargs)
    return Booking.objects.create(**defaults)


class BookingModelTests(TestCase):
    def setUp(self):
        self.package = make_package()
        self.booking = make_booking(self.package)

    def test_booking_reference_auto_generated(self):
        self.assertTrue(self.booking.booking_reference.startswith('BKG-'))

    def test_booking_reference_unique(self):
        b2 = make_booking(self.package)
        self.assertNotEqual(self.booking.booking_reference, b2.booking_reference)

    def test_total_travelers(self):
        self.assertEqual(self.booking.total_travelers, 2)

    def test_total_paid_zero_initially(self):
        self.assertEqual(self.booking.total_paid, Decimal('0'))

    def test_balance_due_equals_quoted_price_when_no_payments(self):
        self.assertEqual(self.booking.balance_due, Decimal('2400.00'))

    def test_is_fully_paid_false_initially(self):
        self.assertFalse(self.booking.is_fully_paid)

    def test_is_fully_paid_true_after_full_payment(self):
        Payment.objects.create(
            booking=self.booking,
            payment_type='full',
            amount=Decimal('2400.00'),
            currency='USD',
            payment_method='bank_transfer',
            status='confirmed',
        )
        self.assertTrue(self.booking.is_fully_paid)

    def test_total_paid_excludes_pending_payments(self):
        Payment.objects.create(
            booking=self.booking,
            payment_type='deposit',
            amount=Decimal('600.00'),
            currency='USD',
            payment_method='cash',
            status='pending',
        )
        self.assertEqual(self.booking.total_paid, Decimal('0'))

    def test_status_badge_color_mapping(self):
        self.booking.status = 'confirmed'
        self.assertEqual(self.booking.status_badge_color, 'success')
        self.booking.status = 'cancelled'
        self.assertEqual(self.booking.status_badge_color, 'secondary')
        self.booking.status = 'pending_deposit'
        self.assertEqual(self.booking.status_badge_color, 'warning')

    def test_str_representation(self):
        self.assertIn(self.booking.booking_reference, str(self.booking))
        self.assertIn('Test Safari', str(self.booking))


class PassengerModelTests(TestCase):
    def setUp(self):
        package = make_package()
        self.booking = make_booking(package)
        self.passenger = Passenger.objects.create(
            booking=self.booking,
            first_name='Jane',
            last_name='Doe',
            is_lead_passenger=True,
        )

    def test_full_name_property(self):
        self.assertEqual(self.passenger.full_name, 'Jane Doe')

    def test_str_includes_lead(self):
        self.assertIn('Lead', str(self.passenger))


class BookingDashboardViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff = User.objects.create_user(
            username='staff', password='pass', is_staff=True
        )
        self.regular = User.objects.create_user(
            username='customer', password='pass', is_staff=False
        )
        self.package = make_package()
        self.booking = make_booking(self.package)

    # --- Auth gates ---

    def test_booking_list_redirects_anonymous(self):
        response = self.client.get(reverse('packages:dashboard_booking_list'))
        self.assertIn(response.status_code, [301, 302])
        self.assertIn('/dashboard/login/', response['Location'])

    def test_booking_list_blocks_non_staff(self):
        self.client.login(username='customer', password='pass')
        response = self.client.get(reverse('packages:dashboard_booking_list'))
        self.assertIn(response.status_code, [301, 302])

    def test_booking_list_accessible_by_staff(self):
        self.client.login(username='staff', password='pass')
        response = self.client.get(reverse('packages:dashboard_booking_list'))
        self.assertEqual(response.status_code, 200)

    def test_booking_detail_accessible_by_staff(self):
        self.client.login(username='staff', password='pass')
        response = self.client.get(
            reverse('packages:dashboard_booking_detail', args=[self.booking.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_booking_create_get_accessible_by_staff(self):
        self.client.login(username='staff', password='pass')
        response = self.client.get(reverse('packages:dashboard_booking_create'))
        self.assertEqual(response.status_code, 200)

    def test_booking_edit_get_accessible_by_staff(self):
        self.client.login(username='staff', password='pass')
        response = self.client.get(
            reverse('packages:dashboard_booking_edit', args=[self.booking.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_booking_cancel_get_shows_confirm_page(self):
        self.client.login(username='staff', password='pass')
        response = self.client.get(
            reverse('packages:dashboard_booking_cancel', args=[self.booking.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_booking_cancel_post_sets_cancelled(self):
        self.client.login(username='staff', password='pass')
        self.client.post(
            reverse('packages:dashboard_booking_cancel', args=[self.booking.pk])
        )
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'cancelled')

    # --- Passenger flow ---

    def test_passenger_add_post_creates_passenger(self):
        self.client.login(username='staff', password='pass')
        url = reverse('packages:dashboard_passenger_add', args=[self.booking.pk])
        self.client.post(url, {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'passport_number': 'AB123456',
            'nationality': 'British',
            'is_lead_passenger': True,
        })
        self.assertEqual(self.booking.passengers.count(), 1)

    def test_passenger_delete_removes_record(self):
        self.client.login(username='staff', password='pass')
        passenger = Passenger.objects.create(
            booking=self.booking, first_name='Bob', last_name='Jones'
        )
        self.client.post(
            reverse('packages:dashboard_passenger_delete', args=[passenger.pk])
        )
        self.assertEqual(self.booking.passengers.count(), 0)

    # --- Payment flow ---

    def test_payment_record_post_creates_payment(self):
        self.client.login(username='staff', password='pass')
        url = reverse('packages:dashboard_payment_record', args=[self.booking.pk])
        self.client.post(url, {
            'payment_type': 'deposit',
            'amount': '600.00',
            'currency': 'USD',
            'payment_method': 'bank_transfer',
            'status': 'confirmed',
            'reference_number': 'TXN-001',
            'notes': '',
        })
        self.assertEqual(self.booking.payments.count(), 1)

    def test_payment_record_deposit_advances_booking_status(self):
        self.client.login(username='staff', password='pass')
        url = reverse('packages:dashboard_payment_record', args=[self.booking.pk])
        self.client.post(url, {
            'payment_type': 'deposit',
            'amount': '600.00',
            'currency': 'USD',
            'payment_method': 'cash',
            'status': 'confirmed',
            'reference_number': '',
            'notes': '',
        })
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'deposit_paid')

    def test_payment_delete_removes_record(self):
        self.client.login(username='staff', password='pass')
        payment = Payment.objects.create(
            booking=self.booking,
            payment_type='deposit',
            amount=Decimal('600.00'),
            currency='USD',
            payment_method='cash',
            status='confirmed',
        )
        self.client.post(
            reverse('packages:dashboard_payment_delete', args=[payment.pk])
        )
        self.assertEqual(self.booking.payments.count(), 0)

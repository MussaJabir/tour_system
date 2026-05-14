from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import Package, Booking, Passenger, Payment, Departure


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


import datetime
from django.utils import timezone


def make_departure(package, days_from_now=30, max_seats=10, **kwargs):
    defaults = dict(
        departure_date=timezone.now().date() + datetime.timedelta(days=days_from_now),
        max_seats=max_seats,
        status='available',
    )
    defaults.update(kwargs)
    return Departure.objects.create(package=package, **defaults)


class DepartureModelTests(TestCase):
    def setUp(self):
        self.package = make_package()
        self.departure = make_departure(self.package)

    def test_seats_remaining_initial(self):
        self.assertEqual(self.departure.seats_remaining, 10)

    def test_is_available_true_when_seats_and_status_available(self):
        self.assertTrue(self.departure.is_available)

    def test_lock_seat_increments_booked(self):
        self.departure.lock_seat()
        self.departure.refresh_from_db()
        self.assertEqual(self.departure.booked_seats, 1)
        self.assertEqual(self.departure.seats_remaining, 9)

    def test_lock_seat_sets_sold_out_when_full(self):
        dep = make_departure(self.package, days_from_now=60, max_seats=1)
        dep.lock_seat()
        dep.refresh_from_db()
        self.assertEqual(dep.status, 'sold_out')
        self.assertFalse(dep.is_available)

    def test_release_seat_decrements_booked(self):
        self.departure.booked_seats = 3
        self.departure.save()
        self.departure.release_seat()
        self.departure.refresh_from_db()
        self.assertEqual(self.departure.booked_seats, 2)

    def test_release_seat_restores_available_from_sold_out(self):
        self.departure.booked_seats = 10
        self.departure.status = 'sold_out'
        self.departure.save()
        self.departure.release_seat()
        self.departure.refresh_from_db()
        self.assertEqual(self.departure.status, 'available')

    def test_is_available_false_when_sold_out(self):
        self.departure.status = 'sold_out'
        self.departure.save()
        self.assertFalse(self.departure.is_available)

    def test_str_includes_package_and_date(self):
        s = str(self.departure)
        self.assertIn('Test Safari', s)

    def test_unique_per_package_date(self):
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Departure.objects.create(
                package=self.package,
                departure_date=self.departure.departure_date,
                max_seats=5,
            )


class BookingLocksSeatOnCreate(TestCase):
    def setUp(self):
        self.package = make_package()
        self.departure = make_departure(self.package)

    def test_booking_locks_departure_seat(self):
        make_booking(self.package, departure=self.departure)
        self.departure.refresh_from_db()
        self.assertEqual(self.departure.booked_seats, 1)

    def test_booking_cancel_releases_seat(self):
        booking = make_booking(self.package, departure=self.departure)
        self.departure.refresh_from_db()
        self.assertEqual(self.departure.booked_seats, 1)
        booking.cancel()
        self.departure.refresh_from_db()
        self.assertEqual(self.departure.booked_seats, 0)
        self.assertEqual(booking.status, 'cancelled')

    def test_booking_without_departure_does_not_error(self):
        booking = make_booking(self.package)
        self.assertIsNone(booking.departure)
        booking.cancel()
        self.assertEqual(booking.status, 'cancelled')


class DepartureDashboardViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff = User.objects.create_user(
            username='depart_staff', password='pass', is_staff=True
        )
        self.regular = User.objects.create_user(
            username='depart_cust', password='pass', is_staff=False
        )
        self.package = make_package(name='Depart Test Safari', slug='depart-test-safari')
        self.departure = make_departure(self.package)

    def test_departure_list_blocks_anonymous(self):
        url = reverse('packages:dashboard_departure_list', args=[self.package.pk])
        response = self.client.get(url)
        self.assertIn(response.status_code, [301, 302])

    def test_departure_list_blocks_non_staff(self):
        self.client.login(username='depart_cust', password='pass')
        url = reverse('packages:dashboard_departure_list', args=[self.package.pk])
        response = self.client.get(url)
        self.assertIn(response.status_code, [301, 302])

    def test_departure_list_accessible_by_staff(self):
        self.client.login(username='depart_staff', password='pass')
        url = reverse('packages:dashboard_departure_list', args=[self.package.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_departure_create_get(self):
        self.client.login(username='depart_staff', password='pass')
        url = reverse('packages:dashboard_departure_create', args=[self.package.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_departure_create_post(self):
        self.client.login(username='depart_staff', password='pass')
        url = reverse('packages:dashboard_departure_create', args=[self.package.pk])
        future = (timezone.now().date() + datetime.timedelta(days=90)).isoformat()
        response = self.client.post(url, {
            'departure_date': future,
            'max_seats': 8,
            'status': 'available',
            'notes': '',
        })
        self.assertIn(response.status_code, [301, 302])
        self.assertEqual(Departure.objects.filter(package=self.package).count(), 2)

    def test_departure_edit_post(self):
        self.client.login(username='depart_staff', password='pass')
        url = reverse('packages:dashboard_departure_edit', args=[self.departure.pk])
        response = self.client.post(url, {
            'departure_date': self.departure.departure_date.isoformat(),
            'max_seats': 20,
            'status': 'available',
            'notes': 'Updated',
        })
        self.assertIn(response.status_code, [301, 302])
        self.departure.refresh_from_db()
        self.assertEqual(self.departure.max_seats, 20)

    def test_departure_delete_blocks_if_booked(self):
        self.client.login(username='depart_staff', password='pass')
        self.departure.booked_seats = 2
        self.departure.save()
        url = reverse('packages:dashboard_departure_delete', args=[self.departure.pk])
        self.client.post(url)
        self.assertTrue(Departure.objects.filter(pk=self.departure.pk).exists())

    def test_departure_delete_succeeds_when_no_bookings(self):
        self.client.login(username='depart_staff', password='pass')
        url = reverse('packages:dashboard_departure_delete', args=[self.departure.pk])
        self.client.post(url)
        self.assertFalse(Departure.objects.filter(pk=self.departure.pk).exists())


# ============================================================================
# CUSTOMER API TESTS
# ============================================================================

from .models import SavedPackage


class CustomerBookingAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        from rest_framework.authtoken.models import Token
        self.user = User.objects.create_user(
            username='flutter_user', email='customer@test.com', password='pass',
        )
        self.token = Token.objects.create(user=self.user)
        self.auth = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

        self.package = make_package(name='Customer Package', slug='customer-package')

        from packages.models import BookingInquiry
        self.inquiry = BookingInquiry.objects.create(
            customer_name='Test Customer',
            customer_email='customer@test.com',
            customer_phone='255700000000',
            number_of_adults=2,
        )
        self.booking = make_booking(
            self.package,
            inquiry=self.inquiry,
            status='confirmed',
        )

    def test_booking_list_requires_auth(self):
        response = self.client.get('/api/v1/customer/bookings/')
        self.assertEqual(response.status_code, 401)

    def test_booking_list_returns_own_bookings(self):
        response = self.client.get('/api/v1/customer/bookings/', **self.auth)
        self.assertEqual(response.status_code, 200)
        refs = [b['booking_reference'] for b in response.json()]
        self.assertIn(self.booking.booking_reference, refs)

    def test_booking_list_excludes_other_customers(self):
        other_user = User.objects.create_user(
            username='other', email='other@test.com', password='pass',
        )
        from rest_framework.authtoken.models import Token
        other_token = Token.objects.create(user=other_user)
        response = self.client.get(
            '/api/v1/customer/bookings/',
            **{'HTTP_AUTHORIZATION': f'Token {other_token.key}'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_booking_detail_returns_passengers_and_payments(self):
        from packages.models import Passenger, Payment
        Passenger.objects.create(
            booking=self.booking, first_name='Alice', last_name='Doe', is_lead_passenger=True,
        )
        response = self.client.get(
            f'/api/v1/customer/bookings/{self.booking.booking_reference}/',
            **self.auth,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['booking_reference'], self.booking.booking_reference)
        self.assertEqual(len(data['passengers']), 1)

    def test_booking_detail_forbidden_for_other_user(self):
        other_user = User.objects.create_user(username='thief', email='thief@x.com', password='pass')
        from rest_framework.authtoken.models import Token
        other_token = Token.objects.create(user=other_user)
        response = self.client.get(
            f'/api/v1/customer/bookings/{self.booking.booking_reference}/',
            **{'HTTP_AUTHORIZATION': f'Token {other_token.key}'},
        )
        self.assertEqual(response.status_code, 404)


class CustomerInquiryAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        from rest_framework.authtoken.models import Token
        self.user = User.objects.create_user(
            username='inq_user', email='inq@test.com', password='pass',
        )
        self.token = Token.objects.create(user=self.user)
        self.auth = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

        self.package = make_package(name='Inquiry Package', slug='inquiry-package')
        from packages.models import BookingInquiry
        self.inquiry = BookingInquiry.objects.create(
            customer_name='Inq Customer',
            customer_email='inq@test.com',
            customer_phone='255700000001',
            number_of_adults=2,
            base_package=self.package,
        )

    def test_inquiry_list_requires_auth(self):
        response = self.client.get('/api/v1/customer/inquiries/')
        self.assertEqual(response.status_code, 401)

    def test_inquiry_list_returns_own_inquiries(self):
        response = self.client.get('/api/v1/customer/inquiries/', **self.auth)
        self.assertEqual(response.status_code, 200)
        refs = [i['inquiry_reference'] for i in response.json()]
        self.assertIn(self.inquiry.inquiry_reference, refs)

    def test_inquiry_detail_returns_package_name(self):
        response = self.client.get(
            f'/api/v1/customer/inquiries/{self.inquiry.inquiry_reference}/',
            **self.auth,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['package_name'], 'Inquiry Package')

    def test_inquiry_detail_404_for_other_user(self):
        other_user = User.objects.create_user(username='spy', email='spy@x.com', password='pass')
        from rest_framework.authtoken.models import Token
        other_token = Token.objects.create(user=other_user)
        response = self.client.get(
            f'/api/v1/customer/inquiries/{self.inquiry.inquiry_reference}/',
            **{'HTTP_AUTHORIZATION': f'Token {other_token.key}'},
        )
        self.assertEqual(response.status_code, 404)


class CustomerSavedPackageAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        from rest_framework.authtoken.models import Token
        self.user = User.objects.create_user(
            username='saver', email='saver@test.com', password='pass',
        )
        self.token = Token.objects.create(user=self.user)
        self.auth = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}
        self.package = make_package(name='Saveable Package', slug='saveable-package')

    def test_saved_list_requires_auth(self):
        response = self.client.get('/api/v1/customer/saved-packages/')
        self.assertEqual(response.status_code, 401)

    def test_save_package_creates_entry(self):
        response = self.client.post(
            f'/api/v1/customer/packages/{self.package.slug}/save/',
            **self.auth,
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(SavedPackage.objects.filter(user=self.user, package=self.package).exists())

    def test_save_package_idempotent(self):
        SavedPackage.objects.create(user=self.user, package=self.package)
        response = self.client.post(
            f'/api/v1/customer/packages/{self.package.slug}/save/',
            **self.auth,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SavedPackage.objects.filter(user=self.user).count(), 1)

    def test_unsave_package(self):
        SavedPackage.objects.create(user=self.user, package=self.package)
        response = self.client.delete(
            f'/api/v1/customer/packages/{self.package.slug}/save/',
            **self.auth,
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(SavedPackage.objects.filter(user=self.user, package=self.package).exists())

    def test_unsave_package_not_saved_returns_404(self):
        response = self.client.delete(
            f'/api/v1/customer/packages/{self.package.slug}/save/',
            **self.auth,
        )
        self.assertEqual(response.status_code, 404)

    def test_saved_list_returns_saved_packages(self):
        SavedPackage.objects.create(user=self.user, package=self.package)
        response = self.client.get('/api/v1/customer/saved-packages/', **self.auth)
        self.assertEqual(response.status_code, 200)
        names = [s['package']['name'] for s in response.json()]
        self.assertIn('Saveable Package', names)

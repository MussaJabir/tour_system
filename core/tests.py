from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class StaffAuthGateTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='staff', password='pass123', is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='customer', password='pass123', is_staff=False
        )
        self.dashboard_urls = [
            reverse('dashboard_home'),
            reverse('dashboard_contact_list'),
            reverse('dashboard_newsletter_list'),
            reverse('dashboard_faq_list'),
            reverse('dashboard_testimonial_list'),
        ]

    def test_dashboard_redirects_anonymous_to_login(self):
        for url in self.dashboard_urls:
            response = self.client.get(url)
            self.assertIn(response.status_code, [301, 302], msg=f"{url} did not redirect anonymous user")
            self.assertIn('/dashboard/login/', response['Location'], msg=f"{url} did not redirect to staff login")

    def test_dashboard_blocks_non_staff_user(self):
        self.client.login(username='customer', password='pass123')
        for url in self.dashboard_urls:
            response = self.client.get(url)
            self.assertIn(response.status_code, [301, 302], msg=f"{url} allowed non-staff user")

    def test_dashboard_accessible_to_staff(self):
        self.client.login(username='staff', password='pass123')
        response = self.client.get(reverse('dashboard_home'))
        self.assertEqual(response.status_code, 200)


class StaffLoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='staff', password='pass123', is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='customer', password='pass123', is_staff=False
        )

    def test_login_page_renders(self):
        response = self.client.get(reverse('staff_login'))
        self.assertEqual(response.status_code, 200)

    def test_valid_staff_login_redirects_to_dashboard(self):
        response = self.client.post(reverse('staff_login'), {
            'username': 'staff',
            'password': 'pass123',
        })
        self.assertRedirects(response, reverse('dashboard_home'))

    def test_non_staff_login_shows_error(self):
        response = self.client.post(reverse('staff_login'), {
            'username': 'customer',
            'password': 'pass123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'staff access')

    def test_invalid_credentials_shows_error(self):
        response = self.client.post(reverse('staff_login'), {
            'username': 'staff',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')

    def test_authenticated_staff_redirected_away_from_login(self):
        self.client.login(username='staff', password='pass123')
        response = self.client.get(reverse('staff_login'))
        self.assertRedirects(response, reverse('dashboard_home'))

    def test_logout_requires_post(self):
        self.client.login(username='staff', password='pass123')
        response = self.client.get(reverse('staff_logout'))
        self.assertEqual(response.status_code, 405)

    def test_logout_post_clears_session(self):
        self.client.login(username='staff', password='pass123')
        self.client.post(reverse('staff_logout'))
        response = self.client.get(reverse('dashboard_home'))
        self.assertIn(response.status_code, [301, 302])

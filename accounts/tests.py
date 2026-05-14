from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

User = get_user_model()


def make_user(**kwargs):
    defaults = dict(username='testuser', email='test@example.com', password='testpass99')
    defaults.update(kwargs)
    return User.objects.create_user(**defaults)


class RegistrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('api_register')

    def test_register_creates_user(self):
        res = self.client.post(self.url, {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass99',
            'password_confirm': 'newpass99',
        }, format='json')
        self.assertEqual(res.status_code, 201)
        self.assertIn('token', res.data)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_password_mismatch_returns_400(self):
        res = self.client.post(self.url, {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'pass1',
            'password_confirm': 'pass2',
        }, format='json')
        self.assertEqual(res.status_code, 400)

    def test_register_duplicate_username_returns_400(self):
        make_user(username='taken')
        res = self.client.post(self.url, {
            'username': 'taken',
            'email': 'other@example.com',
            'password': 'pass1234',
            'password_confirm': 'pass1234',
        }, format='json')
        self.assertEqual(res.status_code, 400)


class LoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('api_login')
        self.user = make_user()

    def test_login_valid_credentials_returns_token(self):
        res = self.client.post(self.url, {
            'username': 'testuser',
            'password': 'testpass99',
        }, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertIn('token', res.data)
        self.assertIn('user', res.data)

    def test_login_wrong_password_returns_400(self):
        res = self.client.post(self.url, {
            'username': 'testuser',
            'password': 'wrongpass',
        }, format='json')
        self.assertEqual(res.status_code, 400)

    def test_login_unknown_user_returns_400(self):
        res = self.client.post(self.url, {
            'username': 'nobody',
            'password': 'anything',
        }, format='json')
        self.assertEqual(res.status_code, 400)


class LogoutTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = make_user()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_logout_deletes_token(self):
        res = self.client.post(reverse('api_logout'))
        self.assertEqual(res.status_code, 200)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_logout_requires_auth(self):
        self.client.credentials()
        res = self.client.post(reverse('api_logout'))
        self.assertEqual(res.status_code, 401)


class ProfileTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = make_user(first_name='Jane', nationality='British')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_get_profile_returns_user_data(self):
        res = self.client.get(reverse('api_profile'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['username'], 'testuser')
        self.assertEqual(res.data['nationality'], 'British')

    def test_patch_profile_updates_fields(self):
        res = self.client.patch(reverse('api_profile'), {
            'nationality': 'Tanzanian',
            'phone': '+255712345678',
        }, format='json')
        self.assertEqual(res.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.nationality, 'Tanzanian')
        self.assertEqual(self.user.phone, '+255712345678')

    def test_profile_requires_auth(self):
        self.client.credentials()
        res = self.client.get(reverse('api_profile'))
        self.assertEqual(res.status_code, 401)


class ChangePasswordTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = make_user()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_change_password_success(self):
        res = self.client.post(reverse('api_change_password'), {
            'current_password': 'testpass99',
            'new_password': 'newpass1234',
            'new_password_confirm': 'newpass1234',
        }, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertIn('token', res.data)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass1234'))

    def test_change_password_wrong_current(self):
        res = self.client.post(reverse('api_change_password'), {
            'current_password': 'wrongpass',
            'new_password': 'newpass1234',
            'new_password_confirm': 'newpass1234',
        }, format='json')
        self.assertEqual(res.status_code, 400)


class CustomUserModelTests(TestCase):
    def test_custom_fields_exist(self):
        user = make_user(phone='+255712000000', nationality='Kenyan', preferred_currency='KES')
        self.assertEqual(user.phone, '+255712000000')
        self.assertEqual(user.nationality, 'Kenyan')
        self.assertEqual(user.preferred_currency, 'KES')

    def test_str_returns_full_name_or_username(self):
        user = make_user(first_name='Ali', last_name='Hassan')
        self.assertEqual(str(user), 'Ali Hassan')

    def test_str_falls_back_to_username(self):
        user = make_user()
        self.assertEqual(str(user), 'testuser')

from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from packages.models import Package, Booking
from .models import Review, ReviewPhoto

User = get_user_model()


def make_user(**kwargs):
    defaults = dict(username='tester', password='pass123', email='t@t.com')
    defaults.update(kwargs)
    return User.objects.create_user(**defaults)


def make_package(**kwargs):
    defaults = dict(
        name='Serengeti Safari',
        slug='serengeti-safari',
        short_description='Amazing safari',
        description='Full description',
        duration_days=7,
        duration_nights=6,
        price_per_person=Decimal('2000.00'),
        availability_status='available',
        is_active=True,
    )
    defaults.update(kwargs)
    return Package.objects.create(**defaults)


def make_review(package, rating=5, **kwargs):
    defaults = dict(
        package=package,
        reviewer_name='Alice',
        rating=rating,
        title='Great trip',
        body='Loved every moment.',
        status='pending',
        is_approved=False,
    )
    defaults.update(kwargs)
    return Review.objects.create(**defaults)


class ReviewModelTests(TestCase):
    def setUp(self):
        self.staff = make_user(username='staff', is_staff=True)
        self.package = make_package()

    def test_str_representation(self):
        review = make_review(self.package)
        self.assertIn('Alice', str(review))
        self.assertIn('Serengeti Safari', str(review))

    def test_approve_sets_flags(self):
        review = make_review(self.package)
        review.approve(self.staff)
        self.assertTrue(review.is_approved)
        self.assertEqual(review.status, 'approved')
        self.assertEqual(review.approved_by, self.staff)
        self.assertIsNotNone(review.approved_at)

    def test_approve_updates_package_rating(self):
        make_review(self.package, rating=5, status='approved', is_approved=True)
        make_review(self.package, rating=3, status='approved', is_approved=True)
        self.package.update_rating()
        self.package.refresh_from_db()
        self.assertEqual(float(self.package.rating_average), 4.0)
        self.assertEqual(self.package.review_count, 2)

    def test_reject_clears_approval(self):
        review = make_review(self.package, status='approved', is_approved=True)
        review.reject('Spam content')
        self.assertFalse(review.is_approved)
        self.assertEqual(review.status, 'rejected')
        self.assertEqual(review.rejection_reason, 'Spam content')

    def test_update_rating_excludes_unapproved(self):
        make_review(self.package, rating=1)  # pending — should not count
        make_review(self.package, rating=5, status='approved', is_approved=True)
        self.package.update_rating()
        self.package.refresh_from_db()
        self.assertEqual(float(self.package.rating_average), 5.0)
        self.assertEqual(self.package.review_count, 1)

    def test_rating_reset_when_no_approved_reviews(self):
        self.package.rating_average = Decimal('4.5')
        self.package.review_count = 3
        self.package.save()
        self.package.update_rating()
        self.package.refresh_from_db()
        self.assertEqual(float(self.package.rating_average), 0.0)
        self.assertEqual(self.package.review_count, 0)


class ReviewDashboardViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff = make_user(username='staff', is_staff=True)
        self.regular = make_user(username='regular', is_staff=False)
        self.package = make_package()
        self.review = make_review(self.package)

    def _login_staff(self):
        self.client.login(username='staff', password='pass123')

    # Auth gates
    def test_review_list_redirects_anonymous(self):
        res = self.client.get(reverse('reviews:dashboard_review_list'))
        self.assertIn(res.status_code, [301, 302])

    def test_review_list_blocks_non_staff(self):
        self.client.login(username='regular', password='pass123')
        res = self.client.get(reverse('reviews:dashboard_review_list'))
        self.assertIn(res.status_code, [301, 302])

    def test_review_list_accessible_by_staff(self):
        self._login_staff()
        res = self.client.get(reverse('reviews:dashboard_review_list'))
        self.assertEqual(res.status_code, 200)

    def test_review_detail_accessible_by_staff(self):
        self._login_staff()
        res = self.client.get(reverse('reviews:dashboard_review_detail', args=[self.review.pk]))
        self.assertEqual(res.status_code, 200)

    def test_approve_post_approves_review(self):
        self._login_staff()
        self.client.post(reverse('reviews:dashboard_review_approve', args=[self.review.pk]))
        self.review.refresh_from_db()
        self.assertEqual(self.review.status, 'approved')
        self.assertTrue(self.review.is_approved)

    def test_reject_post_rejects_review(self):
        self._login_staff()
        self.client.post(
            reverse('reviews:dashboard_review_reject', args=[self.review.pk]),
            {'reason': 'Off-topic'}
        )
        self.review.refresh_from_db()
        self.assertEqual(self.review.status, 'rejected')
        self.assertFalse(self.review.is_approved)

    def test_delete_post_removes_review(self):
        self._login_staff()
        pk = self.review.pk
        self.client.post(reverse('reviews:dashboard_review_delete', args=[pk]))
        self.assertFalse(Review.objects.filter(pk=pk).exists())


class ReviewPublicViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.package = make_package()
        make_review(self.package, status='approved', is_approved=True)
        make_review(self.package, rating=3, status='approved', is_approved=True)
        make_review(self.package, rating=2, status='pending')  # should not appear

    def test_review_list_shows_only_approved(self):
        res = self.client.get(
            reverse('reviews:public_review_list', args=[self.package.slug])
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['page_obj'].paginator.count, 2)

    def test_submit_page_renders(self):
        user = make_user()
        self.client.login(username='tester', password='pass123')
        res = self.client.get(
            reverse('reviews:review_submit', args=[self.package.slug])
        )
        self.assertEqual(res.status_code, 200)

    def test_submit_post_creates_pending_review(self):
        user = make_user()
        self.client.login(username='tester', password='pass123')
        self.client.post(
            reverse('reviews:review_submit', args=[self.package.slug]),
            {
                'rating': 4,
                'title': 'Very good',
                'body': 'Had a great time on this safari.',
                'reviewer_name': 'Bob',
                'reviewer_country': 'Kenya',
            }
        )
        new_review = Review.objects.filter(title='Very good').first()
        self.assertIsNotNone(new_review)
        self.assertEqual(new_review.status, 'pending')
        self.assertFalse(new_review.is_approved)


class ReviewAPITests(TestCase):
    def setUp(self):
        from rest_framework.test import APIClient
        from rest_framework.authtoken.models import Token
        self.client = APIClient()
        self.package = make_package()
        make_review(self.package, status='approved', is_approved=True)
        make_review(self.package, rating=4, status='approved', is_approved=True)
        make_review(self.package, status='pending')  # should not appear

        self.user = make_user()
        self.token = Token.objects.create(user=self.user)

    def test_package_reviews_api_returns_approved_only(self):
        res = self.client.get(f'/api/v1/packages/{self.package.slug}/reviews/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['count'], 2)

    def test_create_review_requires_auth(self):
        res = self.client.post('/api/v1/reviews/', {
            'package': self.package.pk,
            'rating': 4,
            'title': 'Good',
            'body': 'Nice experience.',
        }, format='json')
        self.assertEqual(res.status_code, 401)

    def test_authenticated_user_can_create_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        res = self.client.post('/api/v1/reviews/', {
            'package': self.package.pk,
            'rating': 5,
            'title': 'Excellent',
            'body': 'Best safari of my life.',
        }, format='json')
        self.assertEqual(res.status_code, 201)
        review = Review.objects.get(title='Excellent')
        self.assertEqual(review.status, 'pending')
        self.assertEqual(review.author, self.user)

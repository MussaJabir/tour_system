from decimal import Decimal
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


def make_destination():
    from destinations.models import Destination
    return Destination.objects.create(
        name='Serengeti', slug='serengeti',
        short_description='Wildlife paradise',
        description='Full description of Serengeti.',
        latitude='2.3333', longitude='34.8333',
        is_active=True,
    )


def make_activity():
    from activities.models import Activity
    from destinations.models import Destination
    dest, _ = Destination.objects.get_or_create(
        slug='serengeti',
        defaults=dict(
            name='Serengeti', short_description='Wildlife paradise',
            description='Full description.', latitude='2.3333', longitude='34.8333',
            is_active=True,
        )
    )
    return Activity.objects.create(
        name='Hot Air Balloon', slug='hot-air-balloon',
        short_description='Sunrise balloon ride',
        description='Float above the plains.',
        destination=dest,
        duration=Decimal('3.0'), duration_unit='hours',
        price_per_person=Decimal('200.00'),
        is_active=True,
    )


def make_accommodation():
    from accommodations.models import Accommodation
    return Accommodation.objects.create(
        name='Serengeti Lodge', slug='serengeti-lodge',
        short_description='Luxury lodge',
        description='A beautiful lodge.',
        is_active=True,
    )


def make_package():
    from packages.models import Package
    return Package.objects.create(
        name='Sitemap Safari', slug='sitemap-safari',
        short_description='A test safari',
        description='Full description.',
        duration_days=5, duration_nights=4,
        price_per_person=Decimal('1500.00'),
        is_active=True,
    )


class SitemapTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.destination = make_destination()
        self.activity = make_activity()
        self.accommodation = make_accommodation()
        self.package = make_package()

    def test_sitemap_returns_200(self):
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'urlset', response.content)

    def test_sitemap_contains_package_url(self):
        response = self.client.get('/sitemap.xml')
        self.assertIn(b'sitemap-safari', response.content)

    def test_sitemap_contains_destination_url(self):
        response = self.client.get('/sitemap.xml')
        self.assertIn(b'serengeti', response.content)

    def test_sitemap_contains_activity_url(self):
        response = self.client.get('/sitemap.xml')
        self.assertIn(b'hot-air-balloon', response.content)

    def test_sitemap_contains_accommodation_url(self):
        response = self.client.get('/sitemap.xml')
        self.assertIn(b'serengeti-lodge', response.content)

    def test_sitemap_valid_xml(self):
        response = self.client.get('/sitemap.xml')
        self.assertIn(b'<?xml', response.content)
        self.assertIn(b'<urlset', response.content)
        self.assertIn(b'<url>', response.content)


class SEOMetaTagTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_package_detail_meta_title(self):
        pkg = make_package()
        response = self.client.get(reverse('packages:public_package_detail', args=[pkg.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, pkg.get_meta_title())

    def test_package_detail_meta_description(self):
        pkg = make_package()
        response = self.client.get(reverse('packages:public_package_detail', args=[pkg.slug]))
        self.assertContains(response, 'name="description"')

    def test_package_detail_og_type(self):
        pkg = make_package()
        response = self.client.get(reverse('packages:public_package_detail', args=[pkg.slug]))
        self.assertContains(response, 'og:type')

    def test_package_detail_canonical(self):
        pkg = make_package()
        response = self.client.get(reverse('packages:public_package_detail', args=[pkg.slug]))
        self.assertContains(response, 'rel="canonical"')

    def test_destination_detail_meta_title(self):
        dest = make_destination()
        response = self.client.get(reverse('public_destination_detail', args=[dest.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, dest.get_meta_title())

    def test_activity_detail_meta_title(self):
        act = make_activity()
        response = self.client.get(reverse('public_activity_detail', args=[act.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, act.get_meta_title())

    def test_accommodation_detail_meta_title(self):
        acc = make_accommodation()
        response = self.client.get(reverse('public_accommodation_detail', args=[acc.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, acc.get_meta_title())

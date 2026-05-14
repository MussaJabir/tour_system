from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from packages.models import Package
from destinations.models import Destination
from activities.models import Activity
from accommodations.models import Accommodation


class PackageSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Package.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class DestinationSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return Destination.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class ActivitySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Activity.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class AccommodationSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Accommodation.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class StaticSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return [
            'public_home',
            'public_destination_list',
            'public_activity_list',
            'public_accommodation_list',
            'packages:public_package_list',
        ]

    def location(self, item):
        return reverse(item)

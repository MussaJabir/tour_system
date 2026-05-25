"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from core.sitemaps import (
    PackageSitemap, DestinationSitemap, ActivitySitemap,
    AccommodationSitemap, StaticSitemap,
)


def robots_txt(request):
    """
    Public robots.txt — allow everything except /admin/ and /dashboard/,
    point crawlers at our sitemap.
    """
    site_url = settings.SITE_URL.rstrip('/')
    body = (
        "User-agent: *\n"
        "Disallow: /admin/\n"
        "Disallow: /dashboard/\n"
        "Disallow: /api/\n"
        "Disallow: /custom/\n"
        "\n"
        f"Sitemap: {site_url}/sitemap.xml\n"
    )
    return HttpResponse(body, content_type='text/plain')

sitemaps = {
    'packages': PackageSitemap,
    'destinations': DestinationSitemap,
    'activities': ActivitySitemap,
    'accommodations': AccommodationSitemap,
    'static': StaticSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
    
    # API endpoints (v1)
    path('api/v1/', include('api.urls')),
    
    # Web routes
    path('', include('destinations.urls')),
    path('', include('activities.urls')),
    path('', include('accommodations.urls')),
    path('', include('packages.urls')),
    path('', include('core.urls')),
    path('', include('reviews.urls')),
    path('', include('ai_assistant.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

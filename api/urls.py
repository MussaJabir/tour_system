"""
Main API URL Configuration
All API endpoints are versioned under /api/v1/
"""
from django.urls import path, include

urlpatterns = [
    # Auth (login, logout, register, profile, change-password)
    path('', include('accounts.api_urls')),

    # Destinations API
    path('', include('destinations.api_urls')),

    # Activities API
    path('', include('activities.api_urls')),

    # Accommodations API
    path('', include('accommodations.api_urls')),

    # Packages API
    path('', include('packages.api_urls')),
]

from django.urls import path, include

"""
Main API URL Configuration
All API endpoints are versioned under /api/v1/
"""

urlpatterns = [
    # Destinations API
    path('', include('destinations.api_urls')),
    
    # Activities API
    path('', include('activities.api_urls')),
    
    # Future app APIs will be added here:
    # path('', include('packages.api_urls')),
    # path('', include('accommodations.api_urls')),
    # path('', include('reviews.api_urls')),
]


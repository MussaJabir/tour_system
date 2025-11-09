from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import DestinationViewSet, DestinationImageViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'destinations', DestinationViewSet, basename='destination')
router.register(r'destination-images', DestinationImageViewSet, basename='destination-image')

urlpatterns = [
    path('', include(router.urls)),
]


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import AccommodationViewSet, AccommodationImageViewSet, RoomViewSet

router = DefaultRouter()
router.register(r'accommodations', AccommodationViewSet, basename='accommodation')
router.register(r'accommodation-images', AccommodationImageViewSet, basename='accommodation-image')
router.register(r'rooms', RoomViewSet, basename='room')

urlpatterns = [
    path('', include(router.urls)),
]


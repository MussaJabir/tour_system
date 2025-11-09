from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ActivityViewSet, ActivityImageViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'activity-images', ActivityImageViewSet, basename='activity-image')

urlpatterns = [
    path('', include(router.urls)),
]


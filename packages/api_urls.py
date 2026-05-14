from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'packages', api_views.PackageViewSet, basename='package')
router.register(r'package-images', api_views.PackageImageViewSet, basename='packageimage')
router.register(r'package-itineraries', api_views.PackageItineraryViewSet, basename='packageitinerary')
router.register(r'package-inclusions', api_views.PackageInclusionViewSet, basename='packageinclusion')
router.register(r'departures', api_views.DepartureViewSet, basename='departure')

urlpatterns = [
    path('', include(router.urls)),
]


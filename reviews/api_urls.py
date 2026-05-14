from django.urls import path
from . import api_views

urlpatterns = [
    path('packages/<slug:package_slug>/reviews/', api_views.PackageReviewListAPIView.as_view(), name='api_package_reviews'),
    path('reviews/', api_views.ReviewCreateAPIView.as_view(), name='api_review_create'),
]

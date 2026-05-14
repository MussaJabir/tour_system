import logging
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Review
from .serializers import ReviewListSerializer, ReviewCreateSerializer

logger = logging.getLogger(__name__)


class PackageReviewListAPIView(generics.ListAPIView):
    """GET /api/v1/packages/<slug>/reviews/ — approved reviews for a package."""
    serializer_class = ReviewListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return (
            Review.objects
            .filter(package__slug=self.kwargs['package_slug'], is_approved=True)
            .select_related('author')
            .prefetch_related('photos')
            .order_by('-created_at')
        )


class ReviewCreateAPIView(generics.CreateAPIView):
    """POST /api/v1/reviews/ — submit a new review (authenticated users only)."""
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        name = self.request.user.get_full_name() or self.request.user.username
        serializer.save(
            author=self.request.user,
            reviewer_name=serializer.validated_data.get('reviewer_name') or name,
            status='pending',
        )

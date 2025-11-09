from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Activity, ActivityImage
from .serializers import (
    ActivityListSerializer,
    ActivityDetailSerializer,
    ActivityWriteSerializer,
    ActivityImageSerializer
)


class ActivityViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for Activities
    
    Provides:
    - list: GET /api/v1/activities/
    - retrieve: GET /api/v1/activities/{slug}/
    - create: POST /api/v1/activities/
    - update: PUT /api/v1/activities/{slug}/
    - partial_update: PATCH /api/v1/activities/{slug}/
    - destroy: DELETE /api/v1/activities/{slug}/
    - featured: GET /api/v1/activities/featured/
    - by_destination: GET /api/v1/activities/by-destination/{destination-slug}/
    - by_category: GET /api/v1/activities/by-category/{category}/
    - search: GET /api/v1/activities/search/?q=query
    """
    queryset = Activity.objects.filter(is_active=True).select_related('destination')
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['destination__slug', 'category', 'difficulty', 'is_featured']
    search_fields = ['name', 'description', 'destination__name']
    ordering_fields = ['name', 'created_at', 'view_count', 'order', 'price_per_person', 'duration']
    ordering = ['order', '-is_featured', 'name']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return ActivityListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ActivityWriteSerializer
        return ActivityDetailSerializer
    
    def get_queryset(self):
        """
        Optionally restricts the returned activities
        """
        queryset = super().get_queryset()
        
        # If user is authenticated and staff, show all activities
        if self.request.user.is_authenticated and self.request.user.is_staff:
            queryset = Activity.objects.select_related('destination').all()
        
        # Filter by price range (optional)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        
        if min_price:
            queryset = queryset.filter(price_per_person__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_person__lte=max_price)
        
        # Filter by duration
        min_duration = self.request.query_params.get('min_duration', None)
        max_duration = self.request.query_params.get('max_duration', None)
        
        if min_duration:
            queryset = queryset.filter(duration__gte=min_duration)
        if max_duration:
            queryset = queryset.filter(duration__lte=max_duration)
        
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve an activity and increment view count
        """
        instance = self.get_object()
        
        # Increment view count (only for non-staff users)
        if not (request.user.is_authenticated and request.user.is_staff):
            instance.increment_view_count()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        """Save activity with created_by user"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        Return only featured activities
        GET /api/v1/activities/featured/
        """
        featured_activities = self.get_queryset().filter(is_featured=True)
        
        page = self.paginate_queryset(featured_activities)
        if page is not None:
            serializer = ActivityListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ActivityListSerializer(featured_activities, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='by-destination/(?P<destination_slug>[^/.]+)')
    def by_destination(self, request, destination_slug=None):
        """
        Get activities for a specific destination
        GET /api/v1/activities/by-destination/{destination-slug}/
        """
        activities = self.get_queryset().filter(destination__slug=destination_slug)
        
        page = self.paginate_queryset(activities)
        if page is not None:
            serializer = ActivityListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ActivityListSerializer(activities, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='by-category/(?P<category>[^/.]+)')
    def by_category(self, request, category=None):
        """
        Get activities by category
        GET /api/v1/activities/by-category/{category}/
        """
        activities = self.get_queryset().filter(category=category)
        
        page = self.paginate_queryset(activities)
        if page is not None:
            serializer = ActivityListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ActivityListSerializer(activities, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Advanced search for activities
        GET /api/v1/activities/search/?q=query&destination=slug&category=safari&difficulty=easy
        """
        query = request.query_params.get('q', '')
        destination = request.query_params.get('destination', '')
        category = request.query_params.get('category', '')
        difficulty = request.query_params.get('difficulty', '')
        
        queryset = self.get_queryset()
        
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(destination__name__icontains=query)
            )
        
        if destination:
            queryset = queryset.filter(destination__slug=destination)
        
        if category:
            queryset = queryset.filter(category=category)
        
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ActivityListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ActivityListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """
        Get list of all activity categories
        GET /api/v1/activities/categories/
        """
        return Response({
            'categories': [{'value': cat[0], 'label': cat[1]} for cat in Activity.CATEGORY_CHOICES]
        })
    
    @action(detail=False, methods=['get'])
    def difficulties(self, request):
        """
        Get list of all difficulty levels
        GET /api/v1/activities/difficulties/
        """
        return Response({
            'difficulties': [{'value': diff[0], 'label': diff[1]} for diff in Activity.DIFFICULTY_CHOICES]
        })
    
    @action(detail=True, methods=['get'])
    def gallery(self, request, slug=None):
        """
        Get gallery images for a specific activity
        GET /api/v1/activities/{slug}/gallery/
        """
        activity = self.get_object()
        images = activity.gallery_images.all()
        serializer = ActivityImageSerializer(images, many=True)
        return Response(serializer.data)


class ActivityImageViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for Activity Images
    """
    queryset = ActivityImage.objects.all()
    serializer_class = ActivityImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """Filter by activity if provided"""
        queryset = super().get_queryset()
        activity_slug = self.request.query_params.get('activity', None)
        
        if activity_slug:
            queryset = queryset.filter(activity__slug=activity_slug)
        
        return queryset


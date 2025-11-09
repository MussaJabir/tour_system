from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Destination, DestinationImage
from .serializers import (
    DestinationListSerializer,
    DestinationDetailSerializer,
    DestinationWriteSerializer,
    DestinationImageSerializer
)


class DestinationViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for Destinations
    
    Provides:
    - list: GET /api/destinations/
    - retrieve: GET /api/destinations/{slug}/
    - create: POST /api/destinations/
    - update: PUT /api/destinations/{slug}/
    - partial_update: PATCH /api/destinations/{slug}/
    - destroy: DELETE /api/destinations/{slug}/
    - featured: GET /api/destinations/featured/
    - search: GET /api/destinations/search/?q=query
    """
    queryset = Destination.objects.filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['country', 'region', 'is_featured']
    search_fields = ['name', 'description', 'country', 'region']
    ordering_fields = ['name', 'created_at', 'view_count', 'order']
    ordering = ['order', '-is_featured', 'name']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return DestinationListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return DestinationWriteSerializer
        return DestinationDetailSerializer
    
    def get_queryset(self):
        """
        Optionally restricts the returned destinations
        """
        queryset = super().get_queryset()
        
        # If user is authenticated and staff, show all destinations
        if self.request.user.is_authenticated and self.request.user.is_staff:
            queryset = Destination.objects.all()
        
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a destination and increment view count
        """
        instance = self.get_object()
        
        # Increment view count (only for non-staff users)
        if not (request.user.is_authenticated and request.user.is_staff):
            instance.increment_view_count()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        """Save destination with created_by user"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        Return only featured destinations
        GET /api/destinations/featured/
        """
        featured_destinations = self.get_queryset().filter(is_featured=True)
        
        page = self.paginate_queryset(featured_destinations)
        if page is not None:
            serializer = DestinationListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = DestinationListSerializer(featured_destinations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Advanced search for destinations
        GET /api/destinations/search/?q=query&country=Kenya
        """
        query = request.query_params.get('q', '')
        country = request.query_params.get('country', '')
        
        queryset = self.get_queryset()
        
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(country__icontains=query) |
                Q(region__icontains=query)
            )
        
        if country:
            queryset = queryset.filter(country__iexact=country)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = DestinationListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = DestinationListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def countries(self, request):
        """
        Get list of all countries with destinations
        GET /api/destinations/countries/
        """
        countries = self.get_queryset().values_list('country', flat=True).distinct()
        return Response({'countries': list(countries)})
    
    @action(detail=True, methods=['get'])
    def gallery(self, request, slug=None):
        """
        Get gallery images for a specific destination
        GET /api/destinations/{slug}/gallery/
        """
        destination = self.get_object()
        images = destination.gallery_images.all()
        serializer = DestinationImageSerializer(images, many=True)
        return Response(serializer.data)


class DestinationImageViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for Destination Images
    """
    queryset = DestinationImage.objects.all()
    serializer_class = DestinationImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """Filter by destination if provided"""
        queryset = super().get_queryset()
        destination_slug = self.request.query_params.get('destination', None)
        
        if destination_slug:
            queryset = queryset.filter(destination__slug=destination_slug)
        
        return queryset


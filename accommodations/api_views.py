from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Accommodation, AccommodationImage, Room
from .serializers import (AccommodationListSerializer, AccommodationDetailSerializer,
                         AccommodationWriteSerializer, AccommodationImageSerializer, RoomSerializer)


class AccommodationViewSet(viewsets.ModelViewSet):
    queryset = Accommodation.objects.filter(is_active=True).select_related('destination')
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['destination__slug', 'accommodation_type', 'star_rating', 'is_featured']
    search_fields = ['name', 'description', 'destination__name', 'address']
    ordering_fields = ['name', 'created_at', 'view_count', 'order', 'star_rating']
    ordering = ['order', '-is_featured', 'name']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AccommodationListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return AccommodationWriteSerializer
        return AccommodationDetailSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and self.request.user.is_staff:
            queryset = Accommodation.objects.select_related('destination').all()
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not (request.user.is_authenticated and request.user.is_staff):
            instance.increment_view_count()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured = self.get_queryset().filter(is_featured=True)
        page = self.paginate_queryset(featured)
        if page is not None:
            serializer = AccommodationListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = AccommodationListSerializer(featured, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='by-destination/(?P<destination_slug>[^/.]+)')
    def by_destination(self, request, destination_slug=None):
        accommodations = self.get_queryset().filter(destination__slug=destination_slug)
        page = self.paginate_queryset(accommodations)
        if page is not None:
            serializer = AccommodationListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = AccommodationListSerializer(accommodations, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def rooms(self, request, slug=None):
        accommodation = self.get_object()
        rooms = accommodation.rooms.filter(is_available=True)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)


class AccommodationImageViewSet(viewsets.ModelViewSet):
    queryset = AccommodationImage.objects.all()
    serializer_class = AccommodationImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.filter(is_available=True)
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


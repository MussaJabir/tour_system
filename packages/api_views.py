from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Package, PackageImage, PackageItinerary, PackageInclusion
from .serializers import (
    PackageListSerializer,
    PackageDetailSerializer,
    PackageCreateUpdateSerializer,
    PackageImageSerializer,
    PackageItinerarySerializer,
    PackageInclusionSerializer
)


class PackageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for packages
    List, create, retrieve, update, delete packages
    """
    queryset = Package.objects.filter(is_active=True).prefetch_related('destinations')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'difficulty_level', 'availability_status', 'is_featured']
    search_fields = ['name', 'short_description', 'description', 'destinations__name']
    ordering_fields = ['price_per_person', 'duration_days', 'rating_average', 'booking_count', 'created_at']
    ordering = ['-is_featured', 'order', '-created_at']
    
    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.action == 'list':
            return PackageListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PackageCreateUpdateSerializer
        return PackageDetailSerializer
    
    def get_queryset(self):
        """Custom queryset with filtering"""
        queryset = super().get_queryset()
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price_per_person__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_person__lte=max_price)
        
        # Filter by duration
        min_days = self.request.query_params.get('min_days')
        max_days = self.request.query_params.get('max_days')
        if min_days:
            queryset = queryset.filter(duration_days__gte=min_days)
        if max_days:
            queryset = queryset.filter(duration_days__lte=max_days)
        
        # Filter by destination
        destination = self.request.query_params.get('destination')
        if destination:
            queryset = queryset.filter(destinations__slug=destination)
        
        return queryset.distinct()
    
    def retrieve(self, request, *args, **kwargs):
        """Increment view count when retrieving a package"""
        instance = self.get_object()
        instance.increment_view_count()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured packages only"""
        queryset = self.get_queryset().filter(is_featured=True)
        serializer = PackageListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Check package availability"""
        package = self.get_object()
        data = {
            'is_available': package.is_available,
            'availability_status': package.availability_status,
            'spots_remaining': package.spots_remaining,
            'max_bookings': package.max_bookings,
            'current_bookings': package.current_bookings,
        }
        return Response(data)
    
    @action(detail=True, methods=['post'])
    def calculate_price(self, request, pk=None):
        """Calculate total price for a booking"""
        package = self.get_object()
        num_travelers = request.data.get('num_travelers', 1)
        
        try:
            num_travelers = int(num_travelers)
            if num_travelers < 1:
                return Response(
                    {'error': 'Number of travelers must be at least 1'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(
                {'error': 'Invalid number of travelers'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate prices
        base_price = package.price_per_person * num_travelers
        discount = package.discount_amount * num_travelers
        final_price = package.final_price * num_travelers
        
        data = {
            'num_travelers': num_travelers,
            'price_per_person': package.price_per_person,
            'discount_percentage': package.discount_percentage,
            'discount_per_person': package.discount_amount,
            'final_price_per_person': package.final_price,
            'base_total': base_price,
            'total_discount': discount,
            'final_total': final_price,
            'currency': package.currency,
        }
        return Response(data)


class PackageImageViewSet(viewsets.ModelViewSet):
    """API endpoint for package images"""
    queryset = PackageImage.objects.filter(is_active=True)
    serializer_class = PackageImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """Filter by package if provided"""
        queryset = super().get_queryset()
        package_id = self.request.query_params.get('package')
        if package_id:
            queryset = queryset.filter(package_id=package_id)
        return queryset


class PackageItineraryViewSet(viewsets.ModelViewSet):
    """API endpoint for package itineraries"""
    queryset = PackageItinerary.objects.filter(is_active=True)
    serializer_class = PackageItinerarySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """Filter by package if provided"""
        queryset = super().get_queryset()
        package_id = self.request.query_params.get('package')
        if package_id:
            queryset = queryset.filter(package_id=package_id)
        return queryset.order_by('day_number')


class PackageInclusionViewSet(viewsets.ModelViewSet):
    """API endpoint for package inclusions/exclusions"""
    queryset = PackageInclusion.objects.filter(is_active=True)
    serializer_class = PackageInclusionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """Filter by package if provided"""
        queryset = super().get_queryset()
        package_id = self.request.query_params.get('package')
        if package_id:
            queryset = queryset.filter(package_id=package_id)
        
        # Filter by inclusion/exclusion
        is_included = self.request.query_params.get('is_included')
        if is_included is not None:
            queryset = queryset.filter(is_included=is_included.lower() == 'true')
        
        return queryset.order_by('order')


from rest_framework import serializers
from .models import Package, PackageImage, PackageItinerary, PackageInclusion, Departure
from destinations.serializers import DestinationListSerializer
from activities.serializers import ActivityListSerializer
from accommodations.serializers import AccommodationListSerializer


class DepartureSerializer(serializers.ModelSerializer):
    seats_remaining = serializers.ReadOnlyField()
    is_available = serializers.ReadOnlyField()

    class Meta:
        model = Departure
        fields = [
            'id', 'departure_date', 'max_seats', 'booked_seats',
            'seats_remaining', 'is_available', 'status',
        ]


class PackageImageSerializer(serializers.ModelSerializer):
    """Serializer for package gallery images"""
    
    class Meta:
        model = PackageImage
        fields = ['id', 'image', 'caption', 'order', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class PackageItinerarySerializer(serializers.ModelSerializer):
    """Serializer for package itinerary"""
    activities = ActivityListSerializer(many=True, read_only=True)
    accommodation = AccommodationListSerializer(read_only=True)
    meals_display = serializers.ReadOnlyField()
    
    class Meta:
        model = PackageItinerary
        fields = [
            'id', 'day_number', 'title', 'description',
            'activities', 'accommodation',
            'breakfast_included', 'lunch_included', 'dinner_included', 'meals_display',
            'highlights', 'notes',
            'order', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class PackageInclusionSerializer(serializers.ModelSerializer):
    """Serializer for package inclusions/exclusions"""
    
    class Meta:
        model = PackageInclusion
        fields = [
            'id', 'inclusion_type', 'item_name', 'description', 'quantity',
            'is_included', 'order', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class PackageListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for package listings"""
    destinations = DestinationListSerializer(many=True, read_only=True)
    final_price = serializers.ReadOnlyField()
    discount_amount = serializers.ReadOnlyField()
    duration_display = serializers.ReadOnlyField()
    is_available = serializers.ReadOnlyField()
    spots_remaining = serializers.ReadOnlyField()
    
    class Meta:
        model = Package
        fields = [
            'id', 'name', 'slug',
            'destinations',
            'category', 'difficulty_level',
            'short_description',
            'duration_days', 'duration_nights', 'duration_display',
            'price_per_person', 'currency', 'discount_percentage',
            'final_price', 'discount_amount',
            'availability_status', 'is_available', 'spots_remaining',
            'featured_image',
            'rating_average', 'review_count', 'booking_count',
            'is_active', 'is_featured',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


class PackageDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single package view"""
    destinations = DestinationListSerializer(many=True, read_only=True)
    gallery_images = PackageImageSerializer(many=True, read_only=True)
    itineraries = PackageItinerarySerializer(many=True, read_only=True)
    inclusions = PackageInclusionSerializer(many=True, read_only=True)
    upcoming_departures = serializers.SerializerMethodField()

    final_price = serializers.ReadOnlyField()
    discount_amount = serializers.ReadOnlyField()
    duration_display = serializers.ReadOnlyField()
    is_available = serializers.ReadOnlyField()
    spots_remaining = serializers.ReadOnlyField()

    # Convert text fields to lists
    highlights_list = serializers.SerializerMethodField()
    included_items_list = serializers.SerializerMethodField()
    excluded_items_list = serializers.SerializerMethodField()
    requirements_list = serializers.SerializerMethodField()

    class Meta:
        model = Package
        fields = [
            'id', 'name', 'slug',
            'destinations',
            'category', 'difficulty_level',
            'description', 'short_description',
            'highlights', 'highlights_list',
            'duration_days', 'duration_nights', 'duration_display',
            'group_size_min', 'group_size_max',
            'price_per_person', 'currency', 'discount_percentage',
            'final_price', 'discount_amount',
            'availability_status', 'is_available',
            'start_date', 'end_date',
            'max_bookings', 'current_bookings', 'spots_remaining',
            'included_items', 'included_items_list',
            'excluded_items', 'excluded_items_list',
            'requirements', 'requirements_list',
            'cancellation_policy', 'terms_and_conditions',
            'featured_image', 'video_url',
            'gallery_images',
            'itineraries',
            'inclusions',
            'upcoming_departures',
            'is_customizable',
            'rating_average', 'review_count',
            'booking_count', 'view_count',
            'is_active', 'is_featured', 'order',
            'meta_title', 'meta_description', 'meta_keywords',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'slug', 'current_bookings', 'booking_count',
            'view_count', 'rating_average', 'review_count',
            'created_at', 'updated_at'
        ]
    
    def get_upcoming_departures(self, obj):
        from django.utils import timezone
        qs = obj.departures.filter(
            status=Departure.STATUS_AVAILABLE,
            departure_date__gte=timezone.now().date(),
        )
        return DepartureSerializer(qs, many=True).data

    def get_highlights_list(self, obj):
        """Convert highlights text to list"""
        if not obj.highlights:
            return []
        # Split by newline or comma
        items = [h.strip() for h in obj.highlights.replace('\r\n', '\n').split('\n') if h.strip()]
        if not items and ',' in obj.highlights:
            items = [h.strip() for h in obj.highlights.split(',') if h.strip()]
        return items
    
    def get_included_items_list(self, obj):
        """Convert included_items text to list"""
        if not obj.included_items:
            return []
        items = [i.strip() for i in obj.included_items.replace('\r\n', '\n').split('\n') if i.strip()]
        if not items and ',' in obj.included_items:
            items = [i.strip() for i in obj.included_items.split(',') if i.strip()]
        return items
    
    def get_excluded_items_list(self, obj):
        """Convert excluded_items text to list"""
        if not obj.excluded_items:
            return []
        items = [e.strip() for e in obj.excluded_items.replace('\r\n', '\n').split('\n') if e.strip()]
        if not items and ',' in obj.excluded_items:
            items = [e.strip() for e in obj.excluded_items.split(',') if e.strip()]
        return items
    
    def get_requirements_list(self, obj):
        """Convert requirements text to list"""
        if not obj.requirements:
            return []
        items = [r.strip() for r in obj.requirements.replace('\r\n', '\n').split('\n') if r.strip()]
        if not items and ',' in obj.requirements:
            items = [r.strip() for r in obj.requirements.split(',') if r.strip()]
        return items


class PackageCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating packages"""
    
    class Meta:
        model = Package
        fields = [
            'name', 'destinations',
            'category', 'difficulty_level',
            'description', 'short_description', 'highlights',
            'duration_days', 'duration_nights',
            'group_size_min', 'group_size_max',
            'price_per_person', 'currency', 'discount_percentage',
            'availability_status', 'start_date', 'end_date',
            'max_bookings',
            'included_items', 'excluded_items', 'requirements',
            'cancellation_policy', 'terms_and_conditions',
            'featured_image', 'video_url',
            'is_customizable',
            'is_active', 'is_featured', 'order',
            'meta_title', 'meta_description', 'meta_keywords',
        ]
    
    def validate(self, data):
        """Custom validation"""
        # Validate group sizes
        if 'group_size_min' in data and 'group_size_max' in data:
            if data['group_size_min'] > data['group_size_max']:
                raise serializers.ValidationError({
                    'group_size_min': 'Minimum group size cannot be greater than maximum.'
                })
        
        # Validate dates
        if 'start_date' in data and 'end_date' in data:
            if data.get('start_date') and data.get('end_date'):
                if data['start_date'] > data['end_date']:
                    raise serializers.ValidationError({
                        'start_date': 'Start date cannot be after end date.'
                    })
        
        # Validate duration
        if 'duration_days' in data and 'duration_nights' in data:
            if data.get('duration_nights') and data.get('duration_days'):
                if data['duration_nights'] >= data['duration_days']:
                    raise serializers.ValidationError({
                        'duration_nights': 'Nights should be less than days.'
                    })
        
        return data


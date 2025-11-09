from rest_framework import serializers
from .models import Activity, ActivityImage
from destinations.serializers import DestinationListSerializer


class ActivityImageSerializer(serializers.ModelSerializer):
    """
    Serializer for activity gallery images
    """
    class Meta:
        model = ActivityImage
        fields = ['id', 'image', 'caption', 'order', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class ActivityListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing activities
    """
    destination_name = serializers.CharField(source='destination.name', read_only=True)
    destination_slug = serializers.CharField(source='destination.slug', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)
    duration_display = serializers.CharField(read_only=True)
    price_display = serializers.CharField(read_only=True)
    absolute_url = serializers.SerializerMethodField()
    image_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Activity
        fields = [
            'id', 'name', 'slug', 'short_description',
            'destination_name', 'destination_slug',
            'category', 'category_display',
            'difficulty', 'difficulty_display',
            'duration', 'duration_unit', 'duration_display',
            'price_per_person', 'currency', 'price_display',
            'featured_image', 'is_featured', 'view_count',
            'absolute_url', 'image_count'
        ]
    
    def get_absolute_url(self, obj):
        return obj.get_absolute_url()
    
    def get_image_count(self, obj):
        return obj.gallery_images.count()


class ActivityDetailSerializer(serializers.ModelSerializer):
    """
    Complete serializer for activity details
    """
    destination = DestinationListSerializer(read_only=True)
    gallery_images = ActivityImageSerializer(many=True, read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)
    duration_display = serializers.CharField(read_only=True)
    price_display = serializers.CharField(read_only=True)
    absolute_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Activity
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'destination',
            'category', 'category_display',
            'difficulty', 'difficulty_display',
            'duration', 'duration_unit', 'duration_display',
            'min_age', 'max_group_size',
            'price_per_person', 'currency', 'price_display',
            'featured_image', 'video_url',
            'requirements', 'included_items', 'excluded_items', 'best_season',
            'is_featured', 'is_active', 'view_count', 'order',
            'meta_title', 'meta_description', 'meta_keywords',
            'created_at', 'updated_at',
            'gallery_images', 'absolute_url'
        ]
        read_only_fields = ['id', 'slug', 'view_count', 'created_at', 'updated_at']
    
    def get_absolute_url(self, obj):
        return obj.get_absolute_url()


class ActivityWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating activities
    """
    class Meta:
        model = Activity
        fields = [
            'name', 'description', 'short_description',
            'destination',
            'category', 'difficulty',
            'duration', 'duration_unit',
            'min_age', 'max_group_size',
            'price_per_person', 'currency',
            'featured_image', 'video_url',
            'requirements', 'included_items', 'excluded_items', 'best_season',
            'is_featured', 'is_active', 'order',
            'meta_title', 'meta_description', 'meta_keywords'
        ]
    
    def validate_duration(self, value):
        """Validate duration is positive"""
        if value <= 0:
            raise serializers.ValidationError("Duration must be greater than 0")
        return value
    
    def validate_price_per_person(self, value):
        """Validate price is non-negative"""
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative")
        return value
    
    def validate_min_age(self, value):
        """Validate minimum age is reasonable"""
        if value and (value < 1 or value > 100):
            raise serializers.ValidationError("Minimum age must be between 1 and 100")
        return value
    
    def validate_max_group_size(self, value):
        """Validate group size is positive"""
        if value and value < 1:
            raise serializers.ValidationError("Maximum group size must be at least 1")
        return value


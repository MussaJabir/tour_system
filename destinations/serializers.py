from rest_framework import serializers
from .models import Destination, DestinationImage


class DestinationImageSerializer(serializers.ModelSerializer):
    """
    Serializer for destination gallery images
    """
    class Meta:
        model = DestinationImage
        fields = ['id', 'image', 'caption', 'order', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class DestinationListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing destinations
    """
    absolute_url = serializers.SerializerMethodField()
    image_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Destination
        fields = [
            'id', 'name', 'slug', 'short_description',
            'country', 'region', 'featured_image',
            'is_featured', 'view_count', 'absolute_url',
            'image_count'
        ]
    
    def get_absolute_url(self, obj):
        return obj.get_absolute_url()
    
    def get_image_count(self, obj):
        return obj.gallery_images.count()


class DestinationDetailSerializer(serializers.ModelSerializer):
    """
    Complete serializer for destination details
    """
    gallery_images = DestinationImageSerializer(many=True, read_only=True)
    absolute_url = serializers.SerializerMethodField()
    coordinates = serializers.SerializerMethodField()
    
    class Meta:
        model = Destination
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'country', 'region', 'latitude', 'longitude', 'coordinates',
            'featured_image', 'video_url',
            'best_time_to_visit', 'climate', 'wildlife',
            'is_featured', 'view_count',
            'meta_title', 'meta_description', 'meta_keywords',
            'created_at', 'updated_at',
            'gallery_images', 'absolute_url'
        ]
        read_only_fields = ['id', 'slug', 'view_count', 'created_at', 'updated_at']
    
    def get_absolute_url(self, obj):
        return obj.get_absolute_url()
    
    def get_coordinates(self, obj):
        if obj.latitude and obj.longitude:
            return {
                'lat': float(obj.latitude),
                'lng': float(obj.longitude)
            }
        return None


class DestinationWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating destinations
    """
    class Meta:
        model = Destination
        fields = [
            'name', 'description', 'short_description',
            'country', 'region', 'latitude', 'longitude',
            'featured_image', 'video_url',
            'best_time_to_visit', 'climate', 'wildlife',
            'is_featured', 'is_active', 'order',
            'meta_title', 'meta_description', 'meta_keywords'
        ]
    
    def validate_latitude(self, value):
        """Validate latitude is within valid range"""
        if value and (value < -90 or value > 90):
            raise serializers.ValidationError("Latitude must be between -90 and 90")
        return value
    
    def validate_longitude(self, value):
        """Validate longitude is within valid range"""
        if value and (value < -180 or value > 180):
            raise serializers.ValidationError("Longitude must be between -180 and 180")
        return value


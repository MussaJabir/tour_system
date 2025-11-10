from rest_framework import serializers
from .models import Accommodation, AccommodationImage, Room
from destinations.serializers import DestinationListSerializer


class AccommodationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccommodationImage
        fields = ['id', 'image', 'caption', 'order', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class RoomSerializer(serializers.ModelSerializer):
    price_display = serializers.CharField(read_only=True)
    amenities_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Room
        fields = ['id', 'name', 'room_type', 'description', 'max_occupancy', 'bed_type', 
                 'number_of_beds', 'size_sqm', 'price_per_night', 'price_display', 
                 'amenities', 'amenities_list', 'is_available', 'image']
    
    def get_amenities_list(self, obj):
        return obj.get_amenities_list()


class AccommodationListSerializer(serializers.ModelSerializer):
    destination_name = serializers.CharField(source='destination.name', read_only=True)
    destination_slug = serializers.CharField(source='destination.slug', read_only=True)
    type_display = serializers.CharField(source='get_accommodation_type_display', read_only=True)
    price_range_display = serializers.CharField(read_only=True)
    absolute_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Accommodation
        fields = ['id', 'name', 'slug', 'short_description', 'destination_name', 'destination_slug',
                 'accommodation_type', 'type_display', 'star_rating', 'featured_image',
                 'price_range_display', 'is_featured', 'view_count', 'absolute_url']
    
    def get_absolute_url(self, obj):
        return obj.get_absolute_url()


class AccommodationDetailSerializer(serializers.ModelSerializer):
    destination = DestinationListSerializer(read_only=True)
    gallery_images = AccommodationImageSerializer(many=True, read_only=True)
    rooms = RoomSerializer(many=True, read_only=True)
    type_display = serializers.CharField(source='get_accommodation_type_display', read_only=True)
    price_range_display = serializers.CharField(read_only=True)
    amenities_list = serializers.SerializerMethodField()
    coordinates = serializers.SerializerMethodField()
    absolute_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Accommodation
        fields = ['id', 'name', 'slug', 'description', 'short_description', 'destination',
                 'accommodation_type', 'type_display', 'star_rating', 'address', 'latitude', 
                 'longitude', 'coordinates', 'phone', 'email', 'website', 'amenities', 
                 'amenities_list', 'total_rooms', 'price_per_night_min', 'price_per_night_max', 
                 'currency', 'price_range_display', 'check_in_time', 'check_out_time', 'policies',
                 'featured_image', 'video_url', 'is_featured', 'view_count', 'created_at', 
                 'updated_at', 'gallery_images', 'rooms', 'absolute_url']
        read_only_fields = ['id', 'slug', 'view_count', 'created_at', 'updated_at']
    
    def get_amenities_list(self, obj):
        return obj.get_amenities_list()
    
    def get_coordinates(self, obj):
        return obj.coordinates
    
    def get_absolute_url(self, obj):
        return obj.get_absolute_url()


class AccommodationWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        fields = ['name', 'description', 'short_description', 'destination', 'accommodation_type',
                 'star_rating', 'address', 'latitude', 'longitude', 'phone', 'email', 'website',
                 'amenities', 'total_rooms', 'price_per_night_min', 'price_per_night_max', 'currency',
                 'check_in_time', 'check_out_time', 'policies', 'featured_image', 'video_url',
                 'is_featured', 'is_active', 'order', 'meta_title', 'meta_description', 'meta_keywords']


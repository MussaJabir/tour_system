from django.contrib import admin
from .models import Accommodation, AccommodationImage, Room


class AccommodationImageInline(admin.StackedInline):
    """Inline admin for accommodation gallery images"""
    model = AccommodationImage
    extra = 1
    fields = ('image', 'caption', 'order')


class RoomInline(admin.TabularInline):
    """Inline admin for rooms"""
    model = Room
    extra = 1
    fields = ('name', 'room_type', 'max_occupancy', 'price_per_night', 'is_available')


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    """Admin interface for Accommodation model"""
    list_display = [
        'name', 'destination', 'accommodation_type', 'star_rating',
        'price_range_display', 'is_featured', 'is_active', 
        'view_count', 'created_at'
    ]
    list_filter = [
        'accommodation_type', 'star_rating', 'is_featured', 
        'is_active', 'destination', 'created_at'
    ]
    search_fields = ['name', 'description', 'destination__name', 'address']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['view_count', 'created_at', 'updated_at']
    inlines = [RoomInline, AccommodationImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'short_description', 'description', 'destination')
        }),
        ('Classification', {
            'fields': ('accommodation_type', 'star_rating')
        }),
        ('Location', {
            'fields': ('address', 'latitude', 'longitude')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'website')
        }),
        ('Amenities & Features', {
            'fields': ('amenities', 'total_rooms')
        }),
        ('Pricing', {
            'fields': ('price_per_night_min', 'price_per_night_max', 'currency')
        }),
        ('Check-in/Check-out', {
            'fields': ('check_in_time', 'check_out_time', 'policies'),
            'classes': ('collapse',)
        }),
        ('Media', {
            'fields': ('featured_image', 'video_url')
        }),
        ('Status & Visibility', {
            'fields': ('is_featured', 'is_active', 'order', 'view_count')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Set created_by user on save"""
        if not change:  # Only on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(AccommodationImage)
class AccommodationImageAdmin(admin.ModelAdmin):
    """Admin interface for AccommodationImage model"""
    list_display = ['accommodation', 'caption', 'order', 'uploaded_at']
    list_filter = ['accommodation', 'uploaded_at']
    search_fields = ['accommodation__name', 'caption']
    ordering = ['accommodation', 'order']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Admin interface for Room model"""
    list_display = [
        'name', 'accommodation', 'room_type', 'max_occupancy',
        'price_display', 'is_available'
    ]
    list_filter = ['room_type', 'is_available', 'accommodation']
    search_fields = ['name', 'accommodation__name']
    ordering = ['accommodation', 'price_per_night']

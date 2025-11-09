from django.contrib import admin
from django.utils.html import format_html
from .models import Destination, DestinationImage


class DestinationImageInline(admin.TabularInline):
    """
    Inline admin for destination gallery images
    """
    model = DestinationImage
    extra = 1
    fields = ['image', 'caption', 'order', 'image_preview']
    readonly_fields = ['image_preview', 'uploaded_at']
    
    def image_preview(self, obj):
        """Display thumbnail preview of image"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px;" />',
                obj.image.url
            )
        return "-"
    image_preview.short_description = 'Preview'


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    """
    Admin interface for Destination model
    """
    list_display = [
        'name',
        'country',
        'region',
        'is_featured',
        'is_active',
        'view_count',
        'order',
        'image_preview',
        'created_at'
    ]
    
    list_filter = [
        'is_featured',
        'is_active',
        'country',
        'created_at'
    ]
    
    search_fields = [
        'name',
        'country',
        'region',
        'description',
        'wildlife'
    ]
    
    prepopulated_fields = {'slug': ('name',)}
    
    readonly_fields = [
        'view_count',
        'created_at',
        'updated_at',
        'featured_image_preview',
        'map_preview'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name',
                'slug',
                'short_description',
                'description'
            )
        }),
        ('Location', {
            'fields': (
                'country',
                'region',
                'latitude',
                'longitude',
                'map_preview'
            )
        }),
        ('Media', {
            'fields': (
                'featured_image',
                'featured_image_preview',
                'video_url'
            )
        }),
        ('Details', {
            'fields': (
                'best_time_to_visit',
                'climate',
                'wildlife'
            ),
            'classes': ('collapse',)
        }),
        ('Visibility & Status', {
            'fields': (
                'is_featured',
                'is_active',
                'order',
                'view_count'
            )
        }),
        ('SEO', {
            'fields': (
                'meta_title',
                'meta_description',
                'meta_keywords'
            ),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': (
                'created_by',
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        })
    )
    
    inlines = [DestinationImageInline]
    
    list_editable = ['is_featured', 'is_active', 'order']
    
    actions = [
        'make_featured',
        'remove_featured',
        'activate_destinations',
        'deactivate_destinations'
    ]
    
    def save_model(self, request, obj, form, change):
        """Set created_by when creating new destination"""
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def featured_image_preview(self, obj):
        """Display preview of featured image"""
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 300px;" />',
                obj.featured_image.url
            )
        return "-"
    featured_image_preview.short_description = 'Featured Image Preview'
    
    def image_preview(self, obj):
        """Display small thumbnail in list view"""
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-height: 50px; border-radius: 5px;" />',
                obj.featured_image.url
            )
        return "-"
    image_preview.short_description = 'Image'
    
    def map_preview(self, obj):
        """Display map preview with coordinates"""
        if obj.latitude and obj.longitude:
            # Using OpenStreetMap for preview
            map_url = f"https://www.openstreetmap.org/?mlat={obj.latitude}&mlon={obj.longitude}#map=10/{obj.latitude}/{obj.longitude}"
            return format_html(
                '<p><strong>Coordinates:</strong> {}, {}</p>'
                '<a href="{}" target="_blank" class="button">View on Map</a>',
                obj.latitude,
                obj.longitude,
                map_url
            )
        return "-"
    map_preview.short_description = 'Location Map'
    
    # Custom Actions
    def make_featured(self, request, queryset):
        """Mark selected destinations as featured"""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} destination(s) marked as featured.')
    make_featured.short_description = 'Mark as featured'
    
    def remove_featured(self, request, queryset):
        """Remove featured status from selected destinations"""
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} destination(s) removed from featured.')
    remove_featured.short_description = 'Remove from featured'
    
    def activate_destinations(self, request, queryset):
        """Activate selected destinations"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} destination(s) activated.')
    activate_destinations.short_description = 'Activate selected'
    
    def deactivate_destinations(self, request, queryset):
        """Deactivate selected destinations"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} destination(s) deactivated.')
    deactivate_destinations.short_description = 'Deactivate selected'


@admin.register(DestinationImage)
class DestinationImageAdmin(admin.ModelAdmin):
    """
    Admin interface for destination images
    """
    list_display = ['destination', 'image_preview', 'caption', 'order', 'uploaded_at']
    list_filter = ['destination', 'uploaded_at']
    search_fields = ['destination__name', 'caption']
    list_editable = ['order']
    
    def image_preview(self, obj):
        """Display image thumbnail"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 75px;" />',
                obj.image.url
            )
        return "-"
    image_preview.short_description = 'Preview'

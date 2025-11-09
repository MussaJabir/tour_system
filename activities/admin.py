from django.contrib import admin
from .models import Activity, ActivityImage


class ActivityImageInline(admin.StackedInline):
    """Inline admin for activity gallery images"""
    model = ActivityImage
    extra = 1
    fields = ('image', 'caption', 'order')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin interface for Activity model"""
    list_display = [
        'name', 'destination', 'category', 'difficulty', 
        'price_per_person', 'duration_display', 'is_featured', 
        'is_active', 'view_count', 'created_at'
    ]
    list_filter = [
        'category', 'difficulty', 'is_featured', 'is_active', 
        'destination', 'created_at'
    ]
    search_fields = ['name', 'description', 'destination__name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['view_count', 'created_at', 'updated_at']
    inlines = [ActivityImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'short_description', 'description', 'destination')
        }),
        ('Classification', {
            'fields': ('category', 'difficulty')
        }),
        ('Logistics', {
            'fields': (
                'duration', 'duration_unit', 'min_age', 
                'max_group_size'
            )
        }),
        ('Pricing', {
            'fields': ('price_per_person', 'currency')
        }),
        ('Media', {
            'fields': ('featured_image', 'video_url')
        }),
        ('Details', {
            'fields': (
                'requirements', 'included_items', 
                'excluded_items', 'best_season'
            ),
            'classes': ('collapse',)
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


@admin.register(ActivityImage)
class ActivityImageAdmin(admin.ModelAdmin):
    """Admin interface for ActivityImage model"""
    list_display = ['activity', 'caption', 'order', 'uploaded_at']
    list_filter = ['activity', 'uploaded_at']
    search_fields = ['activity__name', 'caption']
    ordering = ['activity', 'order']

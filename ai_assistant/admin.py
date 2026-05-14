from django.contrib import admin
from django.utils.html import format_html

from .models import (
    AIConfiguration,
    BrochureParseJob,
    ItineraryGenerationJob,
    QuoteSuggestionJob,
    RouteOptimizationJob,
)


@admin.register(AIConfiguration)
class AIConfigurationAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Vendor', {
            'fields': ('vendor', 'api_key', 'model_name'),
        }),
        ('Parameters', {
            'fields': ('max_tokens', 'temperature', 'is_active'),
        }),
    )
    list_display = ('vendor', 'model_name', 'max_tokens', 'temperature', 'is_active')

    def has_add_permission(self, request):
        return not AIConfiguration.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


def _status_badge(obj):
    colors = {
        'pending': 'secondary',
        'processing': 'warning',
        'done': 'success',
        'failed': 'danger',
    }
    color = colors.get(obj.status, 'secondary')
    return format_html(
        '<span class="badge bg-{}">{}</span>', color, obj.get_status_display()
    )
_status_badge.short_description = 'Status'


@admin.register(BrochureParseJob)
class BrochureParseJobAdmin(admin.ModelAdmin):
    list_display = ('__str__', _status_badge, 'target_accommodation', 'created_by', 'created_at')
    list_filter = ('status',)
    readonly_fields = ('status', 'error_message', 'started_at', 'completed_at', 'extracted_data')
    raw_id_fields = ('target_accommodation', 'created_by')


@admin.register(ItineraryGenerationJob)
class ItineraryGenerationJobAdmin(admin.ModelAdmin):
    list_display = ('__str__', _status_badge, 'destination', 'duration_days', 'created_by', 'created_at')
    list_filter = ('status',)
    readonly_fields = ('status', 'error_message', 'started_at', 'completed_at', 'raw_output')
    raw_id_fields = ('destination', 'created_by')


@admin.register(QuoteSuggestionJob)
class QuoteSuggestionJobAdmin(admin.ModelAdmin):
    list_display = ('__str__', _status_badge, 'inquiry', 'created_by', 'created_at')
    list_filter = ('status',)
    readonly_fields = ('status', 'error_message', 'started_at', 'completed_at', 'suggestions')
    raw_id_fields = ('inquiry', 'created_by')


@admin.register(RouteOptimizationJob)
class RouteOptimizationJobAdmin(admin.ModelAdmin):
    list_display = ('__str__', _status_badge, 'created_by', 'created_at')
    list_filter = ('status',)
    readonly_fields = ('status', 'error_message', 'started_at', 'completed_at', 'optimized_route')
    raw_id_fields = ('created_by',)

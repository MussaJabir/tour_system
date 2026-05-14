from django.contrib import admin
from django.utils.html import format_html
from .models import Review, ReviewPhoto


class ReviewPhotoInline(admin.TabularInline):
    model = ReviewPhoto
    extra = 0
    fields = ['photo', 'caption', 'order']
    classes = ['collapse']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'package', 'reviewer_name', 'rating_stars',
        'status_badge', 'featured', 'created_at', 'approve_action',
    ]
    list_filter = ['status', 'rating', 'featured', 'created_at']
    search_fields = ['reviewer_name', 'title', 'body', 'package__name']
    readonly_fields = ['is_approved', 'approved_by', 'approved_at', 'created_at', 'updated_at']
    list_per_page = 30
    date_hierarchy = 'created_at'
    inlines = [ReviewPhotoInline]
    actions = ['approve_selected', 'reject_selected', 'feature_selected']

    fieldsets = (
        ('Review Content', {
            'fields': ('package', 'booking', 'author', 'reviewer_name', 'reviewer_country',
                       'rating', 'title', 'body'),
        }),
        ('Moderation', {
            'fields': ('status', 'is_approved', 'approved_by', 'approved_at',
                       'rejection_reason', 'featured'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def rating_stars(self, obj):
        filled = '★' * obj.rating
        empty = '☆' * (5 - obj.rating)
        color = '#f59e0b' if obj.rating >= 4 else ('#6b7280' if obj.rating <= 2 else '#d97706')
        return format_html(
            '<span style="color: {}; font-size: 16px;">{}{}</span>',
            color, filled, empty,
        )
    rating_stars.short_description = 'Rating'

    def status_badge(self, obj):
        colors = {
            'pending': '#f59e0b',
            'approved': '#10b981',
            'rejected': '#ef4444',
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background: {}; color: white; padding: 2px 8px; '
            'border-radius: 4px; font-size: 11px; font-weight: 600;">{}</span>',
            color, obj.get_status_display(),
        )
    status_badge.short_description = 'Status'

    def approve_action(self, obj):
        if obj.status == 'pending':
            return format_html(
                '<a href="reviews/review/{}/approve/" class="button" '
                'style="padding: 2px 8px; background: #10b981; color: white; '
                'border-radius: 4px; font-size: 11px; text-decoration: none;">Approve</a>',
                obj.pk,
            )
        return ''
    approve_action.short_description = ''

    def approve_selected(self, request, queryset):
        count = 0
        for review in queryset.filter(status='pending'):
            review.approve(request.user)
            count += 1
        self.message_user(request, f'{count} review(s) approved.')
    approve_selected.short_description = 'Approve selected reviews'

    def reject_selected(self, request, queryset):
        count = queryset.update(status='rejected', is_approved=False)
        for review in queryset:
            review.package.update_rating()
        self.message_user(request, f'{count} review(s) rejected.')
    reject_selected.short_description = 'Reject selected reviews'

    def feature_selected(self, request, queryset):
        count = queryset.filter(is_approved=True).update(featured=True)
        self.message_user(request, f'{count} review(s) marked as featured.')
    feature_selected.short_description = 'Feature selected (approved only)'


@admin.register(ReviewPhoto)
class ReviewPhotoAdmin(admin.ModelAdmin):
    list_display = ['review', 'caption', 'order', 'created_at']
    list_filter = ['created_at']
    list_per_page = 50

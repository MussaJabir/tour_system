"""
Core App - Django Admin Configuration

Professional admin interface for managing:
- Contact Messages (Lead Management)
- Newsletter Subscribers (Email Marketing)
- FAQs (Customer Support)
- Testimonials (Social Proof)
"""
from django.contrib import admin
from django.utils.html import format_html
from django.utils.timezone import now
from .models import ContactMessage, NewsletterSubscriber, FAQ, Testimonial


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Admin interface for Contact Messages.
    
    CRITICAL: These are your LEADS - potential customers!
    """
    list_display = [
        'name', 
        'email', 
        'subject', 
        'status_badge', 
        'created_at', 
        'action_buttons'
    ]
    list_filter = [
        'status', 
        'created_at',
    ]
    search_fields = [
        'name', 
        'email', 
        'subject', 
        'message'
    ]
    readonly_fields = [
        'created_at', 
        'updated_at', 
        'ip_address'
    ]
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'ip_address')
        }),
        ('Message Details', {
            'fields': ('subject', 'message')
        }),
        ('Status & Notes', {
            'fields': ('status', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    def status_badge(self, obj):
        """Display status with color-coded badge"""
        colors = {
            'new': '#dc3545',      # Red
            'read': '#ffc107',     # Yellow
            'replied': '#28a745',  # Green
            'archived': '#6c757d'  # Gray
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display().upper()
        )
    status_badge.short_description = 'Status'
    
    def action_buttons(self, obj):
        """Quick action buttons"""
        if obj.status == 'new':
            return format_html(
                '<a class="button" href="#" onclick="return confirm(\'Mark as read?\')">Mark Read</a>'
            )
        return '-'
    action_buttons.short_description = 'Quick Actions'
    
    actions = ['mark_as_read', 'mark_as_replied', 'mark_as_archived']
    
    def mark_as_read(self, request, queryset):
        """Bulk action: Mark messages as read"""
        updated = queryset.filter(status='new').update(status='read')
        self.message_user(request, f'{updated} message(s) marked as read.')
    mark_as_read.short_description = 'Mark selected as Read'
    
    def mark_as_replied(self, request, queryset):
        """Bulk action: Mark messages as replied"""
        updated = queryset.update(status='replied')
        self.message_user(request, f'{updated} message(s) marked as replied.')
    mark_as_replied.short_description = 'Mark selected as Replied'
    
    def mark_as_archived(self, request, queryset):
        """Bulk action: Archive messages"""
        updated = queryset.update(status='archived')
        self.message_user(request, f'{updated} message(s) archived.')
    mark_as_archived.short_description = 'Archive selected messages'


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    """
    Admin interface for Newsletter Subscribers.
    
    MARKETING GOLD: Your email list for promotions!
    """
    list_display = [
        'email', 
        'name', 
        'status_badge', 
        'created_at',
        'subscriber_info'
    ]
    list_filter = [
        'is_active', 
        'created_at',
        'unsubscribed_at'
    ]
    search_fields = [
        'email', 
        'name'
    ]
    readonly_fields = [
        'created_at', 
        'updated_at', 
        'unsubscribed_at',
        'ip_address',
        'subscriber_count'
    ]
    fieldsets = (
        ('Subscriber Information', {
            'fields': ('email', 'name', 'ip_address')
        }),
        ('Status', {
            'fields': ('is_active', 'unsubscribed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('subscriber_count',),
            'classes': ('collapse',)
        }),
    )
    list_per_page = 100
    date_hierarchy = 'created_at'
    
    def status_badge(self, obj):
        """Display subscription status with badge"""
        if obj.is_active:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 10px; '
                'border-radius: 3px; font-weight: bold;">✓ ACTIVE</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">✗ UNSUBSCRIBED</span>'
        )
    status_badge.short_description = 'Status'
    
    def subscriber_info(self, obj):
        """Show additional subscriber info"""
        if obj.unsubscribed_at:
            return format_html(
                '<small style="color: #dc3545;">Unsubscribed: {}</small>',
                obj.unsubscribed_at.strftime('%Y-%m-%d')
            )
        return format_html(
            '<small style="color: #28a745;">Subscribed: {}</small>',
            obj.created_at.strftime('%Y-%m-%d')
        )
    subscriber_info.short_description = 'Info'
    
    def subscriber_count(self, obj):
        """Show total active subscribers"""
        count = NewsletterSubscriber.objects.filter(is_active=True).count()
        return format_html(
            '<strong>{}</strong> active subscriber{}',
            count,
            's' if count != 1 else ''
        )
    subscriber_count.short_description = 'Total Active Subscribers'
    
    actions = ['export_subscribers', 'reactivate_subscribers']
    
    def export_subscribers(self, request, queryset):
        """Export selected subscribers to CSV"""
        # This is a placeholder - full implementation in next phase
        emails = queryset.filter(is_active=True).values_list('email', flat=True)
        email_list = ', '.join(emails)
        self.message_user(
            request, 
            f'Export: {queryset.count()} subscribers. Emails: {email_list[:100]}...'
        )
    export_subscribers.short_description = 'Export selected emails'
    
    def reactivate_subscribers(self, request, queryset):
        """Reactivate unsubscribed users"""
        updated = queryset.filter(is_active=False).update(
            is_active=True,
            unsubscribed_at=None
        )
        self.message_user(request, f'{updated} subscriber(s) reactivated.')
    reactivate_subscribers.short_description = 'Reactivate selected subscribers'


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """
    Admin interface for FAQs.
    
    SAVE TIME: Answer questions once, direct customers here!
    """
    list_display = [
        'question_preview', 
        'category_badge', 
        'status_badge',
        'order',
        'created_at'
    ]
    list_filter = [
        'category', 
        'is_active',
        'created_at'
    ]
    search_fields = [
        'question', 
        'answer'
    ]
    list_editable = ['order']
    readonly_fields = [
        'created_at', 
        'updated_at',
        'created_by'
    ]
    fieldsets = (
        ('FAQ Details', {
            'fields': ('category', 'question', 'answer')
        }),
        ('Publishing', {
            'fields': ('is_active', 'is_featured', 'order')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )
    list_per_page = 50
    
    def question_preview(self, obj):
        """Show truncated question"""
        return obj.question[:80] + '...' if len(obj.question) > 80 else obj.question
    question_preview.short_description = 'Question'
    
    def category_badge(self, obj):
        """Display category with color"""
        colors = {
            'general': '#6c757d',
            'booking': '#007bff',
            'payment': '#28a745',
            'destinations': '#17a2b8',
            'travel': '#ffc107',
            'safety': '#dc3545',
            'cancellation': '#fd7e14',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-size: 11px;">{}</span>',
            colors.get(obj.category, '#6c757d'),
            obj.get_category_display().upper()
        )
    category_badge.short_description = 'Category'
    
    def status_badge(self, obj):
        """Display publish status"""
        if obj.is_active:
            badge = '✓ Published'
            color = '#28a745'
        else:
            badge = '✗ Draft'
            color = '#6c757d'
        
        if obj.is_featured:
            badge += ' ⭐'
            
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            badge
        )
    status_badge.short_description = 'Status'
    
    def save_model(self, request, obj, form, change):
        """Set created_by user"""
        if not change:  # Only on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """
    Admin interface for Testimonials.
    
    SOCIAL PROOF: Build trust with potential customers!
    """
    list_display = [
        'customer_name', 
        'customer_location',
        'rating_stars',
        'status_badge',
        'order',
        'quote_preview',
        'created_at'
    ]
    list_filter = [
        'rating',
        'is_active',
        'is_featured',
        'created_at'
    ]
    search_fields = [
        'customer_name', 
        'customer_location',
        'quote'
    ]
    list_editable = ['order']
    readonly_fields = [
        'created_at', 
        'updated_at',
        'created_by'
    ]
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_location', 'customer_image')
        }),
        ('Testimonial', {
            'fields': ('quote', 'rating')
        }),
        ('Publishing', {
            'fields': ('is_active', 'is_featured', 'order')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )
    list_per_page = 50
    
    def rating_stars(self, obj):
        """Display rating as stars"""
        stars = '⭐' * obj.rating
        gray_stars = '☆' * (5 - obj.rating)
        return format_html(
            '<span style="font-size: 16px;">{}{}</span>',
            stars,
            gray_stars
        )
    rating_stars.short_description = 'Rating'
    
    def quote_preview(self, obj):
        """Show truncated quote"""
        return obj.quote[:50] + '...' if len(obj.quote) > 50 else obj.quote
    quote_preview.short_description = 'Quote'
    
    def status_badge(self, obj):
        """Display publish status"""
        if obj.is_active:
            badge = '✓ Published'
            color = '#28a745'
        else:
            badge = '✗ Draft'
            color = '#6c757d'
        
        if obj.is_featured:
            badge += ' ⭐'
            
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            badge
        )
    status_badge.short_description = 'Status'
    
    def save_model(self, request, obj, form, change):
        """Set created_by user"""
        if not change:  # Only on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

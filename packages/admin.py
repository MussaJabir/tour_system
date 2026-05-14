from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    Package, PackageImage, PackageItinerary, PackageInclusion,
    BookingInquiry, CustomPackage, InquiryMessage,
    Booking, Passenger, Payment,
)


class PackageImageInline(admin.TabularInline):
    """Inline admin for package gallery images"""
    model = PackageImage
    extra = 1
    fields = ['image', 'caption', 'order', 'is_active']
    classes = ['collapse']


class PackageItineraryInline(admin.TabularInline):
    """Inline admin for package itinerary"""
    model = PackageItinerary
    extra = 0
    fields = ['day_number', 'title', 'breakfast_included', 'lunch_included', 'dinner_included', 'is_active']
    classes = ['collapse']
    show_change_link = True


class PackageInclusionInline(admin.TabularInline):
    """Inline admin for package inclusions/exclusions"""
    model = PackageInclusion
    extra = 1
    fields = ['inclusion_type', 'item_name', 'is_included', 'order', 'is_active']
    classes = ['collapse']


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    """Admin interface for Package model"""
    list_display = [
        'name', 'category', 'difficulty_level', 'duration_display',
        'price_display', 'availability_badge', 'booking_stats',
        'is_featured', 'is_active', 'created_at'
    ]
    list_filter = [
        'category', 'difficulty_level', 'availability_status',
        'is_active', 'is_featured', 'is_customizable', 'created_at'
    ]
    search_fields = ['name', 'short_description', 'description']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['destinations']
    readonly_fields = [
        'slug', 'current_bookings', 'booking_count', 'view_count',
        'rating_average', 'review_count', 'created_at', 'updated_at',
        'final_price', 'discount_amount', 'spots_remaining'
    ]
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name', 'slug', 'destinations', 'category', 'difficulty_level',
                'short_description', 'description', 'highlights'
            )
        }),
        ('Duration & Group Size', {
            'fields': (
                'duration_days', 'duration_nights', 'group_size_min', 'group_size_max'
            )
        }),
        ('Pricing', {
            'fields': (
                'price_per_person', 'currency', 'discount_percentage',
                'final_price', 'discount_amount'
            )
        }),
        ('Availability', {
            'fields': (
                'availability_status', 'start_date', 'end_date',
                'max_bookings', 'current_bookings', 'spots_remaining'
            )
        }),
        ('Details', {
            'fields': (
                'included_items', 'excluded_items', 'requirements',
                'cancellation_policy', 'terms_and_conditions'
            ),
            'classes': ('collapse',)
        }),
        ('Media', {
            'fields': ('featured_image', 'video_url')
        }),
        ('Settings', {
            'fields': (
                'is_customizable', 'is_active', 'is_featured', 'order'
            )
        }),
        ('Statistics', {
            'fields': (
                'booking_count', 'view_count', 'rating_average', 'review_count'
            ),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [PackageImageInline, PackageItineraryInline, PackageInclusionInline]
    date_hierarchy = 'created_at'
    list_per_page = 25
    actions = ['make_featured', 'remove_featured', 'activate', 'deactivate']
    
    def duration_display(self, obj):
        """Display duration as days/nights"""
        return f"{obj.duration_days}D/{obj.duration_nights}N"
    duration_display.short_description = 'Duration'
    
    def price_display(self, obj):
        """Display price with currency"""
        if obj.discount_percentage > 0:
            return format_html(
                '<span style="text-decoration: line-through;">{} {}</span><br>'
                '<strong style="color: #28a745;">{} {} (-{}%)</strong>',
                obj.currency, obj.price_per_person,
                obj.currency, obj.final_price, obj.discount_percentage
            )
        return f"{obj.currency} {obj.price_per_person}"
    price_display.short_description = 'Price'
    
    def availability_badge(self, obj):
        """Display availability status with color"""
        colors = {
            'available': '#28a745',
            'sold_out': '#dc3545',
            'coming_soon': '#ffc107',
            'seasonal': '#17a2b8',
        }
        color = colors.get(obj.availability_status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.get_availability_status_display()
        )
    availability_badge.short_description = 'Availability'
    
    def booking_stats(self, obj):
        """Display booking statistics"""
        return format_html(
            '<strong>{}</strong> bookings<br>'
            '<span style="color: #6c757d;">{} views</span>',
            obj.booking_count, obj.view_count
        )
    booking_stats.short_description = 'Stats'
    
    def make_featured(self, request, queryset):
        """Mark selected packages as featured"""
        count = queryset.update(is_featured=True)
        self.message_user(request, f'{count} package(s) marked as featured.')
    make_featured.short_description = 'Mark as featured'
    
    def remove_featured(self, request, queryset):
        """Remove featured status"""
        count = queryset.update(is_featured=False)
        self.message_user(request, f'{count} package(s) removed from featured.')
    remove_featured.short_description = 'Remove from featured'
    
    def activate(self, request, queryset):
        """Activate selected packages"""
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} package(s) activated.')
    activate.short_description = 'Activate'
    
    def deactivate(self, request, queryset):
        """Deactivate selected packages"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} package(s) deactivated.')
    deactivate.short_description = 'Deactivate'
    
    def save_model(self, request, obj, form, change):
        """Set created_by on package creation"""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(PackageImage)
class PackageImageAdmin(admin.ModelAdmin):
    """Admin interface for PackageImage model"""
    list_display = ['package', 'image_preview', 'caption', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['package__name', 'caption']
    list_editable = ['order', 'is_active']
    list_per_page = 50
    
    def image_preview(self, obj):
        """Display image thumbnail"""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return '-'
    image_preview.short_description = 'Preview'


@admin.register(PackageItinerary)
class PackageItineraryAdmin(admin.ModelAdmin):
    """Admin interface for PackageItinerary model"""
    list_display = [
        'package', 'day_number', 'title', 'meals_badge',
        'accommodation', 'is_active', 'created_at'
    ]
    list_filter = [
        'breakfast_included', 'lunch_included', 'dinner_included',
        'is_active', 'created_at'
    ]
    search_fields = ['package__name', 'title', 'description']
    filter_horizontal = ['activities']
    list_per_page = 50
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('package', 'day_number', 'title', 'description')
        }),
        ('Activities & Accommodation', {
            'fields': ('activities', 'accommodation')
        }),
        ('Meals', {
            'fields': ('breakfast_included', 'lunch_included', 'dinner_included')
        }),
        ('Additional Info', {
            'fields': ('highlights', 'notes', 'order', 'is_active')
        }),
    )
    
    def meals_badge(self, obj):
        """Display included meals with icons"""
        meals = []
        if obj.breakfast_included:
            meals.append('🍳 B')
        if obj.lunch_included:
            meals.append('🍽️ L')
        if obj.dinner_included:
            meals.append('🍷 D')
        return ' | '.join(meals) if meals else '-'
    meals_badge.short_description = 'Meals'


@admin.register(PackageInclusion)
class PackageInclusionAdmin(admin.ModelAdmin):
    """Admin interface for PackageInclusion model"""
    list_display = [
        'package', 'item_name', 'inclusion_type',
        'inclusion_badge', 'order', 'is_active', 'created_at'
    ]
    list_filter = ['inclusion_type', 'is_included', 'is_active', 'created_at']
    search_fields = ['package__name', 'item_name', 'description']
    list_editable = ['order', 'is_active']
    list_per_page = 50
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('package', 'inclusion_type', 'item_name', 'description')
        }),
        ('Details', {
            'fields': ('quantity', 'is_included', 'order', 'is_active')
        }),
    )
    
    def inclusion_badge(self, obj):
        """Display inclusion/exclusion badge"""
        if obj.is_included:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 10px; '
                'border-radius: 3px; font-size: 11px;">✓ Included</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px;">✗ Excluded</span>'
        )
    inclusion_badge.short_description = 'Status'


# ============================================================================
# BOOKING INQUIRY & CUSTOM PACKAGE ADMIN (Phase 2A)
# ============================================================================

class InquiryMessageInline(admin.TabularInline):
    """Inline admin for inquiry messages"""
    model = InquiryMessage
    extra = 0
    fields = ['sender_staff', 'message', 'is_internal', 'created_at']
    readonly_fields = ['created_at']
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(BookingInquiry)
class BookingInquiryAdmin(admin.ModelAdmin):
    """Admin interface for Booking Inquiries"""
    list_display = [
        'inquiry_reference', 'customer_name', 'base_package',
        'status_badge', 'priority_badge', 'staff_assigned',
        'total_travelers', 'budget_display', 'created_at', 'action_links'
    ]
    list_filter = [
        'status', 'priority', 'staff_assigned',
        'accommodation_preference', 'created_at', 'preferred_travel_date'
    ]
    search_fields = [
        'inquiry_reference', 'customer_name', 'customer_email',
        'customer_phone', 'special_requests'
    ]
    readonly_fields = [
        'inquiry_reference', 'created_at', 'updated_at',
        'viewed_by_staff', 'first_viewed_at', 'last_activity_at',
        'ip_address', 'days_since_inquiry', 'action_links'
    ]
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Inquiry Information', {
            'fields': ('inquiry_reference', 'base_package', 'status', 'priority')
        }),
        ('Customer Details', {
            'fields': (
                'customer_name', 'customer_email', 'customer_phone',
                'country', 'source'
            )
        }),
        ('Travel Details', {
            'fields': (
                'preferred_travel_date', 'flexible_dates',
                'alternative_date_1', 'alternative_date_2',
                'number_of_adults', 'number_of_children', 'number_of_infants'
            )
        }),
        ('Preferences', {
            'fields': (
                'budget_range', 'specific_budget',
                'accommodation_preference',
                'dietary_requirements', 'special_requests'
            )
        }),
        ('Contact Preferences', {
            'fields': ('prefer_email', 'prefer_phone', 'prefer_whatsapp')
        }),
        ('Management', {
            'fields': ('staff_assigned', 'staff_notes', 'custom_package')
        }),
        ('Tracking', {
            'fields': (
                'viewed_by_staff', 'first_viewed_at', 'last_activity_at',
                'ip_address', 'days_since_inquiry', 'created_at', 'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [InquiryMessageInline]
    
    def status_badge(self, obj):
        """Display colored status badge"""
        colors = {
            'pending': '#dc3545',
            'reviewing': '#ffc107',
            'quote_sent': '#17a2b8',
            'negotiating': '#007bff',
            'approved': '#28a745',
            'payment_pending': '#fd7e14',
            'converted': '#28a745',
            'declined': '#6c757d',
            'expired': '#6c757d',
            'spam': '#343a40',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px; font-weight: 600;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def priority_badge(self, obj):
        """Display priority badge"""
        colors = {
            'normal': '#6c757d',
            'high': '#ffc107',
            'urgent': '#dc3545',
        }
        color = colors.get(obj.priority, '#6c757d')
        icon = '🔥' if obj.priority == 'urgent' else ('⚠️' if obj.priority == 'high' else '📋')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px;">{} {}</span>',
            color, icon, obj.get_priority_display()
        )
    priority_badge.short_description = 'Priority'
    
    def budget_display(self, obj):
        """Display budget range"""
        return obj.get_budget_display_text()
    budget_display.short_description = 'Budget'
    
    def action_links(self, obj):
        """Display action links"""
        if obj.pk:
            dashboard_url = reverse('packages:dashboard_inquiry_detail', args=[obj.pk])
            create_quote_url = reverse('packages:dashboard_custom_package_builder', args=[obj.pk])
            return mark_safe(
                f'<a href="{dashboard_url}" class="button" style="margin-right: 5px;">View Details</a>'
                f'<a href="{create_quote_url}" class="button">Create Quote</a>'
            )
        return '-'
    action_links.short_description = 'Actions'
    
    def days_since_inquiry(self, obj):
        """Display days since inquiry"""
        days = obj.days_since_inquiry
        if days == 0:
            return 'Today'
        elif days == 1:
            return 'Yesterday'
        else:
            return f'{days} days ago'
    days_since_inquiry.short_description = 'Age'


@admin.register(CustomPackage)
class CustomPackageAdmin(admin.ModelAdmin):
    """Admin interface for Custom Packages"""
    list_display = [
        'custom_reference', 'inquiry', 'name',
        'status_badge', 'pricing_display', 'created_by',
        'view_stats', 'expires_display', 'action_links'
    ]
    list_filter = ['status', 'created_by', 'created_at', 'sent_at']
    search_fields = [
        'custom_reference', 'name',
        'inquiry__customer_name', 'inquiry__customer_email'
    ]
    readonly_fields = [
        'custom_reference', 'access_token', 'created_at', 'updated_at',
        'sent_at', 'first_viewed_at', 'last_viewed_at', 'view_count',
        'approved_at', 'rejected_at', 'revision_number',
        'price_difference', 'discount_percentage', 'total_price',
        'is_expired', 'days_until_expiry', 'secure_link'
    ]
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Package Information', {
            'fields': (
                'custom_reference', 'inquiry', 'base_package',
                'name', 'short_description', 'description'
            )
        }),
        ('Duration & Pricing', {
            'fields': (
                'duration_days', 'duration_nights',
                'original_price', 'adjusted_price', 'currency',
                'price_difference', 'discount_percentage', 'total_price'
            )
        }),
        ('Customization Notes', {
            'fields': (
                'modifications_made',
                'staff_notes_to_client',
                'staff_internal_notes',
                'client_feedback'
            )
        }),
        ('Status & Management', {
            'fields': (
                'status', 'expires_at', 'is_expired', 'days_until_expiry',
                'created_by', 'last_modified_by', 'revision_number'
            )
        }),
        ('Client Tracking', {
            'fields': (
                'sent_at', 'first_viewed_at', 'last_viewed_at', 'view_count',
                'approved_at', 'rejected_at'
            ),
            'classes': ('collapse',)
        }),
        ('Access', {
            'fields': ('access_token', 'secure_link'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        """Display colored status badge"""
        colors = {
            'draft': '#6c757d',
            'sent': '#17a2b8',
            'viewed': '#007bff',
            'approved': '#28a745',
            'rejected': '#dc3545',
            'expired': '#6c757d',
            'cancelled': '#343a40',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px; font-weight: 600;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def pricing_display(self, obj):
        """Display pricing with discount"""
        if obj.discount_percentage > 0:
            return format_html(
                '<span style="text-decoration: line-through; color: #999;">{} {}</span><br>'
                '<span style="color: #28a745; font-weight: bold;">{} {}</span> '
                '<span style="background-color: #dc3545; color: white; padding: 2px 6px; '
                'border-radius: 3px; font-size: 10px;">-{}%</span>',
                obj.currency, obj.original_price,
                obj.currency, obj.adjusted_price,
                int(obj.discount_percentage)
            )
        return f'{obj.currency} {obj.adjusted_price}'
    pricing_display.short_description = 'Pricing'
    
    def view_stats(self, obj):
        """Display view statistics"""
        return format_html(
            '👁️ {} view{}<br>',
            obj.view_count,
            's' if obj.view_count != 1 else ''
        )
    view_stats.short_description = 'Views'
    
    def expires_display(self, obj):
        """Display expiry status"""
        if obj.is_expired:
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">⚠️ Expired</span>'
            )
        elif obj.expires_at:
            days = obj.days_until_expiry
            if days == 0:
                return format_html(
                    '<span style="color: #ffc107; font-weight: bold;">⏰ Expires today</span>'
                )
            elif days <= 2:
                return format_html(
                    '<span style="color: #fd7e14; font-weight: bold;">⏰ {} day{} left</span>',
                    days, 's' if days != 1 else ''
                )
            else:
                return f'✓ {days} days left'
        return 'No expiry'
    expires_display.short_description = 'Expiry'
    
    def action_links(self, obj):
        """Display action links"""
        if obj.pk:
            dashboard_url = reverse('packages:dashboard_custom_package_detail', args=[obj.pk])
            send_url = reverse('packages:dashboard_custom_package_send', args=[obj.pk])
            links = f'<a href="{dashboard_url}" class="button" style="margin-right: 5px;">Edit</a>'
            if obj.status == 'draft':
                links += f'<a href="{send_url}" class="button">Send to Client</a>'
            return mark_safe(links)
        return '-'
    action_links.short_description = 'Actions'
    
    def secure_link(self, obj):
        """Display secure client link"""
        if obj.access_token:
            link = f'/packages/custom/{obj.access_token}/'
            return mark_safe(
                f'<a href="{link}" target="_blank" style="font-family: monospace;">{link}</a><br>'
                f'<small style="color: #6c757d;">Share this link with client</small>'
            )
        return '-'
    secure_link.short_description = 'Client Link'


@admin.register(InquiryMessage)
class InquiryMessageAdmin(admin.ModelAdmin):
    """Admin interface for Inquiry Messages"""
    list_display = [
        'inquiry', 'sender_display', 'message_preview',
        'message_type', 'created_at', 'is_read'
    ]
    list_filter = ['is_internal', 'is_automated', 'is_read', 'created_at']
    search_fields = ['inquiry__inquiry_reference', 'message', 'subject']
    readonly_fields = ['created_at', 'read_at']
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Message Information', {
            'fields': ('inquiry', 'subject', 'message', 'attachment')
        }),
        ('Sender', {
            'fields': ('sender_staff', 'sender_email', 'sender_name')
        }),
        ('Type & Status', {
            'fields': ('is_internal', 'is_automated', 'is_read', 'read_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def sender_display(self, obj):
        """Display sender name"""
        if obj.sender_staff:
            return format_html(
                '<span style="color: #007bff;">👤 {} (Staff)</span>',
                obj.sender_staff.get_full_name() or obj.sender_staff.username
            )
        return format_html(
            '<span style="color: #28a745;">👥 {} (Client)</span>',
            obj.sender_name or obj.sender_email
        )
    sender_display.short_description = 'Sender'
    
    def message_preview(self, obj):
        """Display message preview"""
        preview = obj.message[:100] + '...' if len(obj.message) > 100 else obj.message
        return preview
    message_preview.short_description = 'Message'
    
    def message_type(self, obj):
        """Display message type badge"""
        if obj.is_internal:
            return format_html(
                '<span style="background-color: #6c757d; color: white; padding: 2px 8px; '
                'border-radius: 3px; font-size: 10px;">🔒 Internal</span>'
            )
        elif obj.is_automated:
            return format_html(
                '<span style="background-color: #17a2b8; color: white; padding: 2px 8px; '
                'border-radius: 3px; font-size: 10px;">🤖 Auto</span>'
            )
        return format_html(
            '<span style="background-color: #28a745; color: white; padding: 2px 8px; '
            'border-radius: 3px; font-size: 10px;">📧 Public</span>'
        )
    message_type.short_description = 'Type'


# ============================================================================
# BOOKING SYSTEM ADMIN (Phase 2)
# ============================================================================

class PassengerInline(admin.TabularInline):
    model = Passenger
    extra = 0
    fields = ['first_name', 'last_name', 'passport_number', 'nationality', 'is_lead_passenger']
    classes = ['collapse']


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    fields = ['payment_type', 'amount', 'currency', 'payment_method', 'status', 'received_at']
    readonly_fields = ['received_at']
    classes = ['collapse']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'booking_reference', 'package', 'inquiry_link',
        'departure_date', 'travelers_display', 'price_display',
        'status_badge', 'created_at',
    ]
    list_filter = ['status', 'currency', 'departure_date', 'created_at']
    search_fields = [
        'booking_reference', 'package__name',
        'inquiry__customer_name', 'inquiry__customer_email',
    ]
    readonly_fields = [
        'booking_reference', 'total_travelers', 'total_paid',
        'balance_due', 'is_fully_paid', 'created_at', 'updated_at',
    ]
    date_hierarchy = 'created_at'
    list_per_page = 25
    inlines = [PassengerInline, PaymentInline]

    fieldsets = (
        ('Booking Info', {
            'fields': (
                'booking_reference', 'package', 'inquiry', 'custom_package',
                'staff_assigned', 'status',
            )
        }),
        ('Travel Details', {
            'fields': (
                'departure_date', 'return_date',
                'num_adults', 'num_children', 'total_travelers',
            )
        }),
        ('Pricing', {
            'fields': (
                'quoted_price', 'deposit_amount', 'currency',
                'total_paid', 'balance_due', 'is_fully_paid',
            )
        }),
        ('Notes', {
            'fields': ('special_requirements', 'internal_notes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def travelers_display(self, obj):
        return f"{obj.num_adults}A / {obj.num_children}C"
    travelers_display.short_description = 'Travelers'

    def price_display(self, obj):
        return format_html(
            '{} {}<br><small>Deposit: {} {}</small>',
            obj.currency, obj.quoted_price,
            obj.currency, obj.deposit_amount,
        )
    price_display.short_description = 'Price'

    def status_badge(self, obj):
        colors = {
            'pending_deposit': '#ffc107',
            'deposit_paid': '#17a2b8',
            'confirmed': '#28a745',
            'in_progress': '#007bff',
            'completed': '#20c997',
            'cancelled': '#dc3545',
            'refunded': '#6c757d',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px; font-weight: 600;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def inquiry_link(self, obj):
        if obj.inquiry:
            url = reverse('packages:dashboard_inquiry_detail', args=[obj.inquiry.pk])
            return mark_safe(f'<a href="{url}">{obj.inquiry.customer_name}</a>')
        return '-'
    inquiry_link.short_description = 'Customer'


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'booking', 'nationality',
        'passport_number', 'is_lead_passenger', 'created_at',
    ]
    list_filter = ['is_lead_passenger', 'nationality', 'created_at']
    search_fields = [
        'first_name', 'last_name', 'passport_number',
        'booking__booking_reference',
    ]
    list_per_page = 50


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'booking', 'payment_type', 'amount_display',
        'payment_method', 'status_badge', 'received_at', 'recorded_by',
    ]
    list_filter = ['payment_type', 'payment_method', 'status', 'received_at']
    search_fields = [
        'booking__booking_reference', 'reference_number',
        'booking__inquiry__customer_name',
    ]
    readonly_fields = ['received_at', 'created_at', 'updated_at']
    list_per_page = 50
    date_hierarchy = 'received_at'

    def amount_display(self, obj):
        return f"{obj.currency} {obj.amount}"
    amount_display.short_description = 'Amount'

    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'confirmed': '#28a745',
            'refunded': '#17a2b8',
            'failed': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'

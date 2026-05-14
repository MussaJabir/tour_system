from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal
import uuid

from core.models import TimeStampedModel, SEOMixin, PublishableMixin, SlugMixin, ViewCountMixin
from destinations.models import Destination
from activities.models import Activity
from accommodations.models import Accommodation

User = get_user_model()


class Package(TimeStampedModel, SEOMixin, PublishableMixin, SlugMixin, ViewCountMixin):
    """
    Main Package model - The money-making product!
    Represents a complete tour package with destinations, itinerary, and pricing.
    """
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('challenging', 'Challenging'),
        ('extreme', 'Extreme'),
    ]
    
    CATEGORY_CHOICES = [
        ('adventure', 'Adventure'),
        ('luxury', 'Luxury'),
        ('family', 'Family'),
        ('honeymoon', 'Honeymoon'),
        ('group', 'Group'),
        ('budget', 'Budget'),
        ('wildlife', 'Wildlife Safari'),
        ('cultural', 'Cultural'),
        ('beach', 'Beach'),
        ('trekking', 'Trekking'),
    ]
    
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('sold_out', 'Sold Out'),
        ('coming_soon', 'Coming Soon'),
        ('seasonal', 'Seasonal'),
    ]
    
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('KES', 'Kenyan Shilling'),
        ('TZS', 'Tanzanian Shilling'),
    ]

    # Basic Information
    name = models.CharField(max_length=200, unique=True, help_text="Package name (e.g., '7-Day Serengeti Safari Adventure')")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    destinations = models.ManyToManyField(Destination, related_name='packages', help_text="Destinations included in this package")
    
    # Description
    description = models.TextField(help_text="Detailed package description")
    short_description = models.CharField(max_length=300, help_text="Brief summary for listings")
    highlights = models.TextField(blank=True, help_text="Key highlights (one per line or comma-separated)")
    
    # Duration
    duration_days = models.PositiveIntegerField(validators=[MinValueValidator(1)], help_text="Number of days")
    duration_nights = models.PositiveIntegerField(validators=[MinValueValidator(0)], help_text="Number of nights")
    
    # Classification
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='adventure', db_index=True)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='moderate', db_index=True)
    
    # Group Size
    group_size_min = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], help_text="Minimum group size")
    group_size_max = models.PositiveIntegerField(default=12, validators=[MinValueValidator(1)], help_text="Maximum group size")
    
    # Pricing
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], help_text="Base price per person")
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text="Discount percentage (0-100)")
    
    # Availability
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='available', db_index=True)
    start_date = models.DateField(null=True, blank=True, help_text="Package start date (for seasonal packages)")
    end_date = models.DateField(null=True, blank=True, help_text="Package end date (for seasonal packages)")
    
    # Capacity Management
    max_bookings = models.PositiveIntegerField(default=10, help_text="Maximum number of bookings allowed")
    current_bookings = models.PositiveIntegerField(default=0, help_text="Current number of bookings")
    
    # Inclusions & Exclusions
    included_items = models.TextField(blank=True, help_text="What's included (one per line)")
    excluded_items = models.TextField(blank=True, help_text="What's NOT included (one per line)")
    requirements = models.TextField(blank=True, help_text="Requirements (e.g., 'Valid passport', 'Physical fitness')")
    
    # Policies
    cancellation_policy = models.TextField(default="Full refund if cancelled 30 days before departure. 50% refund if cancelled 15-29 days before. No refund if cancelled within 14 days.", help_text="Cancellation and refund policy")
    terms_and_conditions = models.TextField(blank=True, help_text="Terms and conditions")
    
    # Media
    featured_image = models.ImageField(upload_to='packages/', blank=True, null=True, help_text="Main package image")
    video_url = models.URLField(blank=True, null=True, help_text="YouTube or Vimeo video URL")
    
    # Customization
    is_customizable = models.BooleanField(default=False, help_text="Can customers request custom modifications?")
    
    # Tracking & Analytics
    booking_count = models.PositiveIntegerField(default=0, help_text="Total number of bookings")
    rating_average = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    review_count = models.PositiveIntegerField(default=0)
    
    # Management
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='packages_created')

    class Meta:
        ordering = ['order', '-is_featured', '-created_at']
        verbose_name = "Package"
        verbose_name_plural = "Packages"
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['availability_status', 'is_active']),
            models.Index(fields=['price_per_person']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Auto-generate slug
        if not self.slug:
            self.slug = slugify(self.name)
        
        # Auto-generate meta_title if not provided
        if not self.meta_title:
            self.meta_title = f"{self.name} - {self.duration_days}D/{self.duration_nights}N Tour Package"
        
        # Calculate duration_nights if not provided
        if not self.duration_nights and self.duration_days:
            self.duration_nights = max(0, self.duration_days - 1)
        
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('packages:public_package_detail', kwargs={'slug': self.slug})

    def get_dashboard_url(self):
        return reverse('packages:dashboard_package_edit', kwargs={'pk': self.pk})

    @property
    def final_price(self):
        """Calculate final price after discount"""
        if self.discount_percentage > 0:
            discount_amount = self.price_per_person * (self.discount_percentage / 100)
            return self.price_per_person - discount_amount
        return self.price_per_person

    @property
    def discount_amount(self):
        """Calculate discount amount"""
        if self.discount_percentage > 0:
            return self.price_per_person * (self.discount_percentage / 100)
        return Decimal('0.00')

    @property
    def is_available(self):
        """Check if package is available for booking"""
        if not self.is_active:
            return False
        if self.availability_status != 'available':
            return False
        if self.max_bookings > 0 and self.current_bookings >= self.max_bookings:
            return False
        return True

    @property
    def spots_remaining(self):
        """Calculate remaining spots"""
        if self.max_bookings > 0:
            return max(0, self.max_bookings - self.current_bookings)
        return None  # Unlimited

    @property
    def duration_display(self):
        """Human-readable duration"""
        return f"{self.duration_days}D/{self.duration_nights}N"

    def increment_booking_count(self):
        """Increment booking count"""
        self.booking_count += 1
        self.current_bookings += 1
        if self.current_bookings >= self.max_bookings:
            self.availability_status = 'sold_out'
        self.save(update_fields=['booking_count', 'current_bookings', 'availability_status'])

    def decrement_booking_count(self):
        """Decrement booking count (for cancellations)"""
        if self.current_bookings > 0:
            self.current_bookings -= 1
            if self.availability_status == 'sold_out' and self.current_bookings < self.max_bookings:
                self.availability_status = 'available'
            self.save(update_fields=['current_bookings', 'availability_status'])

    def update_rating(self):
        """Recalculate average rating from reviews"""
        reviews = self.reviews.filter(is_approved=True)
        if reviews.exists():
            self.rating_average = reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0
            self.review_count = reviews.count()
        else:
            self.rating_average = 0
            self.review_count = 0
        self.save(update_fields=['rating_average', 'review_count'])
    
    @property
    def total_itinerary_days(self):
        """Calculate total days covered by all itinerary entries"""
        total = 0
        for itinerary in self.itineraries.all():
            total += itinerary.duration_days
        return total


class PackageImage(TimeStampedModel):
    """Gallery images for packages"""
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='packages/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Package Image"
        verbose_name_plural = "Package Images"

    def __str__(self):
        return f"Image for {self.package.name}"


class PackageItinerary(TimeStampedModel):
    """Day-by-day itinerary for packages"""
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='itineraries')
    day_number = models.PositiveIntegerField(validators=[MinValueValidator(1)], help_text="Start day number")
    end_day_number = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        validators=[MinValueValidator(1)],
        help_text="End day number (leave blank for single day, or set for day ranges like Days 3-7)"
    )
    title = models.CharField(max_length=200, help_text="Day title (e.g., 'Day 1: Arrival in Arusha')")
    description = models.TextField(help_text="Detailed activities for this day or period")
    
    # Related entities
    activities = models.ManyToManyField(Activity, blank=True, related_name='package_itineraries', help_text="Activities scheduled for this day")
    accommodation = models.ForeignKey(Accommodation, on_delete=models.SET_NULL, null=True, blank=True, related_name='package_itineraries', help_text="Where guests stay this night")
    
    # Meals
    breakfast_included = models.BooleanField(default=False)
    lunch_included = models.BooleanField(default=False)
    dinner_included = models.BooleanField(default=False)
    
    # Additional Info
    highlights = models.CharField(max_length=500, blank=True, help_text="Key highlights for this day")
    notes = models.TextField(blank=True, help_text="Optional notes (e.g., 'Early morning departure')")
    
    # Ordering
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['package', 'day_number', 'order']
        verbose_name = "Package Itinerary"
        verbose_name_plural = "Package Itineraries"
        unique_together = ['package', 'day_number']

    def __str__(self):
        return f"{self.package.name} - {self.day_display}"

    @property
    def day_display(self):
        """Display day number or range"""
        if self.end_day_number and self.end_day_number > self.day_number:
            return f"Days {self.day_number}-{self.end_day_number}"
        return f"Day {self.day_number}"
    
    @property
    def duration_days(self):
        """Calculate how many days this itinerary covers"""
        if self.end_day_number and self.end_day_number > self.day_number:
            return self.end_day_number - self.day_number + 1
        return 1

    @property
    def meals_display(self):
        """Human-readable meals included"""
        meals = []
        if self.breakfast_included:
            meals.append('Breakfast')
        if self.lunch_included:
            meals.append('Lunch')
        if self.dinner_included:
            meals.append('Dinner')
        return ', '.join(meals) if meals else 'No meals'


class PackageInclusion(TimeStampedModel):
    """What's included/excluded in a package"""
    INCLUSION_TYPE_CHOICES = [
        ('accommodation', 'Accommodation'),
        ('activity', 'Activity'),
        ('transport', 'Transport'),
        ('meals', 'Meals'),
        ('guide', 'Guide'),
        ('equipment', 'Equipment'),
        ('insurance', 'Insurance'),
        ('visa', 'Visa'),
        ('other', 'Other'),
    ]

    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='inclusions')
    inclusion_type = models.CharField(max_length=50, choices=INCLUSION_TYPE_CHOICES, default='other')
    item_name = models.CharField(max_length=200, help_text="e.g., '4-star hotel accommodation'")
    description = models.TextField(blank=True, help_text="Optional detailed description")
    quantity = models.CharField(max_length=100, blank=True, help_text="e.g., '3 nights', '2 meals per day'")
    is_included = models.BooleanField(default=True, help_text="True = Included, False = Excluded")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['package', 'is_included', 'order', 'inclusion_type']
        verbose_name = "Package Inclusion"
        verbose_name_plural = "Package Inclusions"

    def __str__(self):
        status = "Included" if self.is_included else "Excluded"
        return f"{self.package.name} - {status}: {self.item_name}"


# ============================================================================
# BOOKING INQUIRY & CUSTOM PACKAGE MODELS (Phase 2A)
# ============================================================================

class BookingInquiry(TimeStampedModel):
    """
    Initial customer inquiry/request for a package.
    This is the first step before creating a custom package.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending - New Inquiry'),
        ('reviewing', 'Reviewing - Staff Assigned'),
        ('quote_sent', 'Quote Sent - Awaiting Client'),
        ('negotiating', 'Negotiating - Discussion Ongoing'),
        ('approved', 'Approved - Client Confirmed'),
        ('payment_pending', 'Payment Pending'),
        ('converted', 'Converted to Booking'),
        ('declined', 'Declined by Client'),
        ('expired', 'Expired - No Response'),
        ('spam', 'Spam/Invalid'),
    ]
    
    BUDGET_CHOICES = [
        ('flexible', 'Flexible / Open Budget'),
        ('under_1000', 'Under $1,000'),
        ('1000_2000', '$1,000 - $2,000'),
        ('2000_3000', '$2,000 - $3,000'),
        ('3000_5000', '$3,000 - $5,000'),
        ('over_5000', '$5,000+'),
        ('specific', 'Specific Amount'),
    ]
    
    ACCOMMODATION_CHOICES = [
        ('budget', 'Budget Friendly'),
        ('standard', 'Standard'),
        ('luxury', 'Luxury'),
        ('ultra_luxury', 'Ultra Luxury'),
    ]
    
    PRIORITY_CHOICES = [
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Reference Number
    inquiry_reference = models.CharField(
        max_length=50, 
        unique=True, 
        editable=False,
        help_text="Auto-generated unique inquiry reference (e.g., INQ-2024-110001)"
    )
    
    # Package Interest
    base_package = models.ForeignKey(
        Package,
        on_delete=models.SET_NULL,
        null=True,
        related_name='inquiries',
        help_text="Original package customer is interested in"
    )
    
    # Customer Information
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=50)
    country = models.CharField(max_length=100, blank=True)
    
    # How did they find us?
    source = models.CharField(
        max_length=100,
        blank=True,
        help_text="How did they hear about us? (Google, Social Media, Friend, etc.)"
    )
    
    # Travel Details
    preferred_travel_date = models.DateField(null=True, blank=True)
    flexible_dates = models.BooleanField(default=False, help_text="Are dates flexible?")
    alternative_date_1 = models.DateField(null=True, blank=True)
    alternative_date_2 = models.DateField(null=True, blank=True)
    
    # Travelers
    number_of_adults = models.PositiveIntegerField(default=2, validators=[MinValueValidator(1)])
    number_of_children = models.PositiveIntegerField(default=0)
    number_of_infants = models.PositiveIntegerField(default=0)
    
    # Budget & Preferences
    budget_range = models.CharField(max_length=50, choices=BUDGET_CHOICES, default='flexible')
    specific_budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Specific budget per person (if budget_range = 'specific')"
    )
    
    accommodation_preference = models.CharField(
        max_length=50,
        choices=ACCOMMODATION_CHOICES,
        default='standard'
    )
    
    # Special Requirements
    dietary_requirements = models.TextField(blank=True, help_text="Any dietary restrictions")
    special_requests = models.TextField(blank=True, help_text="Any special interests or requests")
    
    # Preferred Contact
    prefer_email = models.BooleanField(default=True)
    prefer_phone = models.BooleanField(default=False)
    prefer_whatsapp = models.BooleanField(default=False)
    
    # Status & Management
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='normal')
    
    staff_assigned = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_inquiries',
        help_text="Staff member handling this inquiry"
    )
    
    staff_notes = models.TextField(
        blank=True,
        help_text="Internal staff notes (not visible to client)"
    )
    
    # Tracking
    viewed_by_staff = models.BooleanField(default=False)
    first_viewed_at = models.DateTimeField(null=True, blank=True)
    last_activity_at = models.DateTimeField(auto_now=True)
    
    # Conversion
    custom_package = models.ForeignKey(
        'CustomPackage',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='linked_inquiry',
        help_text="Custom package created for this inquiry"
    )
    
    # IP tracking for security
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Booking Inquiry"
        verbose_name_plural = "Booking Inquiries"
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['staff_assigned', 'status']),
        ]
    
    def save(self, *args, **kwargs):
        # Generate inquiry reference if not set
        if not self.inquiry_reference:
            from django.utils import timezone
            date_str = timezone.now().strftime('%Y%m%d')
            # Get last inquiry of the day
            last_inquiry = BookingInquiry.objects.filter(
                inquiry_reference__startswith=f'INQ-{date_str}'
            ).order_by('-inquiry_reference').first()
            
            if last_inquiry:
                # Extract number and increment
                last_num = int(last_inquiry.inquiry_reference.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            
            self.inquiry_reference = f'INQ-{date_str}-{new_num:05d}'
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.inquiry_reference} - {self.customer_name}"
    
    @property
    def total_travelers(self):
        return self.number_of_adults + self.number_of_children + self.number_of_infants
    
    @property
    def days_since_inquiry(self):
        from django.utils import timezone
        delta = timezone.now() - self.created_at
        return delta.days
    
    @property
    def is_urgent(self):
        """Mark as urgent if no response in 3+ days"""
        return self.status == 'pending' and self.days_since_inquiry >= 3
    
    @property
    def status_badge_color(self):
        """Return Bootstrap color class for status badge"""
        status_colors = {
            'pending': 'danger',
            'reviewing': 'warning',
            'quote_sent': 'info',
            'negotiating': 'primary',
            'approved': 'success',
            'payment_pending': 'warning',
            'converted': 'success',
            'declined': 'secondary',
            'expired': 'secondary',
            'spam': 'dark',
        }
        return status_colors.get(self.status, 'secondary')
    
    def get_budget_display_text(self):
        """Return human-readable budget"""
        if self.budget_range == 'specific' and self.specific_budget:
            return f"${self.specific_budget:.0f} per person"
        return self.get_budget_range_display()


class CustomPackage(TimeStampedModel):
    """
    Staff-created customized package for specific client.
    Cloned from base package and modified based on client requirements.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft - Staff Working'),
        ('sent', 'Sent to Client'),
        ('viewed', 'Viewed by Client'),
        ('approved', 'Approved by Client'),
        ('rejected', 'Rejected by Client'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Reference & Links
    custom_reference = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
        help_text="Unique reference (e.g., CUSTOM-2024-001)"
    )
    
    inquiry = models.ForeignKey(
        BookingInquiry,
        on_delete=models.CASCADE,
        related_name='custom_packages',
        help_text="Original inquiry this package is for"
    )
    
    base_package = models.ForeignKey(
        Package,
        on_delete=models.SET_NULL,
        null=True,
        related_name='custom_versions',
        help_text="Base package used as template"
    )
    
    # Secure Access
    access_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        help_text="Secure token for client access"
    )
    
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Quote expiry date (typically 7 days)"
    )
    
    # Package Details (Copied from base, then customized)
    name = models.CharField(max_length=200)
    short_description = models.TextField(max_length=500)
    description = models.TextField()
    
    # Duration
    duration_days = models.PositiveIntegerField()
    duration_nights = models.PositiveIntegerField()
    
    # Pricing
    original_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Original base package price per person"
    )
    
    adjusted_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Custom price per person after modifications"
    )
    
    currency = models.CharField(max_length=3, default='USD')
    
    # Customization Notes
    modifications_made = models.TextField(
        blank=True,
        help_text="Summary of changes from base package"
    )
    
    staff_notes_to_client = models.TextField(
        blank=True,
        help_text="Personal message from staff to client (visible)"
    )
    
    staff_internal_notes = models.TextField(
        blank=True,
        help_text="Internal notes (not visible to client)"
    )
    
    # Status & Management
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='draft')
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_custom_packages'
    )
    
    last_modified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='modified_custom_packages'
    )
    
    # Client Interaction Tracking
    sent_at = models.DateTimeField(null=True, blank=True)
    first_viewed_at = models.DateTimeField(null=True, blank=True)
    last_viewed_at = models.DateTimeField(null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    
    approved_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    
    client_feedback = models.TextField(
        blank=True,
        help_text="Client's comments/feedback on the package"
    )
    
    # Versioning
    revision_number = models.PositiveIntegerField(
        default=1,
        help_text="Track how many times this was revised"
    )
    
    # Featured Image (can override base package image)
    featured_image = models.ImageField(
        upload_to='packages/custom/',
        blank=True,
        null=True
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Custom Package"
        verbose_name_plural = "Custom Packages"
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['inquiry', 'status']),
            models.Index(fields=['access_token']),
        ]
    
    def save(self, *args, **kwargs):
        # Generate custom reference if not set
        if not self.custom_reference:
            from django.utils import timezone
            year = timezone.now().year
            # Get last custom package of the year
            last_custom = CustomPackage.objects.filter(
                custom_reference__startswith=f'CUSTOM-{year}'
            ).order_by('-custom_reference').first()
            
            if last_custom:
                last_num = int(last_custom.custom_reference.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            
            self.custom_reference = f'CUSTOM-{year}-{new_num:05d}'
        
        # Set expiry if sent and not set
        if self.status == 'sent' and not self.expires_at:
            from django.utils import timezone
            from datetime import timedelta
            self.expires_at = timezone.now() + timedelta(days=7)
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.custom_reference} - {self.name}"
    
    def get_absolute_url(self):
        return reverse('packages:custom_package_view', kwargs={
            'token': self.access_token
        })
    
    @property
    def price_difference(self):
        """Calculate price difference from original"""
        if self.original_price is not None and self.adjusted_price is not None:
            return self.original_price - self.adjusted_price
        return 0
    
    @property
    def discount_percentage(self):
        """Calculate discount percentage"""
        if self.original_price and self.adjusted_price and self.original_price > 0:
            return ((self.original_price - self.adjusted_price) / self.original_price) * 100
        return 0
    
    @property
    def is_expired(self):
        """Check if quote has expired"""
        if self.expires_at:
            from django.utils import timezone
            return timezone.now() > self.expires_at
        return False
    
    @property
    def days_until_expiry(self):
        """Days remaining until expiry"""
        if self.expires_at:
            from django.utils import timezone
            delta = self.expires_at - timezone.now()
            return max(0, delta.days)
        return None
    
    @property
    def total_price(self):
        """Total price for all travelers"""
        if self.adjusted_price is None:
            return 0
        from decimal import Decimal
        # Children typically 50% discount
        adult_price = self.adjusted_price * self.inquiry.number_of_adults
        child_price = (self.adjusted_price * Decimal('0.5')) * self.inquiry.number_of_children
        return adult_price + child_price
    
    def increment_view_count(self):
        """Track when client views the package"""
        from django.utils import timezone
        self.view_count += 1
        if not self.first_viewed_at:
            self.first_viewed_at = timezone.now()
            self.status = 'viewed'
        self.last_viewed_at = timezone.now()
        self.save(update_fields=['view_count', 'first_viewed_at', 'last_viewed_at', 'status'])


class InquiryMessage(TimeStampedModel):
    """
    Communication thread for booking inquiries.
    Tracks all messages between staff and clients.
    """
    inquiry = models.ForeignKey(
        BookingInquiry,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    
    # Sender Information
    sender_staff = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_inquiry_messages',
        help_text="Staff member who sent this (null = from client)"
    )
    
    sender_email = models.EmailField(
        blank=True,
        help_text="Email of sender (for client messages)"
    )
    
    sender_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Name of sender (for client messages)"
    )
    
    # Message Content
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    
    # Attachments
    attachment = models.FileField(
        upload_to='inquiries/attachments/',
        blank=True,
        null=True
    )
    
    # Message Type
    is_internal = models.BooleanField(
        default=False,
        help_text="Internal staff note (not visible to client)"
    )
    
    is_automated = models.BooleanField(
        default=False,
        help_text="Automated system message"
    )
    
    # Status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = "Inquiry Message"
        verbose_name_plural = "Inquiry Messages"
    
    def __str__(self):
        sender = self.sender_staff.get_full_name() if self.sender_staff else self.sender_name
        return f"{self.inquiry.inquiry_reference} - Message from {sender}"
    
    @property
    def is_from_client(self):
        """Check if message is from client"""
        return self.sender_staff is None
    
    @property
    def is_from_staff(self):
        """Check if message is from staff"""
        return self.sender_staff is not None


class CustomPackageItinerary(TimeStampedModel):
    """
    Custom day-by-day itinerary for a custom package.
    Similar to PackageItinerary but for customized packages.
    """
    custom_package = models.ForeignKey(
        CustomPackage,
        on_delete=models.CASCADE,
        related_name='itinerary_days'
    )
    day_number = models.PositiveIntegerField()
    end_day_number = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="For multi-day ranges (e.g., Days 3-7)"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Location details
    location = models.CharField(max_length=200, blank=True)
    
    # Accommodation
    accommodation_name = models.CharField(max_length=200, blank=True)
    accommodation_type = models.CharField(
        max_length=50,
        choices=[
            ('hotel', 'Hotel'),
            ('lodge', 'Lodge'),
            ('camp', 'Tented Camp'),
            ('resort', 'Resort'),
            ('guesthouse', 'Guest House'),
            ('other', 'Other'),
        ],
        blank=True
    )
    
    # Activities
    activities = models.TextField(
        blank=True,
        help_text="Activities for this day"
    )
    
    # Meals
    breakfast_included = models.BooleanField(default=True)
    lunch_included = models.BooleanField(default=True)
    dinner_included = models.BooleanField(default=True)
    
    # Transport
    transport_details = models.CharField(max_length=200, blank=True)
    
    # Distance/Duration
    distance = models.CharField(max_length=100, blank=True, help_text="e.g., 120km")
    drive_time = models.CharField(max_length=100, blank=True, help_text="e.g., 2-3 hours")
    
    # Media
    featured_image = models.ImageField(
        upload_to='custom_package_itinerary/',
        blank=True,
        null=True
    )
    
    # Display order
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'day_number']
        verbose_name = 'Custom Package Itinerary Day'
        verbose_name_plural = 'Custom Package Itinerary Days'
        unique_together = ['custom_package', 'day_number']
    
    def __str__(self):
        return f"{self.custom_package.custom_reference} - {self.day_display}"
    
    @property
    def day_display(self):
        """Display day number or range"""
        if self.end_day_number and self.end_day_number > self.day_number:
            return f"Days {self.day_number}-{self.end_day_number}"
        return f"Day {self.day_number}"
    
    @property
    def duration_days(self):
        """Calculate how many days this itinerary covers"""
        if self.end_day_number and self.end_day_number > self.day_number:
            return self.end_day_number - self.day_number + 1
        return 1

    @property
    def meals_display(self):
        """Human-readable meals included"""
        meals = []
        if self.breakfast_included:
            meals.append('Breakfast')
        if self.lunch_included:
            meals.append('Lunch')
        if self.dinner_included:
            meals.append('Dinner')
        return ', '.join(meals) if meals else 'No meals'


# ============================================================================
# DEPARTURE / AVAILABILITY CALENDAR
# ============================================================================

class Departure(TimeStampedModel):
    """
    A specific departure date for a package with seat capacity.
    Bookings attach to a Departure to lock seats.
    """
    STATUS_AVAILABLE = 'available'
    STATUS_SOLD_OUT = 'sold_out'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_AVAILABLE, 'Available'),
        (STATUS_SOLD_OUT, 'Sold Out'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, related_name='departures',
    )
    departure_date = models.DateField(db_index=True)
    max_seats = models.PositiveIntegerField(default=12)
    booked_seats = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_AVAILABLE, db_index=True,
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['departure_date']
        verbose_name = 'Departure'
        verbose_name_plural = 'Departures'
        unique_together = ['package', 'departure_date']

    def __str__(self):
        return f"{self.package.name} — {self.departure_date} ({self.seats_remaining} seats left)"

    @property
    def seats_remaining(self):
        return max(0, self.max_seats - self.booked_seats)

    @property
    def is_available(self):
        return self.status == self.STATUS_AVAILABLE and self.seats_remaining > 0

    def lock_seat(self):
        """Increment booked_seats and auto-set sold_out when full."""
        self.booked_seats += 1
        if self.booked_seats >= self.max_seats:
            self.status = self.STATUS_SOLD_OUT
        self.save(update_fields=['booked_seats', 'status'])

    def release_seat(self):
        """Decrement booked_seats (booking cancelled) and restore available if needed."""
        if self.booked_seats > 0:
            self.booked_seats -= 1
        if self.status == self.STATUS_SOLD_OUT and self.booked_seats < self.max_seats:
            self.status = self.STATUS_AVAILABLE
        self.save(update_fields=['booked_seats', 'status'])


# ============================================================================
# BOOKING SYSTEM
# ============================================================================

class Booking(TimeStampedModel):
    STATUS_CHOICES = [
        ('pending_deposit', 'Pending Deposit'),
        ('deposit_paid', 'Deposit Paid'),
        ('confirmed', 'Confirmed - Fully Paid'),
        ('in_progress', 'In Progress - Trip Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('TZS', 'Tanzanian Shilling'),
        ('KES', 'Kenyan Shilling'),
    ]
    booking_reference = models.CharField(max_length=50, unique=True, editable=False)
    inquiry = models.OneToOneField(
        BookingInquiry, on_delete=models.SET_NULL, null=True, blank=True, related_name='booking',
    )
    custom_package = models.ForeignKey(
        CustomPackage, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings',
    )
    package = models.ForeignKey(Package, on_delete=models.PROTECT, related_name='bookings')
    departure = models.ForeignKey(
        'Departure', on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings',
    )
    departure_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    num_adults = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    num_children = models.PositiveIntegerField(default=0)
    quoted_price = models.DecimalField(max_digits=12, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending_deposit', db_index=True
    )
    special_requirements = models.TextField(blank=True)
    staff_assigned = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_bookings',
    )
    internal_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['departure_date']),
        ]

    def __str__(self):
        return f"{self.booking_reference} - {self.package.name}"

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            from django.utils import timezone
            date_str = timezone.now().strftime('%Y%m%d')
            last = Booking.objects.filter(
                booking_reference__startswith=f'BKG-{date_str}'
            ).order_by('-booking_reference').first()
            seq = int(last.booking_reference.split('-')[-1]) + 1 if last else 1
            self.booking_reference = f'BKG-{date_str}-{seq:05d}'

        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Lock a seat on the departure when a booking is first created
        if is_new and self.departure_id:
            self.departure.lock_seat()

    @property
    def total_travelers(self):
        return self.num_adults + self.num_children

    @property
    def total_paid(self):
        return sum(p.amount for p in self.payments.filter(status='confirmed'))

    @property
    def balance_due(self):
        return self.quoted_price - self.total_paid

    @property
    def is_fully_paid(self):
        return self.total_paid >= self.quoted_price

    @property
    def status_badge_color(self):
        return {
            'pending_deposit': 'warning', 'deposit_paid': 'info',
            'confirmed': 'success', 'in_progress': 'primary',
            'completed': 'success', 'cancelled': 'secondary', 'refunded': 'danger',
        }.get(self.status, 'secondary')

    def cancel(self):
        """Cancel booking and release the departure seat."""
        if self.status != 'cancelled':
            self.status = 'cancelled'
            self.save(update_fields=['status'])
            if self.departure_id:
                self.departure.release_seat()


class Passenger(TimeStampedModel):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='passengers')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=50, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    dietary_requirements = models.CharField(max_length=200, blank=True)
    medical_notes = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=50, blank=True)
    is_lead_passenger = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_lead_passenger', 'last_name', 'first_name']
        verbose_name = 'Passenger'
        verbose_name_plural = 'Passengers'

    def __str__(self):
        lead = ' (Lead)' if self.is_lead_passenger else ''
        return f"{self.first_name} {self.last_name}{lead}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Payment(TimeStampedModel):
    PAYMENT_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('balance', 'Balance Payment'),
        ('full', 'Full Payment'),
        ('extra', 'Extra Charge'),
        ('refund', 'Refund'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('mpesa', 'M-Pesa'),
        ('card', 'Credit / Debit Card'),
        ('stripe', 'Stripe (Online)'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed / Received'),
        ('refunded', 'Refunded'),
        ('failed', 'Failed'),
    ]
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, default='deposit')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, default='bank_transfer'
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='confirmed', db_index=True
    )
    reference_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    received_at = models.DateTimeField(null=True, blank=True)
    recorded_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='recorded_payments',
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return (
            f"{self.booking.booking_reference} - "
            f"{self.get_payment_type_display()} {self.currency} {self.amount}"
        )

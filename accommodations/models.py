from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from destinations.models import Destination

User = get_user_model()


class Accommodation(models.Model):
    """
    Model representing accommodations (hotels, lodges, camps, etc.)
    """
    
    # Type Choices
    TYPE_CHOICES = [
        ('hotel', 'Hotel'),
        ('lodge', 'Lodge'),
        ('camp', 'Camp / Tented Camp'),
        ('resort', 'Resort'),
        ('guesthouse', 'Guesthouse'),
        ('hostel', 'Hostel'),
        ('villa', 'Villa'),
        ('apartment', 'Apartment'),
        ('boutique', 'Boutique Hotel'),
        ('other', 'Other'),
    ]
    
    # Star Rating Choices
    STAR_RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    # Basic Information
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Accommodation name"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        help_text="Auto-generated URL slug"
    )
    description = models.TextField(
        help_text="Detailed description of the accommodation"
    )
    short_description = models.CharField(
        max_length=500,
        blank=True,
        help_text="Brief overview for cards/previews"
    )
    
    # Relationship
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name='accommodations',
        help_text="Destination where this accommodation is located"
    )
    
    # Classification
    accommodation_type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        default='hotel',
        db_index=True,
        help_text="Type of accommodation"
    )
    star_rating = models.IntegerField(
        choices=STAR_RATING_CHOICES,
        null=True,
        blank=True,
        help_text="Star rating (1-5 stars)"
    )
    
    # Location Details
    address = models.TextField(
        blank=True,
        help_text="Full address"
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
        help_text="Geographic latitude (-90 to 90)"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)],
        help_text="Geographic longitude (-180 to 180)"
    )
    
    # Contact Information
    phone = models.CharField(
        max_length=50,
        blank=True,
        help_text="Contact phone number"
    )
    email = models.EmailField(
        blank=True,
        help_text="Contact email"
    )
    website = models.URLField(
        blank=True,
        help_text="Official website URL"
    )
    
    # Amenities (stored as comma-separated values)
    amenities = models.TextField(
        blank=True,
        help_text="Comma-separated amenities (e.g., 'WiFi,Pool,Restaurant,Bar')"
    )
    
    # Pricing (approximate ranges)
    price_per_night_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Minimum price per night"
    )
    price_per_night_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Maximum price per night"
    )
    currency = models.CharField(
        max_length=3,
        default='USD',
        help_text="Currency code (default: USD)"
    )
    
    # Media
    featured_image = models.ImageField(
        upload_to='accommodations/featured/',
        blank=True,
        null=True,
        help_text="Main accommodation image"
    )
    video_url = models.URLField(
        blank=True,
        null=True,
        help_text="YouTube/Vimeo video URL (optional)"
    )
    
    # Additional Details
    total_rooms = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Total number of rooms"
    )
    check_in_time = models.CharField(
        max_length=50,
        blank=True,
        help_text="Check-in time (e.g., '2:00 PM')"
    )
    check_out_time = models.CharField(
        max_length=50,
        blank=True,
        help_text="Check-out time (e.g., '11:00 AM')"
    )
    policies = models.TextField(
        blank=True,
        help_text="Cancellation policies, rules, etc."
    )
    
    # Status & Visibility
    is_featured = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Display as featured accommodation"
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Published and visible to public"
    )
    view_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of times viewed"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    
    # SEO Fields
    meta_title = models.CharField(
        max_length=200,
        blank=True,
        help_text="SEO page title (optional, defaults to name)"
    )
    meta_description = models.TextField(
        blank=True,
        help_text="SEO meta description"
    )
    meta_keywords = models.CharField(
        max_length=500,
        blank=True,
        help_text="SEO keywords, comma-separated"
    )
    
    # Timestamps & Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accommodations_created'
    )
    
    class Meta:
        ordering = ['order', '-is_featured', 'name']
        verbose_name = 'Accommodation'
        verbose_name_plural = 'Accommodations'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['accommodation_type', 'star_rating']),
            models.Index(fields=['destination', 'is_active']),
            models.Index(fields=['is_featured', 'is_active']),
            models.Index(fields=['order']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.destination.name}"
    
    def save(self, *args, **kwargs):
        """Auto-generate slug and meta fields"""
        if not self.slug:
            self.slug = slugify(self.name)
        
        if not self.meta_title:
            self.meta_title = self.name
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """Return the URL for this accommodation"""
        return reverse('public_accommodation_detail', kwargs={'slug': self.slug})
    
    def increment_view_count(self):
        """Increment the view counter"""
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    @property
    def coordinates(self):
        """Return coordinates as tuple"""
        if self.latitude and self.longitude:
            return (float(self.latitude), float(self.longitude))
        return None
    
    @property
    def price_range_display(self):
        """Return formatted price range string"""
        if self.price_per_night_min and self.price_per_night_max:
            return f"{self.currency} {self.price_per_night_min:,.0f} - {self.price_per_night_max:,.0f}"
        elif self.price_per_night_min:
            return f"From {self.currency} {self.price_per_night_min:,.0f}"
        return "Contact for pricing"
    
    def get_amenities_list(self):
        """Return amenities as a list"""
        if self.amenities:
            return [amenity.strip() for amenity in self.amenities.split(',')]
        return []
    
    def get_type_display_name(self):
        """Return human-readable accommodation type"""
        return dict(self.TYPE_CHOICES).get(self.accommodation_type, self.accommodation_type)


class AccommodationImage(models.Model):
    """
    Gallery images for accommodations
    """
    accommodation = models.ForeignKey(
        Accommodation,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )
    image = models.ImageField(
        upload_to='accommodations/gallery/',
        help_text="Gallery image"
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        help_text="Image caption (optional)"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'uploaded_at']
        verbose_name = 'Accommodation Image'
        verbose_name_plural = 'Accommodation Images'
    
    def __str__(self):
        return f"{self.accommodation.name} - Image {self.order}"


class Room(models.Model):
    """
    Room types available at accommodations
    """
    
    # Room Type Choices
    ROOM_TYPE_CHOICES = [
        ('single', 'Single Room'),
        ('double', 'Double Room'),
        ('twin', 'Twin Room'),
        ('triple', 'Triple Room'),
        ('suite', 'Suite'),
        ('family', 'Family Room'),
        ('deluxe', 'Deluxe Room'),
        ('executive', 'Executive Room'),
        ('presidential', 'Presidential Suite'),
    ]
    
    # Bed Type Choices
    BED_TYPE_CHOICES = [
        ('single', 'Single Bed'),
        ('double', 'Double Bed'),
        ('queen', 'Queen Bed'),
        ('king', 'King Bed'),
        ('twin', 'Twin Beds'),
        ('bunk', 'Bunk Beds'),
    ]
    
    accommodation = models.ForeignKey(
        Accommodation,
        on_delete=models.CASCADE,
        related_name='rooms'
    )
    name = models.CharField(
        max_length=200,
        help_text="Room name/type"
    )
    room_type = models.CharField(
        max_length=50,
        choices=ROOM_TYPE_CHOICES,
        default='double',
        help_text="Type of room"
    )
    description = models.TextField(
        blank=True,
        help_text="Room description"
    )
    
    # Capacity
    max_occupancy = models.PositiveIntegerField(
        default=2,
        help_text="Maximum number of guests"
    )
    bed_type = models.CharField(
        max_length=50,
        choices=BED_TYPE_CHOICES,
        default='double',
        help_text="Type of bed(s)"
    )
    number_of_beds = models.PositiveIntegerField(
        default=1,
        help_text="Number of beds"
    )
    
    # Size
    size_sqm = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Room size in square meters"
    )
    
    # Pricing
    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price per night"
    )
    
    # Amenities
    amenities = models.TextField(
        blank=True,
        help_text="Room-specific amenities (comma-separated)"
    )
    
    # Availability
    is_available = models.BooleanField(
        default=True,
        help_text="Currently available for booking"
    )
    
    # Media
    image = models.ImageField(
        upload_to='accommodations/rooms/',
        blank=True,
        null=True,
        help_text="Room image"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['accommodation', 'price_per_night']
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
    
    def __str__(self):
        return f"{self.accommodation.name} - {self.name}"
    
    @property
    def price_display(self):
        """Return formatted price string"""
        return f"{self.accommodation.currency} {self.price_per_night:,.2f}"
    
    def get_amenities_list(self):
        """Return amenities as a list"""
        if self.amenities:
            return [amenity.strip() for amenity in self.amenities.split(',')]
        return []

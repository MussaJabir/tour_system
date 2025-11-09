from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


class Destination(models.Model):
    """
    Destination model for safari/tour locations
    """
    # Basic Information
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Name of the destination"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        help_text="URL-friendly version of name (auto-generated)"
    )
    description = models.TextField(
        help_text="Full description of the destination"
    )
    short_description = models.CharField(
        max_length=500,
        help_text="Brief description for cards and previews"
    )
    
    # Location & Geography
    country = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Country where destination is located"
    )
    region = models.CharField(
        max_length=100,
        blank=True,
        help_text="Region or state (e.g., Northern Tanzania)"
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        help_text="Latitude coordinate (-90 to 90)"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        help_text="Longitude coordinate (-180 to 180)"
    )
    
    # Media
    featured_image = models.ImageField(
        upload_to='destinations/featured/',
        help_text="Main image for the destination"
    )
    video_url = models.URLField(
        blank=True,
        help_text="YouTube or Vimeo video URL (optional)"
    )
    
    # Details
    best_time_to_visit = models.CharField(
        max_length=100,
        blank=True,
        help_text="Best months to visit (e.g., 'June - October')"
    )
    climate = models.TextField(
        blank=True,
        help_text="Climate information and weather patterns"
    )
    wildlife = models.TextField(
        blank=True,
        help_text="Wildlife commonly seen in this destination"
    )
    
    # Status & Visibility
    is_featured = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Display on homepage as featured destination"
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Published and visible to public"
    )
    view_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of times this destination was viewed"
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
        related_name='destinations_created'
    )
    
    class Meta:
        ordering = ['order', '-is_featured', 'name']
        verbose_name = 'Destination'
        verbose_name_plural = 'Destinations'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['country']),
            models.Index(fields=['is_featured', 'is_active']),
            models.Index(fields=['order']),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided"""
        if not self.slug:
            self.slug = slugify(self.name)
        
        # Use name for meta_title if not provided
        if not self.meta_title:
            self.meta_title = self.name
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """Return the URL for this destination"""
        return reverse('public_destination_detail', kwargs={'slug': self.slug})
    
    def increment_view_count(self):
        """Increment the view counter"""
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    @property
    def coordinates(self):
        """Return coordinates as tuple"""
        return (float(self.latitude), float(self.longitude))


class DestinationImage(models.Model):
    """
    Gallery images for destinations
    """
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )
    image = models.ImageField(
        upload_to='destinations/gallery/',
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
        verbose_name = 'Destination Image'
        verbose_name_plural = 'Destination Images'
    
    def __str__(self):
        return f"{self.destination.name} - Image {self.order}"

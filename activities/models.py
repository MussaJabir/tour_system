from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from destinations.models import Destination

User = get_user_model()


class Activity(models.Model):
    """
    Model representing activities available at destinations
    Examples: Safari drives, hiking, cultural tours, water sports, etc.
    """
    
    # Category Choices
    CATEGORY_CHOICES = [
        ('safari', 'Safari & Wildlife'),
        ('hiking', 'Hiking & Trekking'),
        ('water_sports', 'Water Sports'),
        ('cultural', 'Cultural Tours'),
        ('adventure', 'Adventure Activities'),
        ('wildlife', 'Wildlife Viewing'),
        ('relaxation', 'Relaxation & Wellness'),
        ('photography', 'Photography Tours'),
        ('bird_watching', 'Bird Watching'),
        ('camping', 'Camping'),
        ('other', 'Other'),
    ]
    
    # Difficulty Choices
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('challenging', 'Challenging'),
        ('extreme', 'Extreme'),
    ]
    
    # Duration Unit Choices
    DURATION_UNIT_CHOICES = [
        ('hours', 'Hours'),
        ('days', 'Days'),
    ]
    
    # Basic Information
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Activity name (e.g., 'Morning Game Drive')"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        help_text="Auto-generated URL slug"
    )
    description = models.TextField(
        help_text="Detailed description of the activity"
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
        related_name='activities',
        help_text="Destination where this activity is available"
    )
    
    # Classification
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='other',
        db_index=True,
        help_text="Activity category"
    )
    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='moderate',
        db_index=True,
        help_text="Difficulty level"
    )
    
    # Logistics
    duration = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        validators=[MinValueValidator(0.5)],
        help_text="Duration (e.g., 2.5)"
    )
    duration_unit = models.CharField(
        max_length=10,
        choices=DURATION_UNIT_CHOICES,
        default='hours',
        help_text="Duration unit (hours or days)"
    )
    min_age = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Minimum age requirement (optional)"
    )
    max_group_size = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Maximum group size (optional)"
    )
    
    # Pricing
    price_per_person = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Price per person in USD"
    )
    currency = models.CharField(
        max_length=3,
        default='USD',
        help_text="Currency code (default: USD)"
    )
    
    # Media
    featured_image = models.ImageField(
        upload_to='activities/featured/',
        blank=True,
        null=True,
        help_text="Main activity image"
    )
    video_url = models.URLField(
        blank=True,
        null=True,
        help_text="YouTube/Vimeo video URL (optional)"
    )
    
    # Requirements & Details
    requirements = models.TextField(
        blank=True,
        help_text="What participants need (e.g., fitness level, equipment)"
    )
    included_items = models.TextField(
        blank=True,
        help_text="What's included in the activity"
    )
    excluded_items = models.TextField(
        blank=True,
        help_text="What's NOT included"
    )
    best_season = models.CharField(
        max_length=255,
        blank=True,
        help_text="Best time of year for this activity (optional)"
    )
    
    # Status & Visibility
    is_featured = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Display as featured activity"
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
        related_name='activities_created'
    )
    
    class Meta:
        ordering = ['order', '-is_featured', 'name']
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category', 'difficulty']),
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
        return reverse('public_activity_detail', kwargs={'slug': self.slug})

    def get_meta_title(self):
        return self.meta_title or self.name

    def get_meta_description(self):
        if self.meta_description:
            return self.meta_description
        if self.short_description:
            return self.short_description[:160]
        return self.description[:160] + '...' if self.description else ''

    def increment_view_count(self):
        """Increment the view counter"""
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    @property
    def duration_display(self):
        """Return formatted duration string"""
        if self.duration_unit == 'days':
            return f"{self.duration} day(s)"
        return f"{self.duration} hour(s)"
    
    @property
    def price_display(self):
        """Return formatted price string"""
        return f"{self.currency} {self.price_per_person:,.2f}"
    
    def get_category_display_name(self):
        """Return human-readable category name"""
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)
    
    def get_difficulty_display_name(self):
        """Return human-readable difficulty name"""
        return dict(self.DIFFICULTY_CHOICES).get(self.difficulty, self.difficulty)


class ActivityImage(models.Model):
    """
    Gallery images for activities
    """
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )
    image = models.ImageField(
        upload_to='activities/gallery/',
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
        verbose_name = 'Activity Image'
        verbose_name_plural = 'Activity Images'
    
    def __str__(self):
        return f"{self.activity.name} - Image {self.order}"

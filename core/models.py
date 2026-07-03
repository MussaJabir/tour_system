"""
Core Abstract Base Models
These models provide common functionality that other apps inherit from.
Following DRY (Don't Repeat Yourself) principle for maintainability.
"""
from django.db import models
from django.core.cache import cache
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


class TimeStampedModel(models.Model):
    """
    Abstract base model that provides self-updating
    'created_at' and 'updated_at' fields.
    
    All models that need timestamp tracking should inherit from this.
    
    Usage:
        class MyModel(TimeStampedModel):
            name = models.CharField(max_length=100)
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Automatically set when object is first created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Automatically updated whenever object is saved"
    )
    
    class Meta:
        abstract = True
        ordering = ['-created_at']  # Newest first by default


class SEOMixin(models.Model):
    """
    Abstract mixin for SEO-related fields.
    Helps with search engine optimization.
    
    CRITICAL FOR YOUR BUSINESS: Better SEO = More Organic Traffic = More Customers!
    
    Usage:
        class MyModel(SEOMixin, models.Model):
            name = models.CharField(max_length=100)
    """
    meta_title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="SEO Title",
        help_text="SEO-optimized title for search engines (max 60 chars recommended)"
    )
    meta_description = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="SEO Description",
        help_text="SEO meta description for search engines (max 160 chars recommended)"
    )
    meta_keywords = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="SEO Keywords",
        help_text="Comma-separated keywords for SEO (e.g., 'safari, tanzania, wildlife')"
    )
    
    class Meta:
        abstract = True
    
    def get_meta_title(self):
        """Return meta_title if set, otherwise fall back to object's name"""
        if self.meta_title:
            return self.meta_title
        return getattr(self, 'name', str(self))
    
    def get_meta_description(self):
        """Return meta_description if set, otherwise fall back to truncated description"""
        if self.meta_description:
            return self.meta_description
        if hasattr(self, 'short_description') and self.short_description:
            return self.short_description[:160]
        if hasattr(self, 'description') and self.description:
            return self.description[:160] + '...'
        return ''


class PublishableMixin(models.Model):
    """
    Abstract mixin for content publishing control.
    
    Provides:
    - is_active: Draft vs Published
    - is_featured: Highlight important content
    - order: Custom ordering
    - created_by: Track who created it
    
    BUSINESS VALUE: Control what customers see without deleting data!
    
    Usage:
        class MyModel(PublishableMixin, models.Model):
            name = models.CharField(max_length=100)
    """
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="Active/Published",
        help_text="Is this content visible to public? Uncheck to make draft."
    )
    is_featured = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="Featured",
        help_text="Featured items appear on homepage and special sections"
    )
    order = models.IntegerField(
        default=0,
        db_index=True,
        verbose_name="Display Order",
        help_text="Lower numbers appear first (0 = highest priority)"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name="%(app_label)s_%(class)s_created",
        help_text="User who created this entry"
    )
    
    class Meta:
        abstract = True
        ordering = ['order', '-is_featured', '-created_at']
    
    @classmethod
    def get_active(cls):
        """Get all active/published objects"""
        return cls.objects.filter(is_active=True)
    
    @classmethod
    def get_featured(cls):
        """Get all featured and active objects"""
        return cls.objects.filter(is_active=True, is_featured=True)


class SlugMixin(models.Model):
    """
    Abstract mixin for slug field with auto-generation.
    
    Slugs are URL-friendly versions of names (e.g., "Serengeti Safari" → "serengeti-safari")
    
    SEO BENEFIT: Clean URLs rank better in search engines!
    
    Usage:
        class MyModel(SlugMixin, models.Model):
            name = models.CharField(max_length=100)
            # slug is automatically created from 'name' field
    """
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        db_index=True,
        help_text="URL-friendly version of name (auto-generated if left blank)"
    )
    
    class Meta:
        abstract = True
    
    def generate_unique_slug(self, source_field='name'):
        """
        Generate a unique slug from the source field.
        If slug already exists, append a number.
        """
        if not hasattr(self, source_field):
            raise ValueError(f"Model must have a '{source_field}' field to generate slug")
        
        base_slug = slugify(getattr(self, source_field))
        slug = base_slug
        counter = 1
        
        # Check if slug already exists (excluding current instance if updating)
        while self.__class__.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        return slug
    
    def save(self, *args, **kwargs):
        """Auto-generate slug if not provided"""
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)


class ViewCountMixin(models.Model):
    """
    Abstract mixin for tracking view counts.
    
    BUSINESS INTELLIGENCE: Know what's popular to optimize your offerings!
    
    Usage:
        class MyModel(ViewCountMixin, models.Model):
            name = models.CharField(max_length=100)
    """
    view_count = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name="View Count",
        help_text="Number of times this item has been viewed"
    )
    
    class Meta:
        abstract = True
    
    def increment_view_count(self):
        """
        Increment the view counter by 1.
        Use update() to avoid triggering save signals.
        """
        self.__class__.objects.filter(pk=self.pk).update(
            view_count=models.F('view_count') + 1
        )
        self.refresh_from_db(fields=['view_count'])


# Combined Base Model (Most Commonly Used)
class BaseModel(TimeStampedModel, SEOMixin, PublishableMixin, SlugMixin, ViewCountMixin):
    """
    Combined base model with all common functionality.
    
    Use this as the base for most content models (destinations, activities, etc.)
    
    Provides:
    - Timestamps (created_at, updated_at)
    - SEO fields (meta_title, meta_description, meta_keywords)
    - Publishing control (is_active, is_featured, order)
    - Slug generation
    - View counting
    
    Usage:
        class MyModel(BaseModel):
            name = models.CharField(max_length=100)
            description = models.TextField()
    """
    class Meta:
        abstract = True
        ordering = ['order', '-is_featured', '-created_at']


# Simple models for core functionality
class ContactMessage(TimeStampedModel):
    """
    Model for storing contact form submissions.
    
    CRITICAL FOR LEAD GENERATION: Every submission is a potential customer!
    """
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    ]
    
    name = models.CharField(
        max_length=200,
        verbose_name="Full Name"
    )
    email = models.EmailField(
        verbose_name="Email Address"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Phone Number"
    )
    subject = models.CharField(
        max_length=200,
        blank=True,
        default="General Inquiry"
    )
    message = models.TextField(
        verbose_name="Message"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        db_index=True
    )
    admin_notes = models.TextField(
        blank=True,
        verbose_name="Internal Notes",
        help_text="Private notes for staff (not visible to customer)"
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        editable=False,
        help_text="IP address of submitter (for spam prevention)"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.subject} ({self.get_status_display()})"
    
    def mark_as_read(self):
        """Mark this message as read"""
        if self.status == 'new':
            self.status = 'read'
            self.save(update_fields=['status'])
    
    def mark_as_replied(self):
        """Mark this message as replied"""
        self.status = 'replied'
        self.save(update_fields=['status'])


class NewsletterSubscriber(TimeStampedModel):
    """
    Model for newsletter subscribers.
    
    MARKETING GOLD: Build your email list to promote tours and drive sales!
    """
    email = models.EmailField(
        unique=True,
        verbose_name="Email Address"
    )
    name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Name"
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="Active Subscription",
        help_text="Is this subscriber still active?"
    )
    unsubscribed_at = models.DateTimeField(
        null=True,
        blank=True,
        editable=False
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        editable=False
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['is_active', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.email} ({self.name or 'No name'})"
    
    def unsubscribe(self):
        """Unsubscribe this user"""
        from django.utils import timezone
        self.is_active = False
        self.unsubscribed_at = timezone.now()
        self.save(update_fields=['is_active', 'unsubscribed_at'])


class FAQ(TimeStampedModel, PublishableMixin):
    """
    Frequently Asked Questions.
    
    REDUCE SUPPORT LOAD: Answer common questions once, refer customers here!
    """
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('booking', 'Booking & Reservations'),
        ('payment', 'Payment & Pricing'),
        ('destinations', 'Destinations'),
        ('travel', 'Travel Information'),
        ('safety', 'Safety & Health'),
        ('cancellation', 'Cancellation & Refunds'),
    ]
    
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='general',
        db_index=True
    )
    question = models.CharField(
        max_length=500,
        verbose_name="Question"
    )
    answer = models.TextField(
        verbose_name="Answer"
    )
    
    class Meta:
        ordering = ['category', 'order', 'question']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        indexes = [
            models.Index(fields=['category', 'is_active']),
        ]
    
    def __str__(self):
        return f"[{self.get_category_display()}] {self.question[:50]}"


class Testimonial(TimeStampedModel, PublishableMixin):
    """
    Customer testimonials (simple quotes).
    
    SOCIAL PROOF: Build trust with potential customers!
    Note: This is different from the 'reviews' app which has detailed ratings.
    """
    customer_name = models.CharField(
        max_length=200,
        verbose_name="Customer Name"
    )
    customer_location = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Location",
        help_text="e.g., 'New York, USA'"
    )
    customer_image = models.ImageField(
        upload_to='testimonials/',
        blank=True,
        null=True,
        verbose_name="Customer Photo"
    )
    quote = models.TextField(
        max_length=500,
        verbose_name="Testimonial Quote",
        help_text="Keep it short and powerful (max 500 chars)"
    )
    rating = models.IntegerField(
        default=5,
        choices=[(i, f"{i} Star{'s' if i != 1 else ''}") for i in range(1, 6)],
        verbose_name="Rating"
    )
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
    
    def __str__(self):
        return f"{self.customer_name} - {self.rating}⭐"


class SiteSettings(TimeStampedModel):
    """
    Singleton for operator-editable site configuration (Dashboard → Settings).

    Values set here take priority over the corresponding environment
    variables, so each deployment can be reconfigured from the dashboard
    without shell access. Always read through SiteSettings.load(), which
    caches the row and enforces the single pk=1 instance.
    """
    CACHE_KEY = 'core:site_settings'

    whatsapp_number = models.CharField(
        max_length=50,
        blank=True,
        help_text=(
            "Business WhatsApp number in international format, e.g. +255744000000. "
            "Leave empty to fall back to the WHATSAPP_BUSINESS_NUMBER environment variable."
        ),
    )

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site settings"

    def save(self, *args, **kwargs):
        self.pk = 1  # enforce singleton
        if self.created_at is None:
            # A fresh instance saved over the existing row takes Django's
            # UPDATE path, where auto_now_add doesn't fire — preserve the
            # original creation timestamp instead of writing NULL.
            self.created_at = (
                SiteSettings.objects
                .filter(pk=1)
                .values_list('created_at', flat=True)
                .first()
            )
        super().save(*args, **kwargs)
        cache.delete(self.CACHE_KEY)

    @classmethod
    def load(cls):
        obj = cache.get(cls.CACHE_KEY)
        if obj is None:
            obj, _ = cls.objects.get_or_create(pk=1)
            cache.set(cls.CACHE_KEY, obj)
        return obj

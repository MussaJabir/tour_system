from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone
from .fields import EncryptedCharField

from core.models import TimeStampedModel


class AIConfiguration(models.Model):
    VENDOR_OPENAI = 'openai'
    VENDOR_ANTHROPIC = 'anthropic'
    VENDOR_CHOICES = [
        (VENDOR_OPENAI, 'OpenAI'),
        (VENDOR_ANTHROPIC, 'Anthropic'),
    ]

    vendor = models.CharField(max_length=20, choices=VENDOR_CHOICES, default=VENDOR_OPENAI)
    api_key = EncryptedCharField()
    model_name = models.CharField(max_length=100, default='gpt-4o')
    max_tokens = models.PositiveIntegerField(default=2000)
    temperature = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal('0.70'))
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'AI Configuration'
        verbose_name_plural = 'AI Configuration'

    def __str__(self):
        return f"{self.get_vendor_display()} — {self.model_name}"

    def save(self, *args, **kwargs):
        self.pk = 1
        kwargs.pop('force_insert', None)  # allow upsert when called via .create()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # prevent deletion via admin

    @classmethod
    def get_active(cls):
        try:
            return cls.objects.get(pk=1, is_active=True)
        except cls.DoesNotExist:
            return None


class BaseAIJob(TimeStampedModel):
    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_DONE = 'done'
    STATUS_FAILED = 'failed'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PROCESSING, 'Processing'),
        (STATUS_DONE, 'Done'),
        (STATUS_FAILED, 'Failed'),
    ]

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING, db_index=True
    )
    error_message = models.TextField(blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
    )

    class Meta:
        abstract = True

    def mark_processing(self):
        self.status = self.STATUS_PROCESSING
        self.started_at = timezone.now()
        self.save(update_fields=['status', 'started_at'])

    def mark_done(self):
        self.status = self.STATUS_DONE
        self.completed_at = timezone.now()
        self.save(update_fields=['status', 'completed_at'])

    def mark_failed(self, error: str):
        self.status = self.STATUS_FAILED
        self.error_message = error
        self.completed_at = timezone.now()
        self.save(update_fields=['status', 'error_message', 'completed_at'])

    @property
    def is_running(self):
        return self.status in (self.STATUS_PENDING, self.STATUS_PROCESSING)


class BrochureParseJob(BaseAIJob):
    pdf_file = models.FileField(upload_to='ai_jobs/brochures/')
    target_accommodation = models.ForeignKey(
        'accommodations.Accommodation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='parse_jobs',
    )
    extracted_data = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = 'Brochure Parse Job'
        verbose_name_plural = 'Brochure Parse Jobs'
        ordering = ['-created_at']

    def __str__(self):
        return f"BrochureJob #{self.pk} — {self.status}"


class ItineraryGenerationJob(BaseAIJob):
    destination = models.ForeignKey(
        'destinations.Destination',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='itinerary_jobs',
    )
    duration_days = models.PositiveSmallIntegerField(default=7)
    budget_usd = models.PositiveIntegerField(default=3000)
    group_size = models.PositiveSmallIntegerField(default=2)
    interests = models.CharField(max_length=300, blank=True)
    raw_output = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Itinerary Generation Job'
        verbose_name_plural = 'Itinerary Generation Jobs'
        ordering = ['-created_at']

    def __str__(self):
        return f"ItineraryJob #{self.pk} — {self.status}"


class QuoteSuggestionJob(BaseAIJob):
    inquiry = models.ForeignKey(
        'packages.BookingInquiry',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='quote_jobs',
    )
    suggestions = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = 'Quote Suggestion Job'
        verbose_name_plural = 'Quote Suggestion Jobs'
        ordering = ['-created_at']

    def __str__(self):
        return f"QuoteJob #{self.pk} — {self.status}"


class RouteOptimizationJob(BaseAIJob):
    destination_names = models.TextField(
        help_text='Comma-separated list of destinations/parks to optimize'
    )
    optimized_route = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = 'Route Optimization Job'
        verbose_name_plural = 'Route Optimization Jobs'
        ordering = ['-created_at']

    def __str__(self):
        return f"RouteJob #{self.pk} — {self.status}"

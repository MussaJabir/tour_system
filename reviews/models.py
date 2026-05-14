from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from core.models import TimeStampedModel


class Review(TimeStampedModel):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    STATUS_CHOICES = [
        ('pending', 'Pending Moderation'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    package = models.ForeignKey(
        'packages.Package',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews',
    )
    booking = models.OneToOneField(
        'packages.Booking',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='review',
    )

    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    title = models.CharField(max_length=200)
    body = models.TextField()
    reviewer_name = models.CharField(max_length=100, blank=True)
    reviewer_country = models.CharField(max_length=100, blank=True)

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True
    )
    is_approved = models.BooleanField(default=False, db_index=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_reviews',
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)

    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        indexes = [
            models.Index(fields=['package', 'is_approved', '-created_at']),
            models.Index(fields=['status', '-created_at']),
        ]

    def __str__(self):
        return f"{self.reviewer_name or 'Anonymous'} — {self.package.name} ({self.rating}★)"

    def approve(self, staff_user):
        self.status = 'approved'
        self.is_approved = True
        self.approved_by = staff_user
        self.approved_at = timezone.now()
        self.save(update_fields=['status', 'is_approved', 'approved_by', 'approved_at'])
        self.package.update_rating()

    def reject(self, reason=''):
        self.status = 'rejected'
        self.is_approved = False
        self.rejection_reason = reason
        self.save(update_fields=['status', 'is_approved', 'rejection_reason'])
        self.package.update_rating()

    @property
    def star_range(self):
        return range(1, 6)


class ReviewPhoto(TimeStampedModel):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='reviews/photos/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Review Photo'
        verbose_name_plural = 'Review Photos'

    def __str__(self):
        return f"Photo for {self.review}"

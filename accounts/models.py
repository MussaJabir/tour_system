from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('TZS', 'Tanzanian Shilling'),
        ('KES', 'Kenyan Shilling'),
    ]

    phone = models.CharField(max_length=50, blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    preferred_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    nationality = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.get_full_name() or self.username

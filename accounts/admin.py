from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = [
        'username', 'email', 'first_name', 'last_name',
        'phone', 'nationality', 'preferred_currency',
        'is_staff', 'is_active', 'date_joined',
    ]
    list_filter = ['is_staff', 'is_active', 'preferred_currency', 'nationality']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    ordering = ['-date_joined']

    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {
            'fields': ('phone', 'profile_photo', 'preferred_currency', 'nationality'),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Profile', {
            'fields': ('phone', 'preferred_currency', 'nationality'),
        }),
    )

from django.urls import path
from . import api_views

urlpatterns = [
    path('auth/register/', api_views.api_register, name='api_register'),
    path('auth/login/', api_views.api_login, name='api_login'),
    path('auth/logout/', api_views.api_logout, name='api_logout'),
    path('auth/profile/', api_views.api_profile, name='api_profile'),
    path('auth/change-password/', api_views.api_change_password, name='api_change_password'),
]

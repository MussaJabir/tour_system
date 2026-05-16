"""
Core App - URL Configuration
"""
from django.urls import path
from . import views

urlpatterns = [
    # ==================== AUTH URLS ====================
    path('dashboard/login/', views.staff_login, name='staff_login'),
    path('dashboard/logout/', views.staff_logout, name='staff_logout'),

    # ==================== PUBLIC URLS ====================
    # Contact
    path('contact/', views.contact_page, name='contact_page'),
    
    # Newsletter
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('newsletter/unsubscribe/<str:token>/', views.newsletter_unsubscribe, name='newsletter_unsubscribe'),
    
    # FAQ
    path('faq/', views.faq_page, name='faq_page'),

    # Styleguide (DEBUG only)
    path('styleguide/', views.styleguide, name='styleguide'),
    
    # ==================== DASHBOARD URLS ====================
    # Dashboard Home
    path('dashboard/', views.dashboard_home, name='dashboard_home'),
    
    # Contact Messages Dashboard
    path('dashboard/contacts/', views.dashboard_contact_list, name='dashboard_contact_list'),
    path('dashboard/contacts/<int:pk>/', views.dashboard_contact_detail, name='dashboard_contact_detail'),
    path('dashboard/contacts/<int:pk>/delete/', views.dashboard_contact_delete, name='dashboard_contact_delete'),
    
    # Newsletter Dashboard
    path('dashboard/newsletter/', views.dashboard_newsletter_list, name='dashboard_newsletter_list'),
    path('dashboard/newsletter/export/', views.dashboard_newsletter_export, name='dashboard_newsletter_export'),
    
    # FAQ Dashboard
    path('dashboard/faqs/', views.dashboard_faq_list, name='dashboard_faq_list'),
    path('dashboard/faqs/create/', views.dashboard_faq_create, name='dashboard_faq_create'),
    path('dashboard/faqs/<int:pk>/edit/', views.dashboard_faq_edit, name='dashboard_faq_edit'),
    path('dashboard/faqs/<int:pk>/delete/', views.dashboard_faq_delete, name='dashboard_faq_delete'),
    
    # Testimonials Dashboard
    path('dashboard/testimonials/', views.dashboard_testimonial_list, name='dashboard_testimonial_list'),
    path('dashboard/testimonials/create/', views.dashboard_testimonial_create, name='dashboard_testimonial_create'),
    path('dashboard/testimonials/<int:pk>/edit/', views.dashboard_testimonial_edit, name='dashboard_testimonial_edit'),
    path('dashboard/testimonials/<int:pk>/delete/', views.dashboard_testimonial_delete, name='dashboard_testimonial_delete'),
]


from django.urls import path
from . import views

app_name = 'packages'

urlpatterns = [
    # ============================================================================
    # DASHBOARD URLs (Admin/Staff)
    # ============================================================================
    
    # Package Management
    path('dashboard/packages/', views.dashboard_package_list, name='dashboard_package_list'),
    path('dashboard/packages/create/', views.dashboard_package_create, name='dashboard_package_create'),
    path('dashboard/packages/<int:pk>/edit/', views.dashboard_package_edit, name='dashboard_package_edit'),
    path('dashboard/packages/<int:pk>/delete/', views.dashboard_package_delete, name='dashboard_package_delete'),
    
    # Package Image Management
    path('dashboard/packages/<int:package_pk>/images/add/', views.dashboard_package_image_add, name='dashboard_package_image_add'),
    path('dashboard/package-images/<int:pk>/delete/', views.dashboard_package_image_delete, name='dashboard_package_image_delete'),
    
    # Package Itinerary Management
    path('dashboard/packages/<int:package_pk>/itinerary/add/', views.dashboard_package_itinerary_add, name='dashboard_package_itinerary_add'),
    path('dashboard/package-itinerary/<int:pk>/edit/', views.dashboard_package_itinerary_edit, name='dashboard_package_itinerary_edit'),
    path('dashboard/package-itinerary/<int:pk>/delete/', views.dashboard_package_itinerary_delete, name='dashboard_package_itinerary_delete'),
    
    # Package Inclusion Management
    path('dashboard/packages/<int:package_pk>/inclusions/add/', views.dashboard_package_inclusion_add, name='dashboard_package_inclusion_add'),
    path('dashboard/package-inclusions/<int:pk>/edit/', views.dashboard_package_inclusion_edit, name='dashboard_package_inclusion_edit'),
    path('dashboard/package-inclusions/<int:pk>/delete/', views.dashboard_package_inclusion_delete, name='dashboard_package_inclusion_delete'),
    
    # ============================================================================
    # DASHBOARD INQUIRY URLs (Phase 2A - Staff Only)
    # ============================================================================
    
    # Inquiry Management
    path('dashboard/inquiries/', views.dashboard_inquiry_list, name='dashboard_inquiry_list'),
    path('dashboard/inquiries/<int:pk>/', views.dashboard_inquiry_detail, name='dashboard_inquiry_detail'),
    
    # Custom Package Builder
    path('dashboard/inquiries/<int:inquiry_pk>/create-quote/', views.dashboard_custom_package_builder, name='dashboard_custom_package_builder'),
    path('dashboard/custom-packages/', views.dashboard_custom_package_list, name='dashboard_custom_package_list'),
    path('dashboard/custom-packages/<int:pk>/', views.dashboard_custom_package_detail, name='dashboard_custom_package_detail'),
    path('dashboard/custom-packages/<int:pk>/send/', views.dashboard_custom_package_send, name='dashboard_custom_package_send'),
    
    # Custom Package Itinerary
    path('dashboard/custom-packages/<int:custom_package_pk>/itinerary/add/', views.dashboard_custom_itinerary_add, name='dashboard_custom_itinerary_add'),
    path('dashboard/custom-packages/<int:custom_package_pk>/itinerary/copy/', views.dashboard_custom_itinerary_copy, name='dashboard_custom_itinerary_copy'),
    path('dashboard/custom-itinerary/<int:pk>/edit/', views.dashboard_custom_itinerary_edit, name='dashboard_custom_itinerary_edit'),
    path('dashboard/custom-itinerary/<int:pk>/delete/', views.dashboard_custom_itinerary_delete, name='dashboard_custom_itinerary_delete'),
    
    # ============================================================================
    # PUBLIC URLs (Customer-Facing)
    # ============================================================================
    
    # Package Browsing
    path('packages/', views.public_package_list, name='public_package_list'),
    path('packages/featured/', views.public_featured_packages, name='public_featured_packages'),
    path('packages/<slug:slug>/', views.public_package_detail, name='public_package_detail'),
    
    # ============================================================================
    # PUBLIC INQUIRY URLs (Phase 2A - Customer-Facing)
    # ============================================================================
    
    # Inquiry Submission
    path('inquiry/', views.inquiry_create, name='inquiry_create'),
    path('inquiry/<slug:package_slug>/', views.inquiry_create, name='inquiry_create_package'),
    path('inquiry/success/<str:reference>/', views.inquiry_success, name='inquiry_success'),
    
    # Custom Package View (Secure Token)
    path('custom/<uuid:token>/', views.custom_package_view, name='custom_package_view'),
    path('custom/<uuid:token>/<str:action>/', views.custom_package_action, name='custom_package_action'),

    # ============================================================================
    # BOOKING SYSTEM URLs
    # ============================================================================
    path('dashboard/bookings/', views.dashboard_booking_list, name='dashboard_booking_list'),
    path('dashboard/bookings/create/', views.dashboard_booking_create, name='dashboard_booking_create'),
    path('dashboard/bookings/create/from-inquiry/<int:inquiry_pk>/', views.dashboard_booking_create, name='dashboard_booking_create_from_inquiry'),
    path('dashboard/bookings/<int:pk>/', views.dashboard_booking_detail, name='dashboard_booking_detail'),
    path('dashboard/bookings/<int:pk>/edit/', views.dashboard_booking_edit, name='dashboard_booking_edit'),
    path('dashboard/bookings/<int:pk>/cancel/', views.dashboard_booking_cancel, name='dashboard_booking_cancel'),

    # Passengers
    path('dashboard/bookings/<int:booking_pk>/passengers/add/', views.dashboard_passenger_add, name='dashboard_passenger_add'),
    path('dashboard/passengers/<int:pk>/edit/', views.dashboard_passenger_edit, name='dashboard_passenger_edit'),
    path('dashboard/passengers/<int:pk>/delete/', views.dashboard_passenger_delete, name='dashboard_passenger_delete'),

    # Payments
    path('dashboard/bookings/<int:booking_pk>/payments/record/', views.dashboard_payment_record, name='dashboard_payment_record'),
    path('dashboard/payments/<int:pk>/delete/', views.dashboard_payment_delete, name='dashboard_payment_delete'),

    # Invoices
    path('dashboard/bookings/<int:booking_pk>/invoices/create/', views.dashboard_invoice_create, name='dashboard_invoice_create'),
    path('dashboard/invoices/<int:pk>/pdf/', views.dashboard_invoice_pdf, name='dashboard_invoice_pdf'),
    path('dashboard/invoices/<int:pk>/email/', views.dashboard_invoice_email, name='dashboard_invoice_email'),

    # ============================================================================
    # DEPARTURE / AVAILABILITY CALENDAR
    # ============================================================================
    path('dashboard/packages/<int:package_pk>/departures/', views.dashboard_departure_list, name='dashboard_departure_list'),
    path('dashboard/packages/<int:package_pk>/departures/add/', views.dashboard_departure_create, name='dashboard_departure_create'),
    path('dashboard/departures/<int:pk>/edit/', views.dashboard_departure_edit, name='dashboard_departure_edit'),
    path('dashboard/departures/<int:pk>/delete/', views.dashboard_departure_delete, name='dashboard_departure_delete'),
]


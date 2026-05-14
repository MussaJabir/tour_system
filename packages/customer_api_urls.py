from django.urls import path
from . import customer_api_views

urlpatterns = [
    # Bookings
    path('customer/bookings/', customer_api_views.customer_booking_list, name='customer-booking-list'),
    path('customer/bookings/<str:reference>/', customer_api_views.customer_booking_detail, name='customer-booking-detail'),

    # Inquiries
    path('customer/inquiries/', customer_api_views.customer_inquiry_list, name='customer-inquiry-list'),
    path('customer/inquiries/<str:reference>/', customer_api_views.customer_inquiry_detail, name='customer-inquiry-detail'),

    # Saved packages
    path('customer/saved-packages/', customer_api_views.customer_saved_package_list, name='customer-saved-list'),
    path('customer/packages/<slug:slug>/save/', customer_api_views.customer_save_package, name='customer-save-package'),
]

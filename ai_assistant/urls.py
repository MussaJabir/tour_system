from django.urls import path

from . import views

app_name = 'ai_assistant'

urlpatterns = [
    path('dashboard/ai/', views.dashboard_ai_home, name='home'),
    # Brochure parser
    path('dashboard/ai/brochure/', views.brochure_upload, name='brochure_upload'),
    path('dashboard/ai/brochure/<int:pk>/', views.brochure_result, name='brochure_result'),
    # Itinerary generator
    path('dashboard/ai/itinerary/', views.itinerary_generate, name='itinerary_generate'),
    path('dashboard/ai/itinerary/<int:pk>/', views.itinerary_result, name='itinerary_result'),
    # Quote builder (triggered from inquiry detail)
    path('dashboard/ai/quote/inquiry/<int:inquiry_pk>/', views.quote_from_inquiry, name='quote_from_inquiry'),
    path('dashboard/ai/quote/<int:pk>/', views.quote_result, name='quote_result'),
    # Route optimizer
    path('dashboard/ai/route/', views.route_optimize, name='route_optimize'),
    path('dashboard/ai/route/<int:pk>/', views.route_result, name='route_result'),
]

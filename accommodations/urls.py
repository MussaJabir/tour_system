from django.urls import path
from . import views

urlpatterns = [
    # Dashboard URLs
    path('dashboard/accommodations/', views.dashboard_accommodation_list, name='dashboard_accommodation_list'),
    path('dashboard/accommodations/create/', views.dashboard_accommodation_create, name='dashboard_accommodation_create'),
    path('dashboard/accommodations/<int:pk>/', views.dashboard_accommodation_detail, name='dashboard_accommodation_detail'),
    path('dashboard/accommodations/<int:pk>/edit/', views.dashboard_accommodation_edit, name='dashboard_accommodation_edit'),
    path('dashboard/accommodations/<int:pk>/delete/', views.dashboard_accommodation_delete, name='dashboard_accommodation_delete'),
    path('dashboard/accommodations/<int:pk>/add-image/', views.dashboard_add_gallery_image, name='dashboard_add_accommodation_gallery_image'),
    path('dashboard/accommodations/image/<int:pk>/delete/', views.dashboard_delete_gallery_image, name='dashboard_delete_accommodation_gallery_image'),
    path('dashboard/accommodations/<int:pk>/add-room/', views.dashboard_add_room, name='dashboard_add_accommodation_room'),
    path('dashboard/accommodations/room/<int:pk>/edit/', views.dashboard_edit_room, name='dashboard_edit_accommodation_room'),
    path('dashboard/accommodations/room/<int:pk>/delete/', views.dashboard_delete_room, name='dashboard_delete_accommodation_room'),
    
    # Public URLs
    path('accommodations/', views.public_accommodation_list, name='public_accommodation_list'),
    path('accommodations/featured/', views.public_accommodation_featured, name='public_accommodation_featured'),
    path('accommodations/destination/<slug:destination_slug>/', views.public_accommodation_by_destination, name='public_accommodation_by_destination'),
    path('accommodations/<slug:slug>/', views.public_accommodation_detail, name='public_accommodation_detail'),
]


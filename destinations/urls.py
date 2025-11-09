from django.urls import path
from . import views

urlpatterns = [
    # Custom Dashboard URLs (Backend)
    path('dashboard/destinations/', views.dashboard_destination_list, name='dashboard_destination_list'),
    path('dashboard/destinations/create/', views.dashboard_destination_create, name='dashboard_destination_create'),
    path('dashboard/destinations/<int:pk>/', views.dashboard_destination_detail, name='dashboard_destination_detail'),
    path('dashboard/destinations/<int:pk>/edit/', views.dashboard_destination_edit, name='dashboard_destination_edit'),
    path('dashboard/destinations/<int:pk>/delete/', views.dashboard_destination_delete, name='dashboard_destination_delete'),
    path('dashboard/destinations/<int:pk>/add-image/', views.dashboard_add_gallery_image, name='dashboard_add_gallery_image'),
    path('dashboard/destinations/image/<int:pk>/delete/', views.dashboard_delete_gallery_image, name='dashboard_delete_gallery_image'),
    
    # Public URLs (Frontend)
    path('', views.public_home, name='public_home'),
    path('destinations/', views.public_destination_list, name='public_destination_list'),
    path('destinations/featured/', views.public_destination_featured, name='public_destination_featured'),
    path('destinations/<slug:slug>/', views.public_destination_detail, name='public_destination_detail'),
]


from django.urls import path
from . import views

urlpatterns = [
    # Custom Dashboard URLs (Backend)
    path('dashboard/activities/', views.dashboard_activity_list, name='dashboard_activity_list'),
    path('dashboard/activities/create/', views.dashboard_activity_create, name='dashboard_activity_create'),
    path('dashboard/activities/<int:pk>/', views.dashboard_activity_detail, name='dashboard_activity_detail'),
    path('dashboard/activities/<int:pk>/edit/', views.dashboard_activity_edit, name='dashboard_activity_edit'),
    path('dashboard/activities/<int:pk>/delete/', views.dashboard_activity_delete, name='dashboard_activity_delete'),
    path('dashboard/activities/<int:pk>/add-image/', views.dashboard_add_gallery_image, name='dashboard_add_activity_gallery_image'),
    path('dashboard/activities/image/<int:pk>/delete/', views.dashboard_delete_gallery_image, name='dashboard_delete_activity_gallery_image'),
    
    # Public URLs (Frontend)
    path('activities/', views.public_activity_list, name='public_activity_list'),
    path('activities/featured/', views.public_activity_featured, name='public_activity_featured'),
    path('activities/destination/<slug:destination_slug>/', views.public_activity_by_destination, name='public_activity_by_destination'),
    path('activities/<slug:slug>/', views.public_activity_detail, name='public_activity_detail'),
]


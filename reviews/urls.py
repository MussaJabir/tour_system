from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    # Public
    path('packages/<slug:package_slug>/reviews/', views.public_review_list, name='public_review_list'),
    path('packages/<slug:package_slug>/reviews/submit/', views.review_submit, name='review_submit'),

    # Dashboard
    path('dashboard/reviews/', views.dashboard_review_list, name='dashboard_review_list'),
    path('dashboard/reviews/<int:pk>/', views.dashboard_review_detail, name='dashboard_review_detail'),
    path('dashboard/reviews/<int:pk>/approve/', views.dashboard_review_approve, name='dashboard_review_approve'),
    path('dashboard/reviews/<int:pk>/reject/', views.dashboard_review_reject, name='dashboard_review_reject'),
    path('dashboard/reviews/<int:pk>/delete/', views.dashboard_review_delete, name='dashboard_review_delete'),
]

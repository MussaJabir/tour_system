from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Activity, ActivityImage
from .forms import ActivityForm, ActivityImageForm


# ============================================
# CUSTOM DASHBOARD VIEWS (Backend)
# ============================================

@login_required
@staff_member_required
def dashboard_activity_list(request):
    """
    List all activities in custom dashboard
    """
    # Get filters
    search_query = request.GET.get('search', '')
    filter_destination = request.GET.get('destination', '')
    filter_category = request.GET.get('category', '')
    filter_difficulty = request.GET.get('difficulty', '')
    
    # Base queryset
    activities = Activity.objects.select_related('destination').all().order_by('-created_at')
    
    # Apply filters
    if search_query:
        activities = activities.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(destination__name__icontains=search_query)
        )
    
    if filter_destination:
        activities = activities.filter(destination__slug=filter_destination)
    
    if filter_category:
        activities = activities.filter(category=filter_category)
    
    if filter_difficulty:
        activities = activities.filter(difficulty=filter_difficulty)
    
    # Pagination
    paginator = Paginator(activities, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    from destinations.models import Destination
    destinations = Destination.objects.filter(is_active=True)
    
    context = {
        'activities': page_obj,
        'destinations': destinations,
        'categories': Activity.CATEGORY_CHOICES,
        'difficulties': Activity.DIFFICULTY_CHOICES,
        'search_query': search_query,
        'filter_destination': filter_destination,
        'filter_category': filter_category,
        'filter_difficulty': filter_difficulty,
        'page_title': 'Manage Activities',
        'active_menu': 'activities',
    }
    
    return render(request, 'activities/dashboard/list.html', context)


@login_required
@staff_member_required
def dashboard_activity_create(request):
    """
    Create new activity in custom dashboard
    """
    if request.method == 'POST':
        form = ActivityForm(request.POST, request.FILES)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.created_by = request.user
            activity.save()
            messages.success(request, f'Activity "{activity.name}" created successfully!')
            return redirect('dashboard_activity_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ActivityForm()
    
    context = {
        'form': form,
        'page_title': 'Create New Activity',
        'active_menu': 'activities',
        'is_edit': False,
    }
    
    return render(request, 'activities/dashboard/form.html', context)


@login_required
@staff_member_required
def dashboard_activity_edit(request, pk):
    """
    Edit existing activity in custom dashboard
    """
    activity = get_object_or_404(Activity, pk=pk)
    
    if request.method == 'POST':
        form = ActivityForm(request.POST, request.FILES, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, f'Activity "{activity.name}" updated successfully!')
            return redirect('dashboard_activity_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ActivityForm(instance=activity)
    
    # Get gallery images
    gallery_images = activity.gallery_images.all()
    
    context = {
        'form': form,
        'activity': activity,
        'gallery_images': gallery_images,
        'page_title': f'Edit Activity: {activity.name}',
        'active_menu': 'activities',
        'is_edit': True,
    }
    
    return render(request, 'activities/dashboard/form.html', context)


@login_required
@staff_member_required
def dashboard_activity_detail(request, pk):
    """
    View activity details in dashboard
    """
    activity = get_object_or_404(Activity, pk=pk)
    gallery_images = activity.gallery_images.all()
    
    context = {
        'activity': activity,
        'gallery_images': gallery_images,
        'page_title': f'Activity Details: {activity.name}',
        'active_menu': 'activities',
    }
    
    return render(request, 'activities/dashboard/detail.html', context)


@login_required
@staff_member_required
def dashboard_activity_delete(request, pk):
    """
    Delete activity
    """
    activity = get_object_or_404(Activity, pk=pk)
    
    if request.method == 'POST':
        name = activity.name
        activity.delete()
        messages.success(request, f'Activity "{name}" deleted successfully!')
        return redirect('dashboard_activity_list')
    
    context = {
        'activity': activity,
        'page_title': f'Delete Activity: {activity.name}',
        'active_menu': 'activities',
    }
    
    return render(request, 'activities/dashboard/delete_confirm.html', context)


@login_required
@staff_member_required
def dashboard_add_gallery_image(request, pk):
    """
    Add image to activity gallery
    """
    activity = get_object_or_404(Activity, pk=pk)
    
    if request.method == 'POST':
        form = ActivityImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.activity = activity
            image.save()
            messages.success(request, 'Image added to gallery!')
            return redirect('dashboard_activity_edit', pk=activity.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ActivityImageForm()
    
    context = {
        'form': form,
        'activity': activity,
        'page_title': f'Add Image to {activity.name}',
        'active_menu': 'activities',
    }
    
    return render(request, 'activities/dashboard/add_image.html', context)


@login_required
@staff_member_required
def dashboard_delete_gallery_image(request, pk):
    """
    Delete image from gallery
    """
    image = get_object_or_404(ActivityImage, pk=pk)
    activity_pk = image.activity.pk
    
    if request.method == 'POST':
        image.delete()
        messages.success(request, 'Image deleted from gallery!')
        return redirect('dashboard_activity_edit', pk=activity_pk)
    
    return redirect('dashboard_activity_edit', pk=activity_pk)


# ============================================
# PUBLIC VIEWS (Frontend)
# ============================================

def public_activity_list(request):
    """
    Public listing of activities
    """
    activities = Activity.objects.filter(is_active=True).select_related('destination')
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        activities = activities.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(destination__name__icontains=search_query)
        )
    
    # Filters
    category = request.GET.get('category', '')
    if category:
        activities = activities.filter(category=category)
    
    difficulty = request.GET.get('difficulty', '')
    if difficulty:
        activities = activities.filter(difficulty=difficulty)
    
    destination_slug = request.GET.get('destination', '')
    if destination_slug:
        activities = activities.filter(destination__slug=destination_slug)
    
    # Pagination
    paginator = Paginator(activities, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    from destinations.models import Destination
    destinations = Destination.objects.filter(is_active=True)
    
    context = {
        'activities': page_obj,
        'destinations': destinations,
        'categories': Activity.CATEGORY_CHOICES,
        'difficulties': Activity.DIFFICULTY_CHOICES,
        'search_query': search_query,
        'selected_category': category,
        'selected_difficulty': difficulty,
        'selected_destination': destination_slug,
    }
    
    return render(request, 'activities/public/list.html', context)


def public_activity_detail(request, slug):
    """
    Public activity detail page
    """
    activity = get_object_or_404(Activity, slug=slug, is_active=True)
    
    # Increment view count (only for non-staff)
    if not (request.user.is_authenticated and request.user.is_staff):
        activity.increment_view_count()
    
    # Get gallery images
    gallery_images = activity.gallery_images.all()
    
    # Get related activities (same destination or category)
    related_activities = Activity.objects.filter(
        is_active=True
    ).filter(
        Q(destination=activity.destination) | Q(category=activity.category)
    ).exclude(pk=activity.pk)[:4]
    
    context = {
        'activity': activity,
        'gallery_images': gallery_images,
        'related_activities': related_activities,
    }
    
    return render(request, 'activities/public/detail.html', context)


def public_activity_featured(request):
    """
    Public listing of featured activities only
    """
    activities = Activity.objects.filter(is_active=True, is_featured=True).select_related('destination')
    
    # Pagination
    paginator = Paginator(activities, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'activities': page_obj,
        'is_featured_page': True,
    }
    
    return render(request, 'activities/public/list.html', context)


def public_activity_by_destination(request, destination_slug):
    """
    Public listing of activities for a specific destination
    """
    from destinations.models import Destination
    destination = get_object_or_404(Destination, slug=destination_slug, is_active=True)
    
    activities = Activity.objects.filter(
        is_active=True,
        destination=destination
    ).select_related('destination')
    
    # Pagination
    paginator = Paginator(activities, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'activities': page_obj,
        'destination': destination,
        'is_destination_filter': True,
    }
    
    return render(request, 'activities/public/list.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Destination, DestinationImage
from .forms import DestinationForm, DestinationImageForm


# ============================================
# CUSTOM DASHBOARD VIEWS (Backend)
# ============================================

@login_required
def dashboard_destination_list(request):
    """
    List all destinations in custom dashboard
    """
    # Get search query
    search_query = request.GET.get('search', '')
    filter_country = request.GET.get('country', '')
    filter_status = request.GET.get('status', '')
    
    # Base queryset
    destinations = Destination.objects.all().order_by('-created_at')
    
    # Apply filters
    if search_query:
        destinations = destinations.filter(
            Q(name__icontains=search_query) |
            Q(country__icontains=search_query) |
            Q(region__icontains=search_query)
        )
    
    if filter_country:
        destinations = destinations.filter(country=filter_country)
    
    if filter_status == 'active':
        destinations = destinations.filter(is_active=True)
    elif filter_status == 'inactive':
        destinations = destinations.filter(is_active=False)
    elif filter_status == 'featured':
        destinations = destinations.filter(is_featured=True)
    
    # Pagination
    paginator = Paginator(destinations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unique countries for filter dropdown
    countries = Destination.objects.values_list('country', flat=True).distinct()
    
    context = {
        'destinations': page_obj,
        'countries': countries,
        'search_query': search_query,
        'filter_country': filter_country,
        'filter_status': filter_status,
    }
    
    return render(request, 'destinations/dashboard/list.html', context)


@login_required
def dashboard_destination_create(request):
    """
    Create new destination in custom dashboard
    """
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            destination = form.save(commit=False)
            destination.created_by = request.user
            destination.save()
            messages.success(request, f'Destination "{destination.name}" created successfully!')
            return redirect('dashboard_destination_list')
    else:
        form = DestinationForm()
    
    context = {
        'form': form,
        'title': 'Create New Destination',
        'action': 'Create'
    }
    
    return render(request, 'destinations/dashboard/form.html', context)


@login_required
def dashboard_destination_edit(request, pk):
    """
    Edit existing destination in custom dashboard
    """
    destination = get_object_or_404(Destination, pk=pk)
    
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            form.save()
            messages.success(request, f'Destination "{destination.name}" updated successfully!')
            return redirect('dashboard_destination_list')
    else:
        form = DestinationForm(instance=destination)
    
    # Get gallery images
    gallery_images = destination.gallery_images.all()
    
    context = {
        'form': form,
        'destination': destination,
        'gallery_images': gallery_images,
        'title': f'Edit: {destination.name}',
        'action': 'Update'
    }
    
    return render(request, 'destinations/dashboard/form.html', context)


@login_required
def dashboard_destination_delete(request, pk):
    """
    Delete destination
    """
    destination = get_object_or_404(Destination, pk=pk)
    
    if request.method == 'POST':
        name = destination.name
        destination.delete()
        messages.success(request, f'Destination "{name}" deleted successfully!')
        return redirect('dashboard_destination_list')
    
    context = {
        'destination': destination
    }
    
    return render(request, 'destinations/dashboard/delete_confirm.html', context)


@login_required
def dashboard_destination_detail(request, pk):
    """
    View destination details in dashboard
    """
    destination = get_object_or_404(Destination, pk=pk)
    gallery_images = destination.gallery_images.all()
    
    context = {
        'destination': destination,
        'gallery_images': gallery_images
    }
    
    return render(request, 'destinations/dashboard/detail.html', context)


@login_required
def dashboard_add_gallery_image(request, pk):
    """
    Add image to destination gallery
    """
    destination = get_object_or_404(Destination, pk=pk)
    
    if request.method == 'POST':
        form = DestinationImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.destination = destination
            image.save()
            messages.success(request, 'Image added to gallery!')
            return redirect('dashboard_destination_edit', pk=destination.pk)
    else:
        form = DestinationImageForm()
    
    context = {
        'form': form,
        'destination': destination
    }
    
    return render(request, 'destinations/dashboard/add_image.html', context)


@login_required
def dashboard_delete_gallery_image(request, pk):
    """
    Delete image from gallery
    """
    image = get_object_or_404(DestinationImage, pk=pk)
    destination_pk = image.destination.pk
    
    if request.method == 'POST':
        image.delete()
        messages.success(request, 'Image deleted from gallery!')
        return redirect('dashboard_destination_edit', pk=destination_pk)
    
    return redirect('dashboard_destination_edit', pk=destination_pk)


# ============================================
# PUBLIC VIEWS (Frontend)
# ============================================

def public_home(request):
    """
    Public homepage
    """
    featured_destinations = Destination.objects.filter(is_active=True, is_featured=True)[:6]
    
    context = {
        'featured_destinations': featured_destinations
    }
    
    return render(request, 'frontend/index.html', context)


def public_destination_list(request):
    """
    Public listing of destinations
    """
    destinations = Destination.objects.filter(is_active=True)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        destinations = destinations.filter(
            Q(name__icontains=search_query) |
            Q(country__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filter by country
    country = request.GET.get('country', '')
    if country:
        destinations = destinations.filter(country=country)
    
    # Pagination
    paginator = Paginator(destinations, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get countries for filter
    countries = Destination.objects.filter(is_active=True).values_list('country', flat=True).distinct()
    
    context = {
        'destinations': page_obj,
        'countries': countries,
        'search_query': search_query,
        'selected_country': country
    }
    
    return render(request, 'destinations/public/list.html', context)


def public_destination_featured(request):
    """
    Public listing of featured destinations only
    """
    destinations = Destination.objects.filter(is_active=True, is_featured=True)
    
    # Pagination
    paginator = Paginator(destinations, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'destinations': page_obj,
        'is_featured_page': True
    }
    
    return render(request, 'destinations/public/list.html', context)


def public_destination_detail(request, slug):
    """
    Public destination detail page
    """
    destination = get_object_or_404(Destination, slug=slug, is_active=True)
    
    # Increment view count
    destination.increment_view_count()
    
    # Get gallery images
    gallery_images = destination.gallery_images.all()
    
    # Get related destinations (same country)
    related_destinations = Destination.objects.filter(
        country=destination.country,
        is_active=True
    ).exclude(pk=destination.pk)[:4]
    
    context = {
        'destination': destination,
        'gallery_images': gallery_images,
        'related_destinations': related_destinations
    }
    
    return render(request, 'destinations/public/detail.html', context)

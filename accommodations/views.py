from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Accommodation, AccommodationImage, Room
from .forms import AccommodationForm, AccommodationImageForm, RoomForm


# ============================================
# CUSTOM DASHBOARD VIEWS (Backend)
# ============================================

@login_required
@staff_member_required
def dashboard_accommodation_list(request):
    """List all accommodations in custom dashboard"""
    search_query = request.GET.get('search', '')
    filter_destination = request.GET.get('destination', '')
    filter_type = request.GET.get('type', '')
    filter_rating = request.GET.get('rating', '')
    
    accommodations = Accommodation.objects.select_related('destination').all().order_by('-created_at')
    
    if search_query:
        accommodations = accommodations.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(destination__name__icontains=search_query)
        )
    
    if filter_destination:
        accommodations = accommodations.filter(destination__slug=filter_destination)
    
    if filter_type:
        accommodations = accommodations.filter(accommodation_type=filter_type)
    
    if filter_rating:
        accommodations = accommodations.filter(star_rating=filter_rating)
    
    paginator = Paginator(accommodations, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    from destinations.models import Destination
    destinations = Destination.objects.filter(is_active=True)
    
    context = {
        'accommodations': page_obj,
        'destinations': destinations,
        'types': Accommodation.TYPE_CHOICES,
        'ratings': Accommodation.STAR_RATING_CHOICES,
        'search_query': search_query,
        'filter_destination': filter_destination,
        'filter_type': filter_type,
        'filter_rating': filter_rating,
        'page_title': 'Manage Accommodations',
        'active_menu': 'accommodations',
    }
    
    return render(request, 'accommodations/dashboard/list.html', context)


@login_required
@staff_member_required
def dashboard_accommodation_create(request):
    """Create new accommodation"""
    if request.method == 'POST':
        form = AccommodationForm(request.POST, request.FILES)
        if form.is_valid():
            accommodation = form.save(commit=False)
            accommodation.created_by = request.user
            accommodation.save()
            messages.success(request, f'Accommodation "{accommodation.name}" created successfully!')
            return redirect('dashboard_accommodation_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AccommodationForm()
    
    context = {
        'form': form,
        'page_title': 'Create New Accommodation',
        'active_menu': 'accommodations',
        'is_edit': False,
    }
    
    return render(request, 'accommodations/dashboard/form.html', context)


@login_required
@staff_member_required
def dashboard_accommodation_edit(request, pk):
    """Edit existing accommodation"""
    accommodation = get_object_or_404(Accommodation, pk=pk)
    
    if request.method == 'POST':
        form = AccommodationForm(request.POST, request.FILES, instance=accommodation)
        if form.is_valid():
            form.save()
            messages.success(request, f'Accommodation "{accommodation.name}" updated successfully!')
            return redirect('dashboard_accommodation_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AccommodationForm(instance=accommodation)
    
    gallery_images = accommodation.gallery_images.all()
    rooms = accommodation.rooms.all()
    
    context = {
        'form': form,
        'accommodation': accommodation,
        'gallery_images': gallery_images,
        'rooms': rooms,
        'page_title': f'Edit Accommodation: {accommodation.name}',
        'active_menu': 'accommodations',
        'is_edit': True,
    }
    
    return render(request, 'accommodations/dashboard/form.html', context)


@login_required
@staff_member_required
def dashboard_accommodation_detail(request, pk):
    """View accommodation details"""
    accommodation = get_object_or_404(Accommodation, pk=pk)
    gallery_images = accommodation.gallery_images.all()
    rooms = accommodation.rooms.all()
    
    context = {
        'accommodation': accommodation,
        'gallery_images': gallery_images,
        'rooms': rooms,
        'page_title': f'Accommodation Details: {accommodation.name}',
        'active_menu': 'accommodations',
    }
    
    return render(request, 'accommodations/dashboard/detail.html', context)


@login_required
@staff_member_required
def dashboard_accommodation_delete(request, pk):
    """Delete accommodation"""
    accommodation = get_object_or_404(Accommodation, pk=pk)
    
    if request.method == 'POST':
        name = accommodation.name
        accommodation.delete()
        messages.success(request, f'Accommodation "{name}" deleted successfully!')
        return redirect('dashboard_accommodation_list')
    
    context = {
        'accommodation': accommodation,
        'page_title': f'Delete Accommodation: {accommodation.name}',
        'active_menu': 'accommodations',
    }
    
    return render(request, 'accommodations/dashboard/delete_confirm.html', context)


@login_required
@staff_member_required
def dashboard_add_gallery_image(request, pk):
    """Add image to accommodation gallery"""
    accommodation = get_object_or_404(Accommodation, pk=pk)
    
    if request.method == 'POST':
        form = AccommodationImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.accommodation = accommodation
            image.save()
            messages.success(request, 'Image added to gallery!')
            return redirect('dashboard_accommodation_edit', pk=accommodation.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AccommodationImageForm()
    
    context = {
        'form': form,
        'accommodation': accommodation,
        'page_title': f'Add Image to {accommodation.name}',
        'active_menu': 'accommodations',
    }
    
    return render(request, 'accommodations/dashboard/add_image.html', context)


@login_required
@staff_member_required
def dashboard_delete_gallery_image(request, pk):
    """Delete image from gallery"""
    image = get_object_or_404(AccommodationImage, pk=pk)
    accommodation_pk = image.accommodation.pk
    
    if request.method == 'POST':
        image.delete()
        messages.success(request, 'Image deleted from gallery!')
        return redirect('dashboard_accommodation_edit', pk=accommodation_pk)
    
    return redirect('dashboard_accommodation_edit', pk=accommodation_pk)


@login_required
@staff_member_required
def dashboard_add_room(request, pk):
    """Add room to accommodation"""
    accommodation = get_object_or_404(Accommodation, pk=pk)
    
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.accommodation = accommodation
            room.save()
            messages.success(request, f'Room "{room.name}" added successfully!')
            return redirect('dashboard_accommodation_edit', pk=accommodation.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RoomForm()
    
    context = {
        'form': form,
        'accommodation': accommodation,
        'page_title': f'Add Room to {accommodation.name}',
        'active_menu': 'accommodations',
    }
    
    return render(request, 'accommodations/dashboard/add_room.html', context)


@login_required
@staff_member_required
def dashboard_edit_room(request, pk):
    """Edit room"""
    room = get_object_or_404(Room, pk=pk)
    
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, f'Room "{room.name}" updated successfully!')
            return redirect('dashboard_accommodation_edit', pk=room.accommodation.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RoomForm(instance=room)
    
    context = {
        'form': form,
        'room': room,
        'accommodation': room.accommodation,
        'page_title': f'Edit Room: {room.name}',
        'active_menu': 'accommodations',
        'is_edit': True,
    }
    
    return render(request, 'accommodations/dashboard/add_room.html', context)


@login_required
@staff_member_required
def dashboard_delete_room(request, pk):
    """Delete room"""
    room = get_object_or_404(Room, pk=pk)
    accommodation_pk = room.accommodation.pk
    
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Room deleted successfully!')
        return redirect('dashboard_accommodation_edit', pk=accommodation_pk)
    
    return redirect('dashboard_accommodation_edit', pk=accommodation_pk)


# ============================================
# PUBLIC VIEWS (Frontend)
# ============================================

def public_accommodation_list(request):
    """Public listing of accommodations"""
    accommodations = Accommodation.objects.filter(is_active=True).select_related('destination')
    
    search_query = request.GET.get('search', '')
    if search_query:
        accommodations = accommodations.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(destination__name__icontains=search_query)
        )
    
    accommodation_type = request.GET.get('type', '')
    if accommodation_type:
        accommodations = accommodations.filter(accommodation_type=accommodation_type)
    
    star_rating = request.GET.get('rating', '')
    if star_rating:
        accommodations = accommodations.filter(star_rating=star_rating)
    
    destination_slug = request.GET.get('destination', '')
    if destination_slug:
        accommodations = accommodations.filter(destination__slug=destination_slug)
    
    paginator = Paginator(accommodations, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    from destinations.models import Destination
    destinations = Destination.objects.filter(is_active=True)
    
    context = {
        'accommodations': page_obj,
        'destinations': destinations,
        'types': Accommodation.TYPE_CHOICES,
        'ratings': Accommodation.STAR_RATING_CHOICES,
        'search_query': search_query,
        'selected_type': accommodation_type,
        'selected_rating': star_rating,
        'selected_destination': destination_slug,
    }
    
    return render(request, 'accommodations/public/list.html', context)


def public_accommodation_detail(request, slug):
    """Public accommodation detail page"""
    accommodation = get_object_or_404(Accommodation, slug=slug, is_active=True)
    
    # Increment view count
    accommodation.increment_view_count()
    
    gallery_images = accommodation.gallery_images.all()
    rooms = accommodation.rooms.filter(is_available=True)
    
    related_accommodations = Accommodation.objects.filter(
        is_active=True
    ).filter(
        Q(destination=accommodation.destination) | Q(accommodation_type=accommodation.accommodation_type)
    ).exclude(pk=accommodation.pk)[:4]
    
    context = {
        'accommodation': accommodation,
        'gallery_images': gallery_images,
        'rooms': rooms,
        'related_accommodations': related_accommodations,
    }
    
    return render(request, 'accommodations/public/detail.html', context)


def public_accommodation_featured(request):
    """Public listing of featured accommodations"""
    accommodations = Accommodation.objects.filter(is_active=True, is_featured=True).select_related('destination')
    
    paginator = Paginator(accommodations, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'accommodations': page_obj,
        'is_featured_page': True,
    }
    
    return render(request, 'accommodations/public/list.html', context)


def public_accommodation_by_destination(request, destination_slug):
    """Public listing of accommodations for a specific destination"""
    from destinations.models import Destination
    destination = get_object_or_404(Destination, slug=destination_slug, is_active=True)
    
    accommodations = Accommodation.objects.filter(
        is_active=True,
        destination=destination
    ).select_related('destination')
    
    paginator = Paginator(accommodations, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'accommodations': page_obj,
        'destination': destination,
        'is_destination_filter': True,
    }
    
    return render(request, 'accommodations/public/list.html', context)

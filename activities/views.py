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

    if not (request.user.is_authenticated and request.user.is_staff):
        activity.increment_view_count()

    gallery_images = activity.gallery_images.all()

    related_activities = Activity.objects.filter(
        is_active=True
    ).filter(
        Q(destination=activity.destination) | Q(category=activity.category)
    ).exclude(pk=activity.pk)[:4]

    # ------------------------------------------------------------------
    # Inline trust elements + cross-sell to packages.
    # ------------------------------------------------------------------
    from core.models import Testimonial
    inline_review_top = (Testimonial.objects
        .filter(is_active=True, is_featured=True, rating__gte=5)
        .order_by('?').first())
    inline_review_bottom = (Testimonial.objects
        .filter(is_active=True, is_featured=True, rating__gte=5)
        .exclude(pk=inline_review_top.pk if inline_review_top else 0)
        .order_by('?').first())

    # Packages that include this activity in any itinerary day
    from packages.models import Package
    packages_with_activity = (Package.objects
        .filter(is_active=True, itineraries__activities=activity)
        .distinct()[:3])

    # ------------------------------------------------------------------
    # "What to expect" — static per-category 3-step (Before/During/After).
    # ------------------------------------------------------------------
    EXPECT_BY_CATEGORY = {
        'game_drive': [
            ("Before", "Early start", "Wake before dawn, a quick coffee at camp, and your guide is at the wheel before the gates open. The cool of first light is when predators are most active."),
            ("During", "On the move", "Open-sided 4×4 with a roof hatch. Your guide reads tracks, listens to alarm calls from other vehicles, and angles for the best photographic light."),
            ("After", "Back to camp", "Brunch under the trees, mid-day downtime, then a second drive in the golden hour. Sundowner drinks at a private spot if conditions allow."),
        ],
        'wildlife_viewing': [
            ("Before", "Set the scene", "Brief with your guide about the species you're hoping to see and the most likely times and locations to find them."),
            ("During", "Quiet patience", "Spotting is a slow craft. You'll move at the pace of the bush — pauses for tracks, calls, and movement, with binocular work in between."),
            ("After", "Recap & log", "Back at camp, your guide walks through what you saw, often with sketches and species photos. Birding lists kept on request."),
        ],
        'cultural': [
            ("Before", "Brief & context", "Your guide explains the cultural norms before arrival — what to ask, what not to photograph, how to greet elders."),
            ("During", "Visit & exchange", "Walk through the village or boma with a local interpreter. Buy directly from artisans if you'd like; nothing is staged."),
            ("After", "Reflection", "Time to absorb. Discussion with your guide back at the vehicle about what you saw and what surprised you."),
        ],
        'hiking': [
            ("Before", "Gear check", "Boots tested, daypack with water and snacks, weather check. Brief on terrain and pace."),
            ("During", "On the trail", "Walking pace set by the slowest in the group — nobody gets left behind. Pauses at viewpoints, often with bush tea."),
            ("After", "Recover", "Back to lodge for a hot shower, lunch, and a quiet afternoon. Sore-knee tip: walking poles available on request."),
        ],
        'climbing': [
            ("Before", "Acclimatisation", "Pre-trip briefing on altitude, gear list verification, and a fitness check with your lead guide."),
            ("During", "Day by day", "Slow walking pace ('pole pole'), water every hour, full meals served by your support team at each camp."),
            ("After", "Descent & celebration", "Descent is typically faster than ascent. Hot meal at base, certificate ceremony, and transfer to a recovery lodge."),
        ],
        'water_sports': [
            ("Before", "Suit up", "Brief on conditions, safety gear fitted, snorkel/dive equipment checked."),
            ("During", "In the water", "Guided session with marine specialist. Underwater visibility and species sightings logged."),
            ("After", "Warm down", "Fresh water rinse, shaded lounge, light meal back at the boat or beach club."),
        ],
        'cycling': [
            ("Before", "Bike fit", "Bike sized to you, helmets fitted, route reviewed with your guide."),
            ("During", "Ride", "Easy off-road pace. Your guide rides ahead, support vehicle behind for water and any swap-outs."),
            ("After", "Cool down", "Stretches at the end, transfer back to lodge, lunch waiting."),
        ],
        'photography': [
            ("Before", "Setup", "Camera settings reviewed with your photographic guide. Time of day chosen for the right light."),
            ("During", "On the shot", "Positioned for optimal angles. Your guide is also a photographer — happy to spot or to make the shot for you."),
            ("After", "Review", "Quick playback back at the vehicle or camp. Tips and editing pointers from your guide."),
        ],
    }
    DEFAULT_EXPECT = [
        ("Before", "Brief & prep", "Your guide walks you through what to expect, kit check, and the day's plan."),
        ("During", "The experience", "Led by an expert. Pace, stops, and depth tuned to your group."),
        ("After", "Wind down", "Return to your lodge or hotel for refreshments and a chance to absorb what you saw."),
    ]
    expect_steps = EXPECT_BY_CATEGORY.get(activity.category, DEFAULT_EXPECT)

    context = {
        'activity': activity,
        'gallery_images': gallery_images,
        'related_activities': related_activities,
        'inline_review_top': inline_review_top,
        'inline_review_bottom': inline_review_bottom,
        'packages_with_activity': packages_with_activity,
        'expect_steps': expect_steps,
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

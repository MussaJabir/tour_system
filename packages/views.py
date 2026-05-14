import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.http import JsonResponse, Http404
from django.utils import timezone
from decimal import Decimal

logger = logging.getLogger(__name__)

from .models import (
    Package, PackageImage, PackageItinerary, PackageInclusion,
    BookingInquiry, CustomPackage, InquiryMessage,
    Booking, Passenger, Payment, Departure,
)
from .forms import (
    PackageForm, PackageImageForm, PackageItineraryForm, PackageInclusionForm,
    BookingInquiryForm, InquiryManagementForm, CustomPackageForm,
    InquiryMessageForm, InquiryFilterForm,
    BookingForm, PassengerForm, PaymentForm, DepartureForm,
)
from destinations.models import Destination


# ============================================================================
# DASHBOARD VIEWS (Admin/Staff Only)
# ============================================================================

@login_required
@staff_member_required
def dashboard_package_list(request):
    """List all packages in the dashboard"""
    packages = Package.objects.all().prefetch_related('destinations')
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        packages = packages.filter(
            Q(name__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(category__icontains=search_query)
        )
    
    # Filter by category
    category_filter = request.GET.get('category', '')
    if category_filter:
        packages = packages.filter(category=category_filter)
    
    # Filter by availability
    availability_filter = request.GET.get('availability', '')
    if availability_filter:
        packages = packages.filter(availability_status=availability_filter)
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter == 'active':
        packages = packages.filter(is_active=True)
    elif status_filter == 'inactive':
        packages = packages.filter(is_active=False)
    elif status_filter == 'featured':
        packages = packages.filter(is_featured=True)
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by in ['name', '-name', 'price_per_person', '-price_per_person', 'created_at', '-created_at', 'booking_count', '-booking_count']:
        packages = packages.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(packages, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter choices
    categories = Package.CATEGORY_CHOICES
    availability_statuses = Package.AVAILABILITY_CHOICES
    
    context = {
        'page_obj': page_obj,
        'packages': page_obj,
        'search_query': search_query,
        'category_filter': category_filter,
        'availability_filter': availability_filter,
        'status_filter': status_filter,
        'sort_by': sort_by,
        'categories': categories,
        'availability_statuses': availability_statuses,
        'total_count': packages.count(),
    }
    return render(request, 'packages/dashboard/list.html', context)


@login_required
@staff_member_required
def dashboard_package_create(request):
    """Create a new package"""
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES)
        if form.is_valid():
            package = form.save(commit=False)
            package.created_by = request.user
            package.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, f'Package "{package.name}" created successfully!')
            return redirect('packages:dashboard_package_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PackageForm()
    
    context = {
        'form': form,
        'title': 'Create New Package',
        'is_create': True,
    }
    return render(request, 'packages/dashboard/form.html', context)


@login_required
@staff_member_required
def dashboard_package_edit(request, pk):
    """Edit an existing package"""
    package = get_object_or_404(Package, pk=pk)
    
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, f'Package "{package.name}" updated successfully!')
            return redirect('packages:dashboard_package_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PackageForm(instance=package)
    
    # Get related data
    gallery_images = package.gallery_images.all()
    itineraries = package.itineraries.all().order_by('day_number')
    inclusions = package.inclusions.filter(is_included=True)
    exclusions = package.inclusions.filter(is_included=False)
    
    context = {
        'form': form,
        'package': package,
        'gallery_images': gallery_images,
        'itineraries': itineraries,
        'inclusions': inclusions,
        'exclusions': exclusions,
        'title': f'Edit Package: {package.name}',
        'is_create': False,
    }
    return render(request, 'packages/dashboard/form.html', context)


@login_required
@staff_member_required
def dashboard_package_delete(request, pk):
    """Delete a package"""
    package = get_object_or_404(Package, pk=pk)
    
    if request.method == 'POST':
        package_name = package.name
        package.delete()
        messages.success(request, f'Package "{package_name}" deleted successfully!')
        return redirect('packages:dashboard_package_list')
    
    context = {
        'package': package,
    }
    return render(request, 'packages/dashboard/delete_confirm.html', context)


# ============================================================================
# PACKAGE IMAGE MANAGEMENT
# ============================================================================

@login_required
@staff_member_required
def dashboard_package_image_add(request, package_pk):
    """Add images to package gallery"""
    package = get_object_or_404(Package, pk=package_pk)
    
    if request.method == 'POST':
        form = PackageImageForm(request.POST, request.FILES)
        if form.is_valid():
            package_image = form.save(commit=False)
            package_image.package = package
            package_image.save()
            messages.success(request, 'Image added successfully!')
            return redirect('packages:dashboard_package_edit', pk=package.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PackageImageForm()
    
    context = {
        'form': form,
        'package': package,
        'title': f'Add Image to {package.name}',
    }
    return render(request, 'packages/dashboard/image_form.html', context)


@login_required
@staff_member_required
def dashboard_package_image_delete(request, pk):
    """Delete a package image"""
    package_image = get_object_or_404(PackageImage, pk=pk)
    package = package_image.package
    
    if request.method == 'POST':
        package_image.delete()
        messages.success(request, 'Image deleted successfully!')
        return redirect('packages:dashboard_package_edit', pk=package.pk)
    
    context = {
        'package_image': package_image,
        'package': package,
    }
    return render(request, 'packages/dashboard/image_delete_confirm.html', context)


# ============================================================================
# PACKAGE ITINERARY MANAGEMENT
# ============================================================================

@login_required
@staff_member_required
def dashboard_package_itinerary_add(request, package_pk):
    """Add a day to package itinerary"""
    package = get_object_or_404(Package, pk=package_pk)
    
    if request.method == 'POST':
        form = PackageItineraryForm(request.POST)
        if form.is_valid():
            itinerary = form.save(commit=False)
            itinerary.package = package
            itinerary.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, f'Day {itinerary.day_number} added successfully!')
            return redirect('packages:dashboard_package_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Auto-fill day number
        last_day = package.itineraries.order_by('-day_number').first()
        initial_day = (last_day.day_number + 1) if last_day else 1
        form = PackageItineraryForm(initial={'day_number': initial_day})
    
    context = {
        'form': form,
        'package': package,
        'title': f'Add Day to {package.name}',
    }
    return render(request, 'packages/dashboard/itinerary_form.html', context)


@login_required
@staff_member_required
def dashboard_package_itinerary_edit(request, pk):
    """Edit a package itinerary day"""
    itinerary = get_object_or_404(PackageItinerary, pk=pk)
    package = itinerary.package
    
    if request.method == 'POST':
        form = PackageItineraryForm(request.POST, instance=itinerary)
        if form.is_valid():
            form.save()
            messages.success(request, f'Day {itinerary.day_number} updated successfully!')
            return redirect('packages:dashboard_package_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PackageItineraryForm(instance=itinerary)
    
    context = {
        'form': form,
        'itinerary': itinerary,
        'package': package,
        'title': f'Edit Day {itinerary.day_number}',
    }
    return render(request, 'packages/dashboard/itinerary_form.html', context)


@login_required
@staff_member_required
def dashboard_package_itinerary_delete(request, pk):
    """Delete a package itinerary day"""
    itinerary = get_object_or_404(PackageItinerary, pk=pk)
    package = itinerary.package
    
    if request.method == 'POST':
        day_number = itinerary.day_number
        itinerary.delete()
        messages.success(request, f'Day {day_number} deleted successfully!')
        return redirect('packages:dashboard_package_edit', pk=package.pk)
    
    context = {
        'itinerary': itinerary,
        'package': package,
    }
    return render(request, 'packages/dashboard/itinerary_delete_confirm.html', context)


# ============================================================================
# PACKAGE INCLUSION MANAGEMENT
# ============================================================================

@login_required
@staff_member_required
def dashboard_package_inclusion_add(request, package_pk):
    """Add inclusion/exclusion to package"""
    package = get_object_or_404(Package, pk=package_pk)
    
    if request.method == 'POST':
        form = PackageInclusionForm(request.POST)
        if form.is_valid():
            inclusion = form.save(commit=False)
            inclusion.package = package
            inclusion.save()
            status = "Inclusion" if inclusion.is_included else "Exclusion"
            messages.success(request, f'{status} added successfully!')
            return redirect('packages:dashboard_package_edit', pk=package.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PackageInclusionForm()
    
    context = {
        'form': form,
        'package': package,
        'title': f'Add Inclusion/Exclusion to {package.name}',
    }
    return render(request, 'packages/dashboard/inclusion_form.html', context)


@login_required
@staff_member_required
def dashboard_package_inclusion_edit(request, pk):
    """Edit a package inclusion/exclusion"""
    inclusion = get_object_or_404(PackageInclusion, pk=pk)
    package = inclusion.package
    
    if request.method == 'POST':
        form = PackageInclusionForm(request.POST, instance=inclusion)
        if form.is_valid():
            form.save()
            status = "Inclusion" if inclusion.is_included else "Exclusion"
            messages.success(request, f'{status} updated successfully!')
            return redirect('packages:dashboard_package_edit', pk=package.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PackageInclusionForm(instance=inclusion)
    
    context = {
        'form': form,
        'inclusion': inclusion,
        'package': package,
        'title': f'Edit Inclusion/Exclusion',
    }
    return render(request, 'packages/dashboard/inclusion_form.html', context)


@login_required
@staff_member_required
def dashboard_package_inclusion_delete(request, pk):
    """Delete a package inclusion/exclusion"""
    inclusion = get_object_or_404(PackageInclusion, pk=pk)
    package = inclusion.package
    
    if request.method == 'POST':
        status = "Inclusion" if inclusion.is_included else "Exclusion"
        inclusion.delete()
        messages.success(request, f'{status} deleted successfully!')
        return redirect('packages:dashboard_package_edit', pk=package.pk)
    
    context = {
        'inclusion': inclusion,
        'package': package,
    }
    return render(request, 'packages/dashboard/inclusion_delete_confirm.html', context)


# ============================================================================
# PUBLIC VIEWS (Customer-Facing)
# ============================================================================

def public_package_list(request):
    """Public listing of all packages"""
    packages = Package.objects.filter(is_active=True).prefetch_related('destinations')
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        packages = packages.filter(
            Q(name__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(destinations__name__icontains=search_query)
        ).distinct()
    
    # Filter by category
    category_filter = request.GET.get('category', '')
    if category_filter:
        packages = packages.filter(category=category_filter)
    
    # Filter by difficulty
    difficulty_filter = request.GET.get('difficulty', '')
    if difficulty_filter:
        packages = packages.filter(difficulty_level=difficulty_filter)
    
    # Filter by destination
    destination_filter = request.GET.get('destination', '')
    if destination_filter:
        packages = packages.filter(destinations__slug=destination_filter)
    
    # Filter by price range
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if min_price:
        try:
            packages = packages.filter(price_per_person__gte=Decimal(min_price))
        except Exception:
            logger.warning("Invalid min_price filter value: %s", min_price)
    if max_price:
        try:
            packages = packages.filter(price_per_person__lte=Decimal(max_price))
        except Exception:
            logger.warning("Invalid max_price filter value: %s", max_price)

    # Filter by duration
    min_days = request.GET.get('min_days', '')
    max_days = request.GET.get('max_days', '')
    if min_days:
        try:
            packages = packages.filter(duration_days__gte=int(min_days))
        except Exception:
            logger.warning("Invalid min_days filter value: %s", min_days)
    if max_days:
        try:
            packages = packages.filter(duration_days__lte=int(max_days))
        except Exception:
            logger.warning("Invalid max_days filter value: %s", max_days)
    
    # Sorting
    sort_by = request.GET.get('sort', '-is_featured')
    if sort_by == 'price_low':
        packages = packages.order_by('price_per_person')
    elif sort_by == 'price_high':
        packages = packages.order_by('-price_per_person')
    elif sort_by == 'duration_short':
        packages = packages.order_by('duration_days')
    elif sort_by == 'duration_long':
        packages = packages.order_by('-duration_days')
    elif sort_by == 'rating':
        packages = packages.order_by('-rating_average', '-review_count')
    elif sort_by == 'popular':
        packages = packages.order_by('-booking_count', '-view_count')
    elif sort_by == 'newest':
        packages = packages.order_by('-created_at')
    else:
        packages = packages.order_by('-is_featured', 'order', '-created_at')
    
    # Pagination
    paginator = Paginator(packages, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter choices
    categories = Package.CATEGORY_CHOICES
    difficulties = Package.DIFFICULTY_CHOICES
    
    # Get destinations for filter
    from destinations.models import Destination
    available_destinations = Destination.objects.filter(is_active=True, packages__is_active=True).distinct()
    
    context = {
        'page_obj': page_obj,
        'packages': page_obj,
        'search_query': search_query,
        'category_filter': category_filter,
        'difficulty_filter': difficulty_filter,
        'destination_filter': destination_filter,
        'min_price': min_price,
        'max_price': max_price,
        'min_days': min_days,
        'max_days': max_days,
        'sort_by': sort_by,
        'categories': categories,
        'difficulties': difficulties,
        'available_destinations': available_destinations,
        'total_count': packages.count(),
    }
    return render(request, 'packages/public/list.html', context)


def public_package_detail(request, slug):
    """Public detail view of a single package"""
    package = get_object_or_404(
        Package.objects.prefetch_related(
            'destinations',
            'gallery_images',
            'itineraries__activities',
            'itineraries__accommodation',
            'inclusions'
        ),
        slug=slug,
        is_active=True
    )
    
    # Increment view count
    package.increment_view_count()
    
    # Get related data
    itineraries = package.itineraries.filter(is_active=True).order_by('day_number')
    inclusions = package.inclusions.filter(is_included=True, is_active=True).order_by('order')
    exclusions = package.inclusions.filter(is_included=False, is_active=True).order_by('order')
    gallery_images = package.gallery_images.filter(is_active=True).order_by('order')
    
    # Get related packages (same category or destination)
    related_packages = Package.objects.filter(
        Q(category=package.category) | Q(destinations__in=package.destinations.all()),
        is_active=True
    ).exclude(pk=package.pk).distinct()[:4]

    from django.utils import timezone
    upcoming_departures = package.departures.filter(
        status=Departure.STATUS_AVAILABLE,
        departure_date__gte=timezone.now().date(),
    )

    context = {
        'package': package,
        'itineraries': itineraries,
        'inclusions': inclusions,
        'exclusions': exclusions,
        'gallery_images': gallery_images,
        'related_packages': related_packages,
        'upcoming_departures': upcoming_departures,
    }
    return render(request, 'packages/public/detail.html', context)


def public_featured_packages(request):
    """Public listing of featured packages only"""
    packages = Package.objects.filter(
        is_active=True,
        is_featured=True
    ).prefetch_related('destinations').order_by('order', '-created_at')
    
    # Pagination
    paginator = Paginator(packages, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'packages': page_obj,
        'total_count': packages.count(),
        'is_featured': True,
    }
    return render(request, 'packages/public/list.html', context)


# ============================================================================
# BOOKING INQUIRY VIEWS (Phase 2A)
# ============================================================================

# -----------------------------------------------------------------------------
# PUBLIC INQUIRY VIEWS
# -----------------------------------------------------------------------------

def inquiry_create(request, package_slug=None):
    """
    Public form for customers to submit package inquiries.
    Can be accessed from package detail page or standalone.
    """
    package = None
    if package_slug:
        package = get_object_or_404(Package, slug=package_slug, is_active=True)
    
    if request.method == 'POST':
        form = BookingInquiryForm(request.POST, package=package)
        if form.is_valid():
            inquiry = form.save(commit=False)
            
            # Get client IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                inquiry.ip_address = x_forwarded_for.split(',')[0]
            else:
                inquiry.ip_address = request.META.get('REMOTE_ADDR')
            
            inquiry.save()
            
            # Send confirmation email to customer
            from .emails import send_inquiry_confirmation_email, send_inquiry_notification_to_staff
            send_inquiry_confirmation_email(inquiry)
            
            # Send notification to staff
            send_inquiry_notification_to_staff(inquiry)
            
            messages.success(
                request,
                f'Thank you! Your inquiry has been submitted. Reference: {inquiry.inquiry_reference}'
            )
            return redirect('packages:inquiry_success', reference=inquiry.inquiry_reference)
    else:
        form = BookingInquiryForm(package=package)
    
    context = {
        'form': form,
        'package': package,
    }
    return render(request, 'packages/inquiry/create.html', context)


def inquiry_success(request, reference):
    """
    Success page after inquiry submission.
    Shows confirmation details and next steps.
    """
    inquiry = get_object_or_404(BookingInquiry, inquiry_reference=reference)
    
    context = {
        'inquiry': inquiry,
    }
    return render(request, 'packages/inquiry/success.html', context)


def custom_package_view(request, token):
    """
    Public view for client to see their custom package.
    Accessed via secure token link sent via email.
    """
    try:
        custom_package = CustomPackage.objects.select_related(
            'inquiry', 'base_package', 'created_by'
        ).get(access_token=token)
    except CustomPackage.DoesNotExist:
        raise Http404("Custom package not found or link has expired.")
    
    # Check if expired
    if custom_package.is_expired:
        messages.warning(request, 'This quote has expired. Please contact us for a new quote.')
    
    # Increment view count
    custom_package.increment_view_count()
    
    # Get inquiry details
    inquiry = custom_package.inquiry
    
    # Calculate total price
    total_price = custom_package.total_price
    
    context = {
        'custom_package': custom_package,
        'inquiry': inquiry,
        'total_price': total_price,
        'is_expired': custom_package.is_expired,
    }
    return render(request, 'packages/inquiry/custom_package_view.html', context)


def custom_package_action(request, token, action):
    """
    Handle client actions on custom package (approve/decline/request_changes).
    """
    custom_package = get_object_or_404(CustomPackage, access_token=token)
    
    if custom_package.is_expired:
        messages.error(request, 'This quote has expired.')
        return redirect('packages:custom_package_view', token=token)
    
    if request.method == 'POST':
        feedback = request.POST.get('feedback', '')
        
        if action == 'approve':
            custom_package.status = 'approved'
            custom_package.approved_at = timezone.now()
            custom_package.client_action = 'approved'
            custom_package.client_action_at = timezone.now()
            custom_package.client_feedback = feedback
            custom_package.save()
            
            # Update inquiry status
            inquiry = custom_package.inquiry
            inquiry.status = 'confirmed'
            inquiry.save()
            
            # Send notification to staff
            from .emails import send_client_action_notification_to_staff
            send_client_action_notification_to_staff(custom_package, 'approved')
            
            messages.success(
                request,
                'Thank you! You have successfully accepted this package. Our team will contact you shortly to proceed with the booking.'
            )
            
        elif action == 'decline':
            custom_package.status = 'rejected'
            custom_package.rejected_at = timezone.now()
            custom_package.client_action = 'declined'
            custom_package.client_action_at = timezone.now()
            custom_package.client_feedback = feedback
            custom_package.save()
            
            # Update inquiry status
            inquiry = custom_package.inquiry
            inquiry.status = 'cancelled'
            inquiry.save()
            
            # Send notification to staff
            from .emails import send_client_action_notification_to_staff
            send_client_action_notification_to_staff(custom_package, 'declined')
            
            messages.info(request, 'Package declined. Thank you for your feedback.')
            
        elif action == 'request_changes':
            custom_package.status = 'revision_requested'
            custom_package.client_action = 'requested_changes'
            custom_package.client_action_at = timezone.now()
            custom_package.client_feedback = feedback
            custom_package.save()
            
            # Update inquiry status
            inquiry = custom_package.inquiry
            inquiry.status = 'reviewing'
            inquiry.save()
            
            # Send notification to staff
            from .emails import send_client_action_notification_to_staff
            send_client_action_notification_to_staff(custom_package, 'requested_changes')
            
            messages.success(
                request,
                'Your change request has been submitted. Our team will review and get back to you soon.'
            )
    
    return redirect('packages:custom_package_view', token=token)


# -----------------------------------------------------------------------------
# STAFF DASHBOARD INQUIRY VIEWS
# -----------------------------------------------------------------------------

@login_required
@staff_member_required
def dashboard_inquiry_list(request):
    """
    Staff dashboard view to list and filter all inquiries.
    """
    inquiries = BookingInquiry.objects.select_related(
        'base_package', 'staff_assigned', 'custom_package'
    ).order_by('-created_at')
    
    # Apply filters
    filter_form = InquiryFilterForm(request.GET)
    if filter_form.is_valid():
        status = filter_form.cleaned_data.get('status')
        if status:
            inquiries = inquiries.filter(status=status)
        
        priority = filter_form.cleaned_data.get('priority')
        if priority:
            inquiries = inquiries.filter(priority=priority)
        
        staff_assigned = filter_form.cleaned_data.get('staff_assigned')
        if staff_assigned:
            inquiries = inquiries.filter(staff_assigned=staff_assigned)
        
        package = filter_form.cleaned_data.get('package')
        if package:
            inquiries = inquiries.filter(base_package=package)
        
        search = filter_form.cleaned_data.get('search')
        if search:
            inquiries = inquiries.filter(
                Q(inquiry_reference__icontains=search) |
                Q(customer_name__icontains=search) |
                Q(customer_email__icontains=search) |
                Q(customer_phone__icontains=search)
            )
        
        date_from = filter_form.cleaned_data.get('date_from')
        if date_from:
            inquiries = inquiries.filter(created_at__gte=date_from)
        
        date_to = filter_form.cleaned_data.get('date_to')
        if date_to:
            inquiries = inquiries.filter(created_at__lte=date_to)
    
    # Get counts by status for quick stats
    status_counts = {
        'pending': inquiries.filter(status='pending').count(),
        'reviewing': inquiries.filter(status='reviewing').count(),
        'quote_sent': inquiries.filter(status='quote_sent').count(),
        'approved': inquiries.filter(status='approved').count(),
        'converted': inquiries.filter(status='converted').count(),
    }
    
    # Pagination
    paginator = Paginator(inquiries, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'inquiries': page_obj,
        'filter_form': filter_form,
        'status_counts': status_counts,
        'total_count': inquiries.count(),
    }
    return render(request, 'packages/inquiry/dashboard/list.html', context)


@login_required
@staff_member_required
def dashboard_inquiry_detail(request, pk):
    """
    Staff view to see full inquiry details and manage it.
    """
    inquiry = get_object_or_404(
        BookingInquiry.objects.select_related('base_package', 'staff_assigned', 'custom_package'),
        pk=pk
    )
    
    # Mark as viewed
    if not inquiry.viewed_by_staff:
        inquiry.viewed_by_staff = True
        inquiry.first_viewed_at = timezone.now()
        inquiry.save(update_fields=['viewed_by_staff', 'first_viewed_at'])
    
    # Handle management form submission
    if request.method == 'POST':
        if 'update_inquiry' in request.POST:
            management_form = InquiryManagementForm(request.POST, instance=inquiry)
            if management_form.is_valid():
                management_form.save()
                messages.success(request, 'Inquiry updated successfully.')
                return redirect('packages:dashboard_inquiry_detail', pk=pk)
        
        elif 'send_message' in request.POST:
            message_form = InquiryMessageForm(request.POST, request.FILES)
            if message_form.is_valid():
                message = message_form.save(commit=False)
                message.inquiry = inquiry
                message.sender_staff = request.user
                message.save()
                
                # Update inquiry last activity
                inquiry.last_activity_at = timezone.now()
                inquiry.save(update_fields=['last_activity_at'])
                
                messages.success(request, 'Message sent successfully.')
                return redirect('packages:dashboard_inquiry_detail', pk=pk)
    else:
        management_form = InquiryManagementForm(instance=inquiry)
        message_form = InquiryMessageForm()
    
    # Get messages
    inquiry_messages = inquiry.messages.select_related('sender_staff').order_by('created_at')
    
    # Get custom packages created for this inquiry
    custom_packages = inquiry.custom_packages.order_by('-created_at')
    
    context = {
        'inquiry': inquiry,
        'management_form': management_form,
        'message_form': message_form,
        'inquiry_messages': inquiry_messages,
        'custom_packages': custom_packages,
    }
    return render(request, 'packages/inquiry/dashboard/detail.html', context)


@login_required
@staff_member_required
def dashboard_custom_package_builder(request, inquiry_pk):
    """
    Staff view to build a custom package for an inquiry.
    This is the main package customization tool.
    """
    inquiry = get_object_or_404(BookingInquiry, pk=inquiry_pk)
    
    if request.method == 'POST':
        form = CustomPackageForm(request.POST, request.FILES, inquiry=inquiry)
        if form.is_valid():
            custom_package = form.save(commit=False)
            custom_package.created_by = request.user
            custom_package.last_modified_by = request.user
            
            # If base package is selected, copy initial data
            if custom_package.base_package and not custom_package.pk:
                base = custom_package.base_package
                custom_package.name = f"{base.name} - Custom for {inquiry.customer_name}"
                if not custom_package.short_description:
                    custom_package.short_description = base.short_description
                if not custom_package.description:
                    custom_package.description = base.description
                if not custom_package.duration_days:
                    custom_package.duration_days = base.duration_days
                if not custom_package.duration_nights:
                    custom_package.duration_nights = base.duration_nights
                if not custom_package.original_price:
                    custom_package.original_price = base.price_per_person
                if not custom_package.adjusted_price:
                    custom_package.adjusted_price = base.price_per_person
                custom_package.currency = base.currency
            
            custom_package.save()
            
            # Link to inquiry
            inquiry.custom_package = custom_package
            inquiry.status = 'reviewing'
            inquiry.save()
            
            messages.success(
                request,
                f'Custom package created! Reference: {custom_package.custom_reference}'
            )
            return redirect('packages:dashboard_custom_package_detail', pk=custom_package.pk)
    else:
        # Pre-populate form with base package data if available
        initial_data = {}
        if inquiry.base_package:
            base = inquiry.base_package
            initial_data = {
                'base_package': base,
                'name': f"{base.name} - Custom for {inquiry.customer_name}",
                'short_description': base.short_description,
                'description': base.description,
                'duration_days': base.duration_days,
                'duration_nights': base.duration_nights,
                'original_price': base.price_per_person,
                'adjusted_price': base.price_per_person,
                'currency': base.currency,
            }
        
        form = CustomPackageForm(initial=initial_data, inquiry=inquiry)
    
    context = {
        'form': form,
        'inquiry': inquiry,
    }
    return render(request, 'packages/inquiry/dashboard/custom_package_builder.html', context)


@login_required
@staff_member_required
def dashboard_custom_package_list(request):
    """
    Staff view to list all custom packages.
    """
    from .models import CustomPackage
    from django.db.models import Q
    
    custom_packages = CustomPackage.objects.select_related(
        'inquiry', 'base_package', 'created_by'
    ).order_by('-created_at')
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        custom_packages = custom_packages.filter(
            Q(custom_reference__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(inquiry__inquiry_reference__icontains=search_query) |
            Q(inquiry__customer_name__icontains=search_query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        custom_packages = custom_packages.filter(status=status_filter)
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(custom_packages, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Status counts
    all_packages = CustomPackage.objects.all()
    status_counts = {
        'draft': all_packages.filter(status='draft').count(),
        'pending_approval': all_packages.filter(status='pending_approval').count(),
        'approved': all_packages.filter(status='approved').count(),
        'rejected': all_packages.filter(status='rejected').count(),
        'expired': all_packages.filter(status='expired').count(),
    }
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_counts': status_counts,
    }
    return render(request, 'packages/inquiry/dashboard/custom_package_list.html', context)


@login_required
@staff_member_required
def dashboard_custom_package_detail(request, pk):
    """
    Staff view to see and edit a custom package.
    """
    custom_package = get_object_or_404(
        CustomPackage.objects.select_related('inquiry', 'base_package', 'created_by'),
        pk=pk
    )
    
    if request.method == 'POST':
        form = CustomPackageForm(request.POST, request.FILES, instance=custom_package)
        if form.is_valid():
            custom_package = form.save(commit=False)
            custom_package.last_modified_by = request.user
            custom_package.revision_number += 1
            custom_package.save()
            
            messages.success(request, 'Custom package updated successfully.')
            return redirect('packages:dashboard_custom_package_detail', pk=pk)
    else:
        form = CustomPackageForm(instance=custom_package)
    
    # Generate secure link using reverse URL
    from django.urls import reverse
    secure_link = request.build_absolute_uri(
        reverse('packages:custom_package_view', kwargs={'token': custom_package.access_token})
    )
    
    context = {
        'custom_package': custom_package,
        'form': form,
        'secure_link': secure_link,
    }
    return render(request, 'packages/inquiry/dashboard/custom_package_detail.html', context)


@login_required
@staff_member_required
def dashboard_custom_package_send(request, pk):
    """
    Send custom package to client via email.
    """
    custom_package = get_object_or_404(CustomPackage, pk=pk)
    
    if request.method == 'POST':
        # Update status to sent
        custom_package.status = 'sent'
        custom_package.sent_at = timezone.now()
        
        # Set expiry date if not set (7 days from now)
        if not custom_package.expires_at:
            from datetime import timedelta
            custom_package.expires_at = timezone.now() + timedelta(days=7)
        
        custom_package.save()
        
        # Update inquiry status
        inquiry = custom_package.inquiry
        inquiry.status = 'quote_sent'
        inquiry.save()
        
        # Send email to client
        from .emails import send_custom_package_to_client
        email_sent = send_custom_package_to_client(custom_package)
        
        if email_sent:
            messages.success(
                request,
                f'Custom package sent to {inquiry.email}! Client can access it via the secure link.'
            )
        else:
            messages.warning(
                request,
                f'Package status updated, but email could not be sent. Please contact {inquiry.email} directly with the secure link.'
            )
        
        return redirect('packages:dashboard_custom_package_detail', pk=pk)
    
    context = {
        'custom_package': custom_package,
    }
    return render(request, 'packages/inquiry/dashboard/custom_package_send_confirm.html', context)


# ============================================================================
# CUSTOM PACKAGE ITINERARY Management (Staff Dashboard)
# ============================================================================

@login_required
@staff_member_required
def dashboard_custom_itinerary_add(request, custom_package_pk):
    """
    Add a new itinerary day to a custom package.
    """
    from .forms import CustomPackageItineraryForm
    from .models import CustomPackage, CustomPackageItinerary
    
    custom_package = get_object_or_404(CustomPackage, pk=custom_package_pk)
    
    if request.method == 'POST':
        form = CustomPackageItineraryForm(request.POST, request.FILES)
        if form.is_valid():
            itinerary = form.save(commit=False)
            itinerary.custom_package = custom_package
            itinerary.save()
            
            messages.success(request, f'Itinerary day {itinerary.day_display} added successfully.')
            return redirect('packages:dashboard_custom_package_detail', pk=custom_package.pk)
    else:
        # Suggest next day number
        last_day = custom_package.itinerary_days.order_by('-day_number').first()
        initial_day = last_day.day_number + 1 if last_day else 1
        form = CustomPackageItineraryForm(initial={'day_number': initial_day})
    
    context = {
        'form': form,
        'custom_package': custom_package,
        'is_edit': False,
    }
    return render(request, 'packages/inquiry/dashboard/custom_itinerary_form.html', context)


@login_required
@staff_member_required
def dashboard_custom_itinerary_edit(request, pk):
    """
    Edit an existing custom itinerary day.
    """
    from .forms import CustomPackageItineraryForm
    from .models import CustomPackageItinerary
    
    itinerary = get_object_or_404(CustomPackageItinerary, pk=pk)
    custom_package = itinerary.custom_package
    
    if request.method == 'POST':
        form = CustomPackageItineraryForm(request.POST, request.FILES, instance=itinerary)
        if form.is_valid():
            form.save()
            messages.success(request, f'Itinerary day {itinerary.day_display} updated successfully.')
            return redirect('packages:dashboard_custom_package_detail', pk=custom_package.pk)
    else:
        form = CustomPackageItineraryForm(instance=itinerary)
    
    context = {
        'form': form,
        'custom_package': custom_package,
        'itinerary': itinerary,
        'is_edit': True,
    }
    return render(request, 'packages/inquiry/dashboard/custom_itinerary_form.html', context)


@login_required
@staff_member_required
def dashboard_custom_itinerary_delete(request, pk):
    """
    Delete a custom itinerary day.
    """
    from .models import CustomPackageItinerary
    
    itinerary = get_object_or_404(CustomPackageItinerary, pk=pk)
    custom_package = itinerary.custom_package
    
    if request.method == 'POST':
        itinerary.delete()
        messages.success(request, f'Itinerary day {itinerary.day_display} deleted successfully.')
        return redirect('packages:dashboard_custom_package_detail', pk=custom_package.pk)
    
    context = {
        'itinerary': itinerary,
        'custom_package': custom_package,
    }
    return render(request, 'packages/inquiry/dashboard/custom_itinerary_delete.html', context)


@login_required
@staff_member_required
def dashboard_custom_itinerary_copy(request, custom_package_pk):
    """
    Copy itinerary from base package to custom package.
    """
    from .models import CustomPackage, CustomPackageItinerary
    
    custom_package = get_object_or_404(CustomPackage, pk=custom_package_pk)
    
    if request.method == 'POST':
        # Clear existing custom itinerary
        custom_package.itinerary_days.all().delete()
        
        # Copy from base package
        if custom_package.base_package:
            base_itinerary = custom_package.base_package.itineraries.all()
            copied_count = 0
            
            for base_day in base_itinerary:
                # Get accommodation name if accommodation exists
                accommodation_name = base_day.accommodation.name if base_day.accommodation else ''
                accommodation_type = 'hotel'  # Default type
                
                # Get location from destinations or accommodation
                location = ''
                if base_day.accommodation and base_day.accommodation.destinations.exists():
                    location = base_day.accommodation.destinations.first().name
                
                # Get activities as text
                activities_text = ', '.join([act.name for act in base_day.activities.all()])
                
                # Get transport details
                transport_details = base_day.transport_type if hasattr(base_day, 'transport_type') else ''
                
                # Get distance and drive time
                distance = base_day.distance_km if hasattr(base_day, 'distance_km') else ''
                drive_time = base_day.drive_duration if hasattr(base_day, 'drive_duration') else ''
                
                CustomPackageItinerary.objects.create(
                    custom_package=custom_package,
                    day_number=base_day.day_number,
                    end_day_number=base_day.end_day_number,
                    title=base_day.title,
                    description=base_day.description,
                    location=location,
                    accommodation_name=accommodation_name,
                    accommodation_type=accommodation_type,
                    activities=activities_text,
                    breakfast_included=base_day.breakfast_included,
                    lunch_included=base_day.lunch_included,
                    dinner_included=base_day.dinner_included,
                    transport_details=transport_details,
                    distance=str(distance) if distance else '',
                    drive_time=str(drive_time) if drive_time else '',
                    order=base_day.order,
                    is_active=base_day.is_active
                )
                copied_count += 1
            
            messages.success(request, f'Copied {copied_count} itinerary days from base package. You can now customize them.')
        else:
            messages.warning(request, 'No base package found to copy from.')
        
        return redirect('packages:dashboard_custom_package_detail', pk=custom_package.pk)
    
    context = {
        'custom_package': custom_package,
    }
    return render(request, 'packages/inquiry/dashboard/custom_itinerary_copy.html', context)


# ============================================================================
# BOOKING DASHBOARD VIEWS
# ============================================================================

@login_required
@staff_member_required
def dashboard_booking_list(request):
    bookings = Booking.objects.select_related('package', 'staff_assigned', 'inquiry').all()
    status_filter = request.GET.get('status', '')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    search = request.GET.get('q', '').strip()
    if search:
        bookings = bookings.filter(
            Q(booking_reference__icontains=search) |
            Q(package__name__icontains=search) |
            Q(inquiry__customer_name__icontains=search) |
            Q(inquiry__customer_email__icontains=search)
        )
    paginator = Paginator(bookings, 20)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'packages/bookings/dashboard/list.html', {
        'page_obj': page,
        'status_filter': status_filter,
        'search': search,
        'status_choices': Booking.STATUS_CHOICES,
        'total_count': bookings.count(),
    })


@login_required
@staff_member_required
def dashboard_booking_create(request, inquiry_pk=None):
    inquiry = None
    initial = {}
    if inquiry_pk:
        inquiry = get_object_or_404(BookingInquiry, pk=inquiry_pk)
        initial = {
            'inquiry': inquiry,
            'num_adults': inquiry.number_of_adults,
            'num_children': inquiry.number_of_children,
            'departure_date': inquiry.preferred_travel_date,
            'package': inquiry.base_package,
            'staff_assigned': inquiry.staff_assigned,
        }
        if inquiry.custom_package:
            initial['custom_package'] = inquiry.custom_package

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            if inquiry:
                inquiry.status = 'converted'
                inquiry.save(update_fields=['status'])
            from .booking_emails import send_booking_confirmation
            send_booking_confirmation(booking)
            messages.success(request, f"Booking {booking.booking_reference} created.")
            return redirect('packages:dashboard_booking_detail', pk=booking.pk)
    else:
        form = BookingForm(initial=initial)

    return render(request, 'packages/bookings/dashboard/form.html', {
        'form': form,
        'inquiry': inquiry,
        'title': 'Create Booking',
    })


@login_required
@staff_member_required
def dashboard_booking_detail(request, pk):
    booking = get_object_or_404(
        Booking.objects.select_related('package', 'inquiry', 'custom_package', 'staff_assigned')
                       .prefetch_related('passengers', 'payments'),
        pk=pk,
    )
    passenger_form = PassengerForm()
    payment_form = PaymentForm()
    return render(request, 'packages/bookings/dashboard/detail.html', {
        'booking': booking,
        'passenger_form': passenger_form,
        'payment_form': payment_form,
    })


@login_required
@staff_member_required
def dashboard_booking_edit(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    old_status = booking.status
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save()
            if booking.status != old_status:
                from .booking_emails import send_booking_status_update
                send_booking_status_update(booking, old_status)
            messages.success(request, "Booking updated.")
            return redirect('packages:dashboard_booking_detail', pk=booking.pk)
    else:
        form = BookingForm(instance=booking)
    return render(request, 'packages/bookings/dashboard/form.html', {
        'form': form,
        'booking': booking,
        'title': 'Edit Booking',
    })


@login_required
@staff_member_required
def dashboard_booking_cancel(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        old_status = booking.status
        booking.cancel()
        from .booking_emails import send_booking_status_update
        send_booking_status_update(booking, old_status)
        messages.success(request, f"Booking {booking.booking_reference} cancelled.")
        return redirect('packages:dashboard_booking_list')
    return render(request, 'packages/bookings/dashboard/cancel_confirm.html', {'booking': booking})


@login_required
@staff_member_required
def dashboard_passenger_add(request, booking_pk):
    booking = get_object_or_404(Booking, pk=booking_pk)
    if request.method == 'POST':
        form = PassengerForm(request.POST)
        if form.is_valid():
            passenger = form.save(commit=False)
            passenger.booking = booking
            if passenger.is_lead_passenger:
                booking.passengers.filter(is_lead_passenger=True).update(is_lead_passenger=False)
            passenger.save()
            messages.success(request, f"Passenger {passenger.full_name} added.")
        else:
            messages.error(request, "Please fix the errors below.")
    return redirect('packages:dashboard_booking_detail', pk=booking_pk)


@login_required
@staff_member_required
def dashboard_passenger_edit(request, pk):
    passenger = get_object_or_404(Passenger, pk=pk)
    booking = passenger.booking
    if request.method == 'POST':
        form = PassengerForm(request.POST, instance=passenger)
        if form.is_valid():
            updated = form.save(commit=False)
            if updated.is_lead_passenger:
                booking.passengers.exclude(pk=pk).filter(
                    is_lead_passenger=True
                ).update(is_lead_passenger=False)
            updated.save()
            messages.success(request, "Passenger updated.")
            return redirect('packages:dashboard_booking_detail', pk=booking.pk)
    else:
        form = PassengerForm(instance=passenger)
    return render(request, 'packages/bookings/dashboard/passenger_form.html', {
        'form': form, 'passenger': passenger, 'booking': booking,
    })


@login_required
@staff_member_required
def dashboard_passenger_delete(request, pk):
    passenger = get_object_or_404(Passenger, pk=pk)
    booking_pk = passenger.booking.pk
    if request.method == 'POST':
        name = passenger.full_name
        passenger.delete()
        messages.success(request, f"Passenger {name} removed.")
    return redirect('packages:dashboard_booking_detail', pk=booking_pk)


@login_required
@staff_member_required
def dashboard_payment_record(request, booking_pk):
    booking = get_object_or_404(Booking, pk=booking_pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.recorded_by = request.user
            payment.save()
            if booking.is_fully_paid and booking.status == 'deposit_paid':
                booking.status = 'confirmed'
                booking.save(update_fields=['status'])
                from .booking_emails import send_booking_status_update
                send_booking_status_update(booking, 'deposit_paid')
            elif payment.payment_type == 'deposit' and booking.status == 'pending_deposit':
                booking.status = 'deposit_paid'
                booking.save(update_fields=['status'])
            from .booking_emails import send_payment_received
            send_payment_received(booking, payment)
            messages.success(request, f"Payment of {payment.currency} {payment.amount} recorded.")
        else:
            messages.error(request, "Please fix the errors below.")
    return redirect('packages:dashboard_booking_detail', pk=booking_pk)


@login_required
@staff_member_required
def dashboard_payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    booking_pk = payment.booking.pk
    if request.method == 'POST':
        payment.delete()
        messages.success(request, "Payment record deleted.")
    return redirect('packages:dashboard_booking_detail', pk=booking_pk)


# ============================================================================
# DEPARTURE / AVAILABILITY CALENDAR VIEWS
# ============================================================================

@login_required
@staff_member_required
def dashboard_departure_list(request, package_pk):
    package = get_object_or_404(Package, pk=package_pk)
    departures = package.departures.all()
    return render(request, 'packages/departures/dashboard/list.html', {
        'package': package,
        'departures': departures,
    })


@login_required
@staff_member_required
def dashboard_departure_create(request, package_pk):
    package = get_object_or_404(Package, pk=package_pk)
    if request.method == 'POST':
        form = DepartureForm(request.POST)
        if form.is_valid():
            departure = form.save(commit=False)
            departure.package = package
            departure.save()
            messages.success(request, f"Departure on {departure.departure_date} added.")
            return redirect('packages:dashboard_departure_list', package_pk=package.pk)
    else:
        form = DepartureForm()
    return render(request, 'packages/departures/dashboard/form.html', {
        'form': form, 'package': package, 'title': 'Add Departure',
    })


@login_required
@staff_member_required
def dashboard_departure_edit(request, pk):
    departure = get_object_or_404(Departure, pk=pk)
    package = departure.package
    if request.method == 'POST':
        form = DepartureForm(request.POST, instance=departure)
        if form.is_valid():
            form.save()
            messages.success(request, "Departure updated.")
            return redirect('packages:dashboard_departure_list', package_pk=package.pk)
    else:
        form = DepartureForm(instance=departure)
    return render(request, 'packages/departures/dashboard/form.html', {
        'form': form, 'package': package, 'departure': departure, 'title': 'Edit Departure',
    })


@login_required
@staff_member_required
def dashboard_departure_delete(request, pk):
    departure = get_object_or_404(Departure, pk=pk)
    package = departure.package
    if request.method == 'POST':
        if departure.booked_seats > 0:
            messages.error(request, "Cannot delete a departure that has confirmed bookings.")
            return redirect('packages:dashboard_departure_list', package_pk=package.pk)
        departure.delete()
        messages.success(request, "Departure removed.")
        return redirect('packages:dashboard_departure_list', package_pk=package.pk)
    return render(request, 'packages/departures/dashboard/delete_confirm.html', {
        'departure': departure, 'package': package,
    })

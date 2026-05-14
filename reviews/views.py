import logging
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render

from packages.models import Booking, Package
from .forms import ReviewSubmitForm
from .models import Review

logger = logging.getLogger(__name__)


# ============================================================================
# PUBLIC VIEWS
# ============================================================================

def public_review_list(request, package_slug):
    package = get_object_or_404(Package, slug=package_slug, is_active=True)
    reviews = Review.objects.filter(
        package=package, is_approved=True
    ).select_related('author').prefetch_related('photos')

    rating_filter = request.GET.get('rating', '')
    if rating_filter:
        reviews = reviews.filter(rating=rating_filter)

    sort = request.GET.get('sort', '-created_at')
    if sort in ['rating', '-rating', '-created_at', 'created_at']:
        reviews = reviews.order_by(sort)

    stats = {
        'count': package.review_count,
        'average': package.rating_average,
        'breakdown': {
            i: Review.objects.filter(package=package, is_approved=True, rating=i).count()
            for i in range(5, 0, -1)
        },
    }

    paginator = Paginator(reviews, 10)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'reviews/public/list.html', {
        'package': package,
        'page_obj': page,
        'stats': stats,
        'rating_filter': rating_filter,
        'sort': sort,
    })


def review_submit(request, package_slug):
    package = get_object_or_404(Package, slug=package_slug, is_active=True)

    # Check eligibility: must have a completed booking for this package
    eligible_booking = None
    if request.user.is_authenticated:
        eligible_booking = (
            Booking.objects.filter(
                package=package,
                status='completed',
                inquiry__customer_email=request.user.email,
            )
            .exclude(review__isnull=False)
            .first()
        )

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to leave a review.')
            return redirect('packages:public_package_detail', slug=package_slug)

        form = ReviewSubmitForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.package = package
            review.author = request.user
            review.booking = eligible_booking
            if not review.reviewer_name:
                review.reviewer_name = request.user.get_full_name() or request.user.username
            review.save()
            messages.success(request, 'Thank you! Your review has been submitted for moderation.')
            return redirect('packages:public_package_detail', slug=package_slug)
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['reviewer_name'] = request.user.get_full_name() or request.user.username
        form = ReviewSubmitForm(initial=initial)

    return render(request, 'reviews/public/submit.html', {
        'package': package,
        'form': form,
        'eligible_booking': eligible_booking,
    })


# ============================================================================
# DASHBOARD VIEWS (Staff)
# ============================================================================

@login_required
@staff_member_required
def dashboard_review_list(request):
    status_filter = request.GET.get('status', 'pending')
    reviews = Review.objects.select_related('package', 'author').all()
    if status_filter:
        reviews = reviews.filter(status=status_filter)

    paginator = Paginator(reviews, 25)
    page = paginator.get_page(request.GET.get('page'))

    counts = {
        'pending': Review.objects.filter(status='pending').count(),
        'approved': Review.objects.filter(status='approved').count(),
        'rejected': Review.objects.filter(status='rejected').count(),
        'total': Review.objects.count(),
    }

    return render(request, 'reviews/dashboard/list.html', {
        'page_obj': page,
        'status_filter': status_filter,
        'counts': counts,
        'status_choices': Review.STATUS_CHOICES,
    })


@login_required
@staff_member_required
def dashboard_review_detail(request, pk):
    review = get_object_or_404(
        Review.objects.select_related('package', 'author', 'booking', 'approved_by')
                      .prefetch_related('photos'),
        pk=pk,
    )
    return render(request, 'reviews/dashboard/detail.html', {'review': review})


@login_required
@staff_member_required
def dashboard_review_approve(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.approve(request.user)
        messages.success(request, f'Review approved and published.')
        return redirect('reviews:dashboard_review_list')
    return render(request, 'reviews/dashboard/approve_confirm.html', {'review': review})


@login_required
@staff_member_required
def dashboard_review_reject(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        review.reject(reason)
        messages.success(request, 'Review rejected.')
        return redirect('reviews:dashboard_review_list')
    return render(request, 'reviews/dashboard/reject_confirm.html', {'review': review})


@login_required
@staff_member_required
def dashboard_review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        package = review.package
        review.delete()
        package.update_rating()
        messages.success(request, 'Review deleted.')
        return redirect('reviews:dashboard_review_list')
    return render(request, 'reviews/dashboard/delete_confirm.html', {'review': review})

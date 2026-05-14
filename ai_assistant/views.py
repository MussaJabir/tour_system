import logging

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from packages.models import BookingInquiry

from .forms import BrochureUploadForm, ItineraryGenerateForm, RouteOptimizeForm
from .models import (
    AIConfiguration,
    BrochureParseJob,
    ItineraryGenerationJob,
    QuoteSuggestionJob,
    RouteOptimizationJob,
)
from .tasks import (
    build_custom_quote_task,
    generate_itinerary_task,
    optimize_route_task,
    parse_brochure_task,
)

logger = logging.getLogger(__name__)


@login_required
@staff_member_required
def dashboard_ai_home(request):
    config = AIConfiguration.get_active()
    context = {
        'config': config,
        'recent_brochure': BrochureParseJob.objects.select_related('created_by').first(),
        'recent_itinerary': ItineraryGenerationJob.objects.select_related('created_by').first(),
        'recent_quote': QuoteSuggestionJob.objects.select_related('created_by').first(),
        'recent_route': RouteOptimizationJob.objects.select_related('created_by').first(),
        'brochure_count': BrochureParseJob.objects.count(),
        'itinerary_count': ItineraryGenerationJob.objects.count(),
        'quote_count': QuoteSuggestionJob.objects.count(),
        'route_count': RouteOptimizationJob.objects.count(),
    }
    return render(request, 'ai_assistant/dashboard/home.html', context)


# ── Brochure Parser ─────────────────────────────────────────────────────────

@login_required
@staff_member_required
def brochure_upload(request):
    if request.method == 'POST':
        form = BrochureUploadForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()
            parse_brochure_task.delay(job.pk)
            messages.success(request, 'PDF uploaded — AI is parsing it now.')
            return redirect('ai_assistant:brochure_result', pk=job.pk)
    else:
        form = BrochureUploadForm()
    return render(request, 'ai_assistant/dashboard/brochure_upload.html', {'form': form})


@login_required
@staff_member_required
def brochure_result(request, pk: int):
    job = get_object_or_404(BrochureParseJob, pk=pk)
    return render(request, 'ai_assistant/dashboard/brochure_result.html', {'job': job})


# ── Itinerary Generator ──────────────────────────────────────────────────────

@login_required
@staff_member_required
def itinerary_generate(request):
    if request.method == 'POST':
        form = ItineraryGenerateForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()
            generate_itinerary_task.delay(job.pk)
            messages.success(request, 'Itinerary generation started.')
            return redirect('ai_assistant:itinerary_result', pk=job.pk)
    else:
        form = ItineraryGenerateForm()
    return render(request, 'ai_assistant/dashboard/itinerary_form.html', {'form': form})


@login_required
@staff_member_required
def itinerary_result(request, pk: int):
    job = get_object_or_404(ItineraryGenerationJob, pk=pk)
    return render(request, 'ai_assistant/dashboard/itinerary_result.html', {'job': job})


# ── Quote Builder ────────────────────────────────────────────────────────────

@login_required
@staff_member_required
def quote_from_inquiry(request, inquiry_pk: int):
    inquiry = get_object_or_404(BookingInquiry, pk=inquiry_pk)
    existing = inquiry.quote_jobs.filter(status__in=['pending', 'processing', 'done']).first()
    if existing:
        return redirect('ai_assistant:quote_result', pk=existing.pk)
    job = QuoteSuggestionJob.objects.create(inquiry=inquiry, created_by=request.user)
    build_custom_quote_task.delay(job.pk)
    messages.success(request, 'AI quote suggestion started.')
    return redirect('ai_assistant:quote_result', pk=job.pk)


@login_required
@staff_member_required
def quote_result(request, pk: int):
    job = get_object_or_404(QuoteSuggestionJob.objects.select_related('inquiry'), pk=pk)
    return render(request, 'ai_assistant/dashboard/quote_result.html', {'job': job})


# ── Route Optimizer ──────────────────────────────────────────────────────────

@login_required
@staff_member_required
def route_optimize(request):
    if request.method == 'POST':
        form = RouteOptimizeForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()
            optimize_route_task.delay(job.pk)
            messages.success(request, 'Route optimization started.')
            return redirect('ai_assistant:route_result', pk=job.pk)
    else:
        form = RouteOptimizeForm()
    return render(request, 'ai_assistant/dashboard/route_form.html', {'form': form})


@login_required
@staff_member_required
def route_result(request, pk: int):
    job = get_object_or_404(RouteOptimizationJob, pk=pk)
    return render(request, 'ai_assistant/dashboard/route_result.html', {'job': job})

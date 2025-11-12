"""
Core App - Views

Views for:
- Contact form (public + dashboard)
- Newsletter subscription (public + dashboard)
- FAQs (public + dashboard)
- Testimonials (dashboard)
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Count
from django.utils import timezone

from .models import ContactMessage, NewsletterSubscriber, FAQ, Testimonial
from .forms import (
    ContactForm, 
    NewsletterSubscriptionForm, 
    ContactMessageReplyForm,
    ContactMessageNotesForm,
    FAQForm,
    TestimonialForm
)


# ==================== PUBLIC VIEWS ====================

def contact_page(request):
    """
    Public contact page.
    
    CRITICAL: This is your LEAD CAPTURE page!
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save contact message
            contact_msg = form.save(commit=False)
            
            # Get IP address for tracking
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                contact_msg.ip_address = x_forwarded_for.split(',')[0]
            else:
                contact_msg.ip_address = request.META.get('REMOTE_ADDR')
            
            contact_msg.save()
            
            # Send notification email to admin
            try:
                send_contact_notification(contact_msg)
            except Exception as e:
                # Log error but don't fail the submission
                print(f"Error sending notification email: {e}")
            
            # Success message
            messages.success(
                request,
                '✅ Thank you for contacting us! We\'ll get back to you within 24 hours.'
            )
            return redirect('contact_page')
        else:
            messages.error(
                request,
                '❌ Please correct the errors below.'
            )
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'page_title': 'Contact Us',
    }
    return render(request, 'core/public/contact.html', context)


@require_http_methods(["POST"])
def newsletter_subscribe(request):
    """
    Newsletter subscription (AJAX endpoint).
    
    Can be called from anywhere (footer, popup, etc.)
    """
    form = NewsletterSubscriptionForm(request.POST)
    
    if form.is_valid():
        # Save subscriber
        subscriber = form.save(commit=False)
        
        # Get IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            subscriber.ip_address = x_forwarded_for.split(',')[0]
        else:
            subscriber.ip_address = request.META.get('REMOTE_ADDR')
        
        subscriber.save()
        
        # Send welcome email
        try:
            send_newsletter_welcome_email(subscriber)
        except Exception as e:
            print(f"Error sending welcome email: {e}")
        
        return JsonResponse({
            'success': True,
            'message': '🎉 Success! Check your email to confirm your subscription.'
        })
    else:
        errors = []
        for field, error_list in form.errors.items():
            for error in error_list:
                errors.append(error)
        
        return JsonResponse({
            'success': False,
            'errors': errors
        }, status=400)


def newsletter_unsubscribe(request, token):
    """
    Unsubscribe from newsletter.
    
    Token-based so users can unsubscribe without logging in.
    """
    # Simple token: base64 encoded email
    import base64
    try:
        email = base64.b64decode(token).decode('utf-8')
        subscriber = NewsletterSubscriber.objects.get(email=email)
        
        if request.method == 'POST':
            subscriber.is_active = False
            subscriber.unsubscribed_at = timezone.now()
            subscriber.save()
            
            messages.success(
                request,
                '✅ You have been unsubscribed. We\'re sorry to see you go!'
            )
            return redirect('public_home')
        
        context = {
            'subscriber': subscriber,
        }
        return render(request, 'core/public/unsubscribe.html', context)
        
    except Exception as e:
        messages.error(request, '❌ Invalid unsubscribe link.')
        return redirect('public_home')


def faq_page(request):
    """
    Public FAQ page.
    
    SAVE TIME: Answer common questions automatically!
    """
    # Get category from query params
    category = request.GET.get('category', '')
    
    # Filter active FAQs
    faqs = FAQ.objects.filter(is_active=True)
    
    if category:
        faqs = faqs.filter(category=category)
    
    # Order by featured first, then by order
    faqs = faqs.order_by('-is_featured', 'order', 'created_at')
    
    # Get all categories with counts
    categories = FAQ.objects.filter(is_active=True).values('category').annotate(
        count=Count('id')
    ).order_by('category')
    
    context = {
        'faqs': faqs,
        'categories': categories,
        'selected_category': category,
        'page_title': 'Frequently Asked Questions',
    }
    return render(request, 'core/public/faq.html', context)


# ==================== DASHBOARD VIEWS - CONTACT MESSAGES ====================

@login_required
def dashboard_contact_list(request):
    """
    Dashboard: List all contact messages.
    
    YOUR LEADS INBOX!
    """
    # Get filter parameters
    status_filter = request.GET.get('status', '')
    search = request.GET.get('search', '')
    
    # Base queryset
    messages_list = ContactMessage.objects.all()
    
    # Apply filters
    if status_filter:
        messages_list = messages_list.filter(status=status_filter)
    
    if search:
        messages_list = messages_list.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(subject__icontains=search) |
            Q(message__icontains=search)
        )
    
    # Order by newest first
    messages_list = messages_list.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(messages_list, 25)
    page = request.GET.get('page', 1)
    messages_page = paginator.get_page(page)
    
    # Get counts for badges
    counts = {
        'new': ContactMessage.objects.filter(status='new').count(),
        'read': ContactMessage.objects.filter(status='read').count(),
        'replied': ContactMessage.objects.filter(status='replied').count(),
        'archived': ContactMessage.objects.filter(status='archived').count(),
        'total': ContactMessage.objects.count(),
    }
    
    context = {
        'messages': messages_page,
        'counts': counts,
        'status_filter': status_filter,
        'search': search,
        'page_title': 'Contact Messages',
    }
    return render(request, 'core/dashboard/contact_list.html', context)


@login_required
def dashboard_contact_detail(request, pk):
    """
    Dashboard: View and reply to a single contact message.
    
    YOUR LEAD DETAILS!
    """
    contact_msg = get_object_or_404(ContactMessage, pk=pk)
    
    # Mark as read if it's new
    if contact_msg.status == 'new':
        contact_msg.status = 'read'
        contact_msg.save(update_fields=['status'])
    
    # Handle reply form
    reply_form = ContactMessageReplyForm()
    notes_form = ContactMessageNotesForm(instance=contact_msg)
    
    if request.method == 'POST':
        if 'send_reply' in request.POST:
            reply_form = ContactMessageReplyForm(request.POST)
            if reply_form.is_valid():
                reply_message = reply_form.cleaned_data['reply_message']
                
                # Send reply email
                try:
                    send_contact_reply_email(contact_msg, reply_message)
                    
                    # Mark as replied if checkbox is checked
                    if reply_form.cleaned_data['mark_as_replied']:
                        contact_msg.status = 'replied'
                        contact_msg.save(update_fields=['status'])
                    
                    messages.success(request, '✅ Reply sent successfully!')
                    return redirect('dashboard_contact_detail', pk=pk)
                except Exception as e:
                    messages.error(request, f'❌ Error sending email: {str(e)}')
        
        elif 'save_notes' in request.POST:
            notes_form = ContactMessageNotesForm(request.POST, instance=contact_msg)
            if notes_form.is_valid():
                notes_form.save()
                messages.success(request, '✅ Notes saved successfully!')
                return redirect('dashboard_contact_detail', pk=pk)
    
    context = {
        'contact_msg': contact_msg,
        'reply_form': reply_form,
        'notes_form': notes_form,
        'page_title': f'Contact Message: {contact_msg.name}',
    }
    return render(request, 'core/dashboard/contact_detail.html', context)


@login_required
@require_http_methods(["POST"])
def dashboard_contact_delete(request, pk):
    """
    Dashboard: Delete a contact message.
    """
    contact_msg = get_object_or_404(ContactMessage, pk=pk)
    contact_msg.delete()
    messages.success(request, '✅ Contact message deleted.')
    return redirect('dashboard_contact_list')


# ==================== DASHBOARD VIEWS - NEWSLETTER ====================

@login_required
def dashboard_newsletter_list(request):
    """
    Dashboard: List all newsletter subscribers.
    
    YOUR EMAIL LIST!
    """
    # Get filter parameters
    status_filter = request.GET.get('status', 'active')
    search = request.GET.get('search', '')
    
    # Base queryset
    subscribers_list = NewsletterSubscriber.objects.all()
    
    # Apply filters
    if status_filter == 'active':
        subscribers_list = subscribers_list.filter(is_active=True)
    elif status_filter == 'inactive':
        subscribers_list = subscribers_list.filter(is_active=False)
    
    if search:
        subscribers_list = subscribers_list.filter(
            Q(email__icontains=search) |
            Q(name__icontains=search)
        )
    
    # Order by newest first
    subscribers_list = subscribers_list.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(subscribers_list, 50)
    page = request.GET.get('page', 1)
    subscribers_page = paginator.get_page(page)
    
    # Get counts
    counts = {
        'active': NewsletterSubscriber.objects.filter(is_active=True).count(),
        'inactive': NewsletterSubscriber.objects.filter(is_active=False).count(),
        'total': NewsletterSubscriber.objects.count(),
    }
    
    context = {
        'subscribers': subscribers_page,
        'counts': counts,
        'status_filter': status_filter,
        'search': search,
        'page_title': 'Newsletter Subscribers',
    }
    return render(request, 'core/dashboard/newsletter_list.html', context)


@login_required
def dashboard_newsletter_export(request):
    """
    Dashboard: Export newsletter subscribers to CSV.
    
    DOWNLOAD YOUR EMAIL LIST!
    """
    import csv
    from django.http import HttpResponse
    
    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="newsletter_subscribers.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Email', 'Name', 'Status', 'Subscribed Date'])
    
    # Get active subscribers
    subscribers = NewsletterSubscriber.objects.filter(is_active=True).order_by('-created_at')
    
    for subscriber in subscribers:
        writer.writerow([
            subscriber.email,
            subscriber.name or '',
            'Active' if subscriber.is_active else 'Inactive',
            subscriber.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        ])
    
    return response


# ==================== EMAIL FUNCTIONS ====================

def send_contact_notification(contact_msg):
    """
    Send email notification to admin when someone submits contact form.
    
    ALERT: NEW LEAD!
    """
    subject = f'🔔 New Contact Message: {contact_msg.subject}'
    message = f"""
New contact form submission!

From: {contact_msg.name}
Email: {contact_msg.email}
Phone: {contact_msg.phone or 'Not provided'}
Subject: {contact_msg.subject}

Message:
{contact_msg.message}

---
View in dashboard: {settings.ALLOWED_HOSTS[0]}/dashboard/contacts/{contact_msg.id}/

Reply ASAP - This is a potential customer! 💰
    """
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.DEFAULT_FROM_EMAIL],  # Send to yourself
        fail_silently=False,
    )


def send_contact_reply_email(contact_msg, reply_message):
    """
    Send reply email to customer who submitted contact form.
    """
    subject = f'Re: {contact_msg.subject}'
    message = f"""
Hi {contact_msg.name},

Thank you for contacting us! Here's our response:

{reply_message}

---
Best regards,
Tour Management Team

If you have any other questions, feel free to reply to this email.
    """
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[contact_msg.email],
        fail_silently=False,
    )


def send_newsletter_welcome_email(subscriber):
    """
    Send welcome email to new newsletter subscriber.
    """
    import base64
    
    # Generate unsubscribe token
    token = base64.b64encode(subscriber.email.encode()).decode()
    unsubscribe_url = f"{settings.ALLOWED_HOSTS[0]}/newsletter/unsubscribe/{token}/"
    
    subject = '🎉 Welcome to Our Newsletter!'
    message = f"""
Hi {subscriber.name or 'there'}!

Thank you for subscribing to our newsletter!

You'll now receive:
✓ Exclusive travel deals
✓ New destination announcements
✓ Travel tips and guides
✓ Special promotions

We promise not to spam you - only the good stuff! 🌍✈️

---
To unsubscribe at any time, click here: {unsubscribe_url}
    """
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[subscriber.email],
        fail_silently=False,
    )


# ==================== DASHBOARD VIEWS - FAQ ====================

@login_required
def dashboard_faq_list(request):
    """
    Dashboard: List all FAQs with filtering.
    """
    # Get filter parameters
    category_filter = request.GET.get('category', '')
    status_filter = request.GET.get('status', '')
    search = request.GET.get('search', '')
    
    # Base queryset
    faqs = FAQ.objects.all()
    
    # Apply filters
    if category_filter:
        faqs = faqs.filter(category=category_filter)
    
    if status_filter == 'active':
        faqs = faqs.filter(is_active=True)
    elif status_filter == 'draft':
        faqs = faqs.filter(is_active=False)
    
    if search:
        faqs = faqs.filter(
            Q(question__icontains=search) |
            Q(answer__icontains=search)
        )
    
    # Order by featured first, then by order
    faqs = faqs.order_by('-is_featured', 'order', '-created_at')
    
    # Pagination
    paginator = Paginator(faqs, 20)
    page = request.GET.get('page', 1)
    faqs_page = paginator.get_page(page)
    
    # Get counts
    counts = {
        'active': FAQ.objects.filter(is_active=True).count(),
        'draft': FAQ.objects.filter(is_active=False).count(),
        'featured': FAQ.objects.filter(is_featured=True).count(),
        'total': FAQ.objects.count(),
    }
    
    # Get all categories
    categories = FAQ.objects.values_list('category', flat=True).distinct()
    
    context = {
        'faqs': faqs_page,
        'counts': counts,
        'categories': categories,
        'category_filter': category_filter,
        'status_filter': status_filter,
        'search': search,
        'page_title': 'FAQs Management',
    }
    return render(request, 'core/dashboard/faq_list.html', context)


@login_required
def dashboard_faq_create(request):
    """
    Dashboard: Create a new FAQ.
    """
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            faq = form.save(commit=False)
            faq.created_by = request.user
            faq.save()
            messages.success(request, '✅ FAQ created successfully!')
            return redirect('dashboard_faq_list')
        else:
            messages.error(request, '❌ Please correct the errors below.')
    else:
        form = FAQForm()
    
    context = {
        'form': form,
        'page_title': 'Create FAQ',
        'form_action': 'Create',
    }
    return render(request, 'core/dashboard/faq_form.html', context)


@login_required
def dashboard_faq_edit(request, pk):
    """
    Dashboard: Edit an existing FAQ.
    """
    faq = get_object_or_404(FAQ, pk=pk)
    
    if request.method == 'POST':
        form = FAQForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ FAQ updated successfully!')
            return redirect('dashboard_faq_list')
        else:
            messages.error(request, '❌ Please correct the errors below.')
    else:
        form = FAQForm(instance=faq)
    
    context = {
        'form': form,
        'faq': faq,
        'page_title': f'Edit FAQ: {faq.question[:50]}',
        'form_action': 'Update',
    }
    return render(request, 'core/dashboard/faq_form.html', context)


@login_required
@require_http_methods(["POST"])
def dashboard_faq_delete(request, pk):
    """
    Dashboard: Delete an FAQ.
    """
    faq = get_object_or_404(FAQ, pk=pk)
    faq.delete()
    messages.success(request, '✅ FAQ deleted successfully.')
    return redirect('dashboard_faq_list')


# ==================== DASHBOARD VIEWS - TESTIMONIALS ====================

@login_required
def dashboard_testimonial_list(request):
    """
    Dashboard: List all testimonials with filtering.
    """
    # Get filter parameters
    rating_filter = request.GET.get('rating', '')
    status_filter = request.GET.get('status', '')
    search = request.GET.get('search', '')
    
    # Base queryset
    testimonials = Testimonial.objects.all()
    
    # Apply filters
    if rating_filter:
        testimonials = testimonials.filter(rating=rating_filter)
    
    if status_filter == 'active':
        testimonials = testimonials.filter(is_active=True)
    elif status_filter == 'draft':
        testimonials = testimonials.filter(is_active=False)
    
    if search:
        testimonials = testimonials.filter(
            Q(customer_name__icontains=search) |
            Q(customer_location__icontains=search) |
            Q(quote__icontains=search)
        )
    
    # Order by featured first, then by order
    testimonials = testimonials.order_by('-is_featured', 'order', '-created_at')
    
    # Pagination
    paginator = Paginator(testimonials, 20)
    page = request.GET.get('page', 1)
    testimonials_page = paginator.get_page(page)
    
    # Get counts
    counts = {
        'active': Testimonial.objects.filter(is_active=True).count(),
        'draft': Testimonial.objects.filter(is_active=False).count(),
        'featured': Testimonial.objects.filter(is_featured=True).count(),
        'total': Testimonial.objects.count(),
    }
    
    context = {
        'testimonials': testimonials_page,
        'counts': counts,
        'rating_filter': rating_filter,
        'status_filter': status_filter,
        'search': search,
        'page_title': 'Testimonials Management',
    }
    return render(request, 'core/dashboard/testimonial_list.html', context)


@login_required
def dashboard_testimonial_create(request):
    """
    Dashboard: Create a new testimonial.
    """
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.created_by = request.user
            testimonial.save()
            messages.success(request, '✅ Testimonial created successfully!')
            return redirect('dashboard_testimonial_list')
        else:
            messages.error(request, '❌ Please correct the errors below.')
    else:
        form = TestimonialForm()
    
    context = {
        'form': form,
        'page_title': 'Create Testimonial',
        'form_action': 'Create',
    }
    return render(request, 'core/dashboard/testimonial_form.html', context)


@login_required
def dashboard_testimonial_edit(request, pk):
    """
    Dashboard: Edit an existing testimonial.
    """
    testimonial = get_object_or_404(Testimonial, pk=pk)
    
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Testimonial updated successfully!')
            return redirect('dashboard_testimonial_list')
        else:
            messages.error(request, '❌ Please correct the errors below.')
    else:
        form = TestimonialForm(instance=testimonial)
    
    context = {
        'form': form,
        'testimonial': testimonial,
        'page_title': f'Edit Testimonial: {testimonial.customer_name}',
        'form_action': 'Update',
    }
    return render(request, 'core/dashboard/testimonial_form.html', context)


@login_required
@require_http_methods(["POST"])
def dashboard_testimonial_delete(request, pk):
    """
    Dashboard: Delete a testimonial.
    """
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if testimonial.customer_image:
        testimonial.customer_image.delete()  # Delete the image file
    testimonial.delete()
    messages.success(request, '✅ Testimonial deleted successfully.')
    return redirect('dashboard_testimonial_list')

"""
Email notification utilities for the packages app.
Handles sending emails for inquiries, custom packages, and client actions.
"""

import logging

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


def send_inquiry_confirmation_email(inquiry):
    """
    Send confirmation email to customer after they submit an inquiry.
    
    Args:
        inquiry: BookingInquiry instance
    """
    subject = f'Inquiry Received - {inquiry.reference}'
    
    # Render HTML template
    html_content = render_to_string('packages/emails/inquiry_confirmation.html', {
        'inquiry': inquiry,
        'site_name': getattr(settings, 'SITE_NAME', 'Tour System'),
    })
    
    # Create plain text version
    text_content = strip_tags(html_content)
    
    # Create email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[inquiry.email]
    )
    
    # Attach HTML version
    email.attach_alternative(html_content, "text/html")
    
    # Send email
    try:
        email.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Error sending inquiry confirmation email: {e}")
        return False


def send_inquiry_notification_to_staff(inquiry):
    """
    Send notification to staff when a new inquiry is submitted.
    
    Args:
        inquiry: BookingInquiry instance
    """
    # Get staff email addresses
    staff_emails = getattr(settings, 'STAFF_NOTIFICATION_EMAILS', [])
    
    if not staff_emails:
        # Fallback to superusers
        from django.contrib.auth import get_user_model
        User = get_user_model()
        staff_emails = list(User.objects.filter(is_staff=True, is_active=True).values_list('email', flat=True))
    
    if not staff_emails:
        print("No staff emails configured for notifications")
        return False
    
    subject = f'New Inquiry: {inquiry.reference} - {inquiry.full_name}'
    
    # Render HTML template
    html_content = render_to_string('packages/emails/inquiry_staff_notification.html', {
        'inquiry': inquiry,
        'site_name': getattr(settings, 'SITE_NAME', 'Tour System'),
        'dashboard_url': f"{settings.SITE_URL}/dashboard/inquiries/{inquiry.pk}/"
    })
    
    # Create plain text version
    text_content = strip_tags(html_content)
    
    # Create email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=staff_emails
    )
    
    # Attach HTML version
    email.attach_alternative(html_content, "text/html")
    
    # Send email
    try:
        email.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Error sending staff notification email: {e}")
        return False


def send_custom_package_to_client(custom_package):
    """
    Send custom package details to client with secure viewing link.
    
    Args:
        custom_package: CustomPackage instance
    """
    subject = f'Your Custom Package Quote - {custom_package.inquiry.reference}'
    
    # Generate secure viewing URL
    view_url = f"{settings.SITE_URL}/packages/custom/{custom_package.token}/"
    
    # Render HTML template
    html_content = render_to_string('packages/emails/custom_package_client.html', {
        'custom_package': custom_package,
        'inquiry': custom_package.inquiry,
        'view_url': view_url,
        'site_name': getattr(settings, 'SITE_NAME', 'Tour System'),
    })
    
    # Create plain text version
    text_content = strip_tags(html_content)
    
    # Create email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[custom_package.inquiry.email]
    )
    
    # Attach HTML version
    email.attach_alternative(html_content, "text/html")
    
    # Send email
    try:
        email.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Error sending custom package email: {e}")
        return False


def send_client_action_notification_to_staff(custom_package, action):
    """
    Send notification to staff when client takes action on custom package.
    
    Args:
        custom_package: CustomPackage instance
        action: str - 'approved', 'declined', or 'requested_changes'
    """
    # Get staff email addresses
    staff_emails = getattr(settings, 'STAFF_NOTIFICATION_EMAILS', [])
    
    if not staff_emails:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        staff_emails = list(User.objects.filter(is_staff=True, is_active=True).values_list('email', flat=True))
    
    if not staff_emails:
        print("No staff emails configured for notifications")
        return False
    
    action_labels = {
        'approved': 'Approved',
        'declined': 'Declined',
        'requested_changes': 'Requested Changes'
    }
    
    subject = f'Client Action: {action_labels.get(action, action)} - {custom_package.inquiry.reference}'
    
    # Render HTML template
    html_content = render_to_string('packages/emails/client_action_staff_notification.html', {
        'custom_package': custom_package,
        'inquiry': custom_package.inquiry,
        'action': action,
        'action_label': action_labels.get(action, action),
        'site_name': getattr(settings, 'SITE_NAME', 'Tour System'),
        'dashboard_url': f"{settings.SITE_URL}/dashboard/custom-packages/{custom_package.pk}/"
    })
    
    # Create plain text version
    text_content = strip_tags(html_content)
    
    # Create email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=staff_emails
    )
    
    # Attach HTML version
    email.attach_alternative(html_content, "text/html")
    
    # Send email
    try:
        email.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Error sending client action notification: {e}")
        return False


def send_custom_package_expiry_reminder(custom_package):
    """
    Send reminder email to client when custom package is about to expire.
    
    Args:
        custom_package: CustomPackage instance
    """
    subject = f'Reminder: Your Package Quote Expires Soon - {custom_package.inquiry.reference}'
    
    # Generate secure viewing URL
    view_url = f"{settings.SITE_URL}/packages/custom/{custom_package.token}/"
    
    # Render HTML template
    html_content = render_to_string('packages/emails/custom_package_expiry_reminder.html', {
        'custom_package': custom_package,
        'inquiry': custom_package.inquiry,
        'view_url': view_url,
        'site_name': getattr(settings, 'SITE_NAME', 'Tour System'),
    })
    
    # Create plain text version
    text_content = strip_tags(html_content)
    
    # Create email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[custom_package.inquiry.email]
    )
    
    # Attach HTML version
    email.attach_alternative(html_content, "text/html")
    
    # Send email
    try:
        email.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Error sending expiry reminder email: {e}")
        return False



def send_invoice_email(invoice):
    """
    Email an invoice PDF to the customer.

    Returns True on success, False if there is no recipient or sending fails.
    """
    to_email = invoice.customer_email or (
        invoice.booking.inquiry.customer_email if invoice.booking.inquiry_id else ''
    )
    if not to_email:
        logger.warning("No recipient email for invoice %s", invoice.invoice_number)
        return False

    from .pdf import render_invoice_pdf

    site_name = getattr(settings, 'SITE_NAME', 'Tour System')
    subject = f'Invoice {invoice.invoice_number} — {site_name}'

    html_content = render_to_string('packages/emails/invoice_email.html', {
        'invoice': invoice,
        'booking': invoice.booking,
        'site_name': site_name,
    })
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )
    email.attach_alternative(html_content, "text/html")

    try:
        pdf_bytes = render_invoice_pdf(invoice)
        email.attach(f'{invoice.invoice_number}.pdf', pdf_bytes, 'application/pdf')
        email.send(fail_silently=False)
        return True
    except Exception:
        logger.exception("Error sending invoice email for %s", invoice.invoice_number)
        return False

"""Email notifications for the booking system."""
import logging
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
User = get_user_model()

SITE_NAME = getattr(settings, 'SITE_NAME', 'Tour Management System')
SITE_URL = getattr(settings, 'SITE_URL', 'http://localhost:8000')
FROM_EMAIL = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@toursystem.com')


def _staff_emails():
    return list(
        User.objects.filter(is_staff=True, is_active=True)
        .exclude(email='')
        .values_list('email', flat=True)
    )


def send_booking_confirmation(booking):
    """Send booking confirmation to the lead passenger / inquiry customer."""
    try:
        to_email = None
        customer_name = 'Valued Customer'
        if booking.inquiry:
            to_email = booking.inquiry.customer_email
            customer_name = booking.inquiry.customer_name

        subject = f"Booking Confirmed — {booking.booking_reference} | {SITE_NAME}"
        body = (
            f"Dear {customer_name},\n\n"
            f"Thank you for booking with us!\n\n"
            f"Booking Reference: {booking.booking_reference}\n"
            f"Package: {booking.package.name}\n"
            f"Departure Date: {booking.departure_date}\n"
            f"Travelers: {booking.num_adults} adult(s), {booking.num_children} child(ren)\n"
            f"Total Price: {booking.currency} {booking.quoted_price}\n"
            f"Deposit Required: {booking.currency} {booking.deposit_amount}\n\n"
            f"Our team will be in touch shortly with further details.\n\n"
            f"Regards,\n{SITE_NAME}"
        )

        recipients = []
        if to_email:
            recipients.append(to_email)
        recipients.extend(_staff_emails())

        if recipients:
            send_mail(subject, body, FROM_EMAIL, recipients, fail_silently=True)
    except Exception:
        logger.exception("Failed to send booking confirmation for %s", booking.booking_reference)


def send_booking_status_update(booking, old_status):
    """Notify staff and customer when a booking status changes."""
    try:
        subject = (
            f"Booking Update — {booking.booking_reference} "
            f"({booking.get_status_display()}) | {SITE_NAME}"
        )
        body = (
            f"Booking {booking.booking_reference} status has changed.\n\n"
            f"Package: {booking.package.name}\n"
            f"Previous Status: {old_status.replace('_', ' ').title()}\n"
            f"New Status: {booking.get_status_display()}\n"
            f"Departure: {booking.departure_date}\n\n"
            f"View booking: {SITE_URL}/dashboard/bookings/{booking.pk}/\n\n"
            f"Regards,\n{SITE_NAME}"
        )
        recipients = _staff_emails()
        if booking.inquiry:
            recipients.append(booking.inquiry.customer_email)
        if recipients:
            send_mail(subject, body, FROM_EMAIL, recipients, fail_silently=True)
    except Exception:
        logger.exception("Failed to send status update for %s", booking.booking_reference)


def send_payment_received(booking, payment):
    """Notify customer and staff that a payment has been recorded."""
    try:
        subject = f"Payment Received — {booking.booking_reference} | {SITE_NAME}"
        body = (
            f"A payment has been recorded for your booking.\n\n"
            f"Booking Reference: {booking.booking_reference}\n"
            f"Payment Type: {payment.get_payment_type_display()}\n"
            f"Amount: {payment.currency} {payment.amount}\n"
            f"Method: {payment.get_payment_method_display()}\n"
            f"Balance Remaining: {booking.currency} {booking.balance_due}\n\n"
            f"Regards,\n{SITE_NAME}"
        )
        recipients = _staff_emails()
        if booking.inquiry:
            recipients.append(booking.inquiry.customer_email)
        if recipients:
            send_mail(subject, body, FROM_EMAIL, recipients, fail_silently=True)
    except Exception:
        logger.exception("Failed to send payment notification for %s", booking.booking_reference)

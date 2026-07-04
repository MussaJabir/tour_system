"""PDF generation helpers for the packages app (WeasyPrint)."""
from django.conf import settings
from django.template.loader import render_to_string

from core.models import SiteSettings


def render_invoice_pdf(invoice):
    """
    Render an Invoice to PDF bytes.

    The template is fully self-contained (inline CSS, no external images), so
    no base_url / network resolution is needed and the output is deterministic.
    """
    # Imported lazily so the app still loads in environments without the
    # WeasyPrint native libraries (e.g. running a subset of unit tests).
    from weasyprint import HTML

    booking = invoice.booking
    context = {
        'invoice': invoice,
        'booking': booking,
        'site': SiteSettings.load(),
        'site_name': getattr(settings, 'SITE_NAME', 'Tour System'),
        'payments': booking.payments.filter(status='confirmed').order_by('created_at'),
    }
    html = render_to_string('packages/invoices/invoice_pdf.html', context)
    return HTML(string=html).write_pdf()

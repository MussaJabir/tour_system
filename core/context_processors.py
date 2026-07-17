"""Context processors exposing site-wide settings to every template render."""
from django.conf import settings

from .models import SiteSettings
from .utils import normalize_whatsapp_number


def site_settings(request):
    """
    Site identity + contact channels, available on all templates.

    `whatsapp_number` resolution order: dashboard Site Settings →
    WHATSAPP_BUSINESS_NUMBER environment variable → '' (all WhatsApp UI
    hidden). The value is pre-normalized to wa.me format; templates should
    guard WhatsApp UI with {% if whatsapp_number %}.
    """
    site = SiteSettings.load()
    raw_number = site.whatsapp_number or getattr(
        settings, 'WHATSAPP_BUSINESS_NUMBER', ''
    )
    site_name = getattr(settings, 'SITE_NAME', '')
    # Short wordmark for the header/sidebar: explicit SITE_SHORT_NAME, else the
    # first word of the full name ("Enteipa Adventures" -> "Enteipa").
    site_short_name = getattr(settings, 'SITE_SHORT_NAME', '') or (
        site_name.split()[0] if site_name else ''
    )
    return {
        'site_name': site_name,
        'site_short_name': site_short_name,
        'whatsapp_number': normalize_whatsapp_number(raw_number),
    }

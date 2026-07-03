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
    return {
        'site_name': getattr(settings, 'SITE_NAME', ''),
        'whatsapp_number': normalize_whatsapp_number(raw_number),
    }

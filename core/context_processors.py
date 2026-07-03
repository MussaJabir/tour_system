"""Context processors exposing site-wide settings to every template render."""
from django.conf import settings

from .utils import normalize_whatsapp_number


def site_settings(request):
    """
    Site identity + contact channels, available on all templates.

    `whatsapp_number` is pre-normalized to wa.me format; templates should
    guard WhatsApp UI with {% if whatsapp_number %} so nothing renders
    when WHATSAPP_BUSINESS_NUMBER is unset or invalid.
    """
    return {
        'site_name': getattr(settings, 'SITE_NAME', ''),
        'whatsapp_number': normalize_whatsapp_number(
            getattr(settings, 'WHATSAPP_BUSINESS_NUMBER', '')
        ),
    }

"""Template tags for building WhatsApp click-to-chat (wa.me) links."""
from urllib.parse import quote

from django import template

from core.utils import normalize_whatsapp_number

register = template.Library()


@register.simple_tag
def whatsapp_url(number, message=''):
    """
    Build a wa.me deep link for `number`, optionally prefilled with `message`.

    Returns '' when the number can't be normalized — wrap usages in
    {% if %} so no dead button is rendered.

    Usage:
        {% whatsapp_url whatsapp_number "Hi! I'd like to plan a trip." as wa_href %}
        {% if wa_href %}<a href="{{ wa_href }}">…</a>{% endif %}
    """
    digits = normalize_whatsapp_number(number)
    if not digits:
        return ''
    url = f'https://wa.me/{digits}'
    if message:
        url = f'{url}?text={quote(str(message))}'
    return url

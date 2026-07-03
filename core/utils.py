"""Shared utilities used across apps."""
import re

# Month name → 1-based index. Includes long, short, and a few common variants.
_MONTH_TOKENS = {
    'january': 1, 'jan': 1,
    'february': 2, 'feb': 2,
    'march': 3, 'mar': 3,
    'april': 4, 'apr': 4,
    'may': 5,
    'june': 6, 'jun': 6,
    'july': 7, 'jul': 7,
    'august': 8, 'aug': 8,
    'september': 9, 'sep': 9, 'sept': 9,
    'october': 10, 'oct': 10,
    'november': 11, 'nov': 11,
    'december': 12, 'dec': 12,
}

# Captures either a single month "Sep", or a range "June-October" / "Jun to Oct".
_MONTH_RANGE_RE = re.compile(
    r'\b(' + '|'.join(_MONTH_TOKENS.keys()) + r')'
    r'(?:\s*(?:-|–|—|to|through|–|until)\s*'
    r'(' + '|'.join(_MONTH_TOKENS.keys()) + r'))?\b',
    re.IGNORECASE,
)


def parse_best_months(text):
    """
    Extract month indices (1-12) referenced in a free-text best-time-to-visit string.

    Examples
        "Jun-Oct (Mara crossings), Jan-Mar (calving)"  → [1, 2, 3, 6, 7, 8, 9, 10]
        "Year-round"                                    → []
        "Best September through November"               → [9, 10, 11]

    Returns a sorted list of unique month indices. Empty list means we couldn't
    confidently parse anything — callers should fall back to rendering the raw
    prose instead of a blank calendar.
    """
    if not text:
        return []

    months = set()
    for match in _MONTH_RANGE_RE.finditer(text):
        start_token, end_token = match.group(1), match.group(2)
        start = _MONTH_TOKENS[start_token.lower()]
        end = _MONTH_TOKENS[end_token.lower()] if end_token else start
        if start <= end:
            months.update(range(start, end + 1))
        else:
            # Wrap-around (e.g. Nov-Feb)
            months.update(range(start, 13))
            months.update(range(1, end + 1))
    return sorted(months)


# All 12 month abbreviations, for rendering the calendar shell.
MONTH_ABBR = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def normalize_whatsapp_number(raw, default_country_code='255'):
    """
    Normalize a phone number into the digits-only international format that
    wa.me links require (e.g. '0744 123 456' → '255744123456').

    Handles the forms customers actually type:
        '+255 744 123 456'  → '255744123456'   (already international)
        '00255744123456'    → '255744123456'   (00 international prefix)
        '0744123456'        → '255744123456'   (local with leading zero)
        '744123456'         → '255744123456'   (local without leading zero)

    Returns '' when the input can't be a dialable number, so callers can
    hide WhatsApp actions instead of rendering a dead link.
    """
    if not raw:
        return ''
    raw = str(raw).strip()
    digits = re.sub(r'\D', '', raw)

    if raw.startswith('+'):
        pass  # already international — digits are usable as-is
    elif digits.startswith('00'):
        digits = digits[2:]
    elif digits.startswith('0'):
        digits = default_country_code + digits[1:]
    elif len(digits) <= 9:
        # Local number typed without the leading zero
        digits = default_country_code + digits

    # Full international numbers are 10-15 digits (E.164 upper bound)
    if not 10 <= len(digits) <= 15:
        return ''
    return digits

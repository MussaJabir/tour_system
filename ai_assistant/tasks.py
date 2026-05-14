import json
import logging
import re

from celery import shared_task

logger = logging.getLogger(__name__)

_JSON_STRIP = re.compile(r'^```(?:json)?\n?|\n?```$')


def _strip_json(raw: str) -> str:
    return _JSON_STRIP.sub('', raw.strip())


def _extract_pdf_text(path: str) -> str:
    try:
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            return '\n'.join(p.extract_text() or '' for p in pdf.pages)
    except ImportError:
        pass
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(path)
        return '\n'.join(p.extract_text() or '' for p in reader.pages)
    except Exception:
        pass
    return ''


@shared_task(bind=True, max_retries=2)
def parse_brochure_task(self, job_id: int) -> None:
    from .models import BrochureParseJob
    from .ai_client import get_ai_response, AIServiceError

    try:
        job = BrochureParseJob.objects.get(pk=job_id)
    except BrochureParseJob.DoesNotExist:
        logger.error('BrochureParseJob %s not found', job_id)
        return

    job.mark_processing()

    try:
        text = _extract_pdf_text(job.pdf_file.path)
        if not text.strip():
            job.mark_failed('Could not extract text from PDF.')
            return

        system = (
            'You are an expert at extracting structured data from tourism accommodation brochures. '
            'Return ONLY valid JSON with these keys: name, description, short_description, '
            'amenities (list), room_types (list of {name, description}), highlights (list), '
            'location_description, policies. Use null for missing values.'
        )
        prompt = f'Extract structured data from this lodge brochure:\n\n{text[:8000]}'
        raw = get_ai_response(prompt, system)
        job.extracted_data = json.loads(_strip_json(raw))
        job.save(update_fields=['extracted_data'])
        job.mark_done()
    except AIServiceError as exc:
        job.mark_failed(str(exc))
    except json.JSONDecodeError as exc:
        job.mark_failed(f'AI returned invalid JSON: {exc}')
    except Exception as exc:
        logger.exception('Brochure parse job %s failed', job_id)
        job.mark_failed(str(exc))


@shared_task(bind=True, max_retries=2)
def generate_itinerary_task(self, job_id: int) -> None:
    from .models import ItineraryGenerationJob
    from .ai_client import get_ai_response, AIServiceError

    try:
        job = ItineraryGenerationJob.objects.select_related('destination').get(pk=job_id)
    except ItineraryGenerationJob.DoesNotExist:
        return

    job.mark_processing()

    try:
        dest = job.destination.name if job.destination else 'Tanzania'
        system = (
            'You are an expert Tanzanian safari tour planner. '
            'Create detailed, practical, day-by-day itineraries formatted as clean markdown.'
        )
        prompt = (
            f'Create a {job.duration_days}-day itinerary for {dest}, Tanzania.\n'
            f'Budget: ~USD {job.budget_usd} per person\n'
            f'Group size: {job.group_size} people\n'
            f'Interests: {job.interests or "wildlife safari, culture, photography"}\n\n'
            'Include: daily schedule, accommodation type, activities, travel notes, and tips.'
        )
        job.raw_output = get_ai_response(prompt, system)
        job.save(update_fields=['raw_output'])
        job.mark_done()
    except AIServiceError as exc:
        job.mark_failed(str(exc))
    except Exception as exc:
        logger.exception('Itinerary job %s failed', job_id)
        job.mark_failed(str(exc))


@shared_task(bind=True, max_retries=2)
def build_custom_quote_task(self, job_id: int) -> None:
    from .models import QuoteSuggestionJob
    from .ai_client import get_ai_response, AIServiceError
    from packages.models import Package

    try:
        job = QuoteSuggestionJob.objects.select_related('inquiry__base_package').get(pk=job_id)
    except QuoteSuggestionJob.DoesNotExist:
        return

    job.mark_processing()

    try:
        inquiry = job.inquiry
        packages = Package.objects.filter(is_active=True).values(
            'pk', 'name', 'duration_days', 'price_per_person', 'short_description'
        )[:20]
        package_list = '\n'.join(
            f"- ID {p['pk']}: {p['name']} ({p['duration_days']} days, ${p['price_per_person']}) "
            f"— {p['short_description']}"
            for p in packages
        )
        system = (
            'You are a Tanzanian safari sales specialist. '
            'Match customer inquiries to the most suitable packages. '
            'Return ONLY valid JSON: a list of up to 3 objects with keys: '
            'package_id (int), package_name (str), match_score (1-10), reason (str).'
        )
        group = inquiry.number_of_adults + inquiry.number_of_children
        prompt = (
            f'Customer: {inquiry.customer_name}\n'
            f'Package interest: {inquiry.base_package.name if inquiry.base_package else "not specified"}\n'
            f'Travel date: {inquiry.preferred_travel_date or "flexible"}\n'
            f'Group size: {group} ({inquiry.number_of_adults} adults, {inquiry.number_of_children} children)\n'
            f'Budget: {inquiry.get_budget_range_display()}\n'
            f'Accommodation: {inquiry.get_accommodation_preference_display()}\n\n'
            f'Available packages:\n{package_list}\n\n'
            'Suggest the 3 best-matching packages with reasons.'
        )
        raw = get_ai_response(prompt, system)
        job.suggestions = json.loads(_strip_json(raw))
        job.save(update_fields=['suggestions'])
        job.mark_done()
    except AIServiceError as exc:
        job.mark_failed(str(exc))
    except json.JSONDecodeError as exc:
        job.mark_failed(f'AI returned invalid JSON: {exc}')
    except Exception as exc:
        logger.exception('Quote suggestion job %s failed', job_id)
        job.mark_failed(str(exc))


@shared_task(bind=True, max_retries=2)
def optimize_route_task(self, job_id: int) -> None:
    from .models import RouteOptimizationJob
    from .ai_client import get_ai_response, AIServiceError

    try:
        job = RouteOptimizationJob.objects.get(pk=job_id)
    except RouteOptimizationJob.DoesNotExist:
        return

    job.mark_processing()

    try:
        system = (
            "You are an expert on Tanzania's geography and road network. "
            'Optimize tourist routes for minimum driving time and maximum experience. '
            'Return ONLY valid JSON: a list of objects with keys: '
            'order (int), name (str), drive_from_previous_minutes (int, 0 for first), notes (str).'
        )
        prompt = (
            f'Optimize the visiting order for these Tanzanian destinations/parks:\n'
            f'{job.destination_names}\n\n'
            'Consider driving distances, road quality, and logical flow. '
            'Include estimated driving time from the previous stop.'
        )
        raw = get_ai_response(prompt, system)
        job.optimized_route = json.loads(_strip_json(raw))
        job.save(update_fields=['optimized_route'])
        job.mark_done()
    except AIServiceError as exc:
        job.mark_failed(str(exc))
    except json.JSONDecodeError as exc:
        job.mark_failed(f'AI returned invalid JSON: {exc}')
    except Exception as exc:
        logger.exception('Route optimization job %s failed', job_id)
        job.mark_failed(str(exc))

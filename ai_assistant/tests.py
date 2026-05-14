import json
from decimal import Decimal
from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from destinations.models import Destination
from packages.models import BookingInquiry, Package
from .models import (
    AIConfiguration,
    BrochureParseJob,
    ItineraryGenerationJob,
    QuoteSuggestionJob,
    RouteOptimizationJob,
)

User = get_user_model()


def make_staff(**kwargs):
    defaults = dict(username='staff', password='pass123', email='s@s.com', is_staff=True)
    defaults.update(kwargs)
    return User.objects.create_user(**defaults)


def make_package(**kwargs):
    defaults = dict(
        name='Serengeti Safari',
        slug='serengeti-safari',
        short_description='Amazing safari',
        description='Full description',
        duration_days=7,
        duration_nights=6,
        price_per_person=Decimal('2000.00'),
        availability_status='available',
        is_active=True,
    )
    defaults.update(kwargs)
    return Package.objects.create(**defaults)


def make_inquiry(package, **kwargs):
    defaults = dict(
        inquiry_reference='INQ-2026-00001',
        base_package=package,
        customer_name='Alice',
        customer_email='alice@test.com',
        customer_phone='+255700000000',
        number_of_adults=2,
        number_of_children=0,
        budget_range='2000_3000',
    )
    defaults.update(kwargs)
    return BookingInquiry.objects.create(**defaults)


class AIConfigurationModelTests(TestCase):
    def test_singleton_enforcement(self):
        c1 = AIConfiguration(vendor='openai', api_key='key-a', model_name='gpt-4o')
        c1.save()
        c2 = AIConfiguration(vendor='anthropic', api_key='key-b', model_name='claude-3-5-sonnet-20241022')
        c2.save()
        self.assertEqual(AIConfiguration.objects.count(), 1)
        config = AIConfiguration.objects.get(pk=1)
        self.assertEqual(config.vendor, 'anthropic')

    def test_get_active_returns_none_when_absent(self):
        self.assertIsNone(AIConfiguration.get_active())

    def test_get_active_returns_config_when_active(self):
        AIConfiguration.objects.create(vendor='openai', api_key='k', model_name='gpt-4o')
        self.assertIsNotNone(AIConfiguration.get_active())

    def test_get_active_returns_none_when_inactive(self):
        AIConfiguration.objects.create(
            vendor='openai', api_key='k', model_name='gpt-4o', is_active=False
        )
        self.assertIsNone(AIConfiguration.get_active())

    def test_str(self):
        c = AIConfiguration(vendor='openai', model_name='gpt-4o')
        self.assertIn('OpenAI', str(c))
        self.assertIn('gpt-4o', str(c))


class BaseAIJobTests(TestCase):
    def setUp(self):
        self.job = RouteOptimizationJob.objects.create(
            destination_names='Serengeti, Ngorongoro'
        )

    def test_initial_status_pending(self):
        self.assertEqual(self.job.status, 'pending')

    def test_mark_processing(self):
        self.job.mark_processing()
        self.job.refresh_from_db()
        self.assertEqual(self.job.status, 'processing')
        self.assertIsNotNone(self.job.started_at)

    def test_mark_done(self):
        self.job.mark_done()
        self.job.refresh_from_db()
        self.assertEqual(self.job.status, 'done')
        self.assertIsNotNone(self.job.completed_at)

    def test_mark_failed(self):
        self.job.mark_failed('Connection timeout')
        self.job.refresh_from_db()
        self.assertEqual(self.job.status, 'failed')
        self.assertIn('timeout', self.job.error_message)

    def test_is_running_true_for_pending(self):
        self.assertTrue(self.job.is_running)

    def test_is_running_false_for_done(self):
        self.job.mark_done()
        self.assertFalse(self.job.is_running)


class TaskTests(TestCase):
    def setUp(self):
        self.staff = make_staff()
        self.package = make_package()

    @patch('ai_assistant.ai_client.get_ai_response')
    def test_generate_itinerary_task_success(self, mock_ai):
        mock_ai.return_value = '# Day 1\nArrive in Arusha.'
        job = ItineraryGenerationJob.objects.create(
            duration_days=3, budget_usd=1500, group_size=2, created_by=self.staff
        )
        from ai_assistant.tasks import generate_itinerary_task
        generate_itinerary_task(job.pk)
        job.refresh_from_db()
        self.assertEqual(job.status, 'done')
        self.assertIn('Day 1', job.raw_output)

    @patch('ai_assistant.ai_client.get_ai_response')
    def test_generate_itinerary_task_ai_error(self, mock_ai):
        from ai_assistant.ai_client import AIServiceError
        mock_ai.side_effect = AIServiceError('No API key')
        job = ItineraryGenerationJob.objects.create(
            duration_days=3, budget_usd=1500, group_size=2
        )
        from ai_assistant.tasks import generate_itinerary_task
        generate_itinerary_task(job.pk)
        job.refresh_from_db()
        self.assertEqual(job.status, 'failed')
        self.assertIn('No API key', job.error_message)

    @patch('ai_assistant.ai_client.get_ai_response')
    def test_build_quote_task_success(self, mock_ai):
        inquiry = make_inquiry(self.package)
        mock_ai.return_value = json.dumps([
            {'package_id': self.package.pk, 'package_name': 'Serengeti Safari', 'match_score': 9, 'reason': 'Perfect match.'}
        ])
        job = QuoteSuggestionJob.objects.create(inquiry=inquiry, created_by=self.staff)
        from ai_assistant.tasks import build_custom_quote_task
        build_custom_quote_task(job.pk)
        job.refresh_from_db()
        self.assertEqual(job.status, 'done')
        self.assertIsInstance(job.suggestions, list)
        self.assertEqual(job.suggestions[0]['match_score'], 9)

    @patch('ai_assistant.ai_client.get_ai_response')
    def test_optimize_route_task_success(self, mock_ai):
        mock_ai.return_value = json.dumps([
            {'order': 1, 'name': 'Arusha', 'drive_from_previous_minutes': 0, 'notes': 'Start here.'},
            {'order': 2, 'name': 'Serengeti', 'drive_from_previous_minutes': 240, 'notes': 'Long drive.'},
        ])
        job = RouteOptimizationJob.objects.create(
            destination_names='Serengeti, Arusha', created_by=self.staff
        )
        from ai_assistant.tasks import optimize_route_task
        optimize_route_task(job.pk)
        job.refresh_from_db()
        self.assertEqual(job.status, 'done')
        self.assertEqual(len(job.optimized_route), 2)

    @patch('ai_assistant.ai_client.get_ai_response')
    def test_route_task_bad_json_marks_failed(self, mock_ai):
        mock_ai.return_value = 'Not JSON at all'
        job = RouteOptimizationJob.objects.create(destination_names='Serengeti')
        from ai_assistant.tasks import optimize_route_task
        optimize_route_task(job.pk)
        job.refresh_from_db()
        self.assertEqual(job.status, 'failed')


class AIAssistantViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff = make_staff()
        self.regular = User.objects.create_user(
            username='regular', password='pass123', email='r@r.com'
        )

    def _login_staff(self):
        self.client.login(username='staff', password='pass123')

    def test_home_redirects_anonymous(self):
        res = self.client.get(reverse('ai_assistant:home'))
        self.assertIn(res.status_code, [301, 302])

    def test_home_blocks_non_staff(self):
        self.client.login(username='regular', password='pass123')
        res = self.client.get(reverse('ai_assistant:home'))
        self.assertIn(res.status_code, [301, 302])

    def test_home_accessible_to_staff(self):
        self._login_staff()
        res = self.client.get(reverse('ai_assistant:home'))
        self.assertEqual(res.status_code, 200)

    def test_itinerary_form_renders(self):
        self._login_staff()
        res = self.client.get(reverse('ai_assistant:itinerary_generate'))
        self.assertEqual(res.status_code, 200)

    def test_route_form_renders(self):
        self._login_staff()
        res = self.client.get(reverse('ai_assistant:route_optimize'))
        self.assertEqual(res.status_code, 200)

    @patch('ai_assistant.views.generate_itinerary_task')
    def test_itinerary_post_creates_job_and_redirects(self, mock_task):
        mock_task.delay = MagicMock()
        self._login_staff()
        res = self.client.post(reverse('ai_assistant:itinerary_generate'), {
            'duration_days': 5,
            'budget_usd': 2000,
            'group_size': 2,
            'interests': 'wildlife',
        })
        self.assertEqual(res.status_code, 302)
        self.assertEqual(ItineraryGenerationJob.objects.count(), 1)

    @patch('ai_assistant.views.optimize_route_task')
    def test_route_post_creates_job_and_redirects(self, mock_task):
        mock_task.delay = MagicMock()
        self._login_staff()
        res = self.client.post(reverse('ai_assistant:route_optimize'), {
            'destination_names': 'Serengeti\nNgorongoro',
        })
        self.assertEqual(res.status_code, 302)
        self.assertEqual(RouteOptimizationJob.objects.count(), 1)

    def test_itinerary_result_accessible_to_staff(self):
        job = ItineraryGenerationJob.objects.create(
            duration_days=3, budget_usd=1000, group_size=1, created_by=self.staff
        )
        self._login_staff()
        res = self.client.get(reverse('ai_assistant:itinerary_result', args=[job.pk]))
        self.assertEqual(res.status_code, 200)

    def test_route_result_accessible_to_staff(self):
        job = RouteOptimizationJob.objects.create(
            destination_names='Serengeti', created_by=self.staff
        )
        self._login_staff()
        res = self.client.get(reverse('ai_assistant:route_result', args=[job.pk]))
        self.assertEqual(res.status_code, 200)

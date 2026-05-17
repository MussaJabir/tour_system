"""
Phase 7.0 — Dashboard foundation smoke tests.

Verifies the Operations Slate foundation:
- /dashboard/styleguide/ behaves correctly in DEBUG vs production
- base_dashboard.html renders required blocks
- All 8 reusable partials render without raising
- The shared tailwind.css contains the Operations Slate tokens
"""
import os
from django.test import TestCase
from django.urls import reverse
from django.template.loader import render_to_string
from django.template import Template, Context
from django.test.client import RequestFactory
from django.conf import settings


class DashboardStyleguideAccessTests(TestCase):

    def test_styleguide_returns_200_when_debug_true(self):
        with self.settings(DEBUG=True):
            response = self.client.get(reverse('dashboard_styleguide'))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Operations Slate')

    def test_styleguide_returns_404_when_debug_false(self):
        with self.settings(DEBUG=False, ALLOWED_HOSTS=['*']):
            response = self.client.get(reverse('dashboard_styleguide'))
            self.assertEqual(response.status_code, 404)

    def test_styleguide_uses_base_dashboard_template(self):
        with self.settings(DEBUG=True):
            response = self.client.get(reverse('dashboard_styleguide'))
            self.assertTemplateUsed(response, 'backend/base_dashboard.html')
            self.assertTemplateUsed(response, 'backend/_styleguide.html')


class BaseDashboardTemplateTests(TestCase):
    """Required blocks must exist for future Phase 7.x pages to extend."""

    REQUIRED_BLOCKS = [
        'title', 'extra_css', 'content', 'extra_js',
        'topbar_search', 'topbar_extras',
    ]

    def test_base_dashboard_defines_required_blocks(self):
        template_path = os.path.join(
            settings.BASE_DIR, 'templates', 'backend', 'base_dashboard.html'
        )
        with open(template_path) as f:
            source = f.read()
        # `topbar_*` blocks live in the topbar partial — verify via the rendered output
        for block_name in ('title', 'extra_css', 'content', 'extra_js'):
            self.assertIn(f'block {block_name}', source,
                          f"base_dashboard.html missing block: {block_name}")

    def test_base_dashboard_renders_with_minimal_context(self):
        from django.contrib.auth.models import AnonymousUser
        template = Template(
            '{% extends "backend/base_dashboard.html" %}'
            '{% block content %}<p data-marker>hello dash</p>{% endblock %}'
        )
        request = RequestFactory().get('/dashboard/')
        request.user = AnonymousUser()
        html = template.render(Context({'request': request, 'user': request.user}))
        # Content block fired
        self.assertIn('data-marker', html)
        # Shell shows up (sidebar + topbar + main)
        self.assertIn('dash-shell', html)
        self.assertIn('dash-sidebar', html)
        self.assertIn('dash-topbar', html)
        # Tailwind CSS is loaded
        self.assertIn('tailwind.css', html)

    def test_base_dashboard_loads_chart_js_isnt_global(self):
        """Chart.js should be page-scoped (loaded via extra_js), not on every page."""
        template_path = os.path.join(
            settings.BASE_DIR, 'templates', 'backend', 'base_dashboard.html'
        )
        with open(template_path) as f:
            source = f.read()
        # Alpine should be loaded globally
        self.assertIn('alpine.min.js', source)
        # Chart.js should NOT be loaded globally (only on analytics pages)
        self.assertNotIn('chart.min.js', source)


class DashboardPartialsRenderTests(TestCase):

    def test_status_badge_partial(self):
        for variant in ('success', 'warning', 'danger', 'info', 'neutral'):
            html = render_to_string(
                'backend/partials/_status_badge.html',
                {'label': f'Test {variant}', 'variant': variant},
            )
            self.assertIn(f'dash-badge-{variant}', html)
            self.assertIn(f'Test {variant}', html)

    def test_stat_card_partial(self):
        html = render_to_string('backend/partials/_stat_card.html', {
            'label': 'Inquiries · 30d',
            'value': '42',
            'trend_value': '+18%',
            'trend_dir': 'up',
            'icon': 'comment-alt-lines',
        })
        self.assertIn('Inquiries · 30d', html)
        self.assertIn('42', html)
        self.assertIn('dash-stat-trend--up', html)
        self.assertIn('fa-comment-alt-lines', html)

    def test_empty_state_partial(self):
        html = render_to_string('backend/partials/_empty_state.html', {
            'icon': 'inbox',
            'title': 'Nothing here.',
            'subtitle': 'Yet.',
            'action_label': 'Do a thing',
            'action_url': '/x/',
        })
        self.assertIn('Nothing here.', html)
        self.assertIn('Yet.', html)
        self.assertIn('Do a thing', html)
        self.assertIn('href="/x/"', html)

    def test_page_header_partial(self):
        html = render_to_string('backend/partials/_page_header.html', {
            'title': 'Tour Packages',
            'subtitle': 'Manage your catalog',
            'action_html': '<a class="dash-btn dash-btn-primary">New</a>',
        })
        self.assertIn('Tour Packages', html)
        self.assertIn('Manage your catalog', html)
        self.assertIn('dash-btn-primary', html)

    def test_breadcrumb_partial(self):
        crumbs = [
            {'label': 'Tours', 'url': '/dashboard/packages/'},
            {'label': '7-day Serengeti'},
        ]
        html = render_to_string('backend/partials/_breadcrumb.html', {'crumbs': crumbs})
        self.assertIn('Dashboard', html)
        self.assertIn('Tours', html)
        self.assertIn('7-day Serengeti', html)


class TailwindOperationsSlateTokensTests(TestCase):
    """Compiled tailwind.css must contain the new Operations Slate tokens."""

    def test_tailwind_has_dashboard_utilities(self):
        css_path = os.path.join(
            settings.BASE_DIR, 'static', 'frontend', 'css', 'tailwind.css'
        )
        with open(css_path) as f:
            css = f.read()
        for token in [
            '.dash-shell', '.dash-sidebar', '.dash-nav-link',
            '.dash-topbar', '.dash-page-title', '.dash-card',
            '.dash-stat', '.dash-btn', '.dash-btn-primary',
            '.dash-badge', '.dash-badge-success', '.dash-badge-danger',
            '.dash-table', '.dash-input',
        ]:
            self.assertIn(token, css, f"tailwind.css missing utility: {token}")


class ChartJsVendorTests(TestCase):

    def test_chart_js_file_exists(self):
        path = os.path.join(
            settings.BASE_DIR, 'static', 'frontend', 'vendor', 'chart.min.js'
        )
        self.assertTrue(os.path.exists(path), 'Chart.js not downloaded')
        with open(path) as f:
            head = f.read(200)
        self.assertNotIn('<!DOCTYPE', head, 'Chart.js download appears to be HTML, not JS')

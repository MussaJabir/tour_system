"""
Phase 6.0 — Frontend Foundation smoke tests.

Verifies the new Safari Editorial foundation:
- base_modern.html renders with required blocks
- All new partials render without error
- Styleguide returns 200 in DEBUG, 404 in production
- Compiled Tailwind CSS is reachable as a static file
"""
from django.test import TestCase, override_settings
from django.urls import reverse
from django.template.loader import render_to_string
from django.template import Context, Template
from django.conf import settings
import os


class StyleguideAccessTests(TestCase):
    """Styleguide is a development-only page."""

    def test_styleguide_returns_200_when_debug_true(self):
        with self.settings(DEBUG=True):
            response = self.client.get(reverse('styleguide'))
            self.assertEqual(response.status_code, 200)
            # Sanity: hero copy renders
            self.assertContains(response, 'Safari Editorial')

    def test_styleguide_returns_404_when_debug_false(self):
        with self.settings(DEBUG=False, ALLOWED_HOSTS=['*']):
            response = self.client.get(reverse('styleguide'))
            self.assertEqual(response.status_code, 404)

    def test_styleguide_uses_base_modern_template(self):
        with self.settings(DEBUG=True):
            response = self.client.get(reverse('styleguide'))
            self.assertTemplateUsed(response, 'frontend/base_modern.html')
            self.assertTemplateUsed(response, 'frontend/_styleguide.html')


class BaseModernTemplateTests(TestCase):
    """The new base shell must define every block existing pages rely on."""

    REQUIRED_BLOCKS = [
        'meta_description', 'meta_keywords', 'title', 'canonical',
        'og_type', 'og_title', 'title2', 'og_description', 'og_image', 'og_url',
        'meta_tags', 'extra_css', 'content', 'extra_js',
    ]

    def test_base_modern_renders_with_minimal_context(self):
        """Smoke test: template compiles and renders an empty body."""
        template = Template('{% extends "frontend/base_modern.html" %}'
                            '{% block content %}<p>hello</p>{% endblock %}')
        # Build a request-like context so partials with {% url %} resolve
        from django.test.client import RequestFactory
        request = RequestFactory().get('/')
        html = template.render(Context({'request': request}))
        self.assertIn('<p>hello</p>', html)
        # Brand name is now driven by SITE_NAME; assert the stable tagline instead.
        self.assertIn('East African Journeys', html)
        self.assertIn('tailwind.css', html)

    def test_base_modern_defines_required_blocks(self):
        """Every block the legacy base.html exposed must still exist."""
        template_path = os.path.join(
            settings.BASE_DIR, 'templates', 'frontend', 'base_modern.html'
        )
        with open(template_path) as f:
            source = f.read()
        for block_name in self.REQUIRED_BLOCKS:
            self.assertIn(
                f'block {block_name}',
                source,
                f"base_modern.html is missing required block: {block_name}",
            )

    def test_base_modern_loads_vendor_scripts(self):
        with self.settings(DEBUG=True):
            response = self.client.get(reverse('styleguide'))
            self.assertContains(response, 'alpine.min.js')
            self.assertContains(response, 'gsap.min.js')
            self.assertContains(response, 'scrolltrigger.min.js')
            self.assertContains(response, 'lenis.min.js')


class PartialsRenderTests(TestCase):
    """The reusable include partials must render without raising."""

    def test_button_partial_link_variant(self):
        html = render_to_string('frontend/partials/_button.html', {
            'label': 'Click me', 'href': '/foo/', 'variant': 'primary', 'icon': 'arrow-right',
        })
        self.assertIn('href="/foo/"', html)
        self.assertIn('Click me', html)
        self.assertIn('btn-primary', html)
        self.assertIn('fa-arrow-right', html)

    def test_button_partial_button_variant(self):
        html = render_to_string('frontend/partials/_button.html', {
            'label': 'Submit', 'variant': 'secondary',
        })
        self.assertIn('<button', html)
        self.assertIn('btn-secondary', html)

    def test_section_header_partial(self):
        html = render_to_string('frontend/partials/_section_header.html', {
            'eyebrow': 'Curated', 'title': 'Featured tours', 'lede': 'Hand-picked',
        })
        self.assertIn('Curated', html)
        self.assertIn('Featured tours', html)
        self.assertIn('Hand-picked', html)

    def test_card_partial_with_url_string(self):
        html = render_to_string('frontend/partials/_card.html', {
            'image': 'https://example.com/img.jpg',
            'href': '/dest/',
            'title': 'Serengeti',
            'eyebrow': 'Tanzania',
            'meta': '5 days',
        })
        self.assertIn('Serengeti', html)
        self.assertIn('Tanzania', html)
        self.assertIn('5 days', html)
        self.assertIn('href="/dest/"', html)
        self.assertIn('https://example.com/img.jpg', html)

    def test_card_partial_without_image_shows_placeholder(self):
        html = render_to_string('frontend/partials/_card.html', {
            'image': None, 'href': '/x/', 'title': 'No image',
        })
        self.assertIn('fa-image', html)


class TailwindBuildArtifactTests(TestCase):
    """The compiled Tailwind CSS must exist on disk and contain our tokens."""

    def test_tailwind_css_artifact_exists(self):
        css_path = os.path.join(
            settings.BASE_DIR, 'static', 'frontend', 'css', 'tailwind.css'
        )
        self.assertTrue(
            os.path.exists(css_path),
            "tailwind.css not built. Run: tailwindcss -i static/frontend/src/tailwind.css -o static/frontend/css/tailwind.css --minify",
        )

    def test_tailwind_css_contains_safari_editorial_tokens(self):
        css_path = os.path.join(
            settings.BASE_DIR, 'static', 'frontend', 'css', 'tailwind.css'
        )
        with open(css_path) as f:
            css = f.read()
        # Core brand utilities used across templates
        for token in ['.bg-ivory', '.text-charcoal', '.bg-sand-100',
                      '.text-bush-600', '.font-display', '.text-display-xl']:
            self.assertIn(token, css, f"Tailwind output missing utility: {token}")


class VendorAssetsTests(TestCase):
    """All four vendor scripts must be present on disk."""

    VENDOR_FILES = [
        'alpine.min.js',
        'gsap.min.js',
        'scrolltrigger.min.js',
        'lenis.min.js',
    ]

    def test_vendor_files_exist(self):
        vendor_dir = os.path.join(
            settings.BASE_DIR, 'static', 'frontend', 'vendor'
        )
        for fname in self.VENDOR_FILES:
            path = os.path.join(vendor_dir, fname)
            self.assertTrue(os.path.exists(path), f"missing vendor file: {fname}")
            # Sanity-check that the file isn't an HTML error page
            with open(path) as f:
                head = f.read(200)
            self.assertNotIn('<!DOCTYPE', head, f"vendor file is HTML, not JS: {fname}")

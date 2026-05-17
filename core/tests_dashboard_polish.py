"""
Phase 7.6 — Final polish smoke tests.

Verifies the last 8 dashboard templates migrated off backend/base.html and
asserts that no template still references the deleted legacy base.
"""
import os
from django.test import TestCase
from django.conf import settings


class NoLegacyBaseReferenceTests(TestCase):
    """Ensure no template still extends 'backend/base.html' (which has been deleted)."""

    def test_no_template_extends_legacy_base(self):
        offenders = []
        for app_dir in ('accommodations', 'activities', 'ai_assistant', 'core',
                        'destinations', 'packages', 'reviews', 'templates'):
            root = os.path.join(settings.BASE_DIR, app_dir)
            if not os.path.isdir(root):
                continue
            for dirpath, _, filenames in os.walk(root):
                for f in filenames:
                    if not f.endswith('.html'):
                        continue
                    path = os.path.join(dirpath, f)
                    with open(path) as fh:
                        head = fh.read(400)
                    # Match: {% extends "backend/base.html" %} or with single quotes
                    if "extends 'backend/base.html'" in head or \
                       'extends "backend/base.html"' in head:
                        offenders.append(os.path.relpath(path, settings.BASE_DIR))
        self.assertEqual(offenders, [],
                         f"These templates still extend backend/base.html: {offenders}")

    def test_legacy_base_template_is_deleted(self):
        legacy = os.path.join(settings.BASE_DIR, 'templates', 'backend', 'base.html')
        self.assertFalse(os.path.exists(legacy),
                         "templates/backend/base.html should be deleted but still exists.")

    def test_static_backend_directory_is_deleted(self):
        legacy = os.path.join(settings.BASE_DIR, 'static', 'backend')
        self.assertFalse(os.path.exists(legacy),
                         "static/backend/ should be deleted but still exists.")

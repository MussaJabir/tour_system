"""
Seed the catalog with realistic Tanzania-focused content + a handful of
neighbour-country destination stubs.

Idempotent — re-running it skips records that already exist by slug. Pass
`--reset` to truncate Destinations / Accommodations / Activities / Packages
(and their dependent rows) before reseeding.

Images live in `core/seed_data/images/` (committed to git so the seed
travels to production with the codebase). The command copies them into
MEDIA_ROOT during the run.

Usage:
    python manage.py seed_catalog              # idempotent upsert
    python manage.py seed_catalog --reset      # nuke + reseed
    python manage.py seed_catalog --skip-images  # data only, fast iteration
"""

import shutil
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from destinations.models import Destination, DestinationImage
from accommodations.models import Accommodation
from activities.models import Activity
from packages.models import Package, PackageItinerary
from core.models import Testimonial, FAQ

from core.seed_data.destinations import DESTINATIONS
from core.seed_data.accommodations import ACCOMMODATIONS
from core.seed_data.activities import ACTIVITIES
from core.seed_data.packages import PACKAGES
from core.seed_data.testimonials import TESTIMONIALS
from core.seed_data.faqs import FAQS


SEED_IMAGES_ROOT = Path(settings.BASE_DIR) / 'core' / 'seed_data' / 'images'
MEDIA_ROOT = Path(settings.MEDIA_ROOT)
IMAGE_EXTS = ('.jpg', '.jpeg', '.png', '.webp')


def find_seed_image(image_slug, image_dir):
    """Return absolute Path of the seed image matching slug+dir, or None.
    Tries multiple extensions because we accept jpg/png/webp."""
    if not image_slug or not image_dir:
        return None
    base = SEED_IMAGES_ROOT / image_dir
    for ext in IMAGE_EXTS:
        candidate = base / f"{image_slug}{ext}"
        if candidate.exists():
            return candidate
    return None


def copy_to_media(src_path, media_subdir):
    """Copy src to MEDIA_ROOT/<media_subdir>/<filename>. Returns the relative
    path that goes into an ImageField, or None if src missing."""
    if not src_path:
        return None
    dest_dir = MEDIA_ROOT / media_subdir
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / src_path.name
    if not dest_file.exists() or dest_file.stat().st_size != src_path.stat().st_size:
        shutil.copy2(src_path, dest_file)
    return f"{media_subdir}/{src_path.name}"


class Command(BaseCommand):
    help = "Seed the catalog with realistic destinations, accommodations, activities, packages, testimonials, FAQs."

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true',
                            help='Truncate catalog tables before seeding.')
        parser.add_argument('--skip-images', action='store_true',
                            help='Do not copy images — useful for fast data-only iteration.')

    @transaction.atomic
    def handle(self, *args, **opts):
        self.skip_images = opts['skip_images']

        if opts['reset']:
            self._reset()

        self.stdout.write(self.style.MIGRATE_HEADING("\n=== Seeding catalog ==="))
        if self.skip_images:
            self.stdout.write(self.style.WARNING("Images: SKIPPED (--skip-images)"))

        destinations_by_slug = self._seed_destinations()
        accommodations_by_slug = self._seed_accommodations(destinations_by_slug)
        activities_by_slug = self._seed_activities(destinations_by_slug)
        self._seed_packages(destinations_by_slug, accommodations_by_slug, activities_by_slug)
        self._seed_testimonials()
        self._seed_faqs()

        self.stdout.write(self.style.SUCCESS("\n=== Seed complete ==="))
        self._print_summary()

    # =========================================================================

    def _reset(self):
        self.stdout.write(self.style.WARNING("Resetting catalog tables..."))
        # Cascade order matters — children first.
        deleted_counts = {}
        deleted_counts['PackageItinerary'] = PackageItinerary.objects.all().delete()[0]
        deleted_counts['Package'] = Package.objects.all().delete()[0]
        deleted_counts['Accommodation'] = Accommodation.objects.all().delete()[0]
        deleted_counts['Activity'] = Activity.objects.all().delete()[0]
        deleted_counts['DestinationImage'] = DestinationImage.objects.all().delete()[0]
        deleted_counts['Destination'] = Destination.objects.all().delete()[0]
        deleted_counts['Testimonial'] = Testimonial.objects.all().delete()[0]
        deleted_counts['FAQ'] = FAQ.objects.all().delete()[0]
        for k, v in deleted_counts.items():
            self.stdout.write(f"  - {k}: {v}")

    # =========================================================================

    def _seed_destinations(self):
        self.stdout.write(self.style.MIGRATE_HEADING("\n--- Destinations ---"))
        by_slug = {}
        for data in DESTINATIONS:
            dest, created = Destination.objects.update_or_create(
                name=data['name'],
                defaults=dict(
                    description=data['description'],
                    short_description=data['short_description'],
                    country=data['country'],
                    region=data['region'],
                    latitude=Decimal(str(data['latitude'])),
                    longitude=Decimal(str(data['longitude'])),
                    best_time_to_visit=data.get('best_time_to_visit', ''),
                    climate=data.get('climate', ''),
                    wildlife=data.get('wildlife', ''),
                    is_featured=data.get('is_featured', False),
                    is_active=True,
                ),
            )
            by_slug[dest.slug] = dest

            # Hero image
            if not self.skip_images and data.get('image_slug') and data.get('image_dir'):
                hero_src = find_seed_image(f"{data['image_slug']}-1", data['image_dir'])
                if hero_src:
                    rel = copy_to_media(hero_src, 'destinations/featured')
                    if rel:
                        dest.featured_image = rel
                        dest.save(update_fields=['featured_image'])

                # Gallery (slug-2, slug-3, …, slug-N)
                # Skip first since it's the hero.
                gallery_count = data.get('gallery_count', 0)
                for i in range(2, gallery_count + 1):
                    src = find_seed_image(f"{data['image_slug']}-{i}", data['image_dir'])
                    if not src:
                        continue
                    rel = copy_to_media(src, 'destinations/gallery')
                    if rel:
                        DestinationImage.objects.get_or_create(
                            destination=dest,
                            image=rel,
                            defaults={'order': i - 1},
                        )

            action = "Created" if created else "Updated"
            self.stdout.write(f"  {action}: {dest.name} ({dest.country})")
        return by_slug

    # =========================================================================

    def _seed_accommodations(self, destinations_by_slug):
        self.stdout.write(self.style.MIGRATE_HEADING("\n--- Accommodations ---"))
        by_slug = {}
        for data in ACCOMMODATIONS:
            destination = destinations_by_slug.get(data['destination_slug'])
            if not destination:
                self.stdout.write(self.style.WARNING(
                    f"  SKIP {data['name']}: no destination '{data['destination_slug']}'"
                ))
                continue

            acc, created = Accommodation.objects.update_or_create(
                name=data['name'],
                defaults=dict(
                    description=data['description'],
                    short_description=data['short'],
                    destination=destination,
                    accommodation_type=data['type'],
                    star_rating=data['stars'],
                    latitude=Decimal(str(data['lat'])),
                    longitude=Decimal(str(data['lng'])),
                    price_per_night_min=Decimal(str(data['price_min'])),
                    price_per_night_max=Decimal(str(data['price_max'])),
                    currency='USD',
                    amenities=data['amenities'],
                    is_featured=data.get('is_featured', False),
                    is_active=True,
                ),
            )
            by_slug[acc.slug] = acc

            # Featured image — accommodations live under accommodations/ folder
            if not self.skip_images and data.get('image_slug'):
                src = find_seed_image(data['image_slug'], 'accommodations')
                if src:
                    rel = copy_to_media(src, 'accommodations/featured')
                    if rel:
                        acc.featured_image = rel
                        acc.save(update_fields=['featured_image'])

        self.stdout.write(f"  Done — {len(by_slug)} accommodations.")
        return by_slug

    # =========================================================================

    def _seed_activities(self, destinations_by_slug):
        self.stdout.write(self.style.MIGRATE_HEADING("\n--- Activities ---"))
        by_slug = {}
        for data in ACTIVITIES:
            destination = destinations_by_slug.get(data['destination_slug'])
            if not destination:
                self.stdout.write(self.style.WARNING(
                    f"  SKIP {data['name']}: no destination '{data['destination_slug']}'"
                ))
                continue

            activity, created = Activity.objects.update_or_create(
                name=data['name'],
                defaults=dict(
                    description=data['description'],
                    short_description=data['short_description'],
                    destination=destination,
                    category=data['category'],
                    difficulty=data['difficulty'],
                    duration=Decimal(str(data['duration'])),
                    duration_unit=data['duration_unit'],
                    price_per_person=Decimal(str(data['price_per_person'])),
                    currency='USD',
                    requirements=data.get('requirements', ''),
                    included_items=data.get('included_items', ''),
                    excluded_items=data.get('excluded_items', ''),
                    best_season=data.get('best_season', ''),
                    is_featured=data.get('is_featured', False),
                    is_active=True,
                ),
            )
            by_slug[activity.slug] = activity

            if not self.skip_images and data.get('image_slug') and data.get('image_dir'):
                src = find_seed_image(data['image_slug'], data['image_dir'])
                if src:
                    rel = copy_to_media(src, 'activities/featured')
                    if rel:
                        activity.featured_image = rel
                        activity.save(update_fields=['featured_image'])

        self.stdout.write(f"  Done — {len(by_slug)} activities.")
        return by_slug

    # =========================================================================

    def _seed_packages(self, destinations_by_slug, accommodations_by_slug, activities_by_slug):
        self.stdout.write(self.style.MIGRATE_HEADING("\n--- Tour packages ---"))
        for data in PACKAGES:
            pkg, created = Package.objects.update_or_create(
                name=data['name'],
                defaults=dict(
                    description=data['description'],
                    short_description=data['short_description'],
                    highlights=data['highlights'],
                    duration_days=data['duration_days'],
                    duration_nights=data['duration_nights'],
                    category=data['category'],
                    difficulty_level=data['difficulty'],
                    group_size_min=data['group_min'],
                    group_size_max=data['group_max'],
                    price_per_person=Decimal(str(data['price_per_person'])),
                    currency=data.get('currency', 'USD'),
                    included_items=data['included'],
                    excluded_items=data['excluded'],
                    requirements=data['requirements'],
                    is_featured=data.get('is_featured', False),
                    is_customizable=data.get('is_customizable', True),
                    is_active=True,
                    availability_status='available',
                ),
            )

            # M2M destinations
            destinations = [
                destinations_by_slug[s] for s in data['destination_slugs']
                if s in destinations_by_slug
            ]
            pkg.destinations.set(destinations)

            # Image
            if not self.skip_images and data.get('image_slug') and data.get('image_dir'):
                src = find_seed_image(data['image_slug'], data['image_dir'])
                if src:
                    rel = copy_to_media(src, 'packages')
                    if rel:
                        pkg.featured_image = rel
                        pkg.save(update_fields=['featured_image'])

            # Itinerary — wipe + rebuild (safer than diffing day numbers)
            PackageItinerary.objects.filter(package=pkg).delete()
            for entry in data['itinerary']:
                accommodation = None
                if entry.get('accommodation_slug'):
                    accommodation = accommodations_by_slug.get(entry['accommodation_slug'])
                PackageItinerary.objects.create(
                    package=pkg,
                    day_number=entry['day'],
                    title=entry['title'],
                    description=entry['description'],
                    accommodation=accommodation,
                    breakfast_included=entry.get('breakfast', False),
                    lunch_included=entry.get('lunch', False),
                    dinner_included=entry.get('dinner', False),
                    highlights=entry.get('highlights', ''),
                    order=entry['day'],
                )

            action = "Created" if created else "Updated"
            self.stdout.write(
                f"  {action}: {pkg.name} ({pkg.duration_days}D/{pkg.duration_nights}N, "
                f"{len(destinations)} destinations, {len(data['itinerary'])} itinerary days)"
            )

    # =========================================================================

    def _seed_testimonials(self):
        self.stdout.write(self.style.MIGRATE_HEADING("\n--- Testimonials ---"))
        for data in TESTIMONIALS:
            Testimonial.objects.update_or_create(
                customer_name=data['customer_name'],
                defaults=dict(
                    customer_location=data['customer_location'],
                    rating=data['rating'],
                    quote=data['quote'],
                    is_featured=data.get('is_featured', False),
                    is_active=True,
                ),
            )
        self.stdout.write(f"  Done — {len(TESTIMONIALS)} testimonials.")

    # =========================================================================

    def _seed_faqs(self):
        self.stdout.write(self.style.MIGRATE_HEADING("\n--- FAQs ---"))
        for data in FAQS:
            FAQ.objects.update_or_create(
                question=data['question'],
                defaults=dict(
                    answer=data['answer'],
                    category=data['category'],
                    is_featured=data.get('is_featured', False),
                    order=data.get('order', 0),
                    is_active=True,
                ),
            )
        self.stdout.write(f"  Done — {len(FAQS)} FAQs.")

    # =========================================================================

    def _print_summary(self):
        self.stdout.write("")
        rows = [
            ("Destinations",      Destination.objects.count()),
            ("  Tanzania",        Destination.objects.filter(country='Tanzania').count()),
            ("  Other countries", Destination.objects.exclude(country='Tanzania').count()),
            ("DestinationImages", DestinationImage.objects.count()),
            ("Accommodations",    Accommodation.objects.count()),
            ("  with images",     Accommodation.objects.exclude(featured_image='').count()),
            ("Activities",        Activity.objects.count()),
            ("Packages",          Package.objects.count()),
            ("PackageItineraries", PackageItinerary.objects.count()),
            ("Testimonials",      Testimonial.objects.count()),
            ("FAQs",              FAQ.objects.count()),
        ]
        for label, count in rows:
            self.stdout.write(f"  {label:25s}: {count}")

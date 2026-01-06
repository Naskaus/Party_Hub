"""
Seed script to create DeliverableTemplates and test Events.
Run with: python manage.py shell < seed_events.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from datetime import date, timedelta
from apps.venues.models import Bar
from apps.planning.models import DeliverableTemplate, Event, ThemePeriod
from apps.accounts.models import User

# Create DeliverableTemplates based on bar hardware specs
for bar in Bar.objects.all():
    specs = bar.hardware_specs
    
    # Create templates for screens
    for screen in specs.get('screens', []):
        obj, created = DeliverableTemplate.objects.get_or_create(
            name=screen['name'],
            bar=bar,
            defaults={
                'specs': f"{screen.get('resolution', '')} {screen.get('format', 'mp4')}",
                'category': 'screen',
                'is_default': True
            }
        )
        if created:
            print(f"  Created template: {obj}")
    
    # Create templates for print
    for print_item in specs.get('print', []):
        obj, created = DeliverableTemplate.objects.get_or_create(
            name=print_item['name'],
            bar=bar,
            defaults={
                'specs': f"{print_item.get('size', '')} {print_item.get('dpi', 300)}dpi {print_item.get('format', 'pdf')}",
                'category': 'print',
                'is_default': True
            }
        )
        if created:
            print(f"  Created template: {obj}")

print(f"\nTotal templates: {DeliverableTemplate.objects.count()}")

# Create test events
admin_user = User.objects.filter(is_superuser=True).first()
theme = ThemePeriod.objects.filter(month=1, year=2026).first()

# Event in 3 days (past J-7 deadline - should be RED)
event1, created = Event.objects.get_or_create(
    name='Late Night DJ Session',
    date=date.today() + timedelta(days=3),
    defaults={
        'description': 'A test event that is past the J-7 deadline',
        'theme': theme,
        'created_by': admin_user
    }
)
if created:
    event1.bars.add(Bar.objects.get(name='Neon Club'))
    print(f"Created event: {event1} - should be RED (past deadline)")

# Event in 14 days (before J-7 deadline - should be ORANGE)
event2, created = Event.objects.get_or_create(
    name='Weekend Special',
    date=date.today() + timedelta(days=14),
    defaults={
        'description': 'A test event with time before deadline',
        'theme': theme,
        'created_by': admin_user
    }
)
if created:
    event2.bars.add(Bar.objects.get(name='Skyline Rooftop'))
    print(f"Created event: {event2} - should be ORANGE (in progress)")

# Event in 21 days with multiple bars
event3, created = Event.objects.get_or_create(
    name='Monthly Theme Party',
    date=date.today() + timedelta(days=21),
    defaults={
        'description': 'Main monthly event',
        'brief': 'Neon Dreams theme - use cyberpunk colors',
        'theme': theme,
        'created_by': admin_user
    }
)
if created:
    event3.bars.add(Bar.objects.get(name='Neon Club'), Bar.objects.get(name='Underground'))
    print(f"Created event: {event3} - multiple bars")

print(f"\nTotal events: {Event.objects.count()}")
print("Done!")

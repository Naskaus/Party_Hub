"""
Seed script with REAL business data for Phil's bars.
Run with: python seed_real_data.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from datetime import date
from apps.venues.models import Bar
from apps.planning.models import DeliverableTemplate, Event, ThemePeriod, EventDeliverable
from apps.accounts.models import User

# Clear existing test data
print("Clearing existing test data...")
Event.objects.all().delete()
DeliverableTemplate.objects.all().delete()
Bar.objects.all().delete()
ThemePeriod.objects.all().delete()

# =============================================================================
# BARS - Real venues
# =============================================================================
print("\n=== Creating Bars ===")

# Bangkok bars
bars_bkk = [
    {
        'name': 'Red Dragon',
        'location': 'Bangkok',
        'hardware_specs': {
            'screens': [
                {'name': 'Main LED Wall', 'resolution': '3840x2160', 'format': 'mp4'},
                {'name': 'DJ Booth Screen', 'resolution': '1920x1080', 'format': 'mp4'},
                {'name': 'Bar TV', 'resolution': '1920x1080', 'format': 'jpg'}
            ],
            'print': [
                {'name': 'Poster A3', 'size': 'A3', 'dpi': 300, 'format': 'pdf'},
                {'name': 'Flyer A5', 'size': 'A5', 'dpi': 300, 'format': 'pdf'}
            ]
        }
    },
    {
        'name': 'Mandarin',
        'location': 'Bangkok',
        'hardware_specs': {
            'screens': [
                {'name': 'Entrance LED', 'resolution': '1920x1080', 'format': 'mp4'},
                {'name': 'VIP Screen', 'resolution': '1920x1080', 'format': 'mp4'}
            ],
            'print': [
                {'name': 'Menu Card', 'size': 'A5', 'dpi': 300, 'format': 'pdf'},
                {'name': 'Table Tent', 'size': 'Custom', 'dpi': 300, 'format': 'pdf'}
            ]
        }
    },
    {
        'name': 'Shark',
        'location': 'Bangkok',
        'hardware_specs': {
            'screens': [
                {'name': 'Dance Floor LED', 'resolution': '2560x1440', 'format': 'mp4'},
                {'name': 'Bar Screen', 'resolution': '1920x1080', 'format': 'jpg'}
            ],
            'print': [
                {'name': 'Poster A2', 'size': 'A2', 'dpi': 300, 'format': 'pdf'}
            ]
        }
    },
]

# Pattaya bars
bars_pattaya = [
    {
        'name': 'Bliss',
        'location': 'Pattaya',
        'hardware_specs': {
            'screens': [
                {'name': 'Stage LED', 'resolution': '1920x1080', 'format': 'mp4'},
                {'name': 'Entrance Screen', 'resolution': '1080x1920', 'format': 'mp4'}
            ],
            'print': [
                {'name': 'Flyer A6', 'size': 'A6', 'dpi': 300, 'format': 'pdf'}
            ]
        }
    },
    {
        'name': 'Shark Pattaya',
        'location': 'Pattaya',
        'hardware_specs': {
            'screens': [
                {'name': 'Main Screen', 'resolution': '1920x1080', 'format': 'mp4'}
            ],
            'print': [
                {'name': 'Poster A3', 'size': 'A3', 'dpi': 300, 'format': 'pdf'}
            ]
        }
    },
    {
        'name': 'Fahrenheit',
        'location': 'Pattaya',
        'hardware_specs': {
            'screens': [
                {'name': 'DJ Screen', 'resolution': '1920x1080', 'format': 'mp4'},
                {'name': 'VIP LED', 'resolution': '1280x720', 'format': 'mp4'}
            ],
            'print': [
                {'name': 'Poster A3', 'size': 'A3', 'dpi': 300, 'format': 'pdf'},
                {'name': 'Wristband Design', 'size': 'Custom', 'dpi': 300, 'format': 'pdf'}
            ]
        }
    },
    {
        'name': 'Geisha',
        'location': 'Pattaya',
        'hardware_specs': {
            'screens': [
                {'name': 'Lounge Screen', 'resolution': '1920x1080', 'format': 'mp4'}
            ],
            'print': [
                {'name': 'Menu A4', 'size': 'A4', 'dpi': 300, 'format': 'pdf'}
            ]
        }
    },
]

# Create all bars
all_bars = bars_bkk + bars_pattaya
created_bars = {}
for bar_data in all_bars:
    bar = Bar.objects.create(**bar_data)
    created_bars[bar.name] = bar
    print(f"  ✓ Created: {bar.name} ({bar.location}) - {bar.screen_count} screens")

# =============================================================================
# DELIVERABLE TEMPLATES - Based on bar hardware
# =============================================================================
print("\n=== Creating Deliverable Templates ===")

for bar in Bar.objects.all():
    specs = bar.hardware_specs
    
    for screen in specs.get('screens', []):
        DeliverableTemplate.objects.create(
            name=screen['name'],
            bar=bar,
            specs=f"{screen.get('resolution', '')} {screen.get('format', 'mp4')}",
            category='screen',
            is_default=True
        )
    
    for print_item in specs.get('print', []):
        DeliverableTemplate.objects.create(
            name=print_item['name'],
            bar=bar,
            specs=f"{print_item.get('size', '')} {print_item.get('dpi', 300)}dpi {print_item.get('format', 'pdf')}",
            category='print',
            is_default=True
        )

print(f"  ✓ Created {DeliverableTemplate.objects.count()} deliverable templates")

# =============================================================================
# THEMES - Q1 2026
# =============================================================================
print("\n=== Creating Themes ===")

themes = [
    {
        'name': 'Eden Reborn',
        'description': 'Forest/village ambiance. Natural elements, greenery, mystical lighting.',
        'month': 1, 'year': 2026,
        'primary_color': '#22c55e',  # Green
        'accent_color': '#a3e635'    # Lime
    },
    {
        'name': 'Japanese Holidays + Valentine',
        'description': 'Japanese aesthetics meets romantic Valentine vibes. Cherry blossoms, lanterns, hearts.',
        'month': 2, 'year': 2026,
        'primary_color': '#f43f5e',  # Rose
        'accent_color': '#fda4af'    # Pink
    },
    {
        'name': 'Carnival / Mardi Gras',
        'description': 'French touch carnival. Feathers, masks, gold, purple, green.',
        'month': 3, 'year': 2026,
        'primary_color': '#a855f7',  # Purple
        'accent_color': '#fbbf24'    # Gold
    },
    {
        'name': 'Songkran',
        'description': 'Thai New Year water festival. Blue, white, traditional Thai elements.',
        'month': 4, 'year': 2026,
        'primary_color': '#06b6d4',  # Cyan
        'accent_color': '#f472b6'    # Pink
    },
    {
        'name': 'May Theme TBD',
        'description': 'Theme to be confirmed.',
        'month': 5, 'year': 2026,
        'primary_color': '#8b5cf6',  # Violet
        'accent_color': '#c4b5fd'    # Light violet
    },
]

for theme_data in themes:
    theme = ThemePeriod.objects.create(**theme_data)
    print(f"  ✓ {theme.get_month_display()} 2026: {theme.name}")

# =============================================================================
# EVENTS - January 2026
# =============================================================================
print("\n=== Creating January 2026 Events ===")

admin_user = User.objects.filter(is_superuser=True).first()
jan_theme = ThemePeriod.objects.get(month=1, year=2026)

# Bangkok bars
bkk_bars = list(Bar.objects.filter(location='Bangkok'))
pattaya_bars = list(Bar.objects.filter(location='Pattaya'))
all_bar_list = list(Bar.objects.all())

january_events = [
    {
        'name': 'Full Moon Party',
        'date': date(2026, 1, 3),
        'description': 'Monthly full moon celebration',
        'brief': 'Eden Reborn theme - forest vibes, natural elements',
        'bars': all_bar_list  # All bars
    },
    {
        'name': 'Ange et Démon',
        'date': date(2026, 1, 10),
        'description': 'Angels & Demons themed night',
        'brief': 'White vs Black. Angel wings, devil horns. Heaven and Hell decor.',
        'bars': bkk_bars  # BKK only
    },
    {
        'name': 'Eden Forest Night',
        'date': date(2026, 1, 17),
        'description': 'Theme night - Eden Reborn showcase',
        'brief': 'Full forest immersion. LED vines, ambient nature sounds.',
        'bars': all_bar_list
    },
    {
        'name': 'VIP Private Event',
        'date': date(2026, 1, 24),
        'description': 'Private VIP event - Red Dragon only',
        'brief': 'Exclusive private party. Minimal deliverables needed.',
        'bars': [created_bars['Red Dragon']]
    },
]

for event_data in january_events:
    bars = event_data.pop('bars')
    event = Event.objects.create(
        **event_data,
        theme=jan_theme,
        created_by=admin_user
    )
    event.bars.set(bars)
    print(f"  ✓ Jan {event.date.day}: {event.name} ({event.deliverables.count()} deliverables)")

# =============================================================================
# EVENTS - February 2026
# =============================================================================
print("\n=== Creating February 2026 Events ===")

feb_theme = ThemePeriod.objects.get(month=2, year=2026)

february_events = [
    {
        'name': 'Full Moon Party',
        'date': date(2026, 2, 2),
        'description': 'February full moon',
        'brief': 'Japanese/Valentine theme mix',
        'bars': all_bar_list
    },
    {
        'name': "Valentine's Night",
        'date': date(2026, 2, 14),
        'description': 'St-Valentine special',
        'brief': 'Romantic vibes. Hearts, roses, couple promotions.',
        'bars': all_bar_list
    },
    {
        'name': 'Chinese New Year',
        'date': date(2026, 2, 17),
        'description': 'CNY celebration - Year of the Snake',
        'brief': 'Red & gold. Dragons, lanterns, lucky money.',
        'bars': bkk_bars  # Mainly BKK
    },
    {
        'name': 'End of CNY Party',
        'date': date(2026, 2, 19),
        'description': 'Closing Chinese New Year festivities',
        'brief': 'Last night of CNY celebrations',
        'bars': bkk_bars
    },
]

for event_data in february_events:
    bars = event_data.pop('bars')
    event = Event.objects.create(
        **event_data,
        theme=feb_theme,
        created_by=admin_user
    )
    event.bars.set(bars)
    print(f"  ✓ Feb {event.date.day}: {event.name} ({event.deliverables.count()} deliverables)")

# =============================================================================
# EVENTS - March 2026
# =============================================================================
print("\n=== Creating March 2026 Events ===")

mar_theme = ThemePeriod.objects.get(month=3, year=2026)

march_events = [
    {
        'name': 'Full Moon / Mardi Gras',
        'date': date(2026, 3, 3),
        'description': 'Carnival Mardi Gras celebration',
        'brief': 'French touch carnival. Feathers, masks, beads, jazz.',
        'bars': all_bar_list
    },
    {
        'name': 'Masquerade Night',
        'date': date(2026, 3, 14),
        'description': 'Masked ball theme',
        'brief': 'Venetian masks, elegant dress code.',
        'bars': bkk_bars
    },
]

for event_data in march_events:
    bars = event_data.pop('bars')
    event = Event.objects.create(
        **event_data,
        theme=mar_theme,
        created_by=admin_user
    )
    event.bars.set(bars)
    print(f"  ✓ Mar {event.date.day}: {event.name} ({event.deliverables.count()} deliverables)")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "="*50)
print("SEED COMPLETE!")
print("="*50)
print(f"Bars: {Bar.objects.count()}")
print(f"  - Bangkok: {Bar.objects.filter(location='Bangkok').count()}")
print(f"  - Pattaya: {Bar.objects.filter(location='Pattaya').count()}")
print(f"Themes: {ThemePeriod.objects.count()}")
print(f"Events: {Event.objects.count()}")
print(f"Deliverable Templates: {DeliverableTemplate.objects.count()}")
print(f"Event Deliverables: {EventDeliverable.objects.count()}")

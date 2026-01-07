#!/usr/bin/env python
"""
Seed script for simplified Party Hub data.

Creates:
- Global hardware items
- Global deliverable templates  
- Bars with assigned hardware

Run with: python seed_simplified.py
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.venues.models import Bar, HardwareItem
from apps.planning.models import DeliverableTemplate


def clear_data():
    """Clear existing data."""
    print("Clearing existing data...")
    DeliverableTemplate.objects.all().delete()
    Bar.objects.all().delete()
    HardwareItem.objects.all().delete()


def create_hardware():
    """Create global hardware items."""
    print("\n=== Creating Hardware Items ===")
    
    hardware_list = [
        # Screens
        {'name': 'Giant LED 320x128cm', 'specs': ''},
        {'name': 'Cube LED', 'specs': '960x192'},
        {'name': 'Circle LED', 'specs': ''},
        {'name': '16:9 TV', 'specs': '1920x1080'},
        {'name': '9:16 TV', 'specs': '1080x1920'},
        {'name': 'Door LED', 'specs': ''},
        {'name': 'Big Vertical LED', 'specs': ''},
        {'name': 'Big Square LED', 'specs': ''},
    ]
    
    items = {}
    for hw in hardware_list:
        item, created = HardwareItem.objects.get_or_create(
            name=hw['name'],
            defaults={'specs': hw['specs']}
        )
        items[hw['name']] = item
        status = "✓ Created" if created else "→ Exists"
        print(f"  {status}: {item.name}")
    
    return items


def create_deliverables():
    """Create global deliverable templates."""
    print("\n=== Creating Deliverable Templates ===")
    
    templates = [
        # Print
        {'name': 'Poster A3', 'specs': 'A3 300dpi', 'category': 'print'},
        
        # Social
        {'name': 'Reel Video', 'specs': '9:16 1080x1920', 'category': 'social'},
        
        # Screen videos
        {'name': 'Video 16:9 TV', 'specs': '1920x1080 mp4', 'category': 'screen'},
        {'name': 'Video Cube LED', 'specs': '960x192 mp4', 'category': 'screen'},
        {'name': 'Video Circle LED', 'specs': 'mp4', 'category': 'screen'},
        {'name': 'Video Giant LED', 'specs': 'mp4', 'category': 'screen'},
        {'name': 'Video Door LED', 'specs': 'mp4', 'category': 'screen'},
        {'name': 'Video Big Vertical LED', 'specs': '9:16 mp4', 'category': 'screen'},
        {'name': 'Video Big Square LED', 'specs': '1:1 mp4', 'category': 'screen'},
        {'name': 'Video 9:16 TV', 'specs': '1080x1920 mp4', 'category': 'screen'},
    ]
    
    for t in templates:
        obj, created = DeliverableTemplate.objects.get_or_create(
            name=t['name'],
            defaults={'specs': t['specs'], 'category': t['category']}
        )
        status = "✓ Created" if created else "→ Exists"
        print(f"  {status}: {obj.name}")


def create_bars(hardware):
    """Create bars with their hardware assignments."""
    print("\n=== Creating Bars ===")
    
    bars_config = [
        {
            'name': 'Red Dragon',
            'location': 'Bangkok',
            'hardware': ['Giant LED 320x128cm', 'Cube LED', 'Circle LED', '16:9 TV']
        },
        {
            'name': 'Shark',
            'location': 'Bangkok',
            'hardware': ['Door LED', 'Cube LED', 'Circle LED', '16:9 TV']
        },
        {
            'name': 'Mandarin',
            'location': 'Bangkok',
            'hardware': ['Big Vertical LED']
        },
        {
            'name': 'Shark Pattaya',
            'location': 'Pattaya',
            'hardware': ['Door LED', 'Cube LED', 'Circle LED', '16:9 TV']
        },
        {
            'name': 'Fahrenheit',
            'location': 'Pattaya',
            'hardware': ['Big Square LED', 'Cube LED', '16:9 TV', '9:16 TV']
        },
        {
            'name': 'Bliss',
            'location': 'Pattaya',
            'hardware': []  # No change for now
        },
        {
            'name': 'Geisha',
            'location': 'Pattaya',
            'hardware': []  # No change for now
        },
    ]
    
    for bar_data in bars_config:
        bar, created = Bar.objects.get_or_create(
            name=bar_data['name'],
            defaults={'location': bar_data['location']}
        )
        
        # Clear and reassign hardware
        bar.hardware.clear()
        for hw_name in bar_data['hardware']:
            if hw_name in hardware:
                bar.hardware.add(hardware[hw_name])
        
        status = "✓ Created" if created else "→ Updated"
        hw_count = bar.hardware.count()
        print(f"  {status}: {bar.name} ({bar.location}) - {hw_count} hardware items")


def main():
    print("=" * 50)
    print("PARTY HUB - SIMPLIFIED SEED DATA")
    print("=" * 50)
    
    clear_data()
    hardware = create_hardware()
    create_deliverables()
    create_bars(hardware)
    
    print("\n" + "=" * 50)
    print("SEED COMPLETE!")
    print("=" * 50)
    print(f"Hardware Items: {HardwareItem.objects.count()}")
    print(f"Deliverable Templates: {DeliverableTemplate.objects.count()}")
    print(f"Bars: {Bar.objects.count()}")


if __name__ == '__main__':
    main()

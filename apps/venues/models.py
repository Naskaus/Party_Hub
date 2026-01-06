"""
Models for the venues app.

Contains Bar model for venue/location management with hardware specifications.
"""

from django.db import models


class Bar(models.Model):
    """
    Represents a bar/venue where events take place.
    
    Each bar has specific hardware (screens, LED displays) that determines
    what types of deliverables are needed for events at that location.
    
    Attributes:
        name: Display name of the bar
        location: City/address
        hardware_specs: JSON containing available screens and their specs
        is_active: Whether this bar is currently active
    
    Example hardware_specs:
        {
            "screens": [
                {"name": "Cube LED", "resolution": "1024x1024", "format": "mp4"},
                {"name": "Door LED", "resolution": "1920x1080", "format": "mp4"},
                {"name": "Bar TV", "resolution": "1920x1080", "format": "jpg"}
            ],
            "print": [
                {"name": "Poster A3", "size": "A3", "dpi": 300, "format": "pdf"},
                {"name": "Flyer A5", "size": "A5", "dpi": 300, "format": "pdf"}
            ]
        }
    """
    
    name = models.CharField(
        max_length=100,
        help_text="Name of the bar/venue"
    )
    
    location = models.CharField(
        max_length=200,
        blank=True,
        help_text="City or address of the venue"
    )
    
    hardware_specs = models.JSONField(
        default=dict,
        blank=True,
        help_text="JSON containing screen and print specifications"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this bar is currently active"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Bar'
        verbose_name_plural = 'Bars'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    @property
    def screen_count(self):
        """Return the number of screens configured for this bar."""
        screens = self.hardware_specs.get('screens', [])
        return len(screens)
    
    @property
    def has_print_deliverables(self):
        """Check if this bar requires print deliverables."""
        return bool(self.hardware_specs.get('print', []))
    
    def get_deliverable_types(self):
        """
        Return a flat list of all deliverable types for this bar.
        
        Used to auto-generate EventDeliverables when creating events.
        """
        types = []
        
        for screen in self.hardware_specs.get('screens', []):
            types.append({
                'category': 'screen',
                'name': screen.get('name'),
                'specs': f"{screen.get('resolution')} {screen.get('format', 'mp4')}"
            })
        
        for print_item in self.hardware_specs.get('print', []):
            types.append({
                'category': 'print',
                'name': print_item.get('name'),
                'specs': f"{print_item.get('size')} {print_item.get('dpi', 300)}dpi {print_item.get('format', 'pdf')}"
            })
        
        return types


class HardwareItem(models.Model):
    """
    Individual hardware or asset specification for a bar.
    
    Replaces the JSON-based hardware_specs for better admin editing.
    
    Categories:
        - screen: Digital displays, LED walls, TVs
        - print: Posters, flyers, printed materials
        - deco: Decoration ideas and references
        - uniform: Staff uniform ideas and references
    """
    
    class Category(models.TextChoices):
        SCREEN = 'screen', 'Screen / Display'
        PRINT = 'print', 'Print Material'
        DECO = 'deco', 'Decoration Idea'
        UNIFORM = 'uniform', 'Uniform Idea'
    
    bar = models.ForeignKey(
        Bar,
        on_delete=models.CASCADE,
        related_name='hardware_items'
    )
    
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.SCREEN
    )
    
    name = models.CharField(
        max_length=100,
        help_text="Name of the item (e.g., 'Main LED Wall', 'Staff Polo')"
    )
    
    specs = models.CharField(
        max_length=200,
        blank=True,
        help_text="Specifications (e.g., '1920x1080 mp4', 'A3 300dpi pdf')"
    )
    
    notes = models.TextField(
        blank=True,
        help_text="Additional notes or description"
    )
    
    # For deco/uniform: reference image
    reference_image = models.ImageField(
        upload_to='hardware_refs/',
        blank=True,
        null=True,
        help_text="Reference image for decoration or uniform ideas"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this item is currently in use"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Hardware Item'
        verbose_name_plural = 'Hardware Items'
        ordering = ['bar', 'category', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.bar.name})"


"""
Models for the venues app.

Contains Bar and HardwareItem models for venue/location management.
"""

from django.db import models


class HardwareItem(models.Model):
    """
    Global hardware/screen item that can be assigned to multiple bars.
    
    Examples: Cube LED, Giant LED, 16:9 TV, Circle LED, etc.
    """
    
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Name of the hardware (e.g., 'Cube LED', 'Giant LED')"
    )
    
    specs = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional specs (e.g., '960x192 mp4')"
    )
    
    notes = models.TextField(
        blank=True,
        help_text="Additional notes"
    )
    
    class Meta:
        verbose_name = 'Hardware Item'
        verbose_name_plural = 'Hardware Items'
        ordering = ['name']
    
    def __str__(self):
        if self.specs:
            return f"{self.name} ({self.specs})"
        return self.name


class Bar(models.Model):
    """
    Represents a bar/venue where events take place.
    
    Each bar can have multiple hardware items assigned to it.
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
    
    hardware = models.ManyToManyField(
        HardwareItem,
        blank=True,
        related_name='bars',
        help_text="Hardware items available at this bar"
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
    def hardware_count(self):
        """Return the number of hardware items."""
        return self.hardware.count()

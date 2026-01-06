"""
Admin configuration for venues app.

Provides admin interface for Bar model management.
"""

from django.contrib import admin
from django.utils.html import format_html

from .models import Bar


@admin.register(Bar)
class BarAdmin(admin.ModelAdmin):
    """Admin interface for Bar model with hardware specs display."""
    
    list_display = ('name', 'location', 'screen_count_display', 'is_active', 'updated_at')
    list_filter = ('is_active', 'location')
    search_fields = ('name', 'location')
    ordering = ('name',)
    
    fieldsets = (
        (None, {
            'fields': ('name', 'location', 'is_active')
        }),
        ('Hardware Specifications', {
            'fields': ('hardware_specs',),
            'description': 'JSON configuration for screens and print materials. '
                          'See model documentation for format.'
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def screen_count_display(self, obj):
        """Display screen count with badge styling."""
        count = obj.screen_count
        if count > 0:
            return format_html(
                '<span style="background: #16a34a; color: white; padding: 2px 8px; '
                'border-radius: 10px;">{} screens</span>',
                count
            )
        return format_html(
            '<span style="background: #6b7280; color: white; padding: 2px 8px; '
            'border-radius: 10px;">No screens</span>'
        )
    screen_count_display.short_description = 'Hardware'
    
    def get_queryset(self, request):
        """Optimize queryset."""
        return super().get_queryset(request)

"""
Admin configuration for venues app.

Provides admin interface for Bar and HardwareItem models.
"""

from django.contrib import admin
from django.utils.html import format_html

from .models import Bar, HardwareItem


@admin.register(HardwareItem)
class HardwareItemAdmin(admin.ModelAdmin):
    """Admin for global HardwareItem pool."""
    list_display = ('name', 'specs', 'bar_count')
    search_fields = ('name', 'specs')
    ordering = ('name',)
    
    def bar_count(self, obj):
        count = obj.bars.count()
        return f"{count} bars"
    bar_count.short_description = 'Used by'


@admin.register(Bar)
class BarAdmin(admin.ModelAdmin):
    """Admin interface for Bar with hardware selection."""
    
    list_display = ('name', 'location', 'hardware_display', 'is_active')
    list_filter = ('is_active', 'location')
    search_fields = ('name', 'location')
    filter_horizontal = ('hardware',)  # Nice M2M widget
    ordering = ('name',)
    
    fieldsets = (
        (None, {
            'fields': ('name', 'location', 'is_active')
        }),
        ('Hardware', {
            'fields': ('hardware',),
            'description': 'Select hardware items available at this bar'
        }),
    )
    
    def hardware_display(self, obj):
        """Show hardware as badges."""
        items = obj.hardware.all()[:4]
        if not items:
            return format_html('<span style="color: #999;">None</span>')
        
        badges = []
        for item in items:
            badges.append(f'<span style="background: #3b82f6; color: white; '
                         f'padding: 2px 6px; border-radius: 8px; font-size: 11px; '
                         f'margin-right: 4px;">{item.name}</span>')
        
        extra = obj.hardware.count() - 4
        if extra > 0:
            badges.append(f'<span style="color: #999;">+{extra}</span>')
        
        return format_html(''.join(badges))
    hardware_display.short_description = 'Hardware'

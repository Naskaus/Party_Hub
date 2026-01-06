"""
Admin configuration for venues app.

Provides admin interface for Bar and HardwareItem models.
"""

from django.contrib import admin
from django.utils.html import format_html

from .models import Bar, HardwareItem


class HardwareItemInline(admin.TabularInline):
    """Inline admin for HardwareItems within Bar."""
    model = HardwareItem
    extra = 1  # Show one empty row for adding
    fields = ('category', 'name', 'specs', 'notes', 'reference_image', 'is_active')
    ordering = ('category', 'name')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('bar')


@admin.register(HardwareItem)
class HardwareItemAdmin(admin.ModelAdmin):
    """Standalone admin for HardwareItem."""
    list_display = ('name', 'bar', 'category', 'specs', 'is_active')
    list_filter = ('category', 'bar', 'is_active')
    search_fields = ('name', 'specs', 'bar__name')
    ordering = ('bar', 'category', 'name')


@admin.register(Bar)
class BarAdmin(admin.ModelAdmin):
    """Admin interface for Bar model with hardware items inline."""
    
    list_display = ('name', 'location', 'hardware_count_display', 'is_active', 'updated_at')
    list_filter = ('is_active', 'location')
    search_fields = ('name', 'location')
    ordering = ('name',)
    
    fieldsets = (
        (None, {
            'fields': ('name', 'location', 'is_active')
        }),
        ('Legacy Hardware Specs (JSON)', {
            'fields': ('hardware_specs',),
            'classes': ('collapse',),  # Collapse by default
            'description': 'Legacy JSON format. Use the inline table below instead.'
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    inlines = [HardwareItemInline]
    
    def hardware_count_display(self, obj):
        """Display hardware item count by category."""
        counts = {}
        for item in obj.hardware_items.filter(is_active=True):
            cat = item.get_category_display()
            counts[cat] = counts.get(cat, 0) + 1
        
        if not counts:
            return format_html(
                '<span style="background: #6b7280; color: white; padding: 2px 8px; '
                'border-radius: 10px;">No items</span>'
            )
        
        badges = []
        colors = {
            'Screen / Display': '#3b82f6',
            'Print Material': '#16a34a',
            'Decoration Idea': '#f59e0b',
            'Uniform Idea': '#8b5cf6'
        }
        for cat, count in counts.items():
            color = colors.get(cat, '#6b7280')
            badges.append(f'<span style="background: {color}; color: white; padding: 2px 6px; '
                         f'border-radius: 8px; font-size: 11px; margin-right: 4px;">'
                         f'{count} {cat.split()[0]}</span>')
        
        return format_html(''.join(badges))
    hardware_count_display.short_description = 'Hardware'


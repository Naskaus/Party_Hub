"""
Admin configuration for planning app.

Provides admin interface for ThemePeriod, Event, and Deliverable models.
"""

from django.contrib import admin
from django.utils.html import format_html

from .models import ThemePeriod, Event, DeliverableTemplate, EventDeliverable


class EventDeliverableInline(admin.TabularInline):
    """Inline admin for EventDeliverables within Event."""
    model = EventDeliverable
    extra = 0
    fields = ('template', 'status', 'assigned_to', 'is_enabled', 'notes')
    readonly_fields = ('template',)
    
    def has_add_permission(self, request, obj=None):
        return False  # Deliverables are auto-generated


@admin.register(ThemePeriod)
class ThemePeriodAdmin(admin.ModelAdmin):
    """Admin interface for ThemePeriod with color picker."""
    
    list_display = ('name', 'period_display', 'color_preview', 'is_active')
    list_filter = ('year', 'is_active')
    search_fields = ('name', 'description')
    ordering = ('-year', '-month')
    
    class Media:
        css = {
            'all': ['admin/css/color-picker.css']  # Optional custom styles
        }
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """Use HTML5 color picker for color fields."""
        if db_field.name in ['primary_color', 'accent_color']:
            from django import forms
            kwargs['widget'] = forms.TextInput(attrs={
                'type': 'color',
                'style': 'width: 100px; height: 40px; padding: 2px; cursor: pointer;'
            })
        return super().formfield_for_dbfield(db_field, request, **kwargs)
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        ('Period', {
            'fields': ('month', 'year', 'is_active')
        }),
        ('Visual Identity', {
            'fields': ('primary_color', 'accent_color'),
            'description': 'Hex colors for the theme visual identity'
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def period_display(self, obj):
        """Display formatted period."""
        return obj.period_display
    period_display.short_description = 'Period'
    
    def color_preview(self, obj):
        """Display color swatches."""
        return format_html(
            '<span style="display: inline-block; width: 20px; height: 20px; '
            'background: {}; border-radius: 4px; margin-right: 4px;"></span>'
            '<span style="display: inline-block; width: 20px; height: 20px; '
            'background: {}; border-radius: 4px;"></span>',
            obj.primary_color or '#ccc',
            obj.accent_color or '#ccc'
        )
    color_preview.short_description = 'Colors'


@admin.register(DeliverableTemplate)
class DeliverableTemplateAdmin(admin.ModelAdmin):
    """Admin interface for DeliverableTemplate."""
    
    list_display = ('name', 'bar', 'category', 'specs', 'is_default')
    list_filter = ('category', 'bar', 'is_default')
    search_fields = ('name', 'specs')
    ordering = ('category', 'name')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'specs', 'category')
        }),
        ('Association', {
            'fields': ('bar', 'is_default'),
            'description': 'Link to a specific bar for hardware-specific deliverables'
        }),
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin interface for Event with health status and inline deliverables."""
    
    list_display = ('name', 'date', 'theme', 'health_badge', 'deadline_display', 'bar_list')
    list_filter = ('date', 'theme', 'bars')
    search_fields = ('name', 'description')
    date_hierarchy = 'date'
    ordering = ('date',)
    filter_horizontal = ('bars',)
    
    fieldsets = (
        (None, {
            'fields': ('name', 'date', 'theme')
        }),
        ('Details', {
            'fields': ('description', 'brief'),
            'classes': ('collapse',)
        }),
        ('Venues', {
            'fields': ('bars',)
        }),
        ('Metadata', {
            'fields': ('created_by',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'created_by')
    inlines = [EventDeliverableInline]
    
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def health_badge(self, obj):
        """Display health status as colored badge."""
        status = obj.health_status
        colors = {
            'green': ('#16a34a', '✓ Ready'),
            'orange': ('#f97316', '◐ In Progress'),
            'red': ('#ef4444', '✗ Late')
        }
        color, text = colors.get(status, ('#6b7280', '?'))
        return format_html(
            '<span style="background: {}; color: white; padding: 2px 8px; '
            'border-radius: 10px; font-size: 11px;">{}</span>',
            color, text
        )
    health_badge.short_description = 'Status'
    
    def deadline_display(self, obj):
        """Display J-7 deadline with countdown."""
        days = obj.days_until_deadline
        if days < 0:
            return format_html(
                '<span style="color: #ef4444;">⚠ {} days overdue</span>',
                abs(days)
            )
        elif days <= 3:
            return format_html(
                '<span style="color: #f97316;">{} in {} days</span>',
                obj.deadline.strftime('%b %d'), days
            )
        return format_html('{} ({} days)', obj.deadline.strftime('%b %d'), days)
    deadline_display.short_description = 'J-7 Deadline'
    
    def bar_list(self, obj):
        """Display list of bars."""
        bars = obj.bars.all()[:3]
        names = ', '.join(b.name for b in bars)
        if obj.bars.count() > 3:
            names += f' +{obj.bars.count() - 3}'
        return names or '-'
    bar_list.short_description = 'Venues'


@admin.register(EventDeliverable)
class EventDeliverableAdmin(admin.ModelAdmin):
    """Admin interface for EventDeliverable."""
    
    list_display = ('template', 'event', 'status_badge', 'is_starred', 'assigned_to', 'is_enabled')
    list_filter = ('status', 'is_starred', 'is_enabled', 'event__date')
    list_editable = ('is_starred',)  # Quick toggle in list view
    search_fields = ('event__name', 'template__name')
    ordering = ('event__date', 'template__name')
    
    def status_badge(self, obj):
        """Display status as colored badge."""
        colors = {
            'todo': '#6b7280',
            'in_progress': '#3b82f6',
            'review': '#eab308',
            'changes': '#ef4444',
            'approved': '#16a34a'
        }
        color = colors.get(obj.status, '#6b7280')
        
        late = ' ⚠' if obj.is_late else ''
        return format_html(
            '<span style="background: {}; color: white; padding: 2px 8px; '
            'border-radius: 10px; font-size: 11px;">{}{}</span>',
            color, obj.get_status_display(), late
        )
    status_badge.short_description = 'Status'


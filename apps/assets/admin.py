"""
Admin configuration for assets app.
"""

from django.contrib import admin
from django.utils.html import format_html

from .models import Asset


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    """Admin interface for Asset with preview."""
    
    list_display = ('thumbnail_preview', 'original_filename', 'file_type', 'deliverable_link', 'file_size_display', 'is_approved', 'created_at')
    list_filter = ('file_type', 'is_approved', 'created_at')
    search_fields = ('original_filename', 'deliverable__event__name', 'deliverable__template__name')
    ordering = ('-created_at',)
    
    readonly_fields = ('file_size', 'file_type', 'original_filename', 'created_at', 'updated_at', 'asset_preview')
    
    fieldsets = (
        (None, {
            'fields': ('file', 'asset_preview')
        }),
        ('Deliverable Link', {
            'fields': ('deliverable', 'is_approved')
        }),
        ('Metadata', {
            'fields': ('notes', 'uploaded_by'),
        }),
        ('Auto-detected', {
            'fields': ('original_filename', 'file_type', 'file_size'),
            'classes': ('collapse',)
        }),
    )
    
    def thumbnail_preview(self, obj):
        """Show small thumbnail in list view."""
        if obj.file and obj.file_type == 'image':
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; object-fit: cover; border-radius: 4px;">',
                obj.file.url
            )
        icons = {
            'video': '🎬',
            'pdf': '📄',
            'other': '📎'
        }
        return format_html(
            '<span style="font-size: 24px;">{}</span>',
            icons.get(obj.file_type, '📎')
        )
    thumbnail_preview.short_description = ''
    
    def asset_preview(self, obj):
        """Show larger preview in detail view."""
        if not obj.file:
            return '-'
        
        if obj.file_type == 'image':
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; border-radius: 8px;">',
                obj.file.url
            )
        elif obj.file_type == 'video':
            return format_html(
                '<video src="{}" controls style="max-width: 300px; max-height: 200px; border-radius: 8px;"></video>',
                obj.file.url
            )
        elif obj.file_type == 'pdf':
            return format_html(
                '<a href="{}" target="_blank" class="button">📄 View PDF</a>',
                obj.file.url
            )
        return format_html('<a href="{}" target="_blank">Download</a>', obj.file.url)
    asset_preview.short_description = 'Preview'
    
    def deliverable_link(self, obj):
        """Link to deliverable."""
        if obj.deliverable:
            return format_html(
                '{} - {}',
                obj.deliverable.event.name[:20],
                obj.deliverable.template.name
            )
        return '-'
    deliverable_link.short_description = 'Deliverable'
    
    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

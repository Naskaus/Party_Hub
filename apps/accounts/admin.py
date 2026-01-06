"""
Admin configuration for User model.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for User model with role management."""
    
    list_display = ('username', 'email', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    # Add role field to the standard UserAdmin fieldsets
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role & Contact', {
            'fields': ('role', 'phone'),
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role & Contact', {
            'fields': ('role', 'phone'),
        }),
    )

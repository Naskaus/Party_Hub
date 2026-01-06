"""
Custom User model for Marketing Event Planner.

Extends AbstractUser to add role management for RBAC.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model with role-based access.
    
    Roles:
        - admin: Full access (CEO/Tech) - can manage users, bars, themes
        - member: Read/Write access on content (designers, staff, managers)
    
    Following 'Open Kitchen' philosophy: everyone sees everything,
    only admin actions (user management, config) are restricted.
    """
    
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Administrator'
        MEMBER = 'member', 'Member'
    
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.MEMBER,
        help_text="User role for permission management"
    )
    
    # Additional fields useful for event planning context
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        help_text="Contact phone for urgent matters"
    )
    
    # Track user activity
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_admin(self):
        """Check if user has admin role."""
        return self.role == self.Role.ADMIN
    
    @property
    def display_name(self):
        """Return full name or username."""
        return self.get_full_name() or self.username

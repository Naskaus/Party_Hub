"""
Models for the assets app.

Handles file uploads for marketing deliverables (images, videos, PDFs).
"""

import os
from django.conf import settings
from django.db import models


def asset_upload_path(instance, filename):
    """
    Generate upload path based on event and deliverable.
    
    Structure: assets/<year>/<event_id>/<deliverable_id>/<filename>
    """
    if instance.deliverable:
        event = instance.deliverable.event
        return f"assets/{event.date.year}/event_{event.pk}/deliv_{instance.deliverable.pk}/{filename}"
    return f"assets/general/{filename}"


class Asset(models.Model):
    """
    Represents an uploaded file for a deliverable.
    
    Supports images, videos, and PDFs. Each asset is linked to
    an EventDeliverable and tracks upload metadata.
    """
    
    class FileType(models.TextChoices):
        IMAGE = 'image', 'Image (JPG/PNG/WebP)'
        VIDEO = 'video', 'Video (MP4/MOV)'
        PDF = 'pdf', 'PDF Document'
        OTHER = 'other', 'Other'
    
    # File
    file = models.FileField(
        upload_to=asset_upload_path,
        help_text="The uploaded file"
    )
    
    file_type = models.CharField(
        max_length=10,
        choices=FileType.choices,
        default=FileType.IMAGE
    )
    
    original_filename = models.CharField(
        max_length=255,
        blank=True,
        help_text="Original filename when uploaded"
    )
    
    file_size = models.PositiveIntegerField(
        default=0,
        help_text="File size in bytes"
    )
    
    # Link to deliverable (optional for now, allows general uploads)
    deliverable = models.ForeignKey(
        'planning.EventDeliverable',
        on_delete=models.CASCADE,
        related_name='assets',
        null=True,
        blank=True,
        help_text="The deliverable this asset belongs to"
    )
    
    # Metadata
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_assets'
    )
    
    notes = models.TextField(
        blank=True,
        help_text="Notes about this asset version"
    )
    
    is_approved = models.BooleanField(
        default=False,
        help_text="Whether this asset version is approved"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Asset'
        verbose_name_plural = 'Assets'
        ordering = ['-created_at']
    
    def __str__(self):
        if self.deliverable:
            return f"{self.original_filename} for {self.deliverable.template.name}"
        return self.original_filename or f"Asset {self.pk}"
    
    def save(self, *args, **kwargs):
        """Auto-detect file type and store metadata on save."""
        if self.file:
            # Store original filename
            if not self.original_filename:
                self.original_filename = os.path.basename(self.file.name)
            
            # Store file size
            if hasattr(self.file, 'size'):
                self.file_size = self.file.size
            
            # Auto-detect file type
            ext = os.path.splitext(self.file.name)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
                self.file_type = self.FileType.IMAGE
            elif ext in ['.mp4', '.mov', '.avi', '.webm']:
                self.file_type = self.FileType.VIDEO
            elif ext == '.pdf':
                self.file_type = self.FileType.PDF
            else:
                self.file_type = self.FileType.OTHER
        
        super().save(*args, **kwargs)
    
    @property
    def file_size_display(self):
        """Return human-readable file size."""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    
    @property
    def extension(self):
        """Return file extension."""
        return os.path.splitext(self.original_filename)[1].lower() if self.original_filename else ''

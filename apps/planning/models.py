"""
Models for the planning app.

Contains ThemePeriod for monthly themes and will contain Event models.
"""

from datetime import timedelta

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver


class ThemePeriod(models.Model):
    """
    Represents a monthly theme for marketing events.
    
    Each month can have a global theme that influences the visual identity
    of all events during that period (e.g., "Cyberpunk", "Eden Reborn").
    
    Attributes:
        name: Theme name (e.g., "Cyberpunk", "Tropical Paradise")
        description: Detailed description of the theme aesthetic
        month: Month number (1-12)
        year: Year
        is_active: Whether this theme is currently active
    """
    
    MONTH_CHOICES = [
        (1, 'January'), (2, 'February'), (3, 'March'),
        (4, 'April'), (5, 'May'), (6, 'June'),
        (7, 'July'), (8, 'August'), (9, 'September'),
        (10, 'October'), (11, 'November'), (12, 'December'),
    ]
    
    name = models.CharField(
        max_length=100,
        help_text="Name of the theme (e.g., 'Cyberpunk', 'Eden Reborn')"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the theme aesthetic and mood"
    )
    
    month = models.PositiveSmallIntegerField(
        choices=MONTH_CHOICES,
        help_text="Month this theme applies to"
    )
    
    year = models.PositiveIntegerField(
        help_text="Year this theme applies to"
    )
    
    # Visual identity
    primary_color = models.CharField(
        max_length=7,
        blank=True,
        default='#d946ef',
        help_text="Primary hex color for the theme (e.g., #d946ef)"
    )
    
    accent_color = models.CharField(
        max_length=7,
        blank=True,
        default='#22d3ee',
        help_text="Accent hex color for the theme"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this theme is currently active"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Theme Period'
        verbose_name_plural = 'Theme Periods'
        ordering = ['-year', '-month']
        unique_together = ['month', 'year']  # Only one theme per month
    
    def __str__(self):
        return f"{self.name} ({self.get_month_display()} {self.year})"
    
    @property
    def period_display(self):
        """Return formatted period string."""
        return f"{self.get_month_display()} {self.year}"
    
    @classmethod
    def get_current_theme(cls):
        """Get the theme for the current month/year."""
        from datetime import date
        today = date.today()
        return cls.objects.filter(
            month=today.month, 
            year=today.year, 
            is_active=True
        ).first()


class DeliverableTemplate(models.Model):
    """
    Template for deliverable types that can be assigned to events.
    
    These are reusable templates (e.g., "Poster A3", "Cube LED Video")
    that define what kind of assets need to be created for events.
    
    Global templates - not linked to specific bars.
    """
    
    class Category(models.TextChoices):
        SCREEN = 'screen', 'Screen/LED'
        PRINT = 'print', 'Print Material'
        SOCIAL = 'social', 'Social Media'
        OTHER = 'other', 'Other'
    
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Name of the deliverable (e.g., 'Cube LED Video', 'Poster A3')"
    )
    
    specs = models.CharField(
        max_length=200,
        blank=True,
        help_text="Technical specifications (e.g., '960x192 mp4', 'A3 300dpi PDF')"
    )
    
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER,
        help_text="Category of deliverable"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this template is currently in use"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Deliverable Template'
        verbose_name_plural = 'Deliverable Templates'
        ordering = ['category', 'name']
    
    def __str__(self):
        return self.name


class Event(models.Model):
    """
    Represents a marketing event at one or more bars.
    
    This is the core entity of the application. Events have:
    - A date and name
    - Optional theme from ThemePeriod
    - One or more associated bars
    - Auto-generated deliverables based on bar hardware
    
    The J-7 rule: All deliverables should be approved 7 days before the event.
    """
    
    name = models.CharField(
        max_length=200,
        help_text="Name of the event (e.g., 'DJ Night with Guest Star')"
    )
    
    date = models.DateField(
        help_text="Date of the event"
    )
    
    description = models.TextField(
        blank=True,
        help_text="Event description and notes"
    )
    
    brief = models.TextField(
        blank=True,
        help_text="Creative brief for designers"
    )
    
    theme = models.ForeignKey(
        ThemePeriod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events',
        help_text="Theme period for this event (auto-selected if not set)"
    )
    
    bars = models.ManyToManyField(
        'venues.Bar',
        related_name='events',
        help_text="Bars where this event takes place"
    )
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_events',
        help_text="User who created this event"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['date', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.date})"
    
    @property
    def deadline(self):
        """Return J-7 deadline date."""
        return self.date - timedelta(days=7)
    
    @property
    def days_until_event(self):
        """Return days until the event."""
        from datetime import date
        delta = self.date - date.today()
        return delta.days
    
    @property
    def days_until_deadline(self):
        """Return days until the J-7 deadline."""
        from datetime import date
        delta = self.deadline - date.today()
        return delta.days
    
    @property
    def is_past_deadline(self):
        """Check if we're past the J-7 deadline."""
        return self.days_until_deadline < 0
    
    @property
    def health_status(self):
        """
        Calculate event health based on deliverable status.
        
        Returns:
            'green': All deliverables approved
            'orange': In progress, deadline OK
            'red': Past deadline with unapproved deliverables
        """
        deliverables = self.deliverables.filter(is_enabled=True)
        
        if not deliverables.exists():
            return 'green'  # No deliverables = nothing to worry about
        
        all_approved = all(d.status == EventDeliverable.Status.APPROVED for d in deliverables)
        
        if all_approved:
            return 'green'
        
        if self.is_past_deadline:
            return 'red'
        
        return 'orange'
    
    def save(self, *args, **kwargs):
        """Auto-assign theme based on event date if not set."""
        if not self.theme:
            self.theme = ThemePeriod.objects.filter(
                month=self.date.month,
                year=self.date.year,
                is_active=True
            ).first()
        super().save(*args, **kwargs)
    
    def generate_deliverables(self):
        """
        Generate EventDeliverables based on the bars' hardware specs.
        
        Called after bars are assigned to the event.
        """
        for bar in self.bars.all():
            # Get templates for this bar
            templates = DeliverableTemplate.objects.filter(
                bar=bar,
                is_default=True
            )
            
            for template in templates:
                EventDeliverable.objects.get_or_create(
                    event=self,
                    template=template,
                    defaults={
                        'status': EventDeliverable.Status.TODO
                    }
                )


class EventDeliverable(models.Model):
    """
    A specific deliverable item for an event.
    
    Links an Event to a DeliverableTemplate with status tracking.
    
    Status workflow:
        TODO -> IN_PROGRESS -> REVIEW -> APPROVED
                                     \-> CHANGES_REQUESTED -> REVIEW
    """
    
    class Status(models.TextChoices):
        TODO = 'todo', 'To Do'
        IN_PROGRESS = 'in_progress', 'In Progress'
        REVIEW = 'review', 'Under Review'
        CHANGES_REQUESTED = 'changes', 'Changes Requested'
        APPROVED = 'approved', 'Approved'
    
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='deliverables'
    )
    
    template = models.ForeignKey(
        DeliverableTemplate,
        on_delete=models.CASCADE,
        related_name='event_deliverables'
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO
    )
    
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_deliverables',
        help_text="User responsible for this deliverable"
    )
    
    is_enabled = models.BooleanField(
        default=True,
        help_text="Can disable if not needed for this specific event"
    )
    
    is_starred = models.BooleanField(
        default=False,
        help_text="Highlight this deliverable in the event panel"
    )
    
    notes = models.TextField(
        blank=True,
        help_text="Notes or feedback about this deliverable"
    )
    
    # Asset will be added in Phase 5
    # asset = models.ForeignKey('assets.Asset', ...)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Event Deliverable'
        verbose_name_plural = 'Event Deliverables'
        ordering = ['template__category', 'template__name']
        unique_together = ['event', 'template']
    
    def __str__(self):
        return f"{self.template.name} for {self.event.name}"
    
    @property
    def is_late(self):
        """Check if this deliverable is late (past J-7 and not approved)."""
        return self.event.is_past_deadline and self.status != self.Status.APPROVED


# Signal to auto-generate deliverables when bars are added to an event
@receiver(m2m_changed, sender=Event.bars.through)
def generate_deliverables_on_bar_add(sender, instance, action, **kwargs):
    """Generate deliverables when bars are added to an event."""
    if action == 'post_add':
        instance.generate_deliverables()


"""
Views for the planning app.

Handles calendar views, events, and deliverables.
"""

import calendar
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from apps.venues.models import Bar
from .models import Event, ThemePeriod


@login_required
def calendar_view(request):
    """
    Main calendar view - the heart of the application.
    
    Displays events in month view with health indicators.
    """
    # Get month/year from query params or use current
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    
    # Build calendar data
    cal = calendar.Calendar(firstweekday=0)  # Monday first
    month_days = cal.monthdayscalendar(year, month)
    
    # Get events for this month
    first_day = date(year, month, 1)
    if month == 12:
        last_day = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(year, month + 1, 1) - timedelta(days=1)
    
    events = Event.objects.filter(
        date__gte=first_day,
        date__lte=last_day
    ).prefetch_related('bars', 'deliverables')
    
    # Build events by day dict
    events_by_day = {}
    for event in events:
        day = event.date.day
        if day not in events_by_day:
            events_by_day[day] = []
        events_by_day[day].append(event)
    
    # Get current theme
    theme = ThemePeriod.get_current_theme()
    
    # Get bars for filter dropdown
    bars = Bar.objects.filter(is_active=True)
    
    # Navigation
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    
    context = {
        'page_title': 'Calendar',
        'page_subtitle': f"{calendar.month_name[month]} {year}" + (f" • {theme.name}" if theme else ""),
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'month_days': month_days,
        'events_by_day': events_by_day,
        'today': today,
        'theme': theme,
        'bars': bars,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
    }
    return render(request, 'planning/calendar.html', context)


@login_required
def event_list(request):
    """
    List all upcoming events.
    """
    events = Event.objects.filter(
        date__gte=date.today()
    ).prefetch_related('bars', 'deliverables').order_by('date')
    
    context = {
        'page_title': 'Events',
        'page_subtitle': f'{events.count()} upcoming events',
        'events': events,
    }
    return render(request, 'planning/event_list.html', context)


@login_required
def event_detail(request, pk):
    """
    Detail view for a single event with deliverables.
    """
    event = get_object_or_404(
        Event.objects.prefetch_related('bars', 'deliverables__template'),
        pk=pk
    )
    
    context = {
        'page_title': event.name,
        'page_subtitle': f"{event.date.strftime('%B %d, %Y')} • {event.bars.count()} venues",
        'event': event,
    }
    return render(request, 'planning/event_detail.html', context)


@login_required
def export_event_pdf(request, pk):
    """
    Export event details and selected assets as PDF.
    
    GET: Show asset selection form
    POST: Generate and download PDF
    """
    from io import BytesIO
    from django.http import HttpResponse
    from django.template.loader import get_template
    from xhtml2pdf import pisa
    
    event = get_object_or_404(
        Event.objects.prefetch_related(
            'bars', 
            'deliverables__template',
            'deliverables__assets'
        ),
        pk=pk
    )
    
    if request.method == 'POST':
        # Get selected deliverable IDs
        selected_ids = request.POST.getlist('deliverables')
        selected_deliverables = event.deliverables.filter(id__in=selected_ids)
        
        # Collect selected assets
        selected_assets = []
        for deliv in selected_deliverables:
            for asset in deliv.assets.all():
                if str(asset.id) in request.POST.getlist('assets'):
                    selected_assets.append(asset)
        
        # Render PDF template
        template = get_template('planning/event_pdf.html')
        context = {
            'event': event,
            'deliverables': selected_deliverables,
            'assets': selected_assets,
            'request': request,
        }
        html = template.render(context)
        
        # Generate PDF
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result)
        
        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            filename = f"{event.name.replace(' ', '_')}_{event.date}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        
        # Error fallback
        return HttpResponse('Error generating PDF', status=500)
    
    # GET: Show selection form
    context = {
        'page_title': f'Export: {event.name}',
        'page_subtitle': 'Select items to include in PDF',
        'event': event,
    }
    return render(request, 'planning/export_select.html', context)



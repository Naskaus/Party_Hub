"""
Views for the venues app.

Handles bar listing and detail views.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Bar


@login_required
def bar_list(request):
    """
    Display list of all active bars with their hardware specs.
    """
    bars = Bar.objects.filter(is_active=True).order_by('name')
    
    context = {
        'bars': bars,
        'page_title': 'Venues',
        'page_subtitle': f'{bars.count()} active venues',
    }
    return render(request, 'venues/bar_list.html', context)


@login_required
def bar_detail(request, pk):
    """
    Display detail view of a single bar.
    """
    bar = get_object_or_404(Bar, pk=pk)
    
    context = {
        'bar': bar,
        'page_title': bar.name,
        'page_subtitle': bar.location,
    }
    return render(request, 'venues/bar_detail.html', context)

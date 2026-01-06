"""
Views for the assets app.

Handles asset listing and file uploads for deliverables.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.planning.models import EventDeliverable
from .models import Asset


@login_required
def asset_list(request):
    """
    List all uploaded assets with filtering.
    """
    assets = Asset.objects.select_related(
        'deliverable__event', 'deliverable__template', 'uploaded_by'
    ).order_by('-created_at')[:50]  # Last 50 assets
    
    context = {
        'page_title': 'Assets',
        'page_subtitle': f'{Asset.objects.count()} files uploaded',
        'assets': assets,
    }
    return render(request, 'assets/asset_list.html', context)


@login_required
@require_POST
def upload_asset(request, deliverable_id):
    """
    Upload an asset for a specific deliverable.
    
    Accepts file via POST and creates Asset linked to the deliverable.
    Returns JSON for HTMX partial update.
    """
    deliverable = get_object_or_404(EventDeliverable, pk=deliverable_id)
    
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file provided'}, status=400)
    
    uploaded_file = request.FILES['file']
    
    # Create asset
    asset = Asset.objects.create(
        file=uploaded_file,
        deliverable=deliverable,
        uploaded_by=request.user,
        notes=request.POST.get('notes', '')
    )
    
    # Update deliverable status to in_progress if it was todo
    if deliverable.status == EventDeliverable.Status.TODO:
        deliverable.status = EventDeliverable.Status.IN_PROGRESS
        deliverable.save()
    
    # If HTMX request, return partial
    if request.headers.get('HX-Request'):
        return render(request, 'assets/_asset_card.html', {'asset': asset})
    
    messages.success(request, f'Asset uploaded: {asset.original_filename}')
    return redirect('planning:event_detail', pk=deliverable.event.pk)


"""
URL configuration for Marketing Event Planner.

Routes are organized by app:
- /accounts/ - Authentication (login, logout)
- /admin/ - Django Admin
- / - Planning (calendar, events)
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Apps
    path('accounts/', include('apps.accounts.urls')),
    path('venues/', include('apps.venues.urls')),
    path('assets/', include('apps.assets.urls')),
    path('', include('apps.planning.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])


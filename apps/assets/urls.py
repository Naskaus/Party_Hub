"""
URL configuration for assets app.

Handles asset listing and uploads.
"""

from django.urls import path

from . import views

app_name = 'assets'

urlpatterns = [
    path('', views.asset_list, name='asset_list'),
    path('upload/<int:deliverable_id>/', views.upload_asset, name='upload_asset'),
]


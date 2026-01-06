"""
URL configuration for venues app.

Handles bars listing and detail views.
"""

from django.urls import path

from . import views

app_name = 'venues'

urlpatterns = [
    path('', views.bar_list, name='bar_list'),
    path('<int:pk>/', views.bar_detail, name='bar_detail'),
]

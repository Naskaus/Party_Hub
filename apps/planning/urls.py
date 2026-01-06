"""
URL configuration for planning app.

Handles events, calendar views, and deliverables.
"""

from django.urls import path

from . import views

app_name = 'planning'

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
]


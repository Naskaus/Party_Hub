"""
Settings package initialization.

Default to development settings for local work.
Use DJANGO_SETTINGS_MODULE=config.settings.production in production.
"""

from .development import *  # noqa: F401, F403

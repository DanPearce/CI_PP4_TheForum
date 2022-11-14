"""
apps.py for forumboard (Django Built In)
"""
# Imports
# -----------------------------------------------------------------------
# Third Party
from django.apps import AppConfig


class ForumboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'forumboard'

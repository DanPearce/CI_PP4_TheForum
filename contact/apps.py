"""
apps.py for contact (Django Built In)
"""
# Imports
# -----------------------------------------------------------------------
# Third Party
from django.apps import AppConfig


class ContactConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contact'

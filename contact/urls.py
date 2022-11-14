"""
URLs for the contact app
"""
# Imports
# -----------------------------------------------------------------------
# Third Party
from django.urls import path
# Internal
from . import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
]

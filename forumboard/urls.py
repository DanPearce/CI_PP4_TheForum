"""
URLs for forumboard
Imports for URLs
"""
from . import views
from django.urls import path

urlpatterns = [
    path('', views.get_topstories, name='home'),
]

"""
URLs for forumboard
Imports for URLs
"""
from . import views
from django.urls import path

urlpatterns = [
    path('', views.IndexPostView.as_view(), name='home'),
]
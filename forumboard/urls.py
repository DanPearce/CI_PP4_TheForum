"""
URLs for forumboard
Imports for URLs
"""
from . import views
from django.urls import path

urlpatterns = [
    path('', views.get_topstories, name='home'),
    path('index_post_view', views.IndexPostView.as_view(),
         name='index_post_view'),
]

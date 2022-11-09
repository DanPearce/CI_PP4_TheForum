"""
URLs for forumboard
Imports for URLs
"""
from . import views
from django.urls import path

urlpatterns = [
    path('', views.get_index, name='home'),
    path('<slug:slug>', views.PostDetail.as_view(), name='post_detail'),
    path('board/<slug:slug>', views.BoardDetail.as_view(),
         name='board_detail'),
]

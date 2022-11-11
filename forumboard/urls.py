"""
URLs for forumboard
Imports for URLs
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_index, name='home'),
    path('<slug:slug>', views.PostDetail.as_view(), name='post_detail'),
    path('board/<slug:slug>', views.BoardDetail.as_view(),
         name='board_detail'),
    path('board/<name>/add_post/', views.add_post,
         name='add_post'),
    path('all_boards/', views.get_all_boards, name='all_boards'),
    path('add_board/', views.add_board, name='add_board')
]

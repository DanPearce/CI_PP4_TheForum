"""
Views for ForumBoard
"""
from django.shortcuts import render
from django.views import generic
from .models import ForumBoard, ForumPost, Comment


class IndexPostView(generic.ListView):
    """
    View to generate posts based on likes.
    """
    model = ForumPost
    template_name = 'index.html'
    queryset = ForumPost.objects.order_by('likes')
    paginate_by = 10

"""
Admin set up for ForumBoard and it's posts/comments
"""
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import ForumBoard, ForumPost, Comment

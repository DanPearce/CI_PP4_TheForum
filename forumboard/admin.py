"""
Admin set up for ForumBoard and it's posts/comments
"""
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import ForumBoard, ForumPost, Comment


@admin.register(ForumBoard)
class ForumBoardAdmin(SummernoteModelAdmin):
    """
    Diplay Forum Board sections in Admin Console
    """
    list_display = ('name', 'slug', 'approved_board', 'created_on')
    search_fields = ['name', 'about']
    list_filter = ('created_on', 'approved_board')
    prepopulated_fields = {'slug': ('name',)}
    summernote_fields = ('about',)
    actions = ['approve_board']

    def approve_board(self, request, queryset):
        """
        Allows admins to approve Forum Boards for publishing
        """
        queryset.update(approved_board=True)


@admin.register(ForumPost)
class ForumPostAdmin(SummernoteModelAdmin):
    """
    Display Forum Post sections in Admin Console
    """
    list_display = ('forum_board', 'post_title', 'creator', 'created_on')
    search_fields = ['post_title', 'post_detail']
    list_filter = ('created_on',)
    prepopulated_fields = {'slug': ('forum_board', 'post_title',)}
    summernote_fields = ('post_detail')

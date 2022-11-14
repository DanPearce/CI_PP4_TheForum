"""
Forms used in forumboard
"""
# Imports
# -----------------------------------------------------------------------
# Third Party
from django import forms
# Internal
from .models import Comment, ForumPost, ForumBoard


class CommentForm(forms.ModelForm):
    """
    Class to allow us to use the Comment Form
    """
    class Meta:
        model = Comment
        fields = ('body',)


class PostForm(forms.ModelForm):
    """
    Class to allow us to use the Post Form
    """
    class Meta:
        model = ForumPost
        fields = ('post_title', 'featured_image', 'post_detail',
                  'excerpt',)


class PostBoard(forms.ModelForm):
    """
    Class to allow us to use the Post Board Form
    """
    class Meta:
        model = ForumBoard
        fields = ('name', 'about', 'board_background')

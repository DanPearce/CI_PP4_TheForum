from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    """
    Class to allow us to use the Comment Form
    """
    class Meta:
        model = Comment
        fields = ('body',)

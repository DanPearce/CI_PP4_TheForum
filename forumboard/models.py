"""
Models for the ForumBoard Structure
"""
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class ForumBoard(models.Model):
    """
    This class is used to define the model paramaters for the
    'ForumBoard'.
    """
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    about = models.CharField(max_length=255)
    board_background = CloudinaryField('image', default='placeholder')
    followers = models.ManyToManyField(
            User, related_name="board_followers", blank=True
    )
    approved_board = models.BooleanField(default=False)

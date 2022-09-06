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

    def __str__(self):
        """
        This function returns the name of the ForumBoard
        """
        return f"{self.name}"

    def number_of_followers(self):
        """
        This function returns the number of followers that follow this board
        """
        return self.followers.count()


class ForumPost(models.Model):
    """
    This class is used to define the paramaters for posting to a Forum Board.
    """
    forum_board = models.ForeignKey(
        ForumBoard, on_delete=models.CASCADE, related_name='posts')
    post_title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_posts')
    featured_image = CloudinaryField('image', default='placeholder')
    post_detail = models.TextField()
    excerpt = models.CharField(max_length=250, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        User, related_name='forumpost_like', blank=True)

"""
Views for ForumBoard
"""
import os
import requests
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import ForumBoard, ForumPost, Comment
from .forms import CommentForm


if os.path.isfile('env.py'):
    import env


def get_index(request):
    """
    View to get the latest UK top headlines, using NewsAPI.org,
    Load the latest posts on the website,
    Load the boards on the website.
    """
    api_key = os.environ.get('API_KEY')
    url = f'https://newsapi.org/v2/top-headlines?country=gb&apiKey={api_key}'
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    latest_posts = ForumPost.objects.order_by('-created_on')
    top_boards = ForumBoard.objects.order_by('-created_on')
    context = {
        'articles': articles,
        'latest_posts': latest_posts,
        'top_boards': top_boards,
    }

    return render(request, 'index.html', context)


class PostDetail(View):
    """
    View to generate items related to posts
    """
    def get(self, request, slug, *args, **kwargs):
        """
        Function to generate a view to get the data from a post
        """
        queryset = ForumPost.objects
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.order_by('-created_on')
        board = post.forum_board
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        context = {
            'post': post,
            'comments': comments,
            'liked': liked,
            'comment_form': CommentForm(),
            'board': board
        }

        return render(request, 'post_detail.html', context)

    def post(self, request, slug, *args, **kwargs):
        """
        Function to post a comment to a post
        """
        queryset = ForumPost.objects
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.order_by('-created_on')
        board = post.forum_board
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.creator_id = request.user.id
            comment.save()
            comment_form = CommentForm
        else:
            comment_form = CommentForm

        context = {
            'post': post,
            'comments': comments,
            'liked': liked,
            'comment_form': comment_form,
            'board': board
        }

        return render(request, 'post_detail.html', context)


class BoardDetail(View):
    """
    View to grab the necessary details for the Forum Board
    """
    def get(self, request, slug, *args, **kwargs):
        """
        Function to generate a view to get the data from a forum board
        """
        queryset = ForumBoard.objects
        board = get_object_or_404(queryset, slug=slug)
        posts = board.posts.order_by('-created_on')
        following = False
        if board.followers.filter(id=self.request.user.id).exists():
            following = True
        context = {
            'board': board,
            'posts': posts,
            'following': following
        }

        return render(request, 'board_detail.html', context)

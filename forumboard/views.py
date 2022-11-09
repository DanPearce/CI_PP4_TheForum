"""
Views for ForumBoard
"""
import os
import requests
from .models import ForumBoard, ForumPost, Comment
from django.shortcuts import render
from django.views import generic, View
if os.path.isfile('env.py'):
    import env



def get_index(request):
    """
    View to get the latest UK top headlines, using NewsAPI.org,
    Load trending posts on the website,
    """
    API_KEY = os.environ.get('API_KEY')
    url = f'https://newsapi.org/v2/top-headlines?country=gb&apiKey={API_KEY}'
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

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
    View to get the latest UK top headlines, using NewsAPI.org
    """
    API_KEY = os.environ.get('API_KEY')
    url = f'https://newsapi.org/v2/top-headlines?country=gb&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    latest_posts = ForumPost.objects.order_by('likes')
    context = {
        'articles': articles,
        'latest_posts': latest_posts
    }

    return render(request, 'index.html', context)

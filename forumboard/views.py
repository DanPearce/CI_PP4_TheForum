"""
Views for ForumBoard
"""
import os
import requests
from django.shortcuts import render
from django.views import generic
if os.path.isfile('env.py'):
    import env
# from .models import ForumBoard, ForumPost, Comment


# class IndexPostView(generic.ListView):
#     """
#     View to generate posts based on likes.
#     """
#     model = ForumPost
#     template_name = 'index.html'
#     queryset = ForumPost.objects.order_by('likes')
#     paginate_by = 10


def get_topstories(request):
    """
    View to get the latest UK top headlines, using NewsAPI.org
    """
    API_KEY = os.environ.get('API_KEY')
    url = f'https://newsapi.org/v2/top-headlines?country=gb&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    context = {
        'articles': articles
    }

    return render(request, 'index.html', context)

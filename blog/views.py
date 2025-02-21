from django.shortcuts import render


from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article
import random

# Create your views here.
class ShowAllView(ListView):
    '''Define a view class to show all blog Articles'''
    
    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"

class ArticleView(DetailView):
    '''Display 1 article'''

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"


class RandomArticleView(DetailView):
    '''random'''
    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"

    #methods 
    def get_object(self):
        all_artiles = Article.objects.all()
        article = random.choice(all_artiles)
        return article
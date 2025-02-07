import random
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
from django.templatetags.static import static

quotes = ["I'm for truth, no matter who tells it. I'm for justice, no matter who it's for or against", 
          "I believe that there will be ultimately be a clash between the oppressed and those who do the oppressing", 
          "If you don't stand for something you will fall for anything" ]

images = [
    "images/malcolmx.jpg",
    "images/malcolmx2.jpg",
    "images/malcolmx3.jpg"
]

# Create your views here.
def home(request):
    '''Define a view to show the 'home.html' template.'''

    # the template to which we will delegate the work
    template = 'quotes/base.html'

    # a dict of key/value pairs, to be available for use in template
    context = {
        'quotes' : random.choice(quotes),
        'images' : random.choice(images)
    }

    return render(request, template, context)


def quote(request):
    return render(request, '/quote.html', {'quote': random.choice(quotes)})

def show_all(request):
    template = 'quotes/show_all.html'

    context = {
        'quotes' : quotes,
        'images' : images
    }
    return render(request, template, context)

def about(request):
    
    return render(request, 'quotes/about.html')
#define data models for blog application
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Article(models.Model):
    '''Encapsulate the data of a blog article by an author'''

    #define the data attributes of the Article Object
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)
    #image_url = models.URLField(blank=True) url as a string
    image_file = models.ImageField(blank=True) #an actual image
    user = models.ForeignKey(User, on_delete=models.CASCADE) ## NEW
        
    def __str__(self):
        """return a string represenation of this model isntance"""
        return f'{self.title} by {self.author}'
    
    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('article', kwargs={'pk':self.pk})
    
    def get_all_comments(self):
        '''Return a queryset of comments'''
        comments = Comment.objects.filter(article=self)
        return comments
    
class Comment(models.Model):
    '''Comment in an Article'''

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Comment object.'''
        return f'{self.text}'
#define data models for blog application
from django.db import models

# Create your models here.
class Article(models.Model):
    '''Encapsulate the data of a blog article by an author'''

    #define the data attributes of the Article Object
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        """return a string represenation of this model isntance"""
        return f'{self.title} by {self.author}'
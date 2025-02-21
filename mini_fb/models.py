# File: models.py
# Author: Mohammed Abaherah (abaherah@bu.edu) 20 Feb 2025
# Description: Contains models which model the data attributes of individual Facebook users. 

from django.db import models

# Create your models here.

class Profile(models.Model):
    '''Encapsulate the data of a fb user'''

    #define the data attributes of the Article Object
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    city = models.TextField(blank=True)
    email = models.EmailField(unique=True)
    image_url = models.URLField(blank=True)

def __str__(self):
    """Return a string representation of this profile"""
    return f"{self.first_name} {self.last_name}"
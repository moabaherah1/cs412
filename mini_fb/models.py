# File: models.py
# Author: Mohammed Abaherah (abaherah@bu.edu) 20 Feb 2025
# Description: Contains models which model the data attributes of individual Facebook users. 

from django.db import models
from django.urls import reverse
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

    def get_status_messages(self):
        """Returns all status messages related to this profile, ordered by timestamp."""
        return self.statusmessage_set.all().order_by('-time_stamp')
    
    def get_absolute_url(self) -> str:
        '''returns the reverse of the profile so we can return the user to the correct url after submitting'''
        return reverse('show_profile', kwargs= {"pk":self.pk})


class StatusMessage(models.Model): 
    '''models the data attributes of Facebook status message'''
    time_stamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this Status Message object.'''
        return f'{self.time_stamp, self.message}'

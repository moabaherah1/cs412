# File: models.py
# Author: Mohammed Abaherah (abaherah@bu.edu) 14 April 2025
# Description: Contains models which model the data attributes of individual Users

from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class UserProfile(models.Model):
    '''Models the profile of one of our users on the app'''

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="finalproject_profile")
    first_name = models.CharField(max_length=100, blank=True)
    nick_name = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    email = models.EmailField(unique=True, blank=True)
    dob = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.nick_name}"

    def get_absolute_url(self):
        '''Returns the reverse URL of the profile so we can return the user to the correct URL after submitting'''
        return reverse('show_userprofile', kwargs={"pk": self.pk})

    def get_partner(self):
        '''Returns the partner of the current user, if any'''
        couple = Couple.objects.filter(models.Q(user1=self) | models.Q(user2=self)).first()
        if couple:
            return couple.user2 if couple.user1 == self else couple.user1
        return None
    
    def add_partner(self, partner):
        """Associates the current user with the given partner in a couple."""
        Couple.objects.create(user1=self, user2=partner)    

class Couple(models.Model):
    """Models the Couple of two users on the app that are connected"""
    
    user1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user2')

    anniversary_date = models.DateField()
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user1} & {self.user2}'


class Invitation(models.Model):
    """Models the invitation system which is used to ask users to become one's partner"""

    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name= "from_user")
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name= "to_user")
    message = models.TextField(blank=True)
    sent_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.from_user} invited {self.to_user}"
    


class EventRSVP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_id = models.CharField(max_length=200)  
    event_title = models.CharField(max_length=500)
    attending = models.BooleanField(default=True)
    rsvp_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} RSVP'd to {self.event_title}"
    

class CouplePost(models.Model):
    '''Models a post made by a couple.'''
    couple = models.ForeignKey(Couple, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    time_stamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Post by {self.couple} at {self.time_stamp}'

    def get_absolute_url(self):
        return reverse('show_couple_posts', kwargs={"pk": self.couple.pk})


class CoupleImage(models.Model):
    '''Models an image belonging to a couple post.'''
    couple = models.ForeignKey(Couple, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='couple_images/', blank=True)
    caption = models.TextField(blank=True)
    time_stamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.caption}'


class CouplePostImage(models.Model):
    '''Connects an image to a couple's post.'''
    image = models.ForeignKey(CoupleImage, on_delete=models.CASCADE)
    post = models.ForeignKey(CouplePost, on_delete=models.CASCADE)

    def __str__(self):
        return f'Image {self.image} in Post {self.post}'

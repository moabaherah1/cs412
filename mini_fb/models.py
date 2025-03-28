# File: models.py
# Author: Mohammed Abaherah (abaherah@bu.edu) 20 Feb 2025
# Description: Contains models which model the data attributes of individual Facebook users. 

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    '''Encapsulate the data of a fb user'''

    #define the data attributes of the Article Object
    
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    city = models.TextField(blank=True)
    email = models.EmailField(unique=True)
    image_url = models.URLField(blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        """Return a string representation of this profile"""
        return f"{self.first_name} {self.last_name}"

    def get_status_messages(self):
        """Returns all status messages related to this profile, ordered by timestamp."""
        return self.statusmessage_set.all().order_by('-time_stamp')
    
    def get_absolute_url(self) -> str:
        '''returns the reverse of the profile so we can return the user to the correct url after submitting'''
        return reverse('show_profile', kwargs= {"pk":self.pk})
    
    def get_friends(self):
        '''return a list of friends profiles'''

        friends = []

        friend1 = Friend.objects.filter(profile1 = self)
        for friend in friend1:
            friends.append(friend.profile2)


        friend2 = Friend.objects.filter(profile2 = self)
        for friend in friend2:
            friends.append(friend.profile1)

        return friends
    
    def add_friend(self, other):
        ''' This method takes a parameter other, which refers to another Profile instance, 
        and the effect of the method should be add a Friend relation for the two Profiles: self and other.'''
        if (self == other):
            return
        
        existing_friend = Friend.objects.filter(models.Q(profile1=self, profile2 = other) | models.Q(profile1 = other, profile2 = self)).exists()

        if (not existing_friend ):
            new_friend = Friend(profile1 = self, profile2 = other)

            new_friend.save()

    def get_friend_suggestions(self):
        '''will return a list (or QuerySet) of possible friends for a Profile'''

        all_profiles = Profile.objects.exclude(pk = self.pk)
        friends = Friend.objects.filter(models.Q(profile1 = self) | models.Q(profile2 = self))
        friend_profiles = []
        for friend in friends:
            if friend.profile1 == self :
                friend_profiles.append(friend.profile2)
            else:
                friend_profiles.append(friend.profile1)

        suggestions = []
        for profile in all_profiles:
            if profile not in friend_profiles:
                suggestions.append(profile)

        return suggestions

    def get_news_feed(self):
        ''' on the Profile object, which will return a list (or QuerySet) of all StatusMessages for the profile on which the method was called, as well as all of the friends of that profile.'''

        profile_statuses = StatusMessage.objects.filter(profile = self)
        friends = self.get_friends()
        friend_statuses = StatusMessage.objects.filter(profile__in = friends)
        all_statuses = profile_statuses | friend_statuses

        return all_statuses




class StatusMessage(models.Model): 
    '''models the data attributes of Facebook status message'''
    time_stamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this Status Message object.'''
        return f'{self.time_stamp, self.message, self.profile}'
    
    def get_absolute_url(self) -> str:
        '''returns the reverse of the profile so we can return the user to the correct url after submitting'''
        return reverse('show_profile', kwargs= {"pk":self.profile.pk})
    

    def get_images(self):
        '''use the ORM to find all Images that are related to this StatusMessage, and then return a list or QuerySetof those Image(s)'''
        images = Image.objects.filter(statusimage__statusmessage=self)

        return images




class Image(models.Model): 
    '''models the image attribute of a status message'''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(blank=True)
    time_stamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        '''Return a string representation of this Image object.'''
        return f'{self.caption}'
    

class StatusImage(models.Model):
    '''connects image to statusimage with fk'''

    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    statusmessage = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this StatusImage object.'''
        return f'{self.statusmessage}'
    

class Friend(models.Model): 
    '''connects profile to another profile ie) friend'''
    
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile1')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile2')
    time_stamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a spring representation of '''
        return f'{self.profile1} & {self.profile2}'

# class ContextMixIn(models.Model):
#     '''Creating a custom MixIn for each view to get the certain context we want  '''

#     model = User
#     def get_context_data(self, **kwargs):
#         '''method to get the pk of each profile page'''
#         context = super().get_context_data(**kwargs)
#         context['profile'] = Profile.objects.get(user=self.request.user)
#         return context
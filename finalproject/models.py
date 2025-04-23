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


    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name =  models.TextField(blank=True)
    nick_name =  models.TextField(blank=True)
    address =  models.TextField(blank=True)
    email =  models.TextField(blank=True)
    dob = models.DateField()
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    
    def __str__(self):
        '''Return a spring representation of user'''
        return f'{self.nick_name}'

    def get_absolute_url(self):
        '''Returns the reverse URL of the profile so we can return the user to the correct URL after submitting'''
        return reverse('show_userprofile', kwargs={"pk": self.pk})


    # def add_partner(self, other):
    #     ''' This method takes a parameter other, which refers to another UserProfile instance, 
    #     and the effect of the method should be add a Couple relationship for the two UserProfiles: self and other.'''
    #     if (self == other):
    #         return
        
    #     already_coupled = Couple.objects.filter(models.Q(user1=self, user2 = other) | models.Q(user1 = other, user2 = self)).exists()

    #     if not already_coupled :
    #         Couple.objects.create(user1 = self, user2 = other, creation_date = timezone.now().date())
    #         self.is_in_couple = True
    #         other.is_in_couple = True
    #         self.save()
    #         other.save()

    def get_partner(self):
        """Return the partner of the current user"""
        couple = Couple.objects.filter(
            models.Q(user1=self) | models.Q(user2=self)
        ).first()

        if couple:
            return couple.user2 if couple.user1 == self else couple.user1
        return None



class Couple(models.Model):
    """Models the Couple of two users on the app that are connected"""

    user1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user2')

    anniversary_date = models.DateField()
    creation_date = models.DateField(default=timezone.now)

    def __str__(self):
        '''Return a spring representation of couples'''
        return f'{self.user1} & {self.user2}'


class Invitation(models.Model):
    """Models the invitation system which is used to ask users to become one's partner"""

    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name= "from_user")
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name= "to_user")
    message = models.TextField(blank=True)
    sent_at = models.DateTimeField(default=timezone.now)
    accepted = models.BooleanField(default=False)
    responded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.from_user} invited {self.to_user}"
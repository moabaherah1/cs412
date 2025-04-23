# File: forms.py
# Author: Mohammed Abaherah (abaherah@bu.edu) 14 April 2025
# Description: Create "finalproject/forms.py" to define the CreateProfileForm

from django import forms
from .models import UserProfile, Invitation

class CreateProfileForm(forms.ModelForm):
    '''A form to add a UserProfile to the database'''

    # first_name = forms.CharField(label="First Name", required=True)
    # birth_date = forms.DateField(widget=forms.SelectDateWidget(years=range(2025,1920,-1),),)

    class Meta:
        '''associate this form with the UserProfile model from our database.'''
        model = UserProfile
        fields = ['first_name', 'nick_name', 'address', 'email', 'dob', 'image']

class InvitationForm(forms.ModelForm):
    '''A form to invite someone to a relationship'''

    class Meta:
        '''associate this form with the Invitation model from our database'''
        model = Invitation
        fields = ['from_user', 'to_user', 'message', 'sent_at']



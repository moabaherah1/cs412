# File: forms.py
# Author: Mohammed Abaherah (abaherah@bu.edu) 27 Feb 2025
# Description: Create "mini_fb/forms.py" to define the CreateProfileForm

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    '''A form to add a Profile to the database'''

    # first_name = forms.CharField(label="First Name", required=True)
    # birth_date = forms.DateField(widget=forms.SelectDateWidget(years=range(2025,1920,-1),),)

    class Meta:
        '''associate this form with a model from our database.'''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'image_url']

class CreateStatusMessageForm(forms.ModelForm):
    '''A form to add a status message to the database'''

    class Meta:
        '''Associate this form with a model from our database'''

        model = StatusMessage 
        fields = ['message']


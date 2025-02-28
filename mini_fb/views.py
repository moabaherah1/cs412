# File: views.py
# Author: Mohammed Abaherah (abaherah@bu.edu) 20 Feb 2025
# Description: Defines our classes

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile
from .forms import CreateProfileForm

class ShowAllProfilesView(ListView):
    '''Define a view class to show all Profiles'''
    
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"

class ShowProfilePageView(DetailView):
    '''Define a view class to show a single profile page'''

    model = Profile 
    template_name = "mini_fb/show_profile.html"

class CreateProfileView(CreateView):
    '''Define a view class to show the profile form'''
    
    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''

        return self.object.get_absolute_url()


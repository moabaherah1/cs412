# File: views.py
# Author: Mohammed Abaherah (abaherah@bu.edu) 20 Feb 2025
# Description: Defines our classes

from django.shortcuts import render
from django.views.generic import ListView
from .models import Profile

class ShowAllProfilesView(ListView):
    '''Define a view class to show all Profiles'''
    
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"

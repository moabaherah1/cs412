# File: urls.py
# Author: Mohammed Abaherah (abaherah@bu.edu) 14 April 2025
# Description: Has the paths to all the correct views

from django.urls import path
from .views import  ShowProfilePageView, CreateProfileView
from django.contrib.auth import views as auth_views

'''our url patterns so we can link to the page we want to show'''
urlpatterns = [
    
    path('', ShowProfilePageView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_userprofile'),
    path('create_userprofile/', CreateProfileView.as_view(), name='create_userprofile'), 

]
# File: urls.py
# Author: Mohammed Abaherah (abaherah@bu.edu) 20 Feb 2025
# Description: Has the paths to all the correct views

from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView, CreateProfileView, CreateStatusView, UpdateProfileView, DeleteMessageStatusView, UpdateStatusMessageView

'''our url patterns so we can link to the page we want to show'''
urlpatterns = [
    
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile', CreateProfileView.as_view(), name='create_profile'), #New
    path('profile/<int:pk>/create_status', CreateStatusView.as_view(), name='create_status'), 
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name='update_profile'), 
    path('status/<int:pk>/delete', DeleteMessageStatusView.as_view(), name='delete_status'), 
    path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name='update_status'), 


]
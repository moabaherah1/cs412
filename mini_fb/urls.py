# File: urls.py
# Author: Mohammed Abaherah (abaherah@bu.edu) 20 Feb 2025
# Description: Has the paths to all the correct views

from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView, CreateProfileView, CreateStatusView, UpdateProfileView, DeleteMessageStatusView, UpdateStatusMessageView, AddFriendView, ShowFriendSuggestionsView, ShowNewsFeedView
from django.contrib.auth import views as auth_views

'''our url patterns so we can link to the page we want to show'''
urlpatterns = [
    
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile', CreateProfileView.as_view(), name='create_profile'), #New   
    path('status/<int:pk>/delete', DeleteMessageStatusView.as_view(), name='delete_status'), 
    path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name='update_status'), 
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all_profiles'), name='logout'), ## NEW


     #Specific ones that we are working on removing the pk for
    path('profile/create_status', CreateStatusView.as_view(), name='create_status'), 
    path('profile/update', UpdateProfileView.as_view(), name='update_profile'), 
    path('profile/friend_suggestions', ShowFriendSuggestionsView.as_view(), name = 'friend_suggestions'),
    path('profile/add_friend/<int:friend_pk>', AddFriendView.as_view(), name='add_friend'),
    path('profile/news_feed', ShowNewsFeedView.as_view(), name = 'news_feed'),


]
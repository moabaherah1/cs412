# File: urls.py
# Author: Mohammed Abaherah (abaherah@bu.edu) 14 April 2025
# Description: Has the paths to all the correct views

from django.urls import path
from .views import  ShowAllProfilesView, ShowProfilePageView, CreateProfileView, ShowMapView, ShowCouplePostsView, DeleteCouplePostView, UpdateCouplePostView
from .views import SendInvitationView, RespondToInvitationView, ShowInvitationsView, show_events, RSVPEventView, MyRSVPEventsView, save_locations, CreateCouplePostView
from django.contrib.auth import views as auth_views
from finalproject import views

'''our url patterns so we can link to the page we want to show'''
urlpatterns = [
    
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_userprofile'),
    path('create_userprofile/', CreateProfileView.as_view(), name='create_userprofile'), 
    path('login/', auth_views.LoginView.as_view(template_name='finalproject/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all_profiles'), name='logout'),
    path('profile/invite/send/<int:to_user_pk>/', SendInvitationView.as_view(), name='send_invitation'),
    path('invite/respond/<int:invite_id>/', RespondToInvitationView.as_view(), name='respond_invite'),
    path('invitations/', ShowInvitationsView.as_view(), name='show_invitations'),
    path('events/', show_events, name='show_events'),
    path('events/rsvp/', RSVPEventView.as_view(), name='rsvp_event'),
    path('events/my_rsvps/', MyRSVPEventsView.as_view(), name='my_rsvp_events'),
    path('map_view', ShowMapView.as_view(), name='map_view'),
    path('save_locations/', save_locations, name='save_locations'),
    path('post/create/', CreateCouplePostView.as_view(), name='create_couple_post'),
    path('couple/memories/<int:pk>/', ShowCouplePostsView.as_view(), name='show_couple_posts'),
    path('couple/post/<int:pk>/delete/', DeleteCouplePostView.as_view(), name='delete_couple_post'),
    path('couple/post/<int:pk>/update/', UpdateCouplePostView.as_view(), name='update_couple_post'),
    ]
# File: urls.py
# Author: Mohammed Abaherah (abaherah@bu.edu) 20 Feb 2025
# Description: Has the paths to all the correct views

from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView


urlpatterns = [

    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),

]
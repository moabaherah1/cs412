# File: urls.py
# Author: Mohammed Abaherah (abaherah@bu.edu) 3 April 2025
# Description: Has the paths to all the correct views

from django.urls import path
from . import views
# from views import ResultsListView, VoterDetailView

urlpatterns = [
    # map the URL (empty string) to the view
	path(r'', views.ResultsListView.as_view(), name='home'),
    path(r'voter_list', views.ResultsListView.as_view(), name='voter_list'),
    path(r'voter/<int:pk>', views.VoterDetailView.as_view(), name='voter_detail'),
    path(r'graphs/', views.GraphsListView.as_view(), name='graphs'),



]
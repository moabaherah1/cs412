# File: urls.py
# Author: Mohammed Abaherah (abaherah@bu.edu) 13 Feb 2025
# Description: has all the paths to the correct views

from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static    


urlpatterns = [ 
    # path(r'', views.home, name="home"),
    path(r'', views.home, name="home"),
    path(r'main/', views.main, name="main"),
    path(r"order/", views.order, name = "order"),
    path(r"confirmation/", views.confirmation, name="confirmation")
] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
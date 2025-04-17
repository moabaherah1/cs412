# File: views.py
# Author: Mohammed Abaherah (abaherah@bu.edu) 14 April 2025
# Description: Defines our views to display what we want

from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import  DetailView, CreateView, View
from .models import UserProfile, Couple
from .forms import CreateProfileForm
from django.contrib.auth.forms import UserCreationForm

from finalproject import models

# Create your views here.
class ShowProfilePageView(DetailView):
    '''Define a view class to show a single profile page'''

    model = UserProfile 
    template_name = "finalproject/show_profile.html"
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        '''create this to have access to the context variable and be able to show the partner'''
        context = super().get_context_data(**kwargs)
        partner = self.object.get_partner()  
        context['partner'] = partner
        return context

class CreateProfileView(CreateView):
    '''Define a view class to show the profile form'''
    
    form_class = CreateProfileForm
    template_name = "finalproject/create_profile_form.html"


    def get_context_data(self, **kwargs):
        '''Add the UserCreationForm to the context'''
        context = super().get_context_data(**kwargs)
        context['user_creation_form'] = UserCreationForm() 
        return context
    
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''

        return self.object.get_absolute_url()

    def form_valid(self, form):
        '''Handle both forms when valid'''
        user_form = UserCreationForm(self.request.POST)
        
        if user_form.is_valid():
            user = user_form.save()  
            profile = form.save(commit=False)
            profile.user = user 
            profile.save()  
            return redirect('show_userprofile', pk=profile.pk)

class AddCoupleView(View):
    '''a class-based view to add a partner'''

    def dispatch(self, request, *args, **kwargs):
            if Couple.objects.filter(models.Q(user1=profile) | models.Q(user2=profile)).exists():
                partner_pk = self.kwargs.get('partner_pk')
                profile = UserProfile.objects.get(user = request.user)
                partner_profile = UserProfile.objects.get(pk = partner_pk)
                profile.add_couple(partner_profile)
            return redirect(reverse('show_profile', kwargs={'pk':profile.pk}))




# File: views.py
# Author: Mohammed Abaherah (abaherah@bu.edu) 14 April 2025
# Description: Defines our views to display what we want

from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import  DetailView, CreateView, View, ListView
from .models import UserProfile, Invitation
from .forms import CreateProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator

from finalproject import models


class ShowAllProfilesView(ListView):
    '''Define a view class to show all Profiles'''
    
    model = UserProfile
    template_name = "finalproject/show_all_profiles.html"
    context_object_name = "profiles"

    def get_queryset(self):
        return UserProfile.objects.all()

class ShowProfilePageView(DetailView):
    '''Define a view class to show a single profile page'''

    model = UserProfile 
    template_name = "finalproject/show_profile.html"

    def get_context_data(self, **kwargs):
        '''Add context to display the user's partner if they are in a couple'''
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
        '''Redirect to the newly created user's profile page'''
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


class SendInvitationView(View):
    '''A class-based view to send an invitation'''

    def post(self, request, *args, **kwargs):
        from_user = UserProfile.objects.get(user=request.user)
        to_user = UserProfile.objects.get(pk=self.kwargs['to_user_pk'])

        if not Invitation.objects.filter(from_user=from_user, to_user=to_user, responded=False).exists():
            Invitation.objects.create(from_user=from_user, to_user=to_user)

        return redirect(reverse('show_userprofile', kwargs={'pk': to_user.pk}))



@method_decorator(require_POST, name='dispatch')
class RespondToInvitationView(View):
    '''View to handle invitation response'''

    def post(self, request, *args, **kwargs):
        invite = models.Invitation.objects.get(pk=self.kwargs['invite_id'])
        user_profile = UserProfile.objects.get(user=request.user)

        if invite.to_user != user_profile:
            return HttpResponseForbidden()

        response = request.POST.get('response')
        if response == "accept":
            invite.accepted = True
            invite.from_user.add_partner(invite.to_user)

        invite.responded = True
        invite.save()

        return redirect(reverse('show_userprofile', kwargs={'pk': user_profile.pk}))
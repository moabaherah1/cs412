# File: views.py
# Author: Mohammed Abaherah (abaherah@bu.edu) 14 April 2025
# Description: Defines our views to display what we want

from django.utils import timezone
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import  DetailView, CreateView, View, ListView, FormView
from .models import UserProfile, Invitation, Couple, EventRSVP
from .forms import CreateProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from finalproject import models
import requests


class UserProfileMixIn:
    """Mixin to make things easier """
    def get_context_data(self, **kwargs):
        '''Add context to display the profile linked to the user and their partner'''
        context = super().get_context_data(**kwargs)
        user_profile = None
        partner = None
        if self.request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=self.request.user)
                partner = user_profile.get_partner()
            except UserProfile.DoesNotExist:
                pass
        context["UserProfile"] = user_profile
        context["partner"] = partner
        return context

class ShowAllProfilesView(UserProfileMixIn, ListView):
    '''Define a view class to show all Profiles'''
    
    model = UserProfile
    template_name = "finalproject/show_all_profiles.html"
    context_object_name = "profiles"

    def get_queryset(self):
        '''Returns all UserProfiles so I can display them'''
        return UserProfile.objects.all()

    def get_context_data(self, **kwargs):
        '''Overrides the getcontextdata so I can add my context to the template'''
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=self.request.user)
                sent_invites = Invitation.objects.filter(from_user=user_profile).values_list('to_user__pk', flat=True)
                context['sent_invites'] = list(sent_invites)
            except UserProfile.DoesNotExist:
                context['sent_invites'] = []
        else:
            context['sent_invites'] = []

        return context

class ShowProfilePageView(UserProfileMixIn, DetailView):
    '''Define a view class to show a single profile page'''

    model = UserProfile 
    template_name = "finalproject/show_profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        '''Add context to display the user's partner if they are in a couple'''
        context = super().get_context_data(**kwargs)
        partner = self.object.get_partner()  
        context['partner'] = partner
        return context

class CreateProfileView(UserProfileMixIn, CreateView):
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


class SendInvitationView(UserProfileMixIn, View):
    '''A view to send a invite'''

    def post(self, request, *args, **kwargs):
        '''Sends a post Request to send an invitation'''

        try:
            from_user = request.user.finalproject_profile  
        except UserProfile.DoesNotExist:
            return HttpResponseForbidden("You need to create a profile before sending invites.")

        # check if user already has a partner
        if from_user.get_partner():
            return HttpResponseForbidden("You are already in a relationship and cannot send invitations.")

        to_user_pk = self.kwargs.get('to_user_pk')

        try:
            to_user = UserProfile.objects.get(pk=to_user_pk)
        except UserProfile.DoesNotExist:
            return HttpResponseForbidden("The user you are trying to invite does not exist.")

        if to_user.get_partner():
            return HttpResponseForbidden("This user is already in a relationship.")

        Invitation.objects.create(from_user=from_user, to_user=to_user, message="You have been invited to become a couple!")

        return redirect('show_userprofile', pk=from_user.pk)



class ShowInvitationsView(UserProfileMixIn, ListView):
    """View for users to see all their received invitations."""
    
    model = Invitation
    template_name = "finalproject/show_invitations.html"
    context_object_name = "invitations"

    def get_queryset(self):
        """Filter invitations where the logged-in user is the recipient."""
        return Invitation.objects.filter(to_user__user=self.request.user)

class RespondToInvitationView(View):
    """View to handle accepting or rejecting invitations."""

    def post(self, request, *args, **kwargs):
        invite_id = self.kwargs['invite_id']
        invitation = Invitation.objects.get(pk=invite_id)
        user_profile = request.user.finalproject_profile  

        if invitation.to_user != user_profile:
            return HttpResponseForbidden("You are not authorized to respond to this invitation.")

        response = request.POST.get('response')

        if response == 'accept':
            Couple.objects.create(user1=invitation.from_user, user2=invitation.to_user, anniversary_date=timezone.now().date())
            invitation.delete()

        return redirect('show_userprofile', pk=user_profile.pk)
    


class RSVPEventView(LoginRequiredMixin, View):
    
    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        event_id = request.POST.get('event_id')
        event_title = request.POST.get('event_title')

        user = request.user
        user_profile = request.user.finalproject_profile

        # RSVPs the user
        EventRSVP.objects.get_or_create(
            user=user,
            event_id=event_id,
            defaults={'event_title': event_title}
        )

        # RSVPs the users partner automatically
        partner_profile = user_profile.get_partner()

        if partner_profile:
            EventRSVP.objects.get_or_create(
                user=partner_profile.user,  
                event_id=event_id,
                defaults={'event_title': event_title}
            )

        return redirect('show_events')



def show_events(request):
    '''Being able to display the events using the PredictHQ API for events in this function'''
    api_key = "HBcULnUIMjqoac2uNHEVX330q3u6RKEwYqDHqwEd"
    url = "https://api.predicthq.com/v1/events/"

    category = request.GET.get('category', '')  # get category from search form

    params = {
        "limit": 30,
        "sort": "start",
        "active.gte": "2025-04-25",
    }
    if category:
        params["category"] = category

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers, params=params)
    
    raw_events = response.json().get("results", []) if response.status_code == 200 else []
    
    calendar_events = []
    for event in raw_events:
        calendar_events.append({
            "id": event["id"],
            "title": event["title"],
            "start": event["start"],
            "end": event.get("end", event["start"]),
            "description": event.get("description", ""),
        })

    return render(request, "finalproject/show_events.html", {
        "calendar_events": calendar_events,
        "selected_category": category,
    })

class MyRSVPEventsView(LoginRequiredMixin, ListView):
    '''Users can see all the events they RSVPed to'''
    model = EventRSVP
    template_name = "finalproject/my_rsvp_events.html"
    context_object_name = "rsvp_events"

    def get_queryset(self):
        """Return only the RSVP events of the current logged-in user."""
        return EventRSVP.objects.filter(user=self.request.user)
# File: views.py
# Author: Mohammed Abaherah (abaherah@bu.edu) 14 April 2025
# Description: Defines our views to display what we want

from django.db.models import Q
from django.utils import timezone
from datetime import date
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import  DetailView, CreateView, View, ListView, TemplateView,DeleteView, UpdateView
from .models import UserProfile, Invitation, Couple, EventRSVP, CouplePost, CoupleImage, CouplePostImage
from .forms import CreateProfileForm, CreateCouplePostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from finalproject import models

import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json


class UserProfileMixIn:
    """Mixin to make things easier """
    def get_context_data(self, **kwargs):
        '''Add context to display the profile linked to the user and their partner'''
        context = super().get_context_data(**kwargs)
        user_profile = None
        partner = None
        couple = None
        couple_pk = None

        if self.request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=self.request.user)
                partner = user_profile.get_partner()

                if partner:
                    couple = Couple.objects.filter(
                        (Q(user1=user_profile) & Q(user2=partner)) |
                        (Q(user1=partner) & Q(user2=user_profile))
                    ).first()

                    if couple:
                        couple_pk = couple.pk

            except UserProfile.DoesNotExist:
                pass
        context["UserProfile"] = user_profile
        context["partner"] = partner
        context["couple_pk"] = couple_pk
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
    """View to actually post and rsvp the event the user clicks on rsvp for"""
    @method_decorator(require_POST)
    # ^Ensures that the used method is POST
    def post(self, request, *args, **kwargs):
        '''posts the rsvp and redirects user to show events'''
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
        "active.gte": str(date.today()),
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
    


class ShowMapView(LoginRequiredMixin, TemplateView):
    '''Users can see the Map which displays both their locations and also the distance between them :(!)'''
    template_name = "finalproject/map_view.html"

    def get_context_data(self, **kwargs):
        """Overrides get_context_data to add the logged-in user's profile
    and their partner's profile to the context for the template."""
        context = super().get_context_data(**kwargs)

        user_profile = self.request.user.finalproject_profile
        partner_profile = user_profile.get_partner()

        context['user_profile'] = user_profile
        context['partner_profile'] = partner_profile

        return context
    
@csrf_exempt
@login_required
def save_locations(request):
    '''Save your and your partner's lat/lng after typing addresses'''
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_profile = request.user.finalproject_profile

            # Save your own location
            user_profile.latitude = data.get('your_latitude')
            user_profile.longitude = data.get('your_longitude')

            # Save partner's location if you have a partner
            partner = user_profile.get_partner()
            if partner:
                partner.latitude = data.get('partner_latitude')
                partner.longitude = data.get('partner_longitude')
                partner.save()

            user_profile.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'fail'}, status=400)

class CreateCouplePostView(CreateView):
    '''View to create a new Couple Post.'''
    model = CouplePost
    form_class = CreateCouplePostForm
    template_name = "finalproject/create_couple_post_form.html"

    def form_valid(self, form):
        '''After the form is valid, handle file uploads'''
        post = form.save(commit=False)
        user_profile = self.request.user.finalproject_profile
        
        partner_profile = user_profile.get_partner()

        if not partner_profile:
            return redirect('show_all_profiles')  

        couple = Couple.objects.filter(
            Q(user1=user_profile, user2=partner_profile) |
            Q(user1=partner_profile, user2=user_profile)
        ).first()


        if not couple:
            return redirect('show_all_profiles')  

        post.couple = couple
        post.save()

        files = self.request.FILES.getlist('files')
        for f in files:
            image = CoupleImage(couple=couple, image=f)
            image.save()
            CouplePostImage(image=image, post=post).save()

        return redirect('show_couple_posts', pk=couple.pk)
    
class ShowCouplePostsView(LoginRequiredMixin, DetailView):
    '''View to show all memories for a couple'''
    model = Couple
    template_name = "finalproject/show_couple_posts.html"
    context_object_name = "couple"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        couple = self.get_object()
        posts = CouplePost.objects.filter(couple=couple).order_by('-time_stamp')
        context['posts'] = posts
        return context
    

class DeleteCouplePostView(LoginRequiredMixin, DeleteView):
    '''a class-based view to delete a status message'''
    model = CouplePost
    template_name = "finalproject/delete_couple_post_form.html"
    context_object_name = "couplepost"

    def get_success_url(self):
        '''After deleting, return to the couple's memories page'''
        return reverse('show_couple_posts', kwargs={'pk': self.object.couple.pk})


class UpdateCouplePostView(LoginRequiredMixin, UpdateView):
    '''a class-based view to update a status message'''
    model = CouplePost
    form_class = CreateCouplePostForm
    template_name = "finalproject/update_couple_post_form.html"
    context_object_name = "couplepost"

    def get_success_url(self):
        '''After updating, return to the couple's memories page'''
        return reverse('show_couple_posts', kwargs={'pk': self.object.couple.pk})
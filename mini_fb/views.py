# File: views.py
# Author: Mohammed Abaherah (abaherah@bu.edu) 20 Feb 2025
# Description: Defines our classes

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, StatusMessage, Image, StatusImage
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm

class ShowAllProfilesView(ListView):
    '''Define a view class to show all Profiles'''
    
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"

class ShowProfilePageView(DetailView):
    '''Define a view class to show a single profile page'''

    model = Profile 
    template_name = "mini_fb/show_profile.html"

class CreateProfileView(CreateView):
    '''Define a view class to show the profile form'''
    
    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''

        return self.object.get_absolute_url()


class CreateStatusView(CreateView):
    '''Define a view class for the status form'''

    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self, **kwargs):
        '''To have access to this as a context variable, you will need to implement the special method get_context_data on the CreateStatusMessageView class. '''
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        '''Within that method, you will need to (a) look up the Profile object by its pk. You can find this pk in self.kwargs['pk']. (b) attach this object to the profile attribute of the status message. '''
        
        
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile 
        # save the status message to database


        sm = form.save()
        files = self.request.FILES.getlist('files')

        for file in files:
            image = Image(profile = profile)
            image.image = file 
            image.save()

            status_image = StatusImage(image = image, statusmessage = sm)
            status_image.save()
        

        return super().form_valid(form)
        
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''

        return self.object.get_absolute_url()
    
class UpdateProfileView(UpdateView):
    '''a class-based view called UpdateProfileView, which inherits from the generic UpdateView class'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''

        return reverse('show_profile', kwargs={'pk':self.object.pk})


class DeleteMessageStatusView(DeleteView):
    '''a class-based view to delete a status message'''
    
    template_name = "mini_fb/delete_status_form.html"
    model = StatusMessage
    context_object_name = 'statusmessage'
    
    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''

        # get the pk for this status message
        pk = self.kwargs.get('pk')
        statusmessage = StatusMessage.objects.get(pk=pk)
        
        # reverse to show the profile page
        return reverse('show_profile', kwargs={'pk':statusmessage.profile.pk})


class UpdateStatusMessageView(UpdateView):
    '''a class-based view to update a status message'''

    template_name = "mini_fb/update_status_form.html"
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    
    
    # def form_valid(self, form):
    #     print(form.cleaned_data)
        
    #     return super().form_valid(form)

    def get_success_url(self):
        '''Return a the URL to which we should be directed after the update.'''

        # get the pk for this status message
        pk = self.kwargs.get('pk')
        statusmessage = StatusMessage.objects.get(pk=pk)
        
        # reverse to show the profile page
        return reverse('show_profile', kwargs={'pk':statusmessage.profile.pk})
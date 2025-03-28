# File: views.py
# Author: Mohammed Abaherah (abaherah@bu.edu) 20 Feb 2025
# Description: Defines our classes


from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Profile, StatusMessage, Image, StatusImage, Friend
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm
from django.contrib.auth.forms import UserCreationForm

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
    
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"


    def get_context_data(self, **kwargs):
        '''Add the UserCreationForm to the context'''
        context = super().get_context_data(**kwargs)
        context['user_creation_form'] = UserCreationForm()  # Add the user form to context
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
            return redirect('show_profile', pk=user.profile.pk)


class CreateStatusView(CreateView):
    '''Define a view class for the status form'''

    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self, **kwargs):
        '''To have access to this as a context variable, you will need to implement the special method get_context_data on the CreateStatusMessageView class.'''
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()  # Access the profile object here
        return context
    
    def get_object(self):
        '''Override to get the Profile object for the currently logged-in user.'''
        # Get the Profile associated with the logged-in user
        return Profile.objects.get(user=self.request.user)
    
    def form_valid(self, form):
        '''Within that method, you will need to (a) look up the Profile object by its pk. You can find this pk in self.kwargs['pk']. (b) attach this object to the profile attribute of the status message. '''
        
        
        profile = self.get_object()  
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

    
    def get_object(self, queryset=None):
        '''Override the default get_object to get the logged-in user's first profile or most recent one'''
        profile = Profile.objects.filter(user=self.request.user).first()  # Get the first profile for the user
        return profile
            
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''

        return reverse('show_profile', kwargs={'pk':self.object.pk}
        )    


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
    
class AddFriendView(View):
    '''a class-based view to add a friend'''

    def dispatch(self, request, *args, **kwargs):
            friend_pk = self.kwargs.get('friend_pk')

            profile = Profile.objects.get(user = request.user)
            friend_profile = Profile.objects.get(pk = friend_pk)

            profile.add_friend(friend_profile)

            return redirect(reverse('show_profile', kwargs={'pk':profile.pk}))
    
class ShowFriendSuggestionsView(DetailView):
    '''a class-based view to show friend suggestions'''
    
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get(self, request, *args, **kwargs):
        '''Override the default context to add news feed .'''
        profile = Profile.objects.get(user=request.user)

        friend_suggestions = profile.get_friend_suggestions()
        
        context = {
                    'profile': profile,
                    'friends_suggestions': friend_suggestions
                }
        
        return render(request, self.template_name, context)

class ShowNewsFeedView(DetailView):
    '''a class-based view to show the News Feed'''
    
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get(self, request, *args, **kwargs):
        '''Override the default context to add news feed .'''
        profile = Profile.objects.get(user=request.user)
        
        context = {
                    'profile': profile,
                    'news_feed': profile.get_news_feed()
                }
        
        return render(request, self.template_name, context)
    

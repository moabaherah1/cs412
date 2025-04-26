# File: admin.py
# Author: Mohammed Abaherah (abaherah@bu.edu) 14 April 2025
# Description: where I register the models I creatde

from django.contrib import admin

# Register your models here.

from .models import UserProfile, Couple, Invitation, EventRSVP

admin.site.register(UserProfile)
admin.site.register(Couple)
admin.site.register(Invitation)
admin.site.register(EventRSVP)
class EventRSVPAdmin(admin.ModelAdmin):
    list_display = ('user', 'event_title', 'rsvp_date')
    search_fields = ('user__username', 'event_title')
    list_filter = ('rsvp_date',)
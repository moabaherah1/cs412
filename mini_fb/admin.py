from django.contrib import admin

# Register your models here.

from .models import Profile, StatusMessage, StatusImage, Image

admin.site.register(Profile)
admin.site.register(StatusMessage) #Newmana
admin.site.register(Image)
admin.site.register(StatusImage)

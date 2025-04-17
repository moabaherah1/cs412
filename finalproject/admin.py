# File: admin.py
# Author: Mohammed Abaherah (abaherah@bu.edu) 14 April 2025
# Description: where I register the models I creatde

from django.contrib import admin

# Register your models here.

from .models import UserProfile, Couple

admin.site.register(UserProfile)
admin.site.register(Couple)
from django.contrib import admin

from .models import Profile
#register models for admin panel
admin.site.register(Profile)
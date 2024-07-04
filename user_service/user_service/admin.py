from django.contrib import admin

from .models import User
#register models for admin panel
admin.site.register(User)
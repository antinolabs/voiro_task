# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token



class User(AbstractUser):
    created_at  =   models.DateTimeField( auto_now_add=True)
    updated_at  =   models.DateTimeField(auto_now=True)

    @property
    def owner(self):
        return self.user

    
    USERNAME_FIELD = 'username'



@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)

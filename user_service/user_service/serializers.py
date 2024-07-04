
from rest_framework import serializers
from .models import *


class RUDUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','created_at','updated_at',]



class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['id','username','created_at','updated_at','password']
        extra_kwargs={
            'password':{'write_only':True}
        }


    def save(self):

        user=User(
            username=self.validated_data['username'],
        )

        password=self.validated_data['password']
        user.set_password(password)
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=100)
    password=serializers.CharField(max_length=40)
from rest_framework import serializers
from .models import Profile

class GetProfileSerializer(serializers.ModelSerializer):
    user_id     =   serializers.IntegerField()
    username    =   serializers.CharField()
    user_created_at  =   serializers.DateTimeField()
    user_updated_at  =   serializers.DateTimeField()
    class Meta:
        model  = Profile
        fields = '__all__'
        read_only_fields = ['userid','username','user_created_at','user_updated_at','created_at']

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Profile
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')




        


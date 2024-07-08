from rest_framework import serializers
from .models import Profile
from .helpers import UserHelper

class GetProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    email = serializers.EmailField()
    username = serializers.CharField()
    user_created_at = serializers.DateTimeField()
    user_updated_at = serializers.DateTimeField()
    
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('userid', 'email', 'username', 'user_created_at', 'user_updated_at')

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate(self, data):
        user_id = data.get('user_id')
        if not self.instance:
            user_detail = UserHelper.getUserDetail(user_id)
            is_profile_exist = Profile.objects.filter(user_id=user_id).exists()
            
            if user_detail['status_code'] != 200:
                print(f"Validation error: User not found for user_id {user_id}")  # Debugging line
                raise serializers.ValidationError({'user': 'User not found'})
            
            if is_profile_exist:
                print(f"Validation error: Profile already exists for user_id {user_id}")  # Debugging line
                raise serializers.ValidationError({'profile': 'Profile already exists'})
        
        return data

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

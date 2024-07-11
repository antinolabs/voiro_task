from .models import Profile
from .serializers import ProfileSerializer,GetProfileSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from .helpers import UserHelper
from rest_framework.permissions import IsAuthenticated

class CR_ProfileAPIView(GenericAPIView, ListModelMixin):

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        serialized_data = self.get_serializer(data=request.data)
        
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_201_CREATED)
        
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)



class RUD_ProfileAPIView(APIView):

    def get(self, request, user_id=None):
        user_details = UserHelper().getUserDetail(user_id)

        if user_details['status_code'] != 200:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            user_profile = Profile.objects.get(user_id=user_details['data']['id'])
        except Profile.DoesNotExist:
            return Response({"message": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"message": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data_to_serialize = {
            
            'user_id': user_details['data']['id'],
            'email'  :  user_details['data']['email'],
            'username': user_details['data']['username'],
            'user_created_at': user_details['data']['created_at'],
            'user_updated_at': user_details['data']['updated_at'],
            'firstname': user_profile.firstname,
            'lastname': user_profile.lastname,
            'role': user_profile.role,
            'dob': user_profile.dob,
            'created_at':user_profile.created_at,
            'updated_at':user_profile.updated_at
        }

        serialized_data = GetProfileSerializer(data_to_serialize)

        return Response(serialized_data.data, status=status.HTTP_200_OK)
    
    
    def patch(self, request, user_id=None, *args, **kwargs):
        try:
            profile = Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            return Response({"message": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            request.data['user_id'] = user_id
            serializer = ProfileSerializer(profile, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"An error occurred while updating the profile: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def delete(self, request, user_id=None, *args, **kwargs):
        try:
            profile = Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            return Response({"message": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            profile.delete()
            return Response({"message": "Profile deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message": f"An error occurred while deleting the profile: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



from .models import Profile
from .serializers import ProfileSerializer,GetProfileSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from .helpers import UserHelper

class CR_ProfileAPIView(GenericAPIView,ListModelMixin):
    authentication_classes=[]
    queryset    =   Profile.objects.all()
    serializer_class=ProfileSerializer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    
    def post(self,request,*args,**kwargs):
        user_id =   self.request.data['user_id']
        print('user id',request.data)
        serialized_data=self.get_serializer(data=request.data)

        if  serialized_data.is_valid():
            serialized_data.save()
                
            return Response({"error":False,'data':serialized_data.data,"status_code":status.HTTP_201_CREATED})
        
        return Response({"error":True,"msg":serialized_data.errors,"status_code":status.HTTP_400_BAD_REQUEST})

    


class RUD_ProfileAPIView(APIView):

    def get(self,request,user_id=None):

        user_details=UserHelper().getUserDetail(user_id)

        if user_details and 'username' in user_details:
            user_profile    =   Profile.objects.filter(user_id=user_details['id']).first()
            if user_profile:
                data_to_serialize   ={}
                # user data
                data_to_serialize['user_id']=user_details['id']
                data_to_serialize['username']=user_details['username']
                data_to_serialize['user_created_at']=user_details['created_at']
                data_to_serialize['user_updated_at']=user_details['updated_at']

                # profile data
                data_to_serialize['firstname']=user_profile.firstname
                data_to_serialize['lastname']=user_profile.lastname
                data_to_serialize['role']=user_profile.role
                data_to_serialize['dob']=user_profile.dob

                serialized_data=GetProfileSerializer(data=data_to_serialize)
                if serialized_data.is_valid():
                    return Response({"error":False,"data":serialized_data.data,"status_code":status.HTTP_200_OK})
                else:
                    return Response({"error":False,"msg":"not able to serialize data","status_code":status.HTTP_400_BAD_REQUEST})
                
            else:
                Response({"error":False,"msg":"profile not found","status_code":status.HTTP_404_NOT_FOUND})
            
        return Response({"error":False,"msg":"user service failed","status_code":status.HTTP_424_FAILED_DEPENDENCY})
    

    def put(self,request,user_id):
        pass

    def delete(self,request,user_id):
        pass




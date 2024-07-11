from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate,login
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


# Create your views here.
# import requests



class RegisterApiView(GenericAPIView,ListModelMixin,CreateModelMixin):
    queryset=User.objects.all()
    serializer_class=RegisterSerializer
    authentication_classes          =   []

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    
    def post(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)

        if  serializer.is_valid():
            serializer.save()
                
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    



class RUD_RegisterApi(GenericAPIView,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
    queryset    =           User.objects.all()
    serializer_class    =   RUDUserSerializer
    authentication_classes = [SessionAuthentication]

    lookup_field='id'

    def get(self,request,*args, **kwargs):
        return self.retrieve(request,*args, **kwargs)
    
    def put(self,request,*args, **kwargs):
        return self.update(request,*args, **kwargs)

    def delete(self,request,*args, **kwargs):
        return self.destroy(request,*args, **kwargs)


class LoginWithTokenAuthenticationAPIView(GenericAPIView):
    queryset= User.objects.all()
    serializer_class    =       LoginSerializer
    permission_classes     =   []
    authentication_classes =   []

    def post(self,request):
        username    =   request.data.get('username')
        password    =   request.data.get('password')

        verify_username = User.objects.filter(username=username).first()

        if not verify_username:
            response = {
			"data": {
				"message": "Your login information is invalid",
				"status": "invalid"
			}
		}
            
            return Response(response)
        
        user          =   authenticate(username=verify_username,password=password)
        print('user',user)
        if user is not None:

            token, _ = Token.objects.get_or_create(user = user)
            
           
            return Response({ 
                'token': token.key,
                'id':user.id,
            } )
        
        response = {
        "data": {
            "message": "Your login information is invalid",
            "status": "invalid"
        }
    }
        return Response(response)
    

class CheckTokenView(APIView):
    authentication_classes =   []
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        if not token:
            return Response({'detail': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
            return Response({'valid': True, 'user_id': user.id, 'username': user.username})
        except Token.DoesNotExist:
            return Response({'valid': False, 'detail': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
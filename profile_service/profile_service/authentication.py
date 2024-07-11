import requests
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class TokenCheckAuthentication(BaseAuthentication):
    def authenticate(self, request):

        auth_header = request.headers.get('Authorization')
        auth_user_id = request.data.get('user_id') or self.get_user_id_from_path(request)
        print('body user id',auth_user_id)
        print('param user id',)
        print('user id',auth_user_id)
        if not auth_header or not auth_header.startswith('Token '):
            return None

        token = auth_header.split(' ')[1]
        print('token',token)
        token_response = self.is_token_valid(token)
        if not self.is_token_valid(token):
            raise AuthenticationFailed('Invalid token')
        
        token_user_id = token_response.get('user_id')
        if str(token_user_id) != str(auth_user_id):
                    print('token user',token_user_id,'auth user id',auth_user_id)
                    raise AuthenticationFailed('User ID does not match')

        print('is token valid',self.is_token_valid(token))
        return None,None

    def is_token_valid(self, token):
        url = f'http://{settings.USER_SERVICE_HOST}:{settings.USER_SERVICE_PORT}/checktoken/'
        print('url',url)
        response = requests.post(url, data={'token': token})
        print('response------------;',response)
        if response.status_code == 200 and response.json().get('valid', False):

            return response.json()
        else:
            return False
        
    def get_user_id_from_path(self, request):
        # Extract user_id from URL path parameters
        return request.resolver_match.kwargs.get('user_id')


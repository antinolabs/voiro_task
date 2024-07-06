    
import requests
from django.conf import settings

class UserHelper:
    @staticmethod
    def getUserDetail(user_id):
        host = f"http://{settings.USER_SERVICE_HOST}:{settings.USER_SERVICE_PORT}/"
        endpoint = f"users/{user_id}"

        try:
            response = requests.get(host + endpoint)
            status_code = response.status_code
            data = response.json() if response.status_code == requests.codes.ok else None
        except requests.exceptions.RequestException as e:
            # Handle any request related exceptions 
            status_code = 500
            data = None
        except Exception as e:
            # Handle any other unexpected exceptions
            status_code = 500
            data = None

        return {"status_code": status_code, "data": data}

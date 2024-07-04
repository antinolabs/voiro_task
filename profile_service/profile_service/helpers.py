import requests

class UserHelper:
    @staticmethod
    def getUserDetail(user_id):
        host="http://127.0.0.1:8000/"
        try:
            response=requests.get(host+"users/"+str(user_id))
            return response.json()
        except Exception as e:
            return None

        


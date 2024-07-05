# import requests

# class UserHelper:
#     @staticmethod
#     def getUserDetail(user_id):
#         host="http://127.0.0.1:8001/"
#         try:
#             response=requests.get(host+"users/"+str(user_id))
#             print('respnse user detail',response.status_code)
#             print('json',response.json())
#             return {"status_code":response.status_code,"data":response.json()}
#         except Exception as e:
#             return {"status_code":response.status_code,"data":None}

        


import requests

class UserHelper:
    @staticmethod
    def getUserDetail(user_id):
        host = "http://userservice:8000/"
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

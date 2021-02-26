import json
import bcrypt
import jwt

from django.http            import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from my_settings  import SECRET_KEY, ALGORITHM
from user.models  import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        if 'Authorization' not in request.headers:
            return JsonResponse({"message":"NEED_LOGIN"}, status=401)

        access_token = request.headers['Authorization']
        
        try:
            data         = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            user         = User.objects.get(id = data['user'])
            request.user = user
        
        except jwt.DecodeError:
            return JsonResponse({"message":"INVALID_TOKEN"}, status=401)
        
        except User.DoesNotExist:
            return JsonResponse({"message":"UNKNOWN_USER"}, status=401)

        return func(self, request, *args, **kwargs)
    
    return wrapper
    
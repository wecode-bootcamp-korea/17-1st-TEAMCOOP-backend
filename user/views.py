import json
import bcrypt
import jwt

from django.http        import JsonResponse, HttpResponse
from django.views       import View
from django.db.models   import Q

from my_settings  import SECRET_KEY, ALGORITHM
from user.models  import User


class LoginView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']
        
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
            
                if bcrypt.checkpw(password.encode('utf-8'),user.password.encode('utf-8')):
                    token = jwt.encode({'user':user.id}, SECRET_KEY,ALGORITHM)
                    return JsonResponse({"MESSAGE":"SUCCESS", "ACCESS_TOKEN":token}, status = 200)
                return JsonResponse({"MESSAGE":"INVALID_PASSWORD"}, status = 401)
            return JsonResponse({"MESSAGE":"INVALID_USER"}, status = 401)
        
        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status = 400)

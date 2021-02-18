import json
import jwt
import bcrypt
import re

from django.views     import View
from django.http      import HttpResponse, JsonResponse
from django.db.models import Q

from .models      import User
from my_settings  import SECRET_KEY


MINIMUM_PASSWORD_LENGTH = 8

def validate_email(email):
    pattern = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    if not pattern.match(email):
        return False
    return True

def validate_phone_number(phone_number):
    pattern = re.compile('^[0]\d{2}\d{3,4}\d{4}$')
    if not pattern.match(phone_number):
        return False
    return True
    
class SignupView(View):
    def post(self, request):
        try:
            signup_data  = json.loads(request.body)
            name         = signup_data['name']
            email        = signup_data['email']
            confirm      = signup_data['confirm']
            phone_number = signup_data['number']
            password     = signup_data['password']

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message":"USER_ALREADY_EXISTS"}, status=400)

            if len(password) < MINIMUM_PASSWORD_LENGTH:
                return JsonResponse({"message":"PASSWORD_VALIDATION_ERROR"}, status=400)
            
            if not validate_email(email):
                return JsonResponse({"message":"EMAIL_VALIDATION_ERROR"}, status=400)
            
            if not validate_phone_number(phone_number):
                return JsonResponse({"message":"PHONENUMBER_VALIDATION_ERROR"}, status=400)
            
            hased_pw = bcrypt.hashpw(signup_data['password'].encode('utf-8'), bcrypt.gensalt())
            decoded_hashed_pw = hased_pw.decode('utf-8')
            
            User.objects.create(
                    name         = name,
                    email        = email,
                    phone_number = phone_number,
                    password     = decoded_hashed_pw
            )
            
            return JsonResponse({"message":"SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message":"KeyError"}, status=400)

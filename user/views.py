import re
import json
import bcrypt
import jwt

from django.http import JsonResponse, HttpResponse
from django.views import View
from django.db.models import Q

from my_settings import SECRET_KEY, ALGORITHM
from user.models import User


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
            signup_data = json.loads(request.body)
            name = signup_data['name']
            email = signup_data['email']
            confirm = signup_data['confirm']
            phone_number = signup_data['number']
            password = signup_data['password']

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "USER_ALREADY_EXISTS"}, status=400)

            if len(password) < MINIMUM_PASSWORD_LENGTH:
                return JsonResponse({"message": "PASSWORD_VALIDATION_ERROR"}, status=400)

            if not validate_email(email):
                return JsonResponse({"message": "EMAIL_VALIDATION_ERROR"}, status=400)

            if not validate_phone_number(phone_number):
                return JsonResponse({"message": "PHONENUMBER_VALIDATION_ERROR"}, status=400)

            hased_pw = bcrypt.hashpw(
                signup_data['password'].encode('utf-8'), bcrypt.gensalt())
            decoded_hashed_pw = hased_pw.decode('utf-8')

            User.objects.create(
                name=name,
                email=email,
                phone_number=phone_number,
                password=decoded_hashed_pw
            )

            return JsonResponse({"message": "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KeyError"}, status=400)


class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data['email']
            password = data['password']

            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)

                if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode({'user': user.id}, SECRET_KEY, ALGORITHM)
                    return JsonResponse({"message": "SUCCESS", "ACCESS_TOKEN": token}, status=200)
                
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=401)
            
            return JsonResponse({"message": "INVALID_USER"}, status=401)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

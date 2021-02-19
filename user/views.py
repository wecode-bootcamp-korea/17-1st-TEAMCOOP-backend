import re
import json
import bcrypt
import jwt
import time
import hashlib
import hmac
import base64
import requests

from random       import randint

from django.http  import JsonResponse, HttpResponse
from django.views import View
from django.utils import timezone

from my_settings  import SECRET_KEY, ALGORITHM, SMS
from user.models  import User, AuthNumber


MINIMUM_PASSWORD_LENGTH = 8

def validate_email(email):
    pattern = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    if not pattern.match(email):
        return False
    return True

class SignupView(View):
    def post(self, request):
        try:
            signup_data     = json.loads(request.body)
            name            = signup_data['name']
            email           = signup_data['email']
            phone_number    = signup_data['number']
            password        = signup_data['password']

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "USER_ALREADY_EXISTS"}, status=400)

            if len(password) < MINIMUM_PASSWORD_LENGTH:
                return JsonResponse({"message": "PASSWORD_VALIDATION_ERROR"}, status=400)

            if not validate_email(email):
                return JsonResponse({"message": "EMAIL_VALIDATION_ERROR"}, status=400)

            hased_pw          = bcrypt.hashpw(signup_data['password'].encode('utf-8'), bcrypt.gensalt())
            decoded_hashed_pw = hased_pw.decode('utf-8')

            User.objects.create(
                name          = name,
                email         = email,
                phone_number  = phone_number,
                password      = decoded_hashed_pw
            )

            return JsonResponse({"message": "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KeyError"}, status=400)

class SmsSendView(View):
    def validate_phone_number(self, phone_number):
        pattern = re.compile('^[0]\d{2}\d{3,4}\d{4}$')
        if not pattern.match(phone_number):
            return False
        return True

    def make_signature(self, string):
        secret_key    = bytes(SMS['secret_key'], 'UTF-8')
        string        = bytes(string, 'UTF-8')
        string_hmac   = hmac.new(secret_key, string, digestmod=hashlib.sha256).digest()
        string_base64 = base64.b64encode(string_hmac).decode('UTF-8')
        return string_base64

    def post(self, request):   
        try:
            data         = json.loads(request.body)
            phone_number = data['phone_number']
            
            if not self.validate_phone_number(phone_number=phone_number):
                return JsonResponse({'message':"PHONE_NUMBER_VALIDATION_ERROR"}) 

            url            = "https://sens.apigw.ntruss.com/sms/v2/services/" + SMS['service_id'] + "/messages"
            uri            = "/sms/v2/services/" + SMS['service_id'] + "/messages"
            timestamp      = str(int(time.time() * 1000))
            access_key     = SMS['access_key']
            string_to_sign = "POST " + uri + "\n" + timestamp + "\n" + access_key
            signature      = self.make_signature(string=string_to_sign)
            auth_number    = randint(1000,10000)
            headers        = { 
                "Content-Type"            : "application/json",
                "x-ncp-apigw-timestamp"	  : timestamp,
                'x-ncp-iam-access-key'    : access_key,
                'x-ncp-apigw-signature-v2': signature
            }

            body           = {
                "type": "SMS",
                "from": SMS['from_number'],
                "messages":[{"to":phone_number}],
                "content": "[coreof] Please enter [{}].".format(auth_number)  
            }

            body          = json.dumps(body)
            response      = requests.post(url, headers=headers, data=body)
            response_dict = response.json()
            status_code   = response_dict['statusCode'] if 'statusCode' in response_dict else response_dict['status']

            if int(status_code) != 202:
                return JsonResponse({"message": "SMS_SEND_FAIL"}, status=400)
                
            AuthNumber.objects.update_or_create(
                phone_number = phone_number,
                defaults     = {
                    'auth_number': auth_number
                }
            )
            return JsonResponse({"message": "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

class SmsValidationView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            phone_number = data['phone_number']
            auth_number  = int(data['auth_number'])
            user_auth    = AuthNumber.objects.get(phone_number=phone_number)
            
            if auth_number != user_auth.auth_number:
                return JsonResponse({"message":"WRONG_CODE"}, status=400)

            if (timezone.now() - user_auth.updated_at).seconds >= 60:
                return JsonResponse({"message":"TIMES_UP"}, status=400)

            return JsonResponse({"message":"SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

class LoginView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
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

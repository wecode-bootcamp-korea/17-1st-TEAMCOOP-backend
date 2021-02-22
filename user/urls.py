from django.urls import path
from .views      import SignupView, LoginView, SmsSendView, SmsValidationView

urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/login', LoginView.as_view()),
    path('/sms', SmsSendView.as_view()),
    path('/sms-validation', SmsValidationView.as_view()),
]

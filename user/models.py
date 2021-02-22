from django.db import models

class User(models.Model):
    name         = models.CharField(max_length=10)
    email        = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=20)
    password     = models.CharField(max_length=300)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

class Address(models.Model):
    user    = models.ForeignKey('User', on_delete = models.CASCADE)
    address = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=20)
    is_main  = models.BooleanField(default=True)
    order    = models.OneToOneField('order.Order', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'addresses'

#SMS발송시 인증번호(auth_number)를 저장하는 테이블.
class AuthNumber(models.Model):
    phone_number = models.CharField(primary_key=True, max_length=11)
    auth_number  = models.IntegerField()
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'auth_numbers'

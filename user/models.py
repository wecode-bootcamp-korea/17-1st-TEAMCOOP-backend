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

    class Meta:
        db_table = 'addresses'

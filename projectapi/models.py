from django.db import models

# Create your models here.

class User(models.Model):
    username=models.CharField(max_length=50)
    email=models.EmailField()
    password=models.CharField(max_length=50)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=30,unique=True)
    password= models.CharField(max_length=30)
    first_ex=models.CharField(max_length=100, unique=False, null=True)
    card_number=models.CharField(max_length=16, unique=True,null=True)
    point=models.IntegerField(unique=False, null=True)
    def __str__(self):
        return self.email



#login_id=username
#first_ex=우선권 보유 현황
#card_number=카드 번호
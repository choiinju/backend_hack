from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_ex=models.CharField(max_length=10, unique=False, null=True)
    card_number=models.CharField(max_length=20, unique=True,null=True)
	
    def __str__(self):
        return self.email
    

#first_ex=우선권 보유 현황
#card_number=카드 번호
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# 헬퍼 클래스
class UserManager(BaseUserManager):
    def create_user(self, student_id, username, password, **kwargs):
        if not student_id or len(student_id) != 9 or not student_id.isdigit():
            raise ValueError('Users must have a 9-digit numeric student ID')
        
        user = self.model(
            student_id=student_id,
            username=username,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractUser):
    login_id = models.CharField(max_length=30,unique=True)
    password= models.CharField(max_length=30)
    first_ex=models.CharField(max_length=100, unique=False, null=True)
    card_number=models.CharField(max_length=16, unique=True,null=True)
    point=models.IntegerField(unique=False, null=True)
    
    def __str__(self):
        return self.login_id



#login_id=username
#first_ex=우선권 보유 현황
#card_number=카드 번호
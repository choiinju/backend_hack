from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class User(AbstractUser):
    first_ex=models.CharField(max_length=100, unique=False, null=True)
    card_number=models.CharField(max_length=16, unique=True,null=True)
    point=models.IntegerField(unique=False, default=0)
    def __str__(self):
        return self.email

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


#login_id=username
#first_ex=우선권 보유 현황
#card_number=카드 번호

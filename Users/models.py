from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

# 헬퍼 클래스
class UserManager(BaseUserManager):
    def create_user(self, login_id, username, password, **kwargs):
        user = self.model(
            login_id=login_id,
            username=username,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

# AbstractBaseUser를 상속해서 유저 커스텀
class User(AbstractBaseUser, PermissionsMixin):
    login_id = models.CharField(max_length=30,unique=True)
    username = models.CharField(max_length=100, blank=False, null=False)
    password= models.CharField(max_length=30)
    password_check = models.CharField(max_length=100)  

    has_priority=models.BooleanField(default=False)
    card_number=models.CharField(max_length=16, unique=True,null=True)
    point=models.IntegerField(unique=False, null=True,default=1000)
    
    # 우선권 
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    priority_type = models.CharField(max_length=255, null=True)
    # 임산부이면 1, 부상자이면 2, 노약자이면 3 

	# 헬퍼 클래스 사용
    objects = UserManager()

	# 사용자의 username field는 student_id으로 설정 (student_id로 로그인)
    USERNAME_FIELD = 'login_id'
#login_id=username
#first_ex=우선권 보유 현황
#card_number=카드 번호

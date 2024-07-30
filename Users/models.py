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
    login_id = models.CharField(max_length=30, unique=True)
    username = models.CharField(max_length=100, blank=False, null=False)
    password = models.CharField(max_length=30)
    password_check = models.CharField(max_length=100, null=True, blank=True)  # password_check 필드

    has_priority = models.BooleanField(default=False)
    card_number = models.CharField(max_length=16, unique=True, null=True)
    point = models.IntegerField(default=1000, unique=False)

    # 헬퍼 클래스 사용
    objects = UserManager()

    # 사용자의 username field는 login_id으로 설정 (login_id로 로그인)
    USERNAME_FIELD = 'login_id'

    def save(self, *args, **kwargs):
        # 현재 시간보다 end_date가 큰 우선권이 있는지 확인
        current_time = timezone.now()
        if self.priority_set.filter(end_date__gt=current_time).exists():
            self.has_priority = True
        else:
            self.has_priority = False
        super().save(*args, **kwargs)

class Priority(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    priority_type = models.CharField(max_length=255, null=True)
    # 임산부이면 1, 부상자이면 2, 노약자이면 3

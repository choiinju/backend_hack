from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, Matched
import re


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'login_id', 'username', 'password', 'password_check']

    def validate(self, data):
        if data['password'] != data['password_check']:
            raise serializers.ValidationError("Passwords do not match")
        validate_password(data['password'])
        return data
    
    def validate_password(self, value):
        # 비밀번호 길이 검사
        if len(value) < 8:
            raise ValidationError("Password must be between 8 characters long.")
        # 대문자 포함 검사
        if not re.search(r'[A-Z]', value):
            raise ValidationError("Password must contain at least one uppercase letter.")
        # 숫자 포함 검사
        if not re.search(r'\d', value):
            raise ValidationError("Password must contain at least one number.")
        # 특수문자 포함 검사
        if not re.search(r'[!@#$%^&*()_+{}\[\]:;"\'<>,.?/\\|`~]', value):
            raise ValidationError("Password must contain at least one special character.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            login_id=validated_data['login_id'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class CashBackSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    cash_amount = serializers.IntegerField()

class MatchedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matched
        fields = ['yielding_user', 'receiving_user', 'date', 'review', 'describe']
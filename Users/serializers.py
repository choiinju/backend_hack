from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, Priority
import re

class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ['start_date', 'end_date', 'priority_type']

class UserSerializer(serializers.ModelSerializer):
    password_check = serializers.CharField(write_only=True)
    priority = PrioritySerializer(many=True, read_only=True)  # 우선권 정보 포함

    class Meta:
        model = User
        fields = [
            'id', 'login_id', 'username', 'password', 'password_check',
            'has_priority', 'card_number', 'point', 'priority'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password_check']:
            raise serializers.ValidationError("Passwords do not match")
        validate_password(data['password'])
        return data
    
    def validate_password(self, value):
        # 비밀번호 길이 검사
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
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
        validated_data.pop('password_check')  # password_check 필드를 제거
        user = User.objects.create_user(
            login_id=validated_data['login_id'],
            username=validated_data['username'],
            password=validated_data['password'],
            has_priority=validated_data.get('has_priority', False),
            card_number=validated_data.get('card_number', None),
            point=validated_data.get('point', 1000)
        )
        return user

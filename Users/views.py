from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": {
                        "access": access_token,
                        # "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )

            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)

            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.contrib.auth import authenticate

class LoginAPIView(APIView):
    def post(self, request):
        login_id = request.data.get('login_id')
        password = request.data.get('password')

        # 사용자 인증
        user = authenticate(request, login_id=login_id, password=password)

        if user is not None:
            # 인증이 성공한 경우
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": {
                        "user_id": user.id,
                        "login_id": user.login_id,
                        "username": user.username,
                    },
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        # "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )

            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)

            return res
        else:
            # 인증이 실패한 경우
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class GetInfoAPIView(APIView):
    def get(self, request):
        # Get the current user
        user = request.user

        # Prepare the response data
        data = {
            "user_id": user.id,
            "login_id": user.login_id,
            "username": user.username,
            "has_priority": user.has_priority, 
            "priority_type": user.priority_type,
            "end_date": user.end_date,
            "card_number": user.card_number,
            "point": user.point,
        }

        return Response(data, status=status.HTTP_200_OK)
    
class ChangePriorityAPIView(APIView):
    def post(self, request):
        # Ensure user is authenticated (assuming authentication is handled by JWT tokens)
        user = request.user

        # Retrieve priority_type from request body
        priority_type = request.data.get('priority_type')

        # Define default values for start_date and end_date
        start_date = timezone.now()

        if priority_type == '1':
            end_date = start_date + timedelta(days=365)  # 1 year later
        elif priority_type == '2':
            end_date = start_date + timedelta(weeks=2)  # 2 weeks later
        elif priority_type == '3':
            end_date = start_date + timedelta(days=30*365)  # 30 years later
        else:
            return Response({"message": "Invalid priority type"}, status=status.HTTP_400_BAD_REQUEST)

        # Update user instance
        user.has_priority = True
        user.start_date = start_date
        user.end_date = end_date
        user.priority_type = priority_type
        user.save()

        # Prepare response data
        data = {
            "user_id": user.id,
            "has_priority": user.has_priority,
            "priority_type": user.priority_type,
            "start_date": user.start_date,
            "end_date": user.end_date
        }

        return Response(data, status=status.HTTP_200_OK)
    def update_has_priority(self, user):
        # Check if user has priority based on end_date comparison
        has_priority = False
        if user.end_date is not None:
            if user.end_date >= timezone.now():
                has_priority = True
        
        # Update user instance only if has_priority status has changed
        if user.has_priority != has_priority:
            user.has_priority = has_priority
            user.save()
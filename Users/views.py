from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .serializers import CashBackSerializer

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
class EditscoreAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        yielding_user_id = request.data.get('yielding_user_id')
        receiving_user_id = request.data.get('receiving_user_id')

        try:
            yielding_user = User.objects.get(login_id=yielding_user_id)
            receiving_user = User.objects.get(login_id=receiving_user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Logic for updating points
        if receiving_user.has_priority:
            # No deduction for receiving user with priority
            pass
        else:
            # Deduction for receiving user without priority
            receiving_user.point -= 300

        # Addition for yielding user (regardless of priority)
        yielding_user.point += 150

        yielding_user.save()
        receiving_user.save()

        yielding_serializer = UserSerializer(yielding_user)
        receiving_serializer = UserSerializer(receiving_user)

        return Response({
            'success': True,
            'yielding_user': yielding_serializer.data,
            'receiving_user': receiving_serializer.data
        }, status=status.HTTP_200_OK)
class GetPriorityTypeAPIView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(login_id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        current_time = timezone.now()
        priority = None

        if user.end_date and user.end_date > current_time:
            priority = user.priority_type
        else:
            priority = "일반인"  # Default value for non-priority users

        return Response({
            'user_id': user.login_id,
            'priority_type': priority
        }, status=status.HTTP_200_OK)

class CashBackAPIView(APIView):
    def post(self, request):
        serializer = CashBackSerializer(data=request.data)
        if serializer.is_valid():
            login_id = serializer.validated_data['user_id']
            cash_amount = serializer.validated_data['cash_amount']

            try:
                user = User.objects.get(login_id=login_id)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            # 현금값을 포인트로 변환 (예: 1 현금 = 1 포인트)
            conversion_rate = 1
            points_needed = cash_amount * conversion_rate

            if user.point < points_needed:
                return Response({'error': 'Insufficient points'}, status=status.HTTP_400_BAD_REQUEST)

            # 포인트 차감
            user.point -= points_needed
            user.save()

            return Response({
                'user_id': user.id,
                'remaining_points': user.point,
                'message': f'Converted {cash_amount} cash to points. {points_needed} points deducted.'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MatchedCreateAPIView(APIView):
    def post(self, request):
        yielding_user_id = request.data.get('yielding_user_id')
        receiving_user_id = request.data.get('receiving_user_id')
        review = request.data.get('review')
        describe = request.data.get('describe')

        if not yielding_user_id or not receiving_user_id:
            return Response({'error': 'Both yielding_user_id and receiving_user_id are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            yielding_user = User.objects.get(login_id=yielding_user_id)
            receiving_user = User.objects.get(login_id=receiving_user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        matched = Matched(
            yielding_user=yielding_user,
            receiving_user=receiving_user,
            review=review,
            describe=describe
        )
        matched.save()

        serializer = MatchedSerializer(matched)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class GetDescribeAPIView(APIView):
    def post(self, request):
        yielding_user_id = request.data.get('yielding_user_id')
        receiving_user_id = request.data.get('receiving_user_id')
        date = request.data.get('date')

        if not yielding_user_id or not receiving_user_id or not date:
            return Response({'error': 'yielding_user_id, receiving_user_id, and date are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            yielding_user = User.objects.get(login_id=yielding_user_id)
            receiving_user = User.objects.get(login_id=receiving_user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            matched = Matched.objects.get(yielding_user=yielding_user, receiving_user=receiving_user, date=date)
        except Matched.DoesNotExist:
            return Response({'error': 'Matched event not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'describe': matched.describe}, status=status.HTTP_200_OK)
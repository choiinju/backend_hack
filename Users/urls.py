from django.urls import path
from .views import RegisterAPIView, LoginAPIView

urlpatterns = [
    path('signup/', RegisterAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
]

from django.urls import path
from .views import RegisterAPIView, LoginAPIView, GetInfoAPIView, ChangePriorityAPIView

urlpatterns = [
    path('signup/', RegisterAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('getInfo/', GetInfoAPIView.as_view(), name='getInfo'),
    path('changeMode/', ChangePriorityAPIView.as_view(), name='change_mode'),

]

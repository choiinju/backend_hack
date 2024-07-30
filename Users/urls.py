from django.urls import path
from .views import RegisterAPIView, LoginAPIView, GetInfoAPIView, ChangePriorityAPIView, EditscoreAPIView,CashBackAPIView,GetPriorityTypeAPIView



urlpatterns = [
    path('signup/', RegisterAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('getInfo/', GetInfoAPIView.as_view(), name='getInfo'),
    path('changeMode/', ChangePriorityAPIView.as_view(), name='change_mode'),
    path('edit_score/',EditscoreAPIView.as_view(),name='edit_score'),
    path('api/get-priority-type/<int:user_id>/', GetPriorityTypeAPIView.as_view(), name='get-priority-type'),
    path('api/cash_back/', CashBackAPIView.as_view(), name='cash_back'),
]

from django.urls import path
<<<<<<< HEAD

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
=======
from .views import RegisterAPIView, LoginAPIView, GetInfoAPIView, ChangePriorityAPIView, EditscoreAPIView

urlpatterns = [
    path('signup/', RegisterAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('getInfo/', GetInfoAPIView.as_view(), name='getInfo'),
    path('changeMode/', ChangePriorityAPIView.as_view(), name='change_mode'),
    path('edit_score/',EditscoreAPIView.as_view(),name='edit_score')
]
>>>>>>> nayeon-real

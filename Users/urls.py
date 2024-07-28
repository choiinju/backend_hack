# Users/urls.py
from django.urls import path
from .views import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', lambda request: render(request, 'Users/index.html'), name='index'),  # index view
]
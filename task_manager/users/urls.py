from django.urls import path, include
from .views import UserRegistration

urlpatterns = [
    path('auth/registration/', UserRegistration.as_view(), name='register_user'),
]
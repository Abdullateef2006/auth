from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('register_api/', SignupAPIView.as_view(), name='signup_api'),

    
]
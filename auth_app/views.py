from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.core.mail import send_mail
import requests
from django.urls import reverse
from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.conf import settings


from django.contrib.auth import login
from .serializers import SignupSerializer

class SignupAPIView(APIView):
    """
    API View to handle user signup.
    """
    serializer_class = SignupSerializer
    def post(self, request):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            # Create the user
            user = serializer.save()

            # Automatically log in the user after registration
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            # Return success response
            return Response(
                {"message": "Account created successfully!", "user": {
                    "username": user.username,
                    "email": user.email
                }},
                status=status.HTTP_201_CREATED
            )

        # Return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    

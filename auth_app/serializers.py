from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer to validate and create a new user.
    """
    password1 = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def validate(self, data):
        """
        Custom validation logic.
        """
        # Ensure the two passwords match
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        # Check if the email is already in use
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists."})

        # Check if the username is already in use
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Username already exists."})

        return data

    def create(self, validated_data):
        """
        Create a user instance with a profile.
        """
        # Remove `password1` and `password2` since they are not fields on the `User` model
        validated_data.pop('password2')
        password = validated_data.pop('password1')

        # Create the user
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        # Create a default UserProfile for the user

        return user

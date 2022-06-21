from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from .models import User


class RegisterSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    password = serializers.CharField(
        max_length=128, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        max_length=128, min_length=6, write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'token')

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = User.objects.filter(email=email).first()

        if not user:
            raise NotAuthenticated("User not registered.")

        if not user.check_password(password):
            raise AuthenticationFailed("Invalid credentials.")

        if not user.is_active:
            raise NotAuthenticated("User is not active.")
        validated_data = {
            "id": user.id,
            "email": user.email,
            "token": user.token
        }
        return validated_data

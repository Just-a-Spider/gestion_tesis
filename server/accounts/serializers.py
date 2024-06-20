from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *

"""
We need to create a custom serializer to include the role in the token.
This way we can modify permissions based on the role.
"""
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['code'] = user.code
        token['role'] = user.__class__.__name__
        # ...

        return token

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = [
            'code',
            'first_name', 
            'last_name', 
            'email'
        ]

class RegisterSerializer(serializers.ModelSerializer):
    code = serializers.CharField(
        max_length=BaseUser._meta.get_field(BaseUser.USERNAME_FIELD).max_length
    )
    password = serializers.CharField(
        max_length=128,
        write_only=True
    )
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    
class LoginSerializer(serializers.Serializer):
    code = serializers.CharField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(write_only=True, required=False)


from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import *
from prog_acad.serializers import ProgAcadSerializer
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
        user_class = str(user.__class__.__name__)
        token['role'] = user_class.lower()
        # ...

        return token
    
class CustomTokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = attrs['refresh']
        data = {'refresh': refresh}
        serializer = CustomTokenObtainPairSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

class BaseUserSerializer(serializers.ModelSerializer):
    prog_acad = ProgAcadSerializer()
    class Meta:
        fields = [
            'code',
            'first_name', 
            'last_name', 
            'email',
            'prog_acad',
        ]

class TesistaSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = Tesista

class ProfesorSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = Profesor
        fields = [
            'code',
            'first_name', 
            'last_name', 
            'email',
            'prog_acad',
            'tesis_dirigidas',
            'tesis_juradas',
        ]

class CoordinadorSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = Coordinador

class DecanaSerializer(BaseUserSerializer):
    class Meta:
        model = Decana
        fields = [
            'code',
            'first_name', 
            'last_name', 
            'email',
            'facultad',
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


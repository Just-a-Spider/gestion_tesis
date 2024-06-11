from rest_framework import serializers
from .models import Usuario
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'username',
            'first_name', 
            'last_name', 
            'email'
        ]

class CustomRegisterSerializer(RegisterSerializer):
    username = None
    email = None
    codigo = serializers.CharField(max_length=10)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)

    def save(self, request):
        user = super().save(request)
        self.custom_signup(request, user)
        return user

    class Meta:
        model = Usuario

    def custom_signup(self, request, user):
        try:
            user.username = self.validated_data.get('codigo')
            user.first_name = self.validated_data.get('first_name')
            user.last_name = self.validated_data.get('last_name')
            email = user.username + '@sgt.edu.pe'
            user.email = email
            user.save()
            return super().custom_signup(request, user)
        except Exception as e:
            print(e)
            raise serializers.ValidationError(e)

class CustomLoginSerializer(LoginSerializer):
    # Blank Original Fields
    username = None
    email = None
    password = None

    # Custom Fields
    codigo = serializers.CharField(max_length=10)
    contraseña = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        codigo = attrs.get('codigo')
        contraseña = attrs.get('contraseña')
        user = self.get_auth_user(
            username=codigo, 
            password=contraseña, 
            email=codigo + '@sgt.edu.pe'
        )
        if user:
            if not user.check_password(contraseña):
                raise serializers.ValidationError('Contraseña incorrecta')
        else:
            raise serializers.ValidationError('Usuario no encontrado')
        attrs['user'] = user
        return attrs


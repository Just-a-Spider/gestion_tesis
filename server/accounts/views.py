from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from .models import Tesista
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from .authentication import CustomJWTAuthentication
from .constants import role_to_model, serializer_class_map
from django.utils import timezone

# Custom TokenObtainPairView to include the role in the token
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'detail': 'No se encontró el token de refresco'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CustomTokenRefreshSerializer(data={'refresh': refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'detail': 'Token de refresco no válido'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'access_token': str(serializer.validated_data['access'])})

class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get('code')
        password = serializer.validated_data.get('password')
        first_name = serializer.validated_data.get('first_name')
        last_name = serializer.validated_data.get('last_name')
        email = code + '@udh.edu.pe'

        # Check if the user already exists
        if Tesista.objects.filter(code=code).exists():
            return Response({'detail': 'Usuario ya registrado'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        user = Tesista(
            code=code,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        user.set_password(password)
        user.save()

        return Response({'detail': 'Registro Exitoso'}, status=status.HTTP_201_CREATED)

def set_cookie(response, name, value, path):
    response.set_cookie(
        name,
        value,
        httponly=True,
        samesite='Strict',
        secure=True,  # Consider environment to toggle this for development
        path=path
    )

def login_success_response(user):
    refresh = CustomTokenObtainPairSerializer.get_token(user)
    user.last_login = timezone.now()
    user.save()
    response = Response({'detail': 'Login successful'})
    set_cookie(response, 'refresh_token', str(refresh), '/accounts/refresh')
    set_cookie(response, 'access_token', str(refresh.access_token), '/')
    return response

def authenticate_user(user, password):
    if not user.check_password(password) or not user.is_active:
        return Response({'detail': 'Credenciales Incorrectas'}, status=status.HTTP_401_UNAUTHORIZED)
    return login_success_response(user)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'detail': 'Datos de entrada no válidos'}, status=status.HTTP_400_BAD_REQUEST)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        role = serializer.validated_data.get('role')

        if role in role_to_model:
            model = role_to_model[role]
        else:
            return Response({'detail': 'Rol no Válido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = model.objects.get(username=username)
            if user.is_email_verified == False:
                return Response({'detail': 'Email no Verificado'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'detail': 'Usuario no Encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        if role != 'ciudadano':
            if user.password == password:
                return login_success_response(user)
            else:
                return Response({'detail': 'Credenciales Incorrectas'}, status=status.HTTP_401_UNAUTHORIZED)

        return authenticate_user(user, password)
    
class LogoutView(APIView):
    def post(self, request):
        response = Response({'detail': 'Logout successful'})
        response.delete_cookie('refresh_token')
        response.delete_cookie('access_token')
        return response

class MeView(RetrieveAPIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        user = self.request.user
        user_class_name = user.__class__.__name__
        return serializer_class_map[user_class_name]
    
    def get_object(self):
        user = self.request.user
        if not user:
            raise NotFound('User not found')
        return user
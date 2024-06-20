from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Tesista, Profesor, Coordinador, Decana, SecretariaCoord, SecretariaFacultad
from .serializers import RegisterSerializer, LoginSerializer, UsuarioSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Custom TokenObtainPairView to include the role in the token
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

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
            return Response({'detail': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        user = Tesista(
            code=code,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        user.set_password(password)
        user.save()

        return Response({'detail': 'Registration successful'}, status=status.HTTP_201_CREATED)

# Dictionary to map the role to the model
role_to_model = {
    'Tesista': Tesista,
    'Profesor': Profesor,
    'Coordinador': Coordinador,
    'SecretariaCoord': SecretariaCoord,
    'Decana': Decana,
    'SecretariaFacultad': SecretariaFacultad
}

class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get('code')
        password = serializer.validated_data.get('password')
        role = serializer.validated_data.get('role') or None

        # Determine the model based role provided or not
        if role is None:
            Model = role_to_model['tesista']
        elif role in role_to_model:
            Model = role_to_model[role]
        else:
            return Response({'detail': 'Invalid code length'}, status=status.HTTP_400_BAD_REQUEST)

        # Query the correct model
        try:
            user = Model.objects.get(code=code)
        except Model.DoesNotExist:
            return Response({'detail': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Check the password
        if user.password_changed:
            user = authenticate(request=request, code=code, password=password)
        else:
            if user.password != password:
                return Response({'detail': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)
            
        # Check if the user is active
        if user and user.is_active:
            refresh = CustomTokenObtainPairSerializer.get_token(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })

        return Response({'detail': 'Inactive user'}, status=status.HTTP_403_FORBIDDEN)
    
class MeView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            serializer = UsuarioSerializer(request.user)
            return Response(serializer.data)
        return Response({'detail': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
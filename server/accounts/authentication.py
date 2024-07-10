from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import *
from .constants import role_to_model

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        
        role = validated_token['role']
        user_model = role_to_model.get(role)
        user = user_model.objects.get(code=validated_token['code'])

        return (user, validated_token)
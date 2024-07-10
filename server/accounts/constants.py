from .models import *
from .serializers import *
# Dictionary to map the role to the model usage on the custom jwt authentication
role_to_model = {
    'tesista': Tesista,
    'profesor': Profesor,
    'coordinador': Coordinador,
    'decana': Decana,
}

serializer_class_map = {
    'Tesista': TesistaSerializer,
    'Profesor': ProfesorSerializer,
    'Coordinador': CoordinadorSerializer,
    'Decana': DecanaSerializer,
}
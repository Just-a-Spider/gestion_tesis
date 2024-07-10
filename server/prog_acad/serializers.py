from rest_framework.serializers import ModelSerializer
from .models import Facultad, ProgAcad

class FacultadSerializer(ModelSerializer):
    class Meta:
        model = Facultad
        fields = '__all__'

class ProgAcadSerializer(ModelSerializer):
    facultad = FacultadSerializer()

    class Meta:
        model = ProgAcad
        fields = '__all__'

from rest_framework import serializers
from .models import PropuestaTesis, Tesis, Observacion
from accounts.serializers import TesistaSerializer

class PropuestaTesisSerializer(serializers.ModelSerializer):
    tesista = TesistaSerializer(read_only=True)

    class Meta:
        model = PropuestaTesis
        fields = [
            'id',
            'titulo',
            'docu',
            'fecha',
            'tesista'
        ]

class TesisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tesis
        fields = '__all__'

class ObservacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observacion
        fields = '__all__'

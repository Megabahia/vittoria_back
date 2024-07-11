from rest_framework import serializers

from .models import Integraciones


class IntegracionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Integraciones
        fields = '__all__'

class IntegracionesListaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Integraciones
        fields = '__all__'


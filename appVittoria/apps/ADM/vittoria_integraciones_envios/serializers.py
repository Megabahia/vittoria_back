from rest_framework import serializers

from .models import IntegracionesEnvios


class IntegracionesEnviosSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegracionesEnvios
        fields = '__all__'

class IntegracionesEnviosListaSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegracionesEnvios
        fields = '__all__'


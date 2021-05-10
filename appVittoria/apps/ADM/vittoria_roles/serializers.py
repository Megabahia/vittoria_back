from rest_framework import serializers
from apps.ADM.vittoria_roles.models import Roles

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'

class RolCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['id','nombre','created_at']

class RolFiltroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['id','codigo','nombre']

from rest_framework import serializers

from apps.MDP.mdp_subCategorias.models import SubCategorias
from apps.MDP.mdp_categorias.serializers import CategoriasListarSerializer

class SubCategoriasSerializer(serializers.ModelSerializer):
    categoria = CategoriasListarSerializer(many=False, read_only=True)
    class Meta:
        model = SubCategorias
       	fields = '__all__'
    def to_representation(self, instance):
        data = super(SubCategoriasSerializer, self).to_representation(instance)
        categoria = data.pop('categoria')
        if categoria['nombre']:
            data['categoria'] = categoria['nombre']
        return data

# LISTAR SUB CATEGORIAS
class SubCategoriasListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategorias
       	fields = ['id','nombre']

from rest_framework import serializers

from apps.MDP.mdp_subCategorias.models import SubCategorias


class SubCategoriasSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategorias
       	fields = '__all__'

# LISTAR SUB CATEGORIAS
class SubCategoriasListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategorias
       	fields = ['id','nombre']

from rest_framework import serializers

from apps.MDP.mdp_productos.models import (
    Productos, ReporteAbastecimiento, ReporteStock, ReporteCaducidad, ReporteRotacion, ReporteRefil
)


class ProductosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
       	fields = '__all__'

class ProductosListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
       	fields = ['id','codigoBarras','nombre','categoria','subCategoria','stock','estado']

# STOCK
class AbastecimientoListSerializer(serializers.ModelSerializer):
    producto = ProductosSerializer(many=False, read_only=True)
    class Meta:
        model = ReporteAbastecimiento
       	fields = '__all__'
    def to_representation(self, instance):
        data = super(AbastecimientoListSerializer, self).to_representation(instance)
        producto = data.pop('producto')
        if producto['codigoBarras']:
            data['codigoBarras'] = producto['codigoBarras']
        if producto['nombre']:
            data['nombre'] = producto['nombre']
        if producto['categoria']:
            data['categoria'] = producto['categoria']
        if producto['subCategoria']:
            data['subCategoria'] = producto['subCategoria']
        if producto['stock']:
            data['stock'] = producto['stock']
        if producto['alertaAbastecimiento']:
            data['alertaAbastecimiento'] = producto['alertaAbastecimiento']
        return data

# STOCK
class StockListSerializer(serializers.ModelSerializer):
    producto = ProductosSerializer(many=False, read_only=True)
    class Meta:
        model = ReporteStock
       	fields = '__all__'
    def to_representation(self, instance):
        data = super(StockListSerializer, self).to_representation(instance)
        producto = data.pop('producto')
        if producto['codigoBarras']:
            data['codigoBarras'] = producto['codigoBarras']
        if producto['nombre']:
            data['nombre'] = producto['nombre']
        if producto['categoria']:
            data['categoria'] = producto['categoria']
        if producto['subCategoria']:
            data['subCategoria'] = producto['subCategoria']
        if producto['stock']:
            data['stock'] = producto['stock']
        return data

# CADUCIDAD
class CaducidadListSerializer(serializers.ModelSerializer):
    producto = ProductosSerializer(many=False, read_only=True)
    class Meta:
        model = ReporteCaducidad
       	fields = '__all__'
    def to_representation(self, instance):
        data = super(CaducidadListSerializer, self).to_representation(instance)
        producto = data.pop('producto')
        if producto['codigoBarras']:
            data['codigoBarras'] = producto['codigoBarras']
        if producto['nombre']:
            data['nombre'] = producto['nombre']
        if producto['categoria']:
            data['categoria'] = producto['categoria']
        if producto['subCategoria']:
            data['subCategoria'] = producto['subCategoria']
        return data

# ROTACION
class RotacionListSerializer(serializers.ModelSerializer):
    producto = ProductosSerializer(many=False, read_only=True)
    class Meta:
        model = ReporteRotacion
       	fields = '__all__'
    def to_representation(self, instance):
        data = super(RotacionListSerializer, self).to_representation(instance)
        producto = data.pop('producto')
        if producto['codigoBarras']:
            data['codigoBarras'] = producto['codigoBarras']
        if producto['nombre']:
            data['nombre'] = producto['nombre']
        if producto['categoria']:
            data['categoria'] = producto['categoria']
        if producto['subCategoria']:
            data['subCategoria'] = producto['subCategoria']
        return data

# REFIL
class RefilListSerializer(serializers.ModelSerializer):
    producto = ProductosSerializer(many=False, read_only=True)
    class Meta:
        model = ReporteRefil
       	fields = '__all__'
    def to_representation(self, instance):
        data = super(RefilListSerializer, self).to_representation(instance)
        producto = data.pop('producto')
        if producto['codigoBarras']:
            data['codigoBarras'] = producto['codigoBarras']
        if producto['nombre']:
            data['nombre'] = producto['nombre']
        if producto['categoria']:
            data['categoria'] = producto['categoria']
        if producto['subCategoria']:
            data['subCategoria'] = producto['subCategoria']
        return data


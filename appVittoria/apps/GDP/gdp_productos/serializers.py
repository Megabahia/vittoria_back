from rest_framework import serializers

from .models import (
    Productos, ProductoArchivos,
)


class ProductosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
        fields = '__all__'


# DETALLES IMAGENES
class DetallesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoArchivos
        fields = '__all__'


# IMAGEN URL
class ImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoArchivos
        fields = ['archivo', ]


# CREAR PRODUCTO
class ProductoCreateSerializer(serializers.ModelSerializer):
    imagenes = DetallesSerializer(many=True, required=False, allow_null=True, allow_empty=True)

    class Meta:
        model = Productos
        fields = '__all__'

    def create(self, validated_data):
        if "imagenes" in validated_data:
            detalles_data = validated_data.pop('imagenes')
            producto = Productos.objects.create(**validated_data)
            for detalle_data in detalles_data:
                ProductoArchivos.objects.create(producto=producto, **detalle_data)
        else:
            producto = Productos.objects.create(**validated_data)
        return producto

    def to_representation(self, instance):
        data = super(ProductoCreateSerializer, self).to_representation(instance)
        archivos = data.pop('imagenes')
        if archivos:
            imagenes = ProductoArchivos.objects.filter(producto=instance, tipo='imagen')
            data['imagenes'] = DetallesSerializer(imagenes, many=True).data
            video = ProductoArchivos.objects.filter(producto=instance, tipo='video').first()
            data['video'] = DetallesSerializer(video).data
        return data


# ACTUALIZAR PRODUCTO
class DetallesImagenesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = ProductoArchivos
        fields = '__all__'


class ProductosActualizarSerializer(serializers.ModelSerializer):
    imagenes = DetallesImagenesSerializer(many=True, required=False, allow_null=True, allow_empty=True)

    class Meta:
        model = Productos
        fields = '__all__'

    def create(self, validated_data):
        detalles_data = validated_data.pop('imagenes')
        producto = Productos.objects.create(**validated_data)
        for detalle_data in detalles_data:
            ProductoArchivos.objects.create(producto=producto, **detalle_data)
        return producto

    def update(self, instance, validated_data):
        if "imagenes" in validated_data:
            detalles_database = {detalle.id: detalle for detalle in instance.imagenes.all()}
            detalles_actualizar = {item['id']: item for item in validated_data['imagenes']}

            # Actualiza el producto
            instance.__dict__.update(validated_data)
            instance.save()

            # Eliminar los imagenes que no esté incluida en la solicitud de la productos imagenes
            # for detalle in instance.imagenes.all():
            #     if detalle.id not in detalles_actualizar:
            #         detalle.archivo.delete()
            #         detalle.delete()

            # Crear o actualizar instancias de imagenes que se encuentran en la solicitud de producto imagenes
            for detalle_id, data in detalles_actualizar.items():
                detalle = detalles_database.get(detalle_id, None)
                if detalle is None:
                    data.pop('id')
                    data['producto_id'] = instance.id
                    ProductoArchivos.objects.create(**data)
                # else:
                #     now = timezone.localtime(timezone.now())
                #     data['updated_at'] = str(now)
                #     ProductoArchivos.objects.filter(id=detalle.id).update(**data)
        else:
            # Actualiza el producto
            instance.__dict__.update(validated_data)
            instance.save()

        return instance


# LISTAR PRODUCTOS TABLA
class ProductosListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
        fields = '__all__'

    def to_representation(self, instance):
        data = super(ProductosListSerializer, self).to_representation(instance)
        imagenes = ProductoArchivos.objects.filter(producto=instance, tipo='imagen')
        if imagenes:
            data['imagenes'] = DetallesSerializer(imagenes, many=True).data
        video = ProductoArchivos.objects.filter(producto=instance, tipo='video')
        if video:
            data['video'] = DetallesSerializer(video, many=True).data
        return data

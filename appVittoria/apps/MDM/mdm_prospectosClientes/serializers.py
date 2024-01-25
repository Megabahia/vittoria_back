from rest_framework import serializers
from import_export import resources

from .models import ProspectosClientes, ProspectosClientesDetalles

# CREAR
class ProspectosClientesDetallesSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()

    class Meta:
        model = ProspectosClientesDetalles
        fields = '__all__'


# ACTUALIZAR
class ActualizarProspectosClientesDetallesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = ProspectosClientesDetalles
        fields = '__all__'

# UTILIZO CREATE, UPDATE, RETRIEVE
class ProspectosClientesSerializer(serializers.ModelSerializer):
    detalles = ProspectosClientesDetallesSerializer(many=True, allow_empty=False)

    class Meta:
        model = ProspectosClientes
        fields = '__all__'

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        print('detalles', detalles_data)
        prospectoClienteEncabezado = ProspectosClientes.objects.create(**validated_data)
        for detalle_data in detalles_data:
            ProspectosClientesDetalles.objects.create(prospectoClienteEncabezado=prospectoClienteEncabezado, **detalle_data)
        return prospectoClienteEncabezado

    def update(self, instance, validated_data):
        detalles_database = {detalle.id: detalle for detalle in instance.detalles.all()}
        detalles_actualizar = {item['id']: item for item in validated_data['detalles']}
        # data_mapping = {item['id']: item for item in validated_data.pop('detalles')}

        # Actualiza la factura cabecera
        instance.__dict__.update(validated_data)
        instance.save()

        # Eliminar los detalles que no esté incluida en la solicitud de la factura detalles
        for detalle in instance.detalles.all():
            if detalle.id not in detalles_actualizar:
                detalle.delete()

        # Crear o actualizar instancias de detalles que se encuentran en la solicitud de factura detalles
        for detalle_id, data in detalles_actualizar.items():
            detalle = detalles_database.get(detalle_id, None)
            if detalle is None:
                data.pop('id')
                ProspectosClientesDetalles.objects.create(**data)
            else:
                # now = timezone.localtime(timezone.now())
                # data['updated_at'] = str(now)
                ProspectosClientesDetalles.objects.filter(id=detalle.id).update(**data)

        return instance

# UTILIZO CREATE, UPDATE, RETRIEVE

class ActualizarProspectosClientesSerializer(serializers.ModelSerializer):
    detalles = ActualizarProspectosClientesDetallesSerializer(many=True, allow_empty=False)

    class Meta:
        model = ProspectosClientes
        fields = '__all__'

    def update(self, instance, validated_data):
        detalles_database = {detalle.id: detalle for detalle in instance.detalles.all()}
        detalles_actualizar = {item['id']: item for item in validated_data['detalles']}
        # data_mapping = {item['id']: item for item in validated_data.pop('detalles')}

        # Actualiza la factura cabecera
        instance.__dict__.update(validated_data)
        instance.save()

        # Eliminar los detalles que no esté incluida en la solicitud de la factura detalles
        for detalle in instance.detalles.all():
            if detalle.id not in detalles_actualizar:
                detalle.delete()

        # Crear o actualizar instancias de detalles que se encuentran en la solicitud de factura detalles
        for detalle_id, data in detalles_actualizar.items():
            detalle = detalles_database.get(detalle_id, None)
            if detalle is None:
                data.pop('id')
                ProspectosClientesDetalles.objects.create(**data)
            else:
                # now = timezone.localtime(timezone.now())
                # data['updated_at'] = str(now)
                ProspectosClientesDetalles.objects.filter(id=detalle.id).update(**data)

        return instance


class ProspectosClientesSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProspectosClientes
        fields = ['id', 'nombres', 'apellidos', 'telefono', 'identificacion', 'whatsapp', 'codigoProducto',
                  'nombreProducto', 'precio']


class ProspectosClientesListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProspectosClientes
        fields = ['id', 'nombres', 'apellidos', 'whatsapp', 'correo1', 'correo2', 'ciudad', 'codigoProducto',
                  'created_at', 'confirmacionProspecto']


class ProspectosClienteImagenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProspectosClientes
        fields = ['imagen', 'updated_at']


class ProspectosClientesResource(resources.ModelResource):
    class Meta:
        model = ProspectosClientes
        exclude = ('id', 'created_at', 'updated_at', 'state')

from rest_framework import serializers
from import_export import resources

from .models import Contactos, ContactosDetalles

# CREAR
class ContactosDetallesSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()

    class Meta:
        model = ContactosDetalles
        fields = '__all__'


# ACTUALIZAR
class ActualizarContactosDetallesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = ContactosDetalles
        fields = '__all__'

# UTILIZO CREATE, UPDATE, RETRIEVE
class ContactosSerializer(serializers.ModelSerializer):
    detalles = ContactosDetallesSerializer(many=True, allow_empty=False)

    class Meta:
        model = Contactos
        fields = '__all__'

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        contactoEncabezado = Contactos.objects.create(**validated_data)
        for detalle_data in detalles_data:
            ContactosDetalles.objects.create(contactoEncabezado=contactoEncabezado, **detalle_data)
        return contactoEncabezado

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
                ContactosDetalles.objects.create(**data)
            else:
                # now = timezone.localtime(timezone.now())
                # data['updated_at'] = str(now)
                ContactosDetalles.objects.filter(id=detalle.id).update(**data)

        return instance

# UTILIZO CREATE, UPDATE, RETRIEVE

class ActualizarContactosSerializer(serializers.ModelSerializer):
    detalles = ActualizarContactosDetallesSerializer(many=True, allow_empty=False)

    class Meta:
        model = Contactos
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
        print(detalles_actualizar.items())
        for detalle_id, data in detalles_actualizar.items():
            detalle = detalles_database.get(detalle_id, None)
            if detalle is None:
                print('if')
                data.pop('id')
                ContactosDetalles.objects.create(**data)
            else:
                print('else')
                # now = timezone.localtime(timezone.now())
                # data['updated_at'] = str(now)
                ContactosDetalles.objects.filter(id=detalle.id).update(**data)

        return instance


class ContactosSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contactos
        fields = ['id', 'nombres', 'apellidos', 'telefono', 'identificacion', 'whatsapp', 'codigoProducto',
                  'nombreProducto', 'precio']


class ContactosListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contactos
        fields = ['id', 'nombres', 'apellidos', 'whatsapp', 'correo1', 'correo2', 'ciudad', 'codigoProducto',
                  'created_at', 'confirmacionProspecto','canalOrigen','identificacion']


class ContactoImagenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contactos
        fields = ['imagen', 'updated_at']


class ContactosResource(resources.ModelResource):
    class Meta:
        model = Contactos
        exclude = ('id', 'created_at', 'updated_at', 'state')

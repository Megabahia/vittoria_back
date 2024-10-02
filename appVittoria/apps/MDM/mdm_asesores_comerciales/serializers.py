from rest_framework import serializers
from import_export import resources

from .models import AsesoresComerciales
from .models import MovimientosAsesores

class AsesoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsesoresComerciales
        fields = '__all__'


class AsesorCrearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsesoresComerciales
        fields = ['nombres', 'apellidos', 'email', 'pais', 'whatsapp',
                  'estado','provincia', 'fecha_nacimiento', 'ciudad', 'gender','created_at']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self):
        asesor = AsesoresComerciales(
            nombres=self.validated_data['nombres'],
            apellidos=self.validated_data['apellidos'],
            email=self.validated_data['email'],
            pais=self.validated_data['pais'],
            provincia=self.validated_data['provincia'],
            ciudad=self.validated_data['ciudad'],
            gender=self.validated_data['gender'],
            whatsapp=self.validated_data['whatsapp'],
            estado=self.validated_data['estado'],
            fecha_nacimiento=self.validated_data['fecha_nacimiento'],
        )
        asesor.save()
        return asesor


class AsesorImagenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AsesoresComerciales
        fields = ['imagen', 'updated_at']


class AsesorFiltroSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsesoresComerciales
        fields = ['id', 'nombres', 'apellidos']

    def to_representation(self, instance):
        data = super(AsesorFiltroSerializer, self).to_representation(instance)
        # tomo y uno los nombres y apellidos y los asigno a la data como nombre
        nombreCompleto = str(data.pop('nombres')) + " " + str(data.pop('apellidos'))
        data.update({"nombre": nombreCompleto})
        return data


class AsesorResource(resources.ModelResource):
    class Meta:
        model = AsesoresComerciales
        exclude = ('id', 'idPadre', 'password', 'last_login', 'imagen', 'idRol', 'created_at', 'updated_at', 'state')


#MOVIMIENTOS
class MovimientosAsesoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientosAsesores
        fields = '__all__'
from rest_framework import serializers

from apps.MDM.mdm_negocios.models import Negocios, DireccionesEstablecimientosNegocios, PersonalNegocios

# NEGOCIOS
class NegociosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Negocios
       	fields = '__all__'



# DIRECCIONES ESTABLECIMIENTOS
class DireccionesEstablecimientosNegociosSerializer(serializers.ModelSerializer):
    class Meta:
        model = DireccionesEstablecimientosNegocios
       	fields = '__all__'


# PERSONAL NEGOCIOS
class PersonalNegociosSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalNegocios
       	fields = '__all__'


    

    
from django.urls import path,include
from apps.MDM.mdm_negocios.views.negocio_views import(
	negocio_list, negocio_findOne, negocio_create,
	negocio_update, negocio_delete
)
from apps.MDM.mdm_negocios.views.direccion_establecimiento_views import(
	direccionesNegocio_list, direccionesNegocio_findOne, direccionesNegocio_create,
	direccionesNegocio_update, direccionesNegocio_delete
)
from apps.MDM.mdm_negocios.views.personal_views import(
	personalNegocios_list, personalNegocios_findOne, personalNegocios_create,
	personalNegocios_update, personalNegocios_delete
)

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'negocios'

urlpatterns = [
	# NEGOCIO
	path('list/', negocio_list, name="negocio_list"),
	path('create/', negocio_create, name="negocio_create"),
	path('listOne/<int:pk>', negocio_findOne, name="negocio_findOne"), 
	path('update/<int:pk>', negocio_update, name="negocio_update"), 
	path('delete/<int:pk>', negocio_delete, name="negocio_delete"),
    # DIREECIONES ESTABLECIMIENTOS
    path('list/address/', direccionesNegocio_list, name="direccionesNegocio_list"),
	path('create/address/', direccionesNegocio_create, name="direccionesNegocio_create"),
	path('listOne/address/<int:pk>', direccionesNegocio_findOne, name="direccionesNegocio_findOne"), 
	path('update/address/<int:pk>', direccionesNegocio_update, name="direccionesNegocio_update"), 
	path('delete/address/<int:pk>', direccionesNegocio_delete, name="direccionesNegocio_delete"),
    # PERSONAL
    path('list/personal/', personalNegocios_list, name="personalNegocios_list"),
	path('create/personal/', personalNegocios_create, name="personalNegocios_create"),
	path('listOne/personal/<int:pk>', personalNegocios_findOne, name="personalNegocios_findOne"), 
	path('update/personal/<int:pk>', personalNegocios_update, name="personalNegocios_update"), 
	path('delete/personal/<int:pk>', personalNegocios_delete, name="personalNegocios_delete"),
]

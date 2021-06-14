from django.urls import path,include
from apps.MDM.mdm_facturas.views import(
    factura_list, factura_create, factura_findOne, factura_update, factura_delete, factura_list_cliente, factura_list_negocio
)

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'facturas'

urlpatterns = [
	#facturas
	path('list/', factura_list, name="factura_list"),
	path('list/negocio/', factura_list_negocio, name="factura_list_negocio"),
	path('list/cliente/', factura_list_cliente, name="factura_list_cliente"),
	path('create/', factura_create, name="factura_create"),
	path('listOne/<int:pk>', factura_findOne, name="factura_findOne"), 
	# path('update/<int:pk>', factura_update, name="factura_update"), 
	# path('delete/<int:pk>', factura_delete, name="factura_delete"),
	# path('upload/csv/', uploadCSV_crearProspectosClientes, name="uploadCSV_crearProspectosClientes"),
	# path('upload/excel/', uploadEXCEL_crearProspectosClientes, name="uploadEXCEL_crearProspectosClientes"),		
	
]
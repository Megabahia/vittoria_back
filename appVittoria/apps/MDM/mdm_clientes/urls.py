from django.urls import path,include
from apps.MDM.mdm_clientes.views.cliente_views import(
	cliente_list, cliente_findOne, cliente_create,
	cliente_update, cliente_delete, clienteImagen_update
)

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'clientes'

urlpatterns = [
	#parametrizaciones
	# path('list/', cliente_list, name="cliente_list"),
	path('create/', cliente_create, name="cliente_create"),
	path('listOne/<int:pk>', cliente_findOne, name="cliente_findOne"), 
	path('update/<int:pk>', cliente_update, name="cliente_update"), 
	path('delete/<int:pk>', cliente_delete, name="cliente_delete"),	
	path('update/imagen/<int:pk>', clienteImagen_update, name="clienteImagen_update"),	
]

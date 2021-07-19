from django.urls import path,include

from apps.MDP.mdp_productos.views import (
	productos_list, productos_create, productos_findOne, productos_update, productos_delete,
	search_producto_list, rotacion_list, refil_list
)

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'productos'

urlpatterns = [
	#PRODUCTOS
	path('list/', productos_list, name="productos_list"),
	path('create/', productos_create, name="productos_create"),
	path('listOne/<int:pk>', productos_findOne, name="productos_findOne"), 
	path('update/<int:pk>', productos_update, name="productos_update"), 
	path('delete/<int:pk>', productos_delete, name="productos_delete"),
	path('search/producto/', search_producto_list, name="search_producto_list"),
	# REPORTE ROTACION
	path('rotacion/list/', rotacion_list, name="rotacion_list"),
	# REPORTE REFIL
	path('refil/list/', refil_list, name="refil_list"),
]

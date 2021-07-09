from django.urls import path,include

from apps.MDP.mdp_productos.views import(
	productos_list, productos_create, productos_findOne, productos_update, productos_delete
)

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'productos'

urlpatterns = [
	#SUBCATEGORIAS
	path('list/', productos_list, name="productos_list"),
	path('create/', productos_create, name="productos_create"),
	path('listOne/<int:pk>', productos_findOne, name="productos_findOne"), 
	path('update/<int:pk>', productos_update, name="productos_update"), 
	path('delete/<int:pk>', productos_delete, name="productos_delete"),
]

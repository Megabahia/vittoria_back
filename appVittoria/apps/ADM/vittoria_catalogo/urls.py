from django.urls import path,include
from apps.ADM.vittoria_catalogo.views import(
	catalogo_list,catalogo_create,catalogo_findOne,catalogo_update,catalogo_delete,
	estado_list, pais_list,

)

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'catalogo'

urlpatterns = [
	#catalogo
	path('list/', catalogo_list, name="catalogo_list"),
	path('create/', catalogo_create, name="catalogo_create"),
	path('listOne/<int:pk>', catalogo_findOne, name="catalogo_findOne"), 
	path('update/<int:pk>', catalogo_update, name="catalogo_update"), 
	path('delete/<int:pk>', catalogo_delete, name="catalogo_delete"), 
	#ESTADO
	path('listEstado/', estado_list, name="estado_list"), 
	#PAIS
	path('listPais/', pais_list, name="pais_list"), 
]

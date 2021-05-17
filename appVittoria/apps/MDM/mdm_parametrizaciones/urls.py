from django.urls import path,include
from apps.ADM.vittoria_parametrizaciones.views import(
	parametrizaciones_list,parametrizaciones_create,parametrizaciones_findOne,parametrizaciones_update,parametrizaciones_delete,
	estado_list, pais_list,tipo_list,parametrizaciones_list_hijo,parametrizaciones_list_hijoNombre,parametrizaciones_list_hijos

)

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'parametrizaciones'

urlpatterns = [
	#parametrizaciones
	path('list/', parametrizaciones_list, name="parametrizaciones_list"),
	path('create/', parametrizaciones_create, name="parametrizaciones_create"),
	path('listOne/<int:pk>', parametrizaciones_findOne, name="parametrizaciones_findOne"), 
	path('update/<int:pk>', parametrizaciones_update, name="parametrizaciones_update"), 
	path('delete/<int:pk>', parametrizaciones_delete, name="parametrizaciones_delete"), 
	#ESTADO
	path('list/estado/', estado_list, name="estado_list"), 
	#PAIS
	path('list/pais/', pais_list, name="pais_list"), 
	#TIPO PARAMETRIZACION/parametrizaciones
	path('list/tipo/', tipo_list, name="tipo_list"), 
	#INFORMACION DEL PADRE
	path('list/tipo/hijo/<int:pk>', parametrizaciones_list_hijo, name="tipohijo_list"), 
	#HIJOS DEL TIPO
	path('list/tipo/hijo/nombre/', parametrizaciones_list_hijoNombre, name="tijohijonombre_list"), 
	#buscar todos los nombres que pertenecen al tipo enviado
	path('list/tipo/hijo/', parametrizaciones_list_hijos, name="tipoPadre__list"), 
]

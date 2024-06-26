from django.urls import path,include
from .views import(
	parametrizaciones_list,parametrizaciones_create,parametrizaciones_findOne,parametrizaciones_update,parametrizaciones_delete,
	estado_list, pais_list,tipo_list,parametrizaciones_list_hijo,parametrizaciones_list_hijoNombre,parametrizaciones_list_hijos,
	canales_list, confirmacionProspecto_list, tipoCliente_list,parametrosTipo_list, nacionalidad_list, genero_list,
	nivelEstudios_list, profesion_list, tipoDireccion_list, tipoContacto_list, tipoPariente_list, estadoCivil_list,
	tipoNegocio_list, segmentoActividadEconomica_list, actividadEconomica_list, tipoContactoNegocio_list, llevarContabilidad_list,
	parametrizaciones_filter_name, parametrizaciones_filter_listOne_name_tipo
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
	# CANALES
	path('list/canales/', canales_list, name="canales_list"), 
	# CONFIRMACIONES PROSPECTOS
	path('list/confirmacionProspecto/', confirmacionProspecto_list, name="confirmacionProspecto_list"), 
	# TIPO CLIENTE
	path('list/tipoCliente/', tipoCliente_list, name="tipoCliente_list"), 
	#buscar todos LOS QUE TENGAN EL PARÁMETRO
	path('list/tipo/todos/', parametrosTipo_list, name="catalogo_list_parametrosTipo"), 
	# TIPO CLIENTE
	path('list/nacionalidad/', nacionalidad_list, name="nacionalidad_list"), 
	# TIPO GENERO
	path('list/genero/', genero_list, name="genero_list"),
	# TIPO NIVEL ESTUDIOS
	path('list/nivelEstudios/', nivelEstudios_list, name="nivelEstudios_list"),
	# TIPO PROFESION
	path('list/profesion/', profesion_list, name="profesion_list"),
	# TIPO DIRECCION
	path('list/tipoDireccion/', tipoDireccion_list, name="tipoDireccion_list"),
	# TIPO CONTACTO
	path('list/tipoContacto/', tipoContacto_list, name="tipoContacto_list"),
	# TIPO PARIENTE
	path('list/tipoPariente/', tipoPariente_list, name="tipoPariente_list"),
	# ESTADO CIVIL
	path('list/estadoCivil/', estadoCivil_list, name="estadoCivil_list"),
	# TIPO NEGOCIO
	path('list/tipoNegocio/', tipoNegocio_list, name="tipoNegocio_list"),
	# SEGMENTO ACTIVIDAD ECONOMICA
	path('list/segmentoActividadEconomica/', segmentoActividadEconomica_list, name="segmentoActividadEconomica_list"),
	# SEGMENTO ACTIVIDAD ECONOMICA
	path('list/actividadEconomica/', actividadEconomica_list, name="actividadEconomica_list"),
	# TIPO CONTACTO NEGOCIO
	path('list/tipoContactoNegocio/', tipoContactoNegocio_list, name="tipoContactoNegocio_list"),
	# LLEVAR CONTABILIDAD
	path('list/llevarContabilidad/', llevarContabilidad_list, name="llevarContabilidad_list"),
	# FILTRO Y NOMBRE
	path('list/filtro/nombre', parametrizaciones_filter_name, name="parametrizaciones_filter_name"),
	path('list/listOne', parametrizaciones_filter_listOne_name_tipo, name="parametrizaciones_filter_listOne_name_tipo"),
]

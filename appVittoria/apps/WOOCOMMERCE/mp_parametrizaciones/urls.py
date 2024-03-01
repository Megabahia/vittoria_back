from django.urls import path
from .views import (
    parametrizaciones_list, parametrizaciones_create, parametrizaciones_findOne, parametrizaciones_update,
    parametrizaciones_delete,
    estado_list, tipo_list, parametrizaciones_list_hijo, parametrizaciones_list_hijoNombre,
    parametrizaciones_list_hijos,
    parametrizaciones_filter_name, parametrizaciones_filter_listOne_name_tipo, parametrosTipo_list,
    parametrizaciones_exportar
)

app_name = 'parametrizaciones'

urlpatterns = [
    # parametrizaciones
    path('list/', parametrizaciones_list, name="parametrizaciones_list"),
    path('create/', parametrizaciones_create, name="parametrizaciones_create"),
    path('listOne/<int:pk>', parametrizaciones_findOne, name="parametrizaciones_findOne"),
    path('update/<int:pk>', parametrizaciones_update, name="parametrizaciones_update"),
    path('delete/<int:pk>', parametrizaciones_delete, name="parametrizaciones_delete"),
    # ESTADO
    path('list/estado/', estado_list, name="estado_list"),
    # TIPO PARAMETRIZACION/parametrizaciones
    path('list/tipo/', tipo_list, name="tipo_list"),
    # INFORMACION DEL PADRE
    path('list/tipo/hijo/<int:pk>', parametrizaciones_list_hijo, name="tipohijo_list"),
    # HIJOS DEL TIPO
    path('list/tipo/hijo/nombre/', parametrizaciones_list_hijoNombre, name="tijohijonombre_list"),
    # buscar todos los nombres que pertenecen al tipo enviado
    path('list/tipo/hijo/', parametrizaciones_list_hijos, name="tipoPadre__list"),
    # buscar todos LOS QUE TENGAN EL PARÁMETRO
    path('list/tipo/todos/', parametrosTipo_list, name="catalogo_list_parametrosTipo"),
    # FILTRO Y NOMBRE
    path('list/filtro/nombre', parametrizaciones_filter_name, name="parametrizaciones_filter_name"),
    path('list/listOne', parametrizaciones_filter_listOne_name_tipo, name="parametrizaciones_filter_listOne_name_tipo"),
    # Exportar
    path('exportar/', parametrizaciones_exportar, name="parametrizaciones_exportar"),
]

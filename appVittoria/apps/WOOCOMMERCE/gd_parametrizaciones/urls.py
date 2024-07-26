from django.urls import path
from .views import (
    gd_parametrizaciones_list, gd_parametrizaciones_create, gd_parametrizaciones_findOne, gd_parametrizaciones_update, gd_parametrizaciones_delete, gd_valor_list, gd_estado_list, gd_tipo_list, gd_parametrizaciones_list_hijos, gd_parametrosTipo_list, gd_parametrizaciones_filter_name, gd_parametrizaciones_filter_listOne_name_tipo, gd_parametrizaciones_exportar
)

app_name = 'gd_parametrizaciones'

urlpatterns = [
    # parametrizaciones
    path('list/', gd_parametrizaciones_list, name="gd_parametrizaciones_list"),
    path('create/', gd_parametrizaciones_create, name="gd_parametrizaciones_create"),
    path('listOne/<int:pk>', gd_parametrizaciones_findOne, name="gd_parametrizaciones_findOne"),
    path('update/<int:pk>', gd_parametrizaciones_update, name="gd_parametrizaciones_update"),
    path('delete/<int:pk>', gd_parametrizaciones_delete, name="gd_parametrizaciones_delete"),
    #VALOR
    path('list/valor/', gd_valor_list, name="gd_valor_list"),
    # ESTADO
    path('list/estado/', gd_estado_list, name="gd_estado_list"),
    # TIPO PARAMETRIZACION/parametrizaciones
    path('list/tipo/', gd_tipo_list, name="gd_tipo_list"),
    # buscar todos los nombres que pertenecen al tipo enviado
    path('list/tipo/hijo/', gd_parametrizaciones_list_hijos, name="gd_parametrizaciones_list_hijos"),
    # buscar todos LOS QUE TENGAN EL PARÁMETRO
    path('list/tipo/todos/', gd_parametrosTipo_list, name="gd_parametrosTipo_list"),
    # FILTRO Y NOMBRE
    path('list/filtro/nombre', gd_parametrizaciones_filter_name, name="gd_parametrizaciones_filter_name"),
    path('list/listOne', gd_parametrizaciones_filter_listOne_name_tipo, name="gd_parametrizaciones_filter_listOne_name_tipo"),
    # Exportar
    path('exportar/', gd_parametrizaciones_exportar, name="gd_parametrizaciones_exportar"),
]

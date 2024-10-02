from django.urls import path
from .views import (
    asesor_list,
    asesor_create,
    asesor_findOne,
    asesor_update_state,
    asesor_update,
    asesor_delete,
    activate_asesor,
    movimiento_create,
    movimiento_asesor_update,
    movimiento_asesor_list
)

app_name = 'asesores'

urlpatterns = [
    path('list/', asesor_list, name="asesor_list"),
    path('create/', asesor_create, name="asesor_create"),
    path('listOne/<int:pk>', asesor_findOne, name="asesor_findOne"),
    path('update/status/<int:pk>', asesor_update_state, name="asesor_update_state"),
    path('update/<int:pk>', asesor_update, name="asesor_update"),
    path('activate/<int:pk>', activate_asesor, name="activate_asesor"),
    path('delete/<int:pk>', asesor_delete, name="asesor_delete"),
    #MOVIMIENTOS
    path('create/movimiento/', movimiento_create, name="movimiento_create"),
    path('update/movimiento/<int:pk>', movimiento_asesor_update, name="movimiento_asesor_update"),
    path('list/movimientos', movimiento_asesor_list, name="movimiento_asesor_list"),
]

from django.urls import path
from .views import (
    asesor_list,
    asesor_create,
    asesor_findOne,
    asesor_update,
    asesor_delete,
)

app_name = 'asesores'

urlpatterns = [
    path('list/', asesor_list, name="asesor_list"),
    path('create/', asesor_create, name="asesor_create"),
    path('listOne/<int:pk>', asesor_findOne, name="asesor_findOne"),
    path('update/<int:pk>', asesor_update, name="asesor_update"),
    path('delete/<int:pk>', asesor_delete, name="asesor_delete"),
]

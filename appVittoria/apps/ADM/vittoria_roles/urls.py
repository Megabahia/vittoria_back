from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from apps.ADM.vittoria_roles.views import(
	rol_list,
    rol_listExport,
    rol_create,
    rol_findOne,
    rol_update,
    rol_delete,
    rol_listFiltro,
    rol_listAccionPadre
)

urlpatterns = [
    path('list/', rol_list, name="rol_list"),
    path('list/export/', rol_listExport, name="rol_listExport"),
    path('create/', rol_create, name="rol_create"),
    path('listOne/<int:pk>', rol_findOne, name="rol_findOne"),
    path('update/', rol_update, name="rol_update"),
    path('delete/<int:pk>', rol_delete, name="rol_delete"),
    path('list/filtro/', rol_listFiltro, name="listFiltro"),
    path('list/padres/', rol_listAccionPadre, name="listFiltro"),
]


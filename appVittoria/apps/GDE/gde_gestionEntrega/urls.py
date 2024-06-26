from django.urls import path, include
from .views import (
    generarOferta_list, generarOferta_create, generarOferta_findOne, generarOferta_update, generarOferta_delete,
    detalles_list
)

app_name = 'gestionOferta'

urlpatterns = [
    # generarOfertas
    path('list/', generarOferta_list, name="generarOferta_list"),
    path('create/', generarOferta_create, name="generarOferta_create"),
    path('listOne/<int:pk>', generarOferta_findOne, name="generarOferta_findOne"),
    path('update/<int:pk>', generarOferta_update, name="generarOferta_update"),
    path('delete/<int:pk>', generarOferta_delete, name="generarOferta_delete"),
    path('productosImagenes/<int:pk>', detalles_list, name="detalles_list"),
]

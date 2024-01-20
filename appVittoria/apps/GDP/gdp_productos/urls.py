from django.urls import path

from .views import (
    productos_list, productos_create, productos_findOne, productos_update, productos_delete,
    producto_images_delete, productos_findOne_free, productos_findOne_codigoProducto
)

app_name = 'productos'

urlpatterns = [
    # PRODUCTOS
    path('list/', productos_list, name="productos_list"),
    path('create/', productos_create, name="productos_create"),
    path('listOne/<int:pk>', productos_findOne, name="productos_findOne"),
    path('listOne/free/<int:pk>', productos_findOne_free, name="productos_findOne"),
    path('listOne/codigoProducto/<str:pk>', productos_findOne_codigoProducto, name="productos_findOne_codigoProducto"),
    path('update/<int:pk>', productos_update, name="productos_update"),
    path('delete/<int:pk>', productos_delete, name="productos_delete"),
    # ARCHIVOS
    path('imagen/delete/<int:pk>', producto_images_delete, name="producto_images_delete"),
]

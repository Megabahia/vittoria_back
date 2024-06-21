from django.urls import path

from .views import (
    productos_list, productos_create, productos_findOne, productos_update, productos_delete,
    producto_images_findOne,productos_create_woocommerce,productos_update_woocommerce,
    productos_delete_woocommerce,productos_restore_woocommerce,
    search_producto_list, abastecimiento_list, stock_list, caducidad_list, rotacion_list, refil_list,
    abastecimiento_create,
    uploadEXCEL_crearProductos, productoImagen_list, prediccion_crosseling_list,
    producto_refil_list, prediccion_refil_list, prediccion_productosNuevos_list,
    search_producto_codigo_list, producto_images_delete, productos_findOne_free,
    productos_findOne_codigo_producto, productos_exportar,
)

app_name = 'productos'

urlpatterns = [
    # PRODUCTOS
    path('list/', productos_list, name="productos_list"),
    path('create/', productos_create, name="productos_create"),
    path('create/woocommerce', productos_create_woocommerce, name="productos_create_woocommerce"),
    path('update/woocommerce', productos_update_woocommerce, name="productos_update_woocommerce"),
    path('delete/woocommerce', productos_delete_woocommerce, name="productos_delete_woocommerce"),
    path('restore/woocommerce', productos_restore_woocommerce, name="productos_restore_woocommerce"),
    path('listOne/<int:pk>', productos_findOne, name="productos_findOne"),
    path('listOne/free/<int:pk>', productos_findOne_free, name="productos_findOne_free"),
    path('listOne/codigoProducto/<str:pk>', productos_findOne_codigo_producto, name="productos_findOne_codigo_producto"),
    path('update/<int:pk>', productos_update, name="productos_update"),
    path('delete/<int:pk>', productos_delete, name="productos_delete"),
    path('search/producto/', search_producto_list, name="search_producto_list"),
    path('search/producto/codigo/', search_producto_codigo_list, name="search_producto_codigo_list"),
    path('upload/excel/', uploadEXCEL_crearProductos, name="uploadEXCEL_crearProductos"),
    # IMAGENES PRODUCTOS
    path('imagen/<int:pk>', producto_images_findOne, name="producto_images_findOne"),
    path('imagen/delete/<int:pk>', producto_images_delete, name="producto_images_delete"),
    # REPORTE ABASTECIMIENTO
    path('abastecimiento/create/', abastecimiento_create, name="abastecimiento_create"),
    path('abastecimiento/list/', abastecimiento_list, name="abastecimiento_list"),
    # REPORTE STOCK
    path('stock/list/', stock_list, name="stock_list"),
    # REPORTE CADUCIDAD
    path('caducidad/list/', caducidad_list, name="caducidad_list"),
    # REPORTE ROTACION
    path('rotacion/list/', rotacion_list, name="rotacion_list"),
    # REPORTE REFIL
    path('refil/list/', refil_list, name="refil_list"),
    # OBTENER URL IMAGEN
    path('producto/image/', productoImagen_list, name="productoImagen_list"),
    # OBTENER PREDICCION CROSSELING
    path('prediccionCrosseling/', prediccion_crosseling_list, name="prediccion_crosseling_list"),
    # OBTENER REFIL PRODUCTO
    path('producto/refil/', producto_refil_list, name="producto_refil_list"),
    # OBTENER PREDICCION REFIL
    path('prediccionRefil/', prediccion_refil_list, name="prediccion_refil_list"),
    # OBTENER PREDICCION PRODUCTOS NUEVOS
    path('prediccionProductosNuevos/', prediccion_productosNuevos_list, name="prediccion_productosNuevos_list"),
    # EXPORTAR PRODCUTOS
    path('exportar', productos_exportar, name="productos_exportar"),
]

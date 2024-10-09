from django.urls import path

from .views import (
    uploadEXCEL_subirProductosProveedores, proveedores_list, proveedores_list_distinct, productos_exportar,
    productos_cargar_stock, sincronizar_fotos_productos, generar_productos_stock_exportar,productos_cargar_stock_megabahia, productos_cargar_stock_canales
)

app_name = 'facturacion'

urlpatterns = [
    # PRODUCTOS
    path('cargar-productos-proveedores/', uploadEXCEL_subirProductosProveedores, name="uploadEXCEL_subirProductosProveedores"),
    path('proveedores/list/', proveedores_list, name="proveedores_list"),
    path('proveedores/', proveedores_list_distinct, name="proveedores_list_distinct"),
    path('cargar/stock/', productos_cargar_stock, name="productos_cargar_stock"),
    path('cargar/stock/megabahia', productos_cargar_stock_megabahia, name="productos_cargar_stock_megabahia"),
    path('cargar/stock/canales', productos_cargar_stock_canales, name="productos_cargar_stock_canales"),
    path('sincronizar/fotos/productos/', sincronizar_fotos_productos, name="sincronizar_fotos_productos"),
    # Exportar
    path('exportar/', productos_exportar, name="productos_exportar"),
    path('exportar/productos/stock/', generar_productos_stock_exportar, name="generar_productos_stock_exportar"),
]

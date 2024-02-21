from django.urls import path

from .views import (
    uploadEXCEL_subirProductosProveedores, proveedores_list, proveedores_list_distinct, productos_exportar,
    productos_cargar_stock
)

app_name = 'facturacion'

urlpatterns = [
    # PRODUCTOS
    path('cargar-productos-proveedores/', uploadEXCEL_subirProductosProveedores, name="uploadEXCEL_subirProductosProveedores"),
    path('proveedores/list/', proveedores_list, name="proveedores_list"),
    path('proveedores/', proveedores_list_distinct, name="proveedores_list_distinct"),
    path('cargar/stock/', productos_cargar_stock, name="productos_cargar_stock"),
    # Exportar
    path('exportar/', productos_exportar, name="productos_exportar"),
]

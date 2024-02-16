from django.urls import path

from .views import (
    uploadEXCEL_subirFacturas, facturas_list, factura_findOne, factura_facturar, factura_facturar_locales
)

app_name = 'facturacion'

urlpatterns = [
    # PRODUCTOS
    path('upload/facturas/', uploadEXCEL_subirFacturas, name="uploadEXCEL_subirFacturas"),
    path('facturas/list/', facturas_list, name="facturas_list"),
    path('facturas/listOne/<int:pk>', factura_findOne, name="factura_findOne"),
    path('facturas/facturar/', factura_facturar, name="factura_facturar"),
    path('facturas/locales/facturar/', factura_facturar_locales, name="factura_facturar_locales"),
]

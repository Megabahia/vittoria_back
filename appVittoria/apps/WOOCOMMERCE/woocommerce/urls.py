from django.urls import path

from .views import (
    orders_create, orders_list, orders_listOne, orders_update,
    orders_devolucion, orders_notificacion, orders_list_bodega,
    orders_listOne_bodega, orders_update_bodega, pedidos_exportar, orders_send_code, orders_verify_code,
    orders_create_super_barato
)

app_name = 'woocommerce'

urlpatterns = [
    # PRODUCTOS
    path('orders', orders_create, name="orders_create"),
    path('orders/super/barato', orders_create_super_barato, name="orders_create_super_barato"),
    path('orders/list', orders_list, name="orders_list"),
    path('orders/list/bodega', orders_list_bodega, name="orders_list_bodega"),
    path('orders/update/bodega/<str:pk>', orders_update_bodega, name="orders_update_bodega"),
    path('orders/update/<str:pk>', orders_update, name="orders_update"),
    path('orders/devolucion/<str:pk>', orders_devolucion, name="orders_devolucion"),
    path('orders/listOne/<str:pk>', orders_listOne, name="orders_listOne"),
    path('orders/listOne/bodega/<str:pk>', orders_listOne_bodega, name="orders_listOne_bodega"),
    path('orders/notificacion/<str:pk>', orders_notificacion, name="orders_notificacion"),
    # EXPORTAR PRODCUTOS
    path('orders/exportar', pedidos_exportar, name="pedidos_exportar"),
    #CODIGO DE VERIFICACION POR GMAIL
    path('orders/codigo/email', orders_send_code, name="orders_send_code"),
    path('orders/codigo/email/verify', orders_verify_code, name="orders_verify_code"),

]

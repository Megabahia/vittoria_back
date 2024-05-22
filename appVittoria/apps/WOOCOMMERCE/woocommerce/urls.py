from django.urls import path

from .views import (
    orders_create, orders_list, orders_listOne, orders_update,
    orders_devolucion, orders_notificacion, orders_list_bodega,
    orders_listOne_bodega
)

app_name = 'woocommerce'

urlpatterns = [
    # PRODUCTOS
    path('orders', orders_create, name="orders_create"),
    path('orders/list', orders_list, name="orders_list"),
    path('orders/list/bodega', orders_list_bodega, name="orders_list_bodega"),
    path('orders/update/<str:pk>', orders_update, name="orders_update"),
    path('orders/devolucion/<str:pk>', orders_devolucion, name="orders_devolucion"),
    path('orders/listOne/<str:pk>', orders_listOne, name="orders_listOne"),
    path('orders/listOne/bodega/<str:pk>', orders_listOne_bodega, name="orders_listOne_bodega"),
    path('orders/notificacion/<str:pk>', orders_notificacion, name="orders_notificacion"),
]

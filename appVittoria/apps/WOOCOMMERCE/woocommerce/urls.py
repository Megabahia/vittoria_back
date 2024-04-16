from django.urls import path

from .views import (
    orders_create, orders_list, orders_listOne, orders_update,
    orders_devolucion, orders_notificacion,orders_create_contact
)

app_name = 'woocommerce'

urlpatterns = [
    # PRODUCTOS
    path('orders', orders_create, name="orders_create"),
    path('orders/contact', orders_create_contact, name="orders_create_contact"),
    path('orders/list', orders_list, name="orders_list"),
    path('orders/update/<str:pk>', orders_update, name="orders_update"),
    path('orders/devolucion/<str:pk>', orders_devolucion, name="orders_devolucion"),
    path('orders/listOne/<str:pk>', orders_listOne, name="orders_listOne"),
    path('orders/notificacion/<str:pk>', orders_notificacion, name="orders_notificacion"),
]

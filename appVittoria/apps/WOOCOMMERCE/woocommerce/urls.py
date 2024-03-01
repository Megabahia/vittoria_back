from django.urls import path

from .views import (
    orders_create, orders_list, orders_listOne, orders_update
)

app_name = 'woocommerce'

urlpatterns = [
    # PRODUCTOS
    path('orders', orders_create, name="orders_create"),
    path('orders/list', orders_list, name="orders_list"),
    path('orders/update/<str:pk>', orders_update, name="orders_update"),
    path('orders/listOne/<str:pk>', orders_listOne, name="orders_listOne"),
]

from django.urls import path

from .views import gsb_create_order, gsb_orders_list, gsb_orders_listOne, gsb_validate_order, gsb_update_order

app_name = 'gsb_super_barato'

urlpatterns = [
    # SUPER BARATO
    path('list', gsb_orders_list, name="gsb_orders_list"),
    path('listOne/<str:pk>', gsb_orders_listOne, name="gsb_orders_listOne"),
    path('create', gsb_create_order, name="gsb_create_order"),
    path('update/<str:pk>', gsb_update_order, name="gsb_update_order"),
    path('validate/contact', gsb_validate_order, name="gsb_validate_order"),

]

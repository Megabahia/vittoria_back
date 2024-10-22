from django.urls import path
from .views import mdrp_productos_list, mdrp_productos_create, mdrp_productos_update, mdrp_producto_listOne
app_name = 'mdrp_productos'

urlpatterns = [
    # PRODUCTOS
    path('list/', mdrp_productos_list, name="mdrp_productos_list"),
    path('create/', mdrp_productos_create, name="mdrp_productos_create"),
    path('update/<int:pk>', mdrp_productos_update, name="mdrp_productos_update"),
    path('listOne/<int:pk>', mdrp_producto_listOne, name="mdrp_producto_listOne"),

]

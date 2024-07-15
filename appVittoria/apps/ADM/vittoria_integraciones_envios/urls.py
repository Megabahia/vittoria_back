from django.urls import path, include
from .views import (integraciones_envios_list, integraciones_envios_create, integraciones_envios_findOne, integraciones_envios_update, integraciones_envios_delete)

app_name = 'integraciones_envios_envios'

urlpatterns = [
    # integraciones_envios
    path('list/', integraciones_envios_list, name="integraciones_envios_list"),
    path('create/', integraciones_envios_create, name="integraciones_envios_create"),
    path('listOne/<int:pk>', integraciones_envios_findOne, name="integraciones_envios_findOne"),
    path('update/<int:pk>', integraciones_envios_update, name="integraciones_envios_update"),
    path('delete/<int:pk>', integraciones_envios_delete, name="integraciones_envios_delete"),
]
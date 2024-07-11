from django.urls import path, include
from .views import (integraciones_list, integraciones_create, integraciones_findOne, integraciones_update, integraciones_delete)

app_name = 'integraciones'

urlpatterns = [
    # integraciones
    path('list/', integraciones_list, name="integraciones_list"),
    path('create/', integraciones_create, name="integraciones_create"),
    path('listOne/<int:pk>', integraciones_findOne, name="integraciones_findOne"),
    path('update/<int:pk>', integraciones_update, name="integraciones_update"),
    path('delete/<int:pk>', integraciones_delete, name="integraciones_delete"),
]

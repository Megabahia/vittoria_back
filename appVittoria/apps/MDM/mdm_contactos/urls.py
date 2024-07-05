from django.urls import path
from .views import (
    contacto_list, contacto_findOne, contacto_create,
    contacto_update, contacto_delete, contacto_search,
    contacto_exportar,
)

app_name = 'mdm_contactos'

urlpatterns = [
    # parametrizaciones
    path('list/', contacto_list, name="contacto_list"),
    path('search/', contacto_search, name="contacto_search"),
    path('create/', contacto_create, name="contacto_create"),
    path('listOne/<int:pk>', contacto_findOne, name="contacto_findOne"),
    path('update/<int:pk>', contacto_update, name="contacto_update"),
    path('delete/<int:pk>', contacto_delete, name="contacto_delete"),
    path('exportar/', contacto_exportar, name="contacto_exportar"),
]

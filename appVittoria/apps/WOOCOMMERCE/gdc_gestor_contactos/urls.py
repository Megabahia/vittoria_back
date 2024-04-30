from django.urls import path

from .views import (gdc_create_contact,contacts_list,contact_listOne,gdc_validate_contact,contacts_update)

app_name = 'gdc_gestor_contactos'

urlpatterns = [
    # CONTACTOS
    path('list', contacts_list, name="contacts_list"),
    path('listOne/<str:pk>', contact_listOne, name="contact_listOne"),
    path('create', gdc_create_contact, name="gdc_create_contact"),
    path('update/<str:pk>', contacts_update, name="contacts_update"),
    path('validate/contact', gdc_validate_contact, name="gdc_validate_contact"),

]

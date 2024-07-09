from django.urls import path
from .views import megabahia_list, megabahia_listOne, gmb_create_megabahia, megabahia_update, gmb_validate_megabahia

app_name = 'gmb_despachos'

urlpatterns = [
    # MEGABAHIA
    path('list', megabahia_list, name="megabahia_list"),
    path('listOne/<str:pk>', megabahia_listOne, name="megabahia_listOne"),
    path('create', gmb_create_megabahia, name="gmb_create_megabahia"),
    path('update/<str:pk>', megabahia_update, name="megabahia_update"),
    path('validate/contact', gmb_validate_megabahia, name="gmb_validate_megabahia"),

]

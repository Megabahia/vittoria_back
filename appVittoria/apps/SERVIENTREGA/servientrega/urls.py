from django.urls import path

from .views import (
    productos_list_ciudades, productos_list_guiawebs, productos_list_GuiaRetornoNacional, productos_list_GuiaRecaudo,
    productos_list_GuiasWeb, productos_list_GuiaDigital, productos_list_ImprimeSticker,
    productos_list_Manifiestos, productos_list_ImprimeRotulos,
)

app_name = 'servientrega'

urlpatterns = [
    # PRODUCTOS
    path('api/ciudades/', productos_list_ciudades, name="productos_list_ciudades"),
    path('api/guiawebs/', productos_list_guiawebs, name="productos_list_guiawebs"),
    path('api/GuiaRetornoNacional/', productos_list_GuiaRetornoNacional, name="productos_list_GuiaRetornoNacional"),
    path('api/GuiaRecaudo', productos_list_GuiaRecaudo, name="productos_list_GuiaRecaudo"),
    path('api/GuiasWeb/<str:pk>', productos_list_GuiasWeb, name="productos_list_GuiasWeb"),
    path('api/GuiaDigital/<str:pk>', productos_list_GuiaDigital, name="productos_list_GuiaDigital"),
    path('api/ImprimeSticker/<str:pk>', productos_list_ImprimeSticker, name="productos_list_ImprimeSticker"),
    path('api/Manifiestos/<str:date>', productos_list_Manifiestos, name="productos_list_Manifiestos"),
    path('api/ImprimeRotulos/<str:pk>', productos_list_ImprimeRotulos, name="productos_list_ImprimeRotulos"),
]

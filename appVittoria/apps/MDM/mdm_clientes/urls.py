from django.urls import path,include
from apps.MDM.mdm_clientes.views import(
	clientes_list,
	clientesImagen_update
)

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'clientes'

urlpatterns = [
	#parametrizaciones
	# path('list/', clientes_list, name="clientes_list"),
	# path('update/imagen/<int:pk>', clientesImagen_update, name="clientesImagen_update"),
]

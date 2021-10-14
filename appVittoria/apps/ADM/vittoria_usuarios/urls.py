from django.urls import path,include
from apps.ADM.vittoria_usuarios.views import(
	usuario_list,
	usuario_listExport,
	usuario_create,
	usuario_findOne,
	usuario_update,
	usuario_delete,
	usuarioImagen_update,
	vendedor_list,
	usuarios_list_rol,
	usuario_findOne_image
)
app_name = 'usuarios'

urlpatterns = [
	path('list/', usuario_list, name="usuario_list"),
	path('list/export/', usuario_listExport, name="usuario_export"),
	path('create/', usuario_create, name="usuario_create"),
	path('listOne/<int:pk>', usuario_findOne, name="usuario_findOne"),
	path('listOne/image/<int:pk>', usuario_findOne_image, name="usuario_findOne_image"),
	path('update/<int:pk>', usuario_update, name="usuario_update"),
	path('delete/<int:pk>', usuario_delete, name="usuario_delete"),
	path('update/imagen/<int:pk>', usuarioImagen_update, name="usuarioImagen_update"),
	path('list/vendedor/', vendedor_list, name="vendedor_list"),
	path('list/rol/', usuarios_list_rol, name="usuarios_list_rol"),
]


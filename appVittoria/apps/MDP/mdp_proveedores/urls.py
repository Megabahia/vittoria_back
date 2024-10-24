from django.urls import path
from .views import mdp_proveedores_list, mdp_proveedores_create, mdp_proveedores_update, mdp_proveedores_listOne, mdp_proveedores_delete
app_name = 'mdp_proveedores'

urlpatterns = [
    # PRODUCTOS
    path('list/', mdp_proveedores_list, name="mdp_proveedores_list"),
    path('create/', mdp_proveedores_create, name="mdp_proveedores_create"),
    path('update/<int:pk>', mdp_proveedores_update, name="mdp_proveedores_update"),
    path('listOne/<int:pk>', mdp_proveedores_listOne, name="mdp_proveedoreslistOne"),
    path('delete/<int:pk>', mdp_proveedores_delete, name="mdp_proveedores_delete"),

]

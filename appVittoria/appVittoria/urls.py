"""appVittoria URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    #MODULO ADM
    path('adm/roles/', include(('apps.ADM.vittoria_roles.urls', 'roles'), namespace='roles')),
    path('adm/usuarios/', include(('apps.ADM.vittoria_usuarios.urls', 'usuarios'), namespace='usuarios')),
    path('adm/auth/', include(('apps.ADM.vittoria_autenticacion.urls', 'autenticacion'), namespace='autenticacion')),
    path('adm/acciones/', include(('apps.ADM.vittoria_acciones.urls', 'acciones'), namespace='acciones')),
    path('adm/param/', include(('apps.ADM.vittoria_catalogo.urls', 'catalogo'), namespace='catalogo')),
    url(r'^adm/auth/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    #Modulo MDM
    path('mdm/param/', include(('apps.MDM.mdm_parametrizaciones.urls', 'parametrizaciones'), namespace='parametrizaciones')),
    path('mdm/prospectosClientes/', include(('apps.MDM.mdm_prospectosClientes.urls', 'prospectos_clientes'), namespace='prospectos_clientes')),
    path('mdm/clientes/', include(('apps.MDM.mdm_clientes.urls', 'clientes'), namespace='clientes')),
    path('mdm/negocios/', include(('apps.MDM.mdm_negocios.urls', 'negocios'), namespace='negocios')),
    path('mdm/facturas/', include(('apps.MDM.mdm_facturas.urls', 'facturas'), namespace='facturas')),
    #Modulo MDP
    path('mdp/param/', include(('apps.MDP.mdp_parametrizaciones.urls', 'parametrizaciones'), namespace='parametrizaciones')),
    path('mdp/categorias/', include(('apps.MDP.mdp_categorias.urls', 'categorias'), namespace='categorias')),
    path('mdp/subCategorias/', include(('apps.MDP.mdp_subCategorias.urls', 'subCategorias'), namespace='subCategorias')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

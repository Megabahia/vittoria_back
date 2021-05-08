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

urlpatterns = [
    #MODULO ADM
    path('adm/roles/', include(('apps.ADM.vittoria_roles.urls', 'roles'), namespace='roles')),
    path('adm/usuarios/', include(('apps.ADM.vittoria_usuarios.urls', 'usuarios'), namespace='usuarios')),
    path('adm/auth/', include(('apps.ADM.vittoria_autenticacion.urls', 'autenticacion'), namespace='autenticacion')),
    path('adm/acciones/', include(('apps.ADM.vittoria_acciones.urls', 'acciones'), namespace='acciones')),
    path('adm/param/', include(('apps.ADM.vittoria_catalogo.urls', 'catalogo'), namespace='catalogo')),
    url(r'^adm/auth/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    # path('auth/password_reset/', include(('django_rest_passwordreset.urls', 'password_reset'), namespace='password_reset')),
]

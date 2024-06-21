"""
Django settings for appVittoria project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import environ
from pathlib import Path
import pymysql
import os
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from apps.config import config
pymysql.install_as_MySQLdb()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# environ init
env = environ.Env()
environ.Env.read_env() # LEE ARCHIVO .ENV


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/
# AUTOR:papagyo
# SECURITY WARNING: keep the secret key used in production secret!!
SECRET_KEY = ')+^!3q$nko9e_n0(x!qo24xbh8m%k#0&&r6^%4!4_bp+m%=9!v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    #apps vittoria ADM
    'apps.ADM.vittoria_logs',
    'apps.ADM.vittoria_roles',
    'apps.ADM.vittoria_usuarios',
    'apps.ADM.vittoria_autenticacion',
    'apps.ADM.vittoria_acciones',
    'apps.ADM.vittoria_catalogo',
    #apps vittoria MDM+
    'apps.MDM.mdm_clientes',
    'apps.MDM.mdm_facturas',
    'apps.MDM.mdm_negocios',
    'apps.MDM.mdm_parametrizaciones',
    'apps.MDM.mdm_prospectosClientes',
    #apps Vittoria MDP
    'apps.MDP.mdp_parametrizaciones',
    'apps.MDP.mdp_categorias',
    'apps.MDP.mdp_subCategorias',
    'apps.MDP.mdp_productos',
    'apps.MDP.mdp_fichaTecnicaProductos',
    'apps.MDP.mdp_gestionInventario',
    # apps Vittoria MDO
    'apps.MDO.mdo_parametrizaciones',
    'apps.MDO.mdo_prediccionCrosseling',
    'apps.MDO.mdo_prediccionRefil',
    'apps.MDO.mdo_prediccionProductosNuevos',
    'apps.MDO.mdo_generarOferta',
    # apss Vittoria GDO
    'apps.GDO.gdo_parametrizaciones',
    'apps.GDO.gdo_gestionOferta',
    # apps vittoria GDE
    'apps.GDE.gde_parametrizaciones',
    'apps.GDE.gde_gestionEntrega',
    # apps vittoria GDP
    'apps.GDP.gdp_productos',
    # apps vittoria SERVIENTREGA
    'apps.SERVIENTREGA.servientrega',
    # apps vittoria FACTURACION
    'apps.FACTURACION.facturacion',
    # apps vittoria FACTURACION
    'apps.WOOCOMMERCE.mp_parametrizaciones',
    'apps.WOOCOMMERCE.woocommerce',
    'apps.WOOCOMMERCE.gdc_gestor_contactos',
    #CONFIG
    'apps.config',
    #Django external apps
    'corsheaders',
    'rest_framework',
    # 'rest_framework.authtoken',
    'django_rest_passwordreset',
    'django_filters',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'import_export',
    'django_crontab',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apps.ADM.vittoria_autenticacion.auth.ExpiringTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #CORS
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'appVittoria.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'appVittoria.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES =config.DATABASES

#AGREGO LAS RUTAS DE LAS DIFERENTES BASES DE DATOS
DATABASE_ROUTERS = [
    'apps.config.routersDB.MDMRouter',
    'apps.config.routersDB.MDPRouter',
    'apps.config.routersDB.MDORouter',
    'apps.config.routersDB.MPRouter',
    'apps.config.routersDB.GDORouter',
    'apps.config.routersDB.GDERouter',
    'apps.config.routersDB.USERRouter',
    'apps.config.routersDB.FACTURACIONRouter'
]

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = '/static/'
AUTH_USER_MODEL = "vittoria_usuarios.Usuarios" 
#TIEMPO DE EXPIRACION DE TOKEN (EN SEGUNDOS)
TOKEN_EXPIRED_AFTER_SECONDS = config.TOKEN_EXPIRED_AFTER_SECONDS
#NOMBRE KEYWORK TOKEN
TOKEN_KEYWORD= config.TOKEN_KEYWORD
# Config Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = ''
#CORS
CORS_ALLOWED_ORIGINS = config.CORS_ALLOWED_ORIGINS

# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_URL = '/media/'
SILENCED_SYSTEM_CHECKS = ['auth.E003', 'auth.W004']

# CONFIGURACION DE AMAZON S3
DEFAULT_FILE_STORAGE = env.str('DEFAULT_FILE_STORAGE')
AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env.str('AWS_STORAGE_BUCKET_NAME')
AWS_QUERYSTRING_AUTH = False


CRONJOBS = [
    # La función temporizada se ejecuta cada minuto
    ('*/1 * * * *', "apps.FACTURACION.facturacion.cron_facturasExternas.verificarEstadoFactura"),
    ('*/1 * * * *', "apps.FACTURACION.facturacion.cron_facturasLocales.verificarEstadoFacturaLocal"),
]
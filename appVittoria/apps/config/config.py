# ESte archivo sirve para colocar las variables del entorno
# environ init
import os
import environ

from ..utils.AwsS3 import AwsS3

env = environ.Env()

# Establecer el directorio base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Tomar variables de entorno del archivo .env
environ.Env.read_env(os.path.join(BASE_DIR, '../appVittoria/.env.test'))
#environ.Env.read_env(os.path.join(BASE_DIR, '../appVittoria/.env'))
# VARIABLES GLOBALES
endpointEmailAsignacionPassword = "/auth/usuario/asignacionPassword/"
endpointEmailReseteoPassword = "/auth/usuario/reseteoPassword/"

# VARIABLES VARIAN DE ACUERDO A PRODUCCION O DESARROLLO
# URL BACK END
API_BACK_END = env.str('API_BACK_END')
# URL FRONT END
API_FRONT_END = env.str('API_FRONT_END')
# TIEMPO DE EXPIRACION DE TOKEN (EN SEGUNDOS)
TOKEN_EXPIRED_AFTER_SECONDS = 86400
# NOMBRE KEYWORK TOKEN
TOKEN_KEYWORD = 'Bearer'
# This will display email in Console.
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = ''
# CORS
CORS_ALLOWED_ORIGINS = [
    "http://209.145.61.41:4200",
    "http://127.0.0.1:4200",
    "http://localhost:4200",
    "https://ventas-vittoria.crediventa.com",
    "https://vittoria-test.netlify.app"
]
# databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vittoria_adm' + env.str('MYSQL_BUILD'),
        'USER': env.str('MYSQL_USER'),
        'PASSWORD': env.str('MYSQL_PASSWORD'),
        'HOST': env.str('MYSQL_HOST'),
        'PORT': 3306
    },
    'vittoria_mdm_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vittoria_mdm' + env.str('MYSQL_BUILD'),
        'USER': env.str('MYSQL_USER'),
        'PASSWORD': env.str('MYSQL_PASSWORD'),
        'HOST': env.str('MYSQL_HOST'),
        'PORT': 3306
    },
    'vittoria_mdp_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vittoria_mdp' + env.str('MYSQL_BUILD'),
        'USER': env.str('MYSQL_USER'),
        'PASSWORD': env.str('MYSQL_PASSWORD'),
        'HOST': env.str('MYSQL_HOST'),
        'PORT': 3306
    },
    'vittoria_mdo_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vittoria_mdo' + env.str('MYSQL_BUILD'),
        'USER': env.str('MYSQL_USER'),
        'PASSWORD': env.str('MYSQL_PASSWORD'),
        'HOST': env.str('MYSQL_HOST'),
        'PORT': 3306
    },
    'vittoria_mp_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vittoria_mp' + env.str('MYSQL_BUILD'),
        'USER': env.str('MYSQL_USER'),
        'PASSWORD': env.str('MYSQL_PASSWORD'),
        'HOST': env.str('MYSQL_HOST'),
        'PORT': 3306
    },
    'vittoria_gdo_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vittoria_gdo' + env.str('MYSQL_BUILD'),
        'USER': env.str('MYSQL_USER'),
        'PASSWORD': env.str('MYSQL_PASSWORD'),
        'HOST': env.str('MYSQL_HOST'),
        'PORT': 3306
    },
    'vittoria_gde_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vittoria_gde' + env.str('MYSQL_BUILD'),
        'USER': env.str('MYSQL_USER'),
        'PASSWORD': env.str('MYSQL_PASSWORD'),
        'HOST': env.str('MYSQL_HOST'),
        'PORT': 3306
    },
    'vittoria_facturacion_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vittoria_facturacion' + env.str('MYSQL_BUILD'),
        'USER': env.str('MYSQL_USER'),
        'PASSWORD': env.str('MYSQL_PASSWORD'),
        'HOST': env.str('MYSQL_HOST'),
        'PORT': 3306
    },
    'vittoria_users_db': {
        'ENGINE': 'djongo',
        'NAME': 'vittoria_users',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': env.str('MONGODB_ATLAS'),
        },
        'LOGGING': {
            'version': 1,
            'loggers': {
                'djongo': {
                    'level': 'DEBUG',
                    'propagate': False,
                }
            },
        },
    },
}
TWILIO_ACCOUNT_SID = env.str('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = env.str('TWILIO_AUTH_TOKEN')
SERVIENTREGA_USER = env.str('SERVIENTREGA_USER')
SERVIENTREGA_PASSWORD = env.str('SERVIENTREGA_PASSWORD')
SERVIENTREGA_URL = env.str('SERVIENTREGA_URL')
SERVIENTREGA_URL_GENERACION = env.str('SERVIENTREGA_URL_GENERACION')

FAC_URL = env.str('FAC_URL')
FAC_USER = env.str('FAC_USER')
FAC_PASS = env.str('FAC_PASS')
FAC_AMBIENTE = env.str('FAC_AMBIENTE')

aws_s3_instancia = AwsS3()

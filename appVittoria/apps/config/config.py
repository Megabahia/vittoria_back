PRODUCTION=False

#VARIABLES GLOBALES
endpointEmailAsignacionPassword="/usuario/asignacionPassword/"
endpointEmailReseteoPassword="/usuario/reseteoPassword/"

#VARIABLES VARIAN DE ACUERDO A PRODUCCION O DESARROLLO
if PRODUCTION:
    #URL FRONT END
    API_FRONT_END="209.145.61.41:4200"
    #TIEMPO DE EXPIRACION DE TOKEN (EN SEGUNDOS)
    TOKEN_EXPIRED_AFTER_SECONDS = 86400
    #NOMBRE KEYWORK TOKEN
    TOKEN_KEYWORD= 'Bearer'
    # This will display email in Console.
    EMAIL_HOST = ''
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_PORT = ''
    #CORS
    CORS_ALLOWED_ORIGINS = [
        "http://209.145.61.41:4200",
        "http://127.0.0.1:4200"
    ]
    #databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'vittoria_adm',
            'USER': 'usr_maintainer',
            'PASSWORD': 'Tc2;1EE{DBE^oN',
            'HOST': '209.145.61.41',
            'PORT': 3306
        },
        'vittoria_mdm_db': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'vittoria_mdm',
            'USER': 'usr_maintainer',
            'PASSWORD': 'Tc2;1EE{DBE^oN',
            'HOST': '209.145.61.41',
            'PORT': 3306
        },
        'vittoria_mdp_db': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'vittoria_mdp',
            'USER': 'usr_maintainer',
            'PASSWORD': 'Tc2;1EE{DBE^oN',
            'HOST': '209.145.61.41',
            'PORT': 3306
        }
    }
else:
    #URL FRONT END
    API_FRONT_END="localhost:4200"
    #TIEMPO DE EXPIRACION DE TOKEN (EN SEGUNDOS)
    TOKEN_EXPIRED_AFTER_SECONDS = 86400
    #NOMBRE KEYWORK TOKEN
    TOKEN_KEYWORD= 'Bearer'
    # This will display email in Console.
    EMAIL_HOST = ''
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_PORT = ''
    #CORS
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:4200",
        "http://127.0.0.1:4200"
    ]
    #databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'vittoria_adm',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': 3307
        },
        'vittoria_mdm_db': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'vittoria_mdm',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': 3307
        },
        'vittoria_mdp_db': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'vittoria_mdp',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': 3307
        }
    }

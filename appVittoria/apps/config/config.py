PRODUCTION=False

#VARIABLES GLOBALES
endpointEmailAsignacionPassword="/usuario/asignacionPassword/"
endpointEmailReseteoPassword="/usuario/reseteoPassword/"

#VARIABLES VARIAN DE ACUERDO A PRODUCCION O DESARROLLO
if PRODUCTION:
    #URL FRONT END
    API_FRONT_END="localhost:4200"
    #TIEMPO DE EXPIRACION DE TOKEN (EN SEGUNDOS)
    TOKEN_EXPIRED_AFTER_SECONDS = 86400
    #NOMBRE KEYWORK TOKEN
    TOKEN_KEYWORD= 'Bearer'
    # This will display email in Console.
    EMAIL_HOST = 'smtp.mailtrap.io'
    EMAIL_HOST_USER = 'e1e3590f699072'
    EMAIL_HOST_PASSWORD = 'f140af20266358'
    EMAIL_PORT = '2525'
    #CORS
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:4200",
        "http://127.0.0.1:4200"
    ]
else:
    #URL FRONT END
    API_FRONT_END="localhost:4200"
    #TIEMPO DE EXPIRACION DE TOKEN (EN SEGUNDOS)
    TOKEN_EXPIRED_AFTER_SECONDS = 86400
    #NOMBRE KEYWORK TOKEN
    TOKEN_KEYWORD= 'Bearer'
    # This will display email in Console.
    EMAIL_HOST = 'smtp.mailtrap.io'
    EMAIL_HOST_USER = 'e1e3590f699072'
    EMAIL_HOST_PASSWORD = 'f140af20266358'
    EMAIL_PORT = '2525'
    #CORS
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:4200",
        "http://127.0.0.1:4200"
    ]
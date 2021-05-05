#lib token
from django_rest_passwordreset.serializers import EmailSerializer
from django_rest_passwordreset.models import ResetPasswordToken, clear_expired, get_password_reset_token_expiry_time, \
    get_password_reset_lookup_field
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
#lib email
from apps.config.util import sendEmail
#lib reseteo contraseña
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from django.urls import reverse
from apps.config import config
from rest_framework.response import Response
from rest_framework import status
def resetPasswordNewUser(emailUsuario):
    try:
        User = get_user_model()
        #asignamos el email mandado
        email=emailUsuario
        # borra los tokens expirados
        password_reset_token_validation_time = get_password_reset_token_expiry_time()
        # datetime.now minus expiry hours
        now_minus_expiry_time = timezone.now() - timedelta(hours=password_reset_token_validation_time)
        # borramos los tokens que han pasado mas de 24 horas
        clear_expired(now_minus_expiry_time)
        # buscamos el email del usuario
        users = User.objects.filter(**{'{}__iexact'.format(get_password_reset_lookup_field()): email})
        active_user_found = False
        # iterate over all users and check if there is any user that is active
        # also check whether the password can be changed (is useable), as there could be users that are not allowed
        # to change their password (e.g., LDAP user)
        for user in users:
            if user.eligible_for_reset():
                active_user_found = True
        # Si no esta el usuario activo No enviamos el email
        if not active_user_found:
            return False
        # last but not least: iterate over all users that are active and can change their password
        # and create a Reset Password Token and send a signal with the created token
        for user in users:
            if user.eligible_for_reset():
                # define the token as none for now
                token = None
                # check if the user already has a token
                if user.password_reset_tokens.all().count() > 0:
                    # yes, already has a token, re-use this token
                    token = user.password_reset_tokens.all()[0]
                else:
                    # no token exists, generate a new token
                    token = ResetPasswordToken.objects.create(
                        user=user,
                        user_agent='ADMINISTRADOR',
                        ip_address='',
                    )
                # send a signal that the password token was created
                # let whoever receives this signal handle sending the email for the password reset
                # reset_password_token_created.send(sender=self.__class__, instance=self, reset_password_token=token)
                if enviarEmailAsignacionPassword(token):
                    return str(token.key)
                return 'Token no generado'
        # done
    except Exception as e: 
       return 'Ocurrió un error, Token no generado: {}'.format(e) 
#email

def enviarEmailAsignacionPassword(reset_password_token):
    try:
        #enviar por email
        url=config.API_FRONT_END+config.endpointEmailAsignacionPassword+"?token="+reset_password_token.key+"&user="+reset_password_token.user.username+"&email="+reset_password_token.user.email
        subject, from_email, to = 'Solicitud de Reinicio de contraseña Viitoria', "08d77fe1da-d09822@inbox.mailtrap.io",reset_password_token.user.email
        txt_content="""
                Registro de Contraseña Vittoria
                Para poder ingresar a la plataforma de Vittoria usted """+reset_password_token.user.username+""" debe registrar la contraseña,
                Haga clic en el siguiente enlace para registrar su contraseña:
                """+url+"""
                Si al hacer click en el enlace anterior no funciona, copie y pegue la URL en una nueva ventana del navegador
                Atentamente,
                Equipo Vittoria.
        """
        html_content = """
        <html>
            <body>
                <h1>Registro de Contraseña Vittoria</h1>
                Para poder ingresar a la plataforma de Vittoria usted """+reset_password_token.user.username+""" debe registrar la contraseña<br>
                Haga clic en el siguiente enlace para registrar su contraseña:<br>
                <a href='"""+url+"""'>Clic Aquí!</a><br>
                Si al hacer click en el enlace anterior no funciona, copie y pegue la URL en una nueva ventana del navegador<br>
                Atentamente,<br>
                Equipo Vittoria.<br>
            </body>
        </html>
        """
        if sendEmail(subject, txt_content, from_email,to,html_content):
            return True
        return False
    except:
        return False

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
 
    try:
        #enviar por email
        # email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
        url=config.API_FRONT_END+config.endpointEmailReseteoPassword+"?token="+reset_password_token.key+"&user="+reset_password_token.user.username+"&email="+reset_password_token.user.email
        subject, from_email, to = 'Solicitud de Reinicio de contraseña Viitoria', "08d77fe1da-d09822@inbox.mailtrap.io",reset_password_token.user.email
        txt_content="""
                Reinicio de Contraseña
                Para iniciar el proceso de restablecimiento de contraseña para usted """+reset_password_token.user.username+""" para su cuenta Vittoria,
                Haga clic en el siguiente enlace:
                """+url+"""
                Si al hacer click en el enlace anterior no funciona, copie y pegue la URL en una nueva ventana del navegador
                Atentamente,
                Equipo Vittoria.
        """
        html_content = """
        <html>
            <body>
                <h1>Reinicio de Contraseña</h1>
                Para iniciar el proceso de restablecimiento de contraseña para usted """+reset_password_token.user.username+""" para su cuenta Vittoria,<br>
                Haga clic en el siguiente enlace:<br>
                <a href='"""+url+"""'>Clic Aquí!</a><br>
                Si al hacer click en el enlace anterior no funciona, copie y pegue la URL en una nueva ventana del navegador<br>
                Atentamente,<br>
                Equipo Vittoria.<br>
            </body>
        </html>
        """
        sendEmail(subject, txt_content, from_email,to,html_content)
    
        #enviar por numero de whatsapp
        # numWhatsapp=reset_password_token.user.whatsapp
        # if numWhatsapp:
        #     #aqui codigo de whatsapp
        #     print(numWhatsapp)
        # else:
        #     print('No posee num whatsapp')
    except Exception as e: 
        err={"error":'Un error ha ocurrido: {}'.format(e)}  
        return Response(err, status=status.HTTP_400_BAD_REQUEST)
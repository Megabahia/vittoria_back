#lib email
from django.core.mail import EmailMultiAlternatives
from apps.MDP.mdp_parametrizaciones.models import Parametrizaciones
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import get_connection
def sendEmail(subject, txt_content, from_email,to,html_content):
    try:
        #Realizo la consulta a la bd antes de enviar el email, es lo que ocasiona tener parametrizado el servidor....
        emailHost=Parametrizaciones.objects.filter(tipo="SMTP_EMAIL",nombre="HOST",state=1).first()
        emailUsuario=Parametrizaciones.objects.filter(tipo="SMTP_EMAIL",nombre="USUARIO",state=1).first()
        emailpassword=Parametrizaciones.objects.filter(tipo="SMTP_EMAIL",nombre="PASSWORD",state=1).first()
        emailPuerto=Parametrizaciones.objects.filter(tipo="SMTP_EMAIL",nombre="PUERTO",state=1).first()
        connection = get_connection(host=emailHost.valor, 
                                port=emailPuerto.valor, 
                                username=emailUsuario.valor, 
                                password=emailpassword.valor, 
                                use_tls=True) 
        msg = EmailMultiAlternatives(subject, txt_content, from_email, [to],connection=connection)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return True
    except Exception as e: 
        err={"error":'Un error ha ocurrido: {}'.format(e)}
        return Response(err, status=status.HTTP_400_BAD_REQUEST)


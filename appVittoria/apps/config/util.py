#lib email
from django.core.mail import EmailMultiAlternatives
from rest_framework.response import Response
from rest_framework import status
def sendEmail(subject, txt_content, from_email,to,html_content):
    try:
        msg = EmailMultiAlternatives(subject, txt_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return True
    except Exception as e: 
        err={"error":'Un error ha ocurrido: {}'.format(e)}  
        return Response(err, status=status.HTTP_400_BAD_REQUEST)
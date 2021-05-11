from apps.ADM.vittoria_logs.serializers import LogsSerializer
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
import json
from apps.ADM.vittoria_catalogo.models import Catalogo
#crea el log en la base de datos
def saveLog(logModel):
    try:
        logModel['fechaFin']=str(timezone.localtime(timezone.now()))
        serializer = LogsSerializer(data=logModel,partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e: 
        err={"error":'Un error ha ocurrido: {}'.format(e)}  
        return Response(err,status=status.HTTP_400_BAD_REQUEST)
#ingresa los datos del log
def createLog(logModel,logRecibida,logTransaccion):
    try:
        if logRecibida:
            logModel['dataRecibida']=str(logRecibida)
        if logTransaccion:
            logModel['tipo']=str(logTransaccion)
        #VERIFICA EL PERMISO TOMA DEL CATALOGO
        try:
            permiso=Catalogo.objects.filter(tipo='LOG'+str(logModel['tipo']),nombre=str(logModel['accion']),state=1).only('valor').first()
        except Catalogo.DoesNotExist:
            err={'error':'No existe la configuracion de permisos'}
            return Response(err,status=status.HTTP_404_NOT_FOUND)
        if permiso.valor=='1':
            saveLog(logModel)
    except Exception as e: 
        err={"error":'Un error ha ocurrido: {}'.format(e)}  
        return Response(err,status=status.HTTP_400_BAD_REQUEST)
#TIPOS DE LOG
def datosTipoLog():
    data={
        'excepcion':'EXCEPCIONES',
        'transaccion':'TRANSACCIONES'
    }
    return data
#MODULO ADM-AUTH
def datosAuth():
    data={
        'modulo':'ADM',
        'api':'auth/'
    }
    return data
#MODULO ADM-USUARIOS
def datosUsuarios():
    data={
        'modulo':'ADM',
        'api':'usuarios/'
    }
    return data
#MODULO ADM-ROLES
def datosRoles():
    data={
        'modulo':'ADM',
        'api':'roles/'
    }
    return data
#MODULO ADM-ACCIONES
def datosAcciones():
    data={
        'modulo':'ADM',
        'api':'acciones/'
    }
#MODULO ADM-CATALOGO
def datosCatalogo():
    data={
        'modulo':'ADM',
        'api':'catalogo/'
    }
    return data  


